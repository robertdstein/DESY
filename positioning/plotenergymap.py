import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
from classes import *

def run(statsset, mindetections, cuts):
	
	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors
	
	fig = plt.figure()
	
	k=0
	l=0
	cutset = [cuts,None]
	for currentcuts in cutset:
		plt.subplot(2,1, 2-l)
		fullcount=[]
		labels=[]
		for j in range (detectorcount, mindetections -1, -1):
			specificcount=[]
			print "Ndetections", j
			if currentcuts == None:
				bdtmin = -0.01
			else:
				bdtmin = currentcuts[k]
			
			for simset in datasimset:
				for sim in simset.simulations:	
					recon = sim.reconstructed
					observed = sim.detected
					true = sim.true
					if int(observed.DCmultiplicity) == int(j):
						if recon.BDTscore != None:
							if float(bdtmin) < float(recon.BDTscore):
								e = recon.energy
								specificcount.append(e/1000)
			
			fullcount.append(specificcount)
			label = str(j) + " detections"
			labels.append(label)
			k +=1								

		if currentcuts == None:
			plt.title("Reconstructed energy for all events", fontsize = 20)
		else:
			plt.title("Reconstructed energy for accepted events", fontsize = 20)
		
		erange=[0, 150]
		n, bins, _ = plt.hist(fullcount, bins=25, range=erange, label=labels, histtype='stepfilled',stacked=True)
		
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
	
		plt.ylabel("Count")
		plt.xlabel("Reconstructed energy (TeV)")
		plt.legend()
		l+= 1
		
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)

	plt.tight_layout()
	
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/energymap.pdf')
	path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/energymap.pdf'
	
	plt.savefig(path)
	print "saving to", path
	plt.close()
	
