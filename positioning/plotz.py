import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

def run(source, detectorcount, mindetections, graph, llcuts):

	i=1

	zvalues = [26]
	nplots = len(zvalues)
	bincount = 13
	zrange = [19.5, 32.5]
	reconvalues = np.linspace(zrange[0]+0.5, zrange[1]-0.5, bincount)
	
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
			
			with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				specificcount = []
				
				full=0
				passing=0
				
				i = 0
				
				upperll=llcuts[k]

				for row in reader:
					if i == 0:
						i = 1
					else:
						detections = row[0]
						reconx = row[1]
						recony = row[2]
						reconEPN = row[3]
						reconZ = row[4]
						reconHeight = row[5]
						truex = row[6]
						truey = row[7]
						trueEPN = row[8]
						trueZ = row[9]
						trueHeight = row[10]
						likelihood = row[13]
						
						
						if int(detections) == int(j):
							if int(z) == int(trueZ):
								full += 1
								if float(likelihood) < float(upperll):
									passing += 1
									specificcount.append(float(reconZ))
								
								
				label = str(j) + " detections"
					
				fullcount.append(specificcount)
				labels.append(label)
				
				hist, bin_edges = np.histogram(specificcount, bins=bincount, range=zrange)
				bin_centres = (bin_edges[:-1] + bin_edges[1:])/2
				
				total = len(specificcount)
				
				fraction = float(passing)/float(full)
				info += str("For N = " + str(j) + " we require LL < " + str(upperll) + "\n ")
				info += str("Fraction passing is " + str(fraction) + "\n")
				
				if float(total) > float(0):
				
					specificcount.sort()
					
					interval = (float(0.5)/float(total))
					probinside = 1-interval
					sigmas = scipy.stats.norm(0, 1).ppf(probinside)
					
					lowerz = specificcount[0]
					meanz = specificcount[int(total*0.5)]
					upperz = specificcount[total-1]
					meansigma = (float(upperz)-float(lowerz))/(2*sigmas)
					
					info += ('Lower bound = ' + str(lowerz) + " \n")
					info += ('Upper bound = ' + str(upperz) + " \n")
					info += ('Mean = ' + str(meanz) + " \n")
					
					if float(meansigma) == float(0):
						limitsigma = float(1)/(2*sigmas)
						info += ('Sigma < ' + str(limitsigma) + "\n")

					else:
						info += ('Sigma = ' + str(meansigma) + "\n")
				
				info += "\n"
				
			k +=1
					
		if fullcount != []:
			
			n, bins, _ = plt.hist(fullcount, bins=bincount, histtype='bar', range=zrange, label=labels, stacked=True)
	
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
	
	plt.annotate(info, xy=(0.6, 0.3), xycoords="axes fraction",  fontsize=10)
	plt.suptitle("True Z reconstruction", fontsize=20)
	plt.legend()
	
	plt.savefig('graphs/Z.pdf')
		
	if graph:
		plt.show()
		
	else:
		plt.close()
