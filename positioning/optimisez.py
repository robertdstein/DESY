import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

def run(source, detectorcount, mindetections, graph=False):

	i=1

	Z = 26
	
	upperlim = 150
	lowerlim = 20
	bincount=(upperlim-lowerlim)*2 + 1
	
	zrange = [19.5, 32.5]
	reconvalues = np.linspace(zrange[0]+0.5, zrange[1]-0.5, bincount)
	
	llrange = np.linspace(lowerlim, upperlim, bincount)
	annotation = ""
	llcuts = []
	
	for j in range (detectorcount, mindetections -1, -1):
		lowestsigma = 5
		datawidth = 0
		text = ""
		optimumll = 500
		mincount = 5
		meansigmas=[]
		llvalues =[]
		
		limitsigmas = []
		overflowvalues = []
		
		for ll in llrange:
			with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')

				i=0
				
				specificcount = []

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
						
						if float(detections) == float(j):
							if int(Z) == int(trueZ):
								if float(likelihood) < float(ll):
									specificcount.append(float(reconZ))
									
				line = "Detections = " + str(j)
				
				total = len(specificcount)
				
				if float(total) > float(1):
				
					specificcount.sort()
					
					interval = (float(0.5)/float(total))
					probinside = 1-interval
					sigmas = scipy.stats.norm(0, 1).ppf(probinside)
					
					lowerz = specificcount[0]
					upperz = specificcount[total-1]
					meansigma = (float(upperz)-float(lowerz))/(2*sigmas)
					meansigmas.append(meansigma)
					llvalues.append(ll)
					
					if float(meansigma) == float(0):
						limitsigma = float(1)/(2*sigmas)
						limitsigmas.append(limitsigma)
						overflowvalues.append(ll)
	
					if float(meansigma) > float(lowestsigma):
						pass
					
					else:
						if float(sigmas) > float(datawidth):
							lowestsigma = meansigma
							dataset = total
							text = specificcount
							optimumll=ll
							mincount = j
		
		plt.plot(llvalues, meansigmas, label=line)
		if len(overflowvalues) > 0:
			limitlabel = line + " upper limit"
			plt.plot(overflowvalues, limitsigmas, label=limitlabel, linestyle = "--", color='r')
	
		annotation += "Optimum Cut occurs with LL < " + str(optimumll)+ " and with " + str(mincount) + " detections \n"
		annotation += "This leaves " + str(dataset) + " events \n \n"
		
		llcuts.append(optimumll)

	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.ylim(-0.5, 4)
	
	plt.title("Optimisation of Sigma Z")
	plt.xlabel("Upper Log Likelihood Limit")
	plt.ylabel("Mean Sigma Z")
	plt.xscale('log')
	
	plt.annotate(annotation, (12, -0.5))
	
	plt.legend()
	plt.savefig('graphs/Zcuts.pdf')
	
	if graph:
		plt.show()
		
	else:
		plt.close()
	
	return llcuts
