import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import cPickle as pickle
from classes import *

def run(statsset, mindetections, cuts=None):

	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors

	i=1

	zvalues = [26]
	nplots = len(zvalues)
		
	if cuts == None:
		classifiermax=8.5
		path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/rawZ.pdf'
	else:
		classifiermax=1.5
		path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Z.pdf'
	
	for val in zvalues:
		
		z = val
		
		plt.subplot(nplots, 1, i)
		
		i+=1
		
		plt.subplots_adjust(hspace = 0.5)
		fullcount = []
		labels=[]
		info=""
		
		title = "Z is " + str(int(z))
		
		hist_fit = 0
		k=0
	
		for j in range (detectorcount, mindetections -1, -1):
			print "Ndetections", j
		
	
			specificcount = []
			differences = []
			sqvals=[]
			
			full=0
			passing=0
			plot=True
			
			if cuts == None:
				bdtmin = -0.01
			else:
				bdtmin = cuts[k]
			
			for simset in datasimset:
				for sim in simset.simulations:	
					recon = sim.reconstructed
					observed = sim.detected
					true = sim.true
					if int(observed.DCmultiplicity) == int(j):
						if recon.BDTscore != None:
							if int(true.Z) == int(z):
								full += 1
								if float(bdtmin) < float(recon.BDTscore):
									passing += 1
									specificcount.append(float(recon.Z))
									diff = math.fabs(float(recon.Z)-26)
									sqvals.append(float(recon.Z)**2)
									differences.append(diff)
			
			total = passing
			
			if total > 0:
			
				frac = float(passing)/float(full)					
				meanz = np.mean(specificcount)
				meanz2 = np.mean(sqvals)
				var = meanz2 - (meanz**2)
				
				meansigma=math.sqrt(var)
												
				label = str(j) + " detections"
	
				fullcount.append(specificcount)
				labels.append(label)
				
				info += str("For N = " + str(j) + " we require BDT >  " + str(bdtmin) + "\n ")
				info += str("Fraction passing is " + str(frac) + "\n")
				
				if float(meansigma) == float(0):
					differences.append(1)
					limitsigma = np.mean(differences)
					info += ('Sigma < ' + str(limitsigma) + "\n")
	
				else:
					info += ('Sigma = ' + str(meansigma) + "\n")
				
				info += "\n"
				k +=1
		
		print info
		zmax = max(max(c) for c in fullcount)
		zmin = min(min(c) for c in fullcount)
		gzmin = int(zmin-1)+0.5
		gzmax = int(zmax+0.5)+0.5
		print "Zrange", zmin, gzmin, zmax, gzmax

		zrange = [gzmin, gzmax]
		
		bincount = int(gzmax - gzmin)
				
		if fullcount != []:
			
			n, bins, _ = plt.hist(fullcount, bins=bincount, range=zrange, histtype='bar', label=labels, stacked=True)
	
			mid = (bins[1:] + bins[:-1])*0.5
			if isinstance(n[0], np.ndarray):
				errors = np.zeros(len(n[0]))
				for i in range(0, len(n)):
					array = n[i]
					old = errors
					errors = []
					for j in range(0, len(array)):
						count = array[j]
						oldcount = old[j]
						delta = count-oldcount
						errors.append(math.sqrt(delta))
					
					plt.errorbar(mid, n[i], yerr=errors, fmt='kx')
			
			nmax = np.amax(n)
			
			uplim = nmax + (math.sqrt(nmax))
			
			plt.ylim(0, uplim)
		
		plt.xlim(zrange)
		plt.xlabel('Reconstructed Z', labelpad=0)
		plt.title(title)
		
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.annotate(info, xy=(0.8, 0.8), xycoords="axes fraction",  fontsize=10)
	plt.suptitle("True Z reconstruction", fontsize=20)
	plt.legend()
	
	plt.savefig(path)
	print "saving to", path
	plt.close()
