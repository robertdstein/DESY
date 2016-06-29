import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import cPickle as pickle
from classes import *
import sys
sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/cluster_input')
import initialise as i
numberofhours, mincount, gridwidth, layout, raweff, flux, area, solidangle, selectionefficiency, hmacceptance = i.run()
detectedflux = float(flux)*float(area)*float(solidangle)*float(selectionefficiency)
rateperhour = detectedflux * 60 * 60

def run(statsset, mindetections, cuts=None):

	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors

	i=1

	zvalues = [26]
	nplots = len(zvalues)
	
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
		
		counts=[]
	
		for j in range (detectorcount, mindetections -1, -1):
			print "Ndetections", j
		
			nonDC = 0
			mT=0
			bT=0
			accepted =0
	
			specificcount = []
			differences = []
			sqvals=[]
			counts.append(0)
			
			full=0
			passing=0
			plot=True
			
			if cuts == None:
				bdtmin = -0.01
			else:
				bdtmin = cuts[k]
			
			for simset in datasimset:
				nonDC += simset.nonDC
				mT += simset.hmcount
				bT += simset.lmcount
				accepted += simset.passcount
				
				for sim in simset.simulations:	
					recon = sim.reconstructed
					observed = sim.detected
					true = sim.true
					if int(observed.DCmultiplicity) == int(j):
						counts[k] += 1
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
			
			totalcount = nonDC+mT+bT
			
			if total > 0:
			
				frac = float(passing)/float(full)					
				meanz = np.mean(specificcount)
				meanz2 = np.mean(sqvals)
				var = meanz2 - (meanz**2)
				
				meansigma=math.sqrt(var)
												
				label = str(j) + " detections"
	
				fullcount.append(specificcount)
				labels.append(label)
				
				specificcount.sort()
		
				lower = int(total*0.16)
				mid = int(total*0.5)
				upper = int(total*0.84)
			
				lowerz = specificcount[lower]
				meanz = specificcount[mid]
				upperz = specificcount[upper]
				sigma = (upperz-lowerz) * 0.5
				
				info += str("For N = " + str(j) + "\n ")
				if cuts != None:
					info += str("There were originally " + str(counts[k]) + " events \n")
					info += str("This is a rate of " + str('{0:.2f}'.format(float(100.*float(counts[k])/float(totalcount)))) + "% of all events \n")
					info += str("Fraction of these events passing cuts is " + str('{0:.2f}'.format(frac)) + "\n")

				info += ('Upper bound = ' + str('{0:.2f}'.format(upperz)) + " \n")
				info += ('Median = ' + str('{0:.2f}'.format(meanz)) + " \n")
				info += ('Lower bound = ' + str('{0:.2f}'.format(lowerz)) + " \n")
				
				if float(meansigma) == float(0):
					differences.append(1)
					limitsigma = np.mean(differences)
					info += ('Sigma < ' + str('{0:.2f}'.format(limitsigma)) + "\n")
	
				else:
					#~ info += ('Sigma = ' + str('{0:.2f}'.format(meansigma)) + "\n")
					info += ('Sigma = ' + str('{0:.2f}'.format(sigma)) + "\n")
				
				info += "\n"
				k +=1
		
		print info
		hours = int(float(totalcount)/rateperhour)
		print "In total there were", totalcount, "events, corresponding to an effective run time of", hours, "hours"
		print "Of these,", nonDC, "did not emit,", bT, "were low multiplicity, and", mT, "were high multiplicity, and", accepted, "accepted events."
		
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
	plt.annotate(info, xy=(0.8, 0.6), xycoords="axes fraction",  fontsize=10)
	plt.suptitle("True Z reconstruction for " + str(hours) + " hours", fontsize=20)
	plt.legend()
	
	if cuts == None:
		plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/rawZ.pdf')
		path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/rawZ.pdf'
	else:
		plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/Z.pdf')
		path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Z.pdf'
	
	

	
	plt.savefig(path)
	print "saving to", path
	plt.close()
