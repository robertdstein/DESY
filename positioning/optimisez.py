import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats
import cPickle as pickle

def run(statsset, mindetections):

	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors

	plt.figure()

	Z = 26
	
	BDTrange = np.linspace(-0.01, 1.0, 1001)
	annotation = ""
	
	optimumcuts = []
	
	for j in range (detectorcount, mindetections -1, -1):	
		print "Ndetections", j
		lowestsigma = 10
		optimumbdt = 0.0
		optimumpassing = 1.0
		
		meansigmas=[]
		
		bdtcuts =[]
		
		frac=0
		
		for i in range(0, len(BDTrange)):
			BDTcut = BDTrange[i]
			currentsigma = 5
			specificcount = []
			sqvals=[]
			differences=[]
			full = 0
			passing = 0
		
			for simset in datasimset:
				maxn = simset.ndetectors
				for sim in simset.simulations:	
					recon = sim.reconstructed
					observed = sim.detected
					true = sim.true
					

					if int(observed.DCmultiplicity) == int(j):
					
						if recon.BDTscore != None:

							full += 1
							if float(BDTcut) < float(recon.BDTscore):
								passing += 1
								specificcount.append(float(recon.Z))
								diff = math.fabs(float(recon.Z)-26)
								sqvals.append(float(recon.Z)**2)
								differences.append(diff)
					#~ 
					#~ else:
						#~ raise Exception("NO BDT SCORE ASSIGNED!!!")

									
			line = "Detections = " + str(j)
			
			total = passing
			
			if total > 0:
			
				frac = float(passing)/float(full)					
				meanz = np.mean(specificcount)
				meanz2 = np.mean(sqvals)
				var = meanz2 - (meanz**2)
				
				meansigma=math.sqrt(var)
				
				specificcount.sort()
		
				lower = int(total*0.16)
				mid = int(total*0.5)
				upper = int(total*0.84)
			
				lowerz = specificcount[lower]
				meanz = specificcount[mid]
				upperz = specificcount[upper]
				meansigma = (upperz-lowerz) * 0.5
				
				bdtcuts.append(BDTcut)
				meansigmas.append(meansigma)
				
				if float(frac) > float(0.2):
					if float(24) < float(meanz) < float(28):
						if float(meansigma) < float(lowestsigma):
							lowestsigma=meansigma
							optimumbdt=BDTcut
							optimumpassing = passing
						
		plt.plot(bdtcuts, meansigmas, label=line)
			
		optimumfrac = float(optimumpassing)/float(full)
		
		annotation += "Optimum Cut occurs with BDT > " + str(optimumbdt)+ " and with " + str(j) + " detections \n"
		annotation += "This leaves " + str(optimumpassing) + " events , a fraction of " +  str('{0:.2f}'.format(optimumfrac)) + "\n"
		annotation += "The resultant Sigma is " +  str('{0:.2f}'.format(lowestsigma)) + "\n \n"		
		
		if optimumpassing > 1:
			optimumcuts.append(optimumbdt)

		else:
			optimumcuts.append(0.0)

	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.title("Optimisation of Sigma Z")
	plt.xlabel("Lower BDT Limit")
	plt.ylabel("Mean Sigma Z")
	plt.gca().set_ylim(bottom=-0.05)
	plt.gca().set_xlim(left=-0.05)
	
	plt.annotate(annotation, xy=(0.0, 0.9), xycoords="axes fraction",  fontsize=10)
	
	plt.legend()
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Zcuts.pdf')
	
	print annotation

	plt.close()
	
	return optimumcuts
