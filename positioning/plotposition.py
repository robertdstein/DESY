import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
from classes import *

def run(statsset, mindetections, cuts):
	
	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors
	
	fullcount=[]
	labels=[]
	info = ""
	k=0
	for j in range (detectorcount, mindetections -1, -1):
		specificcount=[]

		full=0
		passing=0
		
		bdtmin = cuts[k]

		for simset in datasimset:
			for sim in simset.simulations:	
				recon = sim.reconstructed
				observed = sim.detected
				true = sim.true
				

				if int(observed.DCmultiplicity) == int(j):
					full += 1
					if recon.BDTscore != None:
						if float(bdtmin) < float(recon.BDTscore):
							passing += 1
							distance = math.sqrt(((recon.rayxpos-true.rayxpos)**2)+(recon.rayypos-true.rayypos)**2)
							specificcount.append(distance)

		total = len(specificcount)
		
		if float(total) > float(0):
			fullcount.append(specificcount)
			label = str(j) + " detections"
			labels.append(label)

			specificcount.sort()
		
			lower = int(0)
			mid = int(total*0.5)
			upper = int(total*0.68)
			
			lowerz = 0
			meanz = specificcount[mid]
			upperz = specificcount[upper]
			sigma = (upperz-lowerz) * 0.5
			
			fraction = float(passing)/float(full)
			info += str("For N = " + str(j) + " we require BDT >  " + str(bdtmin) + "\n ")
			info += str("Fraction passing is " + str(fraction) + "\n")
			
			info += ('Upper bound = ' + str(upperz) + " \n")
			info += ('Median = ' + str(meanz) + " \n")
			info += ('Sigma = ' + str(sigma) + "\n \n")
	
		k +=1
	
	plt.annotate(info, xy=(0.8, 0.6), xycoords="axes fraction",  fontsize=15)
	
	n, bins, _ = plt.hist(fullcount, bins=30, range=[0,30], label=labels, histtype='bar', stacked=True)

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
	
	uplim = nmax + 2*(math.sqrt(nmax))
	
	plt.ylim(0, uplim)
	
	nmax = np.amax(n)
	
	uplim = nmax + (math.sqrt(nmax))
	
	plt.ylim(0, uplim)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)

	plt.xlabel("Distance from True Position")
	plt.ylabel("Count")
	plt.title("Distance Reconstruction")
	plt.legend()
	
	path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/position.pdf'
	plt.savefig(path)
	print "saving to", path
	plt.close()
