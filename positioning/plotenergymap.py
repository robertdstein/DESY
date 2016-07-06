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
		for j in range (detectorcount, mindetections -2, -1):
			specificcount=[]
			print "Ndetections", j
			if (currentcuts == None) or (j < mindetections):
				bdtmin = -0.01
			else:
				bdtmin = currentcuts[k]
			
			for simset in datasimset:
				
				if j < mindetections:
					total = simset.hmcount + simset.lmcount+simset.nonDC
					for q in range(total):
						R = random.random()*3.01*(10**-3)
						Epn = ((1.7*R/321)+(2411**-1.7))**(-1/1.7)
						e = Epn * 56
						specificcount.append(e/1000)
				
				else:
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
			if j < mindetections:
				label = "Simulated Distribution"
			else:
				label = str(j) + " detections"
			
			k +=1
			labels.append(label)
										

		if currentcuts == None:
			plt.title("Reconstructed energy for all events", fontsize = 20)
		else:
			plt.title("Reconstructed energy for accepted events", fontsize = 20)
		
		erange=[0, 150]
		n, bins, _ = plt.hist(fullcount, bins=25, range=erange, log=True, label=labels, histtype='stepfilled',stacked=True)
		
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
		
		truevals = n[2]
		info = ""
		for m in range(0, 2):
			valset = n[m]
			ratios=[]
			weights=[]
			for p in range(len(mid)):
				energy = mid[p]
				if energy > 35:
					trueval = truevals[p] - n[1][p]
					if trueval > 0:
						if m > 0:
							 val = valset[p] - n[0][p]
						else:
							val = valset[p]
						ratio = val/trueval
						weight = val
						wr = ratio * weight
						ratios.append(wr)
						weights.append(weight)
						
			print weights, ratios, np.mean(ratios), np.sum(weights)
			meanratio = float(np.mean(ratios))/float(np.mean(weights))
			message = str("For Multiplicity " + str(detectorcount-m) + ", mean fraction is " + str('{0:.3f}'.format(meanratio)) + "\n")
			info += message
			
		print info
		plt.annotate(info, xy=(0.75, 0.7), xycoords="axes fraction",  fontsize=15)
		
	
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
	
