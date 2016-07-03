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

	fig = plt.figure()

	Z = 26
	
	BDTrange = np.linspace(-0.01, 1.0, 1001)
	annotation = ""
	
	optimumcuts = []
	
	ax1 = plt.subplot(2,1,1)
	ax2 = plt.subplot(2,1,2)
	
	for j in range (detectorcount, mindetections -1, -1):	
		print "Ndetections", j
		lowestsigma = 10
		lowestscalesigma=10
		optimumbdt = 0.0
		optimumpassing = 1.0
		
		meansigmas=[]
		scalesigmas=[]
		
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
				#~ meanz = np.mean(specificcount)
				#~ meanz2 = np.mean(sqvals)
				#~ var = meanz2 - (meanz**2)
				#~ 
				#~ meansigma=math.sqrt(var)
				
				specificcount.sort()
		
				lower = int(total*0.16)
				mid = int(total*0.5)
				upper = int(total*0.84)
			
				lowerz = specificcount[lower]
				meanz = specificcount[mid]
				upperz = specificcount[upper]
				meansigma = (upperz-lowerz) * 0.5
				scalesigma = meansigma/math.sqrt(frac)
				
				if float(frac) > float(0.01):
					bdtcuts.append(BDTcut)
					meansigmas.append(meansigma)
					scalesigmas.append(scalesigma)
					if float(24) < float(meanz) < float(28):
						if float(scalesigma) < float(lowestscalesigma):
							lowestsigma=meansigma
							lowestscalesigma = scalesigma
							optimumbdt=BDTcut
							optimumpassing = passing
					
		ax1.plot(bdtcuts, meansigmas, label=line)
		ax2.plot(bdtcuts, scalesigmas, label=line)
			
		optimumfrac = float(optimumpassing)/float(full)
		
		annotation += "Optimum Cut occurs with BDT > " + str('{0:.2f}'.format(optimumbdt))+ " and with " + str(j) + " detections \n"
		annotation += "This leaves " + str(optimumpassing) + " events , a fraction of " +  str('{0:.2f}'.format(optimumfrac)) + "\n"
		annotation += "The resultant Sigma is " +  str('{0:.2f}'.format(lowestsigma)) + "\n \n"		
		
		if optimumpassing > 1:
			optimumcuts.append(optimumbdt)
			ax1.scatter(optimumbdt, lowestsigma, color="r", s=10)
			ax1.scatter(optimumbdt, lowestsigma, color="r", s=100, alpha = 0.25)
			ax2.scatter(optimumbdt, lowestscalesigma, color="r", s=10)
			ax2.scatter(optimumbdt, lowestscalesigma, color="r", s=100, alpha = 0.25)

		else:
			optimumcuts.append(0.0)

	fig.set_size_inches(15, 10)
	
	plt.suptitle("Optimisation of Sigma Z", fontsize=20)
	ax1.set_ylabel("Sigma Z")
	ax2.set_ylabel("Scaled Sigma Z")
	for ax in [ax1, ax2]:
		ax.set_xlabel("Lower BDT Limit")
		ax.set_ylim(bottom=0.00)
		ax.set_xlim(left=0.00)
	#~ 
	plt.annotate(annotation, xy=(0.2, 0.6), xycoords="axes fraction",  fontsize=10)
	
	plt.legend()
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Zcuts.pdf')
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/Zcuts.pdf')
	
	print annotation

	plt.close()
	
	return optimumcuts
