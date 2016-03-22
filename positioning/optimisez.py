import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats

def run(source, detectorcount, mindetections, graph=False, allcounts=None):

	plt.figure()

	i=1

	Z = 26
	
	BDTrange = np.linspace(0.0, 3.1, 51)
	annotation = ""
	
	optimumcuts = []
	
	for j in range (detectorcount, mindetections -1, -1):
			
		count = allcounts[detectorcount-j]
		
		testcount = int(float(count)/4.) 
		
		if int(testcount) > int(1):
			
			lowestsigma = 5
			optimumbdt = 0.0
			optimumpassing = 1.0
			
			meansigmas=[]
			
			bdtcuts =[]
			
			frac=0
			
			
			for i in range(0, len(BDTrange)):
				BDTcut = BDTrange[i]
				
				currentsigma = 5
				specificcount = []	
				with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					full = 0
					passing = 0
					
					i=-1
					for row in reader:
						if testcount < i < (2*testcount):
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
							BDT = row[15]
							
							if float(detections) == float(j):
								if int(Z) == int(trueZ):
									full += 1
									if float(BDTcut) > float(BDT):
										passing += 1
										specificcount.append(float(reconZ))
						
						else:
							i += 1
										
					line = "Detections = " + str(j)
					
					total = passing
					
					if total > 0:
					
						frac = float(passing)/float(full)
						
						if float(frac) > float(0.2):
							specificcount.sort()
							
							interval = (float(0.5)/float(total))
							probinside = 1-interval
							sigmas = scipy.stats.norm(0, 1).ppf(probinside)
							
							lowerz = specificcount[0]
							upperz = specificcount[total-1]
							meansigma = (float(upperz)-float(lowerz))/(2*sigmas)
							
							bdtcuts.append(BDTcut)
							meansigmas.append(meansigma)
							
							if float(meansigma) > float(lowestsigma):
								pass
								
							elif float(lowerz) > float(26):
								pass
							
							elif float(upperz) < float(26):
								pass
							
							else:
								lowestsigma=meansigma
								optimumbdt=BDTcut
								optimumpassing = passing
		
			if optimumbdt > 0:
			
				plt.plot(bdtcuts, meansigmas, label=line)
				
				optimumfrac = float(optimumpassing)/float(full)
			
				annotation += "Optimum Cut occurs with BDT > " + str(optimumbdt)+ " and with " + str(j) + " detections \n"
				annotation += "This leaves " + str(optimumpassing) + " events , a fraction of " + str(optimumfrac) + "\n \n"
			
			optimumcuts.append(optimumbdt)

		else:
			optimumcuts.append(0.0)

	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.title("Optimisation of Sigma Z")
	plt.xlabel("Lower BDT Limit")
	plt.ylabel("Mean Sigma Z")
	
	plt.annotate(annotation, xy=(0.0, 0.8), xycoords="axes fraction",  fontsize=10)
	
	plt.legend()
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/Zcuts.pdf')
	
	if graph:
		plt.show()
		
	else:
		plt.close()
	
	return optimumcuts
