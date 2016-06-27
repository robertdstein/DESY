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
							difference= (float(recon.height) - float(true.height))/float(true.height)
							specificcount.append(difference)

		total = len(specificcount)
		label = str(j) + " detections"
		labels.append(label)
		
		if float(total) > float(0):
			fullcount.append(specificcount)
			label = str(j) + " detections"
			labels.append(label)

			specificcount.sort()
		
			lower = int(total*0.16)
			mid = int(total*0.5)
			upper = int(total*0.84)
			
			lowerz = specificcount[lower]
			meanz = specificcount[mid]
			upperz = specificcount[upper]
			sigma = (upperz-lowerz) * 0.5
			
			fraction = float(passing)/float(full)
			info += str("For N = " + str(j) + " we require BDT >  " + str('{0:.2f}'.format(bdtmin)) + "\n ")
			info += str("Fraction passing is " + str('{0:.2f}'.format(fraction)) + "\n")
			
			info += ('Upper bound = ' + str('{0:.2f}'.format(upperz)) + " \n")
			info += ('Median = ' + str('{0:.2f}'.format(meanz)) + " \n")
			info += ('Lower bound = ' + str('{0:.2f}'.format(lowerz)) + " \n")
			info += ('Sigma = ' + str('{0:.2f}'.format(sigma)) + "\n \n")
	
		k +=1
	
	plt.annotate(info, xy=(0.8, 0.4), xycoords="axes fraction",  fontsize=10)
	
	n, bins, _ = plt.hist(fullcount, bins=15, label=labels, histtype='bar', stacked=True)
	
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

	plt.xlabel("Fractional Height Error")
	plt.ylabel("Count")
	plt.title("Height Reconstruction")
	plt.legend()
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/height.pdf'
	plt.savefig(path)
	print "saving to", path
	plt.close()
