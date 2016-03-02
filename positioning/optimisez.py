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
	lowerlim = 18
	bincount=(upperlim-lowerlim)*2 + 1
	
	zrange = [19.5, 32.5]
	reconvalues = np.linspace(zrange[0]+0.5, zrange[1]-0.5, bincount)
	
	llrange = np.linspace(lowerlim, upperlim, bincount)
	annotation = ""
	llcuts = []
	llmins=[]
	
	for j in range (detectorcount, mindetections -1, -1):
		lowestsigma = 5
		dataset = 0
		datawidth = 0
		text = ""
		optimumll = 500
		optimummin=0
		mincount = 5
		meansigmas=[]
		llvalues =[]
		
		limitsigmas = []
		overflowvalues = []
		
		frac=0
		
		for i in range(1, len(llrange)):
			ll = llrange[i]
			currentsigma = 5		
			best=['nope']
			for k in range(i-10, i-1):
				specificcount = []
				minll=llrange[k]	
				with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					full = 0
					passing = 0
					
					i=0
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
									full += 1
									if float(minll) < float(likelihood) < float(ll):
										passing += 1
										specificcount.append(float(reconZ))
										
					line = "Detections = " + str(j)
					
					total = passing
					
					
					if float(total) > float(1):
						fraction = float(passing)/float(full)
						specificcount.sort()
						
						interval = (float(0.5)/float(total))
						probinside = 1-interval
						sigmas = scipy.stats.norm(0, 1).ppf(probinside)
						
						lowerz = specificcount[0]
						upperz = specificcount[total-1]
						meansigma = (float(upperz)-float(lowerz))/(2*sigmas)

						#~ lower = int(total*0.16)
						#~ upper = int(total*0.84)
						#~ 
						#~ lowerz = specificcount[lower]
						#~ upperz = specificcount[upper]
						#~ sixtyeightsigma = (upperz-lowerz) * 0.5
						
						#~ if extremesigma < sixtyeightsigma:
							#~ meansigma = sixtyeightsigma
						#~ else:
							#~ meansigma = extremesigma
						
						
						if float(meansigma) > float(currentsigma):
							pass
							
						elif fraction > 0.05:
							if int(lowerz) > int(26):
								pass
							elif int(26) > int(upperz):
								pass
							else:
								best = [meansigma, sigmas, ll, minll, total, specificcount, fraction]
							
			if len(best) > 1:
							
				meansigmas.append(best[0])
				llvalues.append(best[2])
				
				if float(best[0]) == float(0):
					limitsigma = float(1)/(2*sigmas)
					limitsigmas.append(limitsigma)
					overflowvalues.append(ll)
	
				if float(best[0]) > float(lowestsigma):
					pass
				
				else:
					if float(best[1]) > float(datawidth):
						lowestsigma = best[0]
						optimumll=best[2]
						optimummin=best[3]
						dataset = best[4]
						text = best[5]
						frac = best[6]
						mincount = j
		
		plt.plot(llvalues, meansigmas, label=line)
	
		annotation += "Optimum Cut occurs with " + str(optimummin) + " < LL < " + str(optimumll)+ " and with " + str(mincount) + " detections \n"
		annotation += "This leaves " + str(dataset) + " events , a fraction of " + str(frac) + "\n \n"
		
		llcuts.append(optimumll)
		llmins.append(optimummin)

	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.ylim(-0.5, 4)
	
	plt.title("Optimisation of Sigma Z")
	plt.xlabel("Upper Log Likelihood Limit")
	plt.ylabel("Mean Sigma Z")
	plt.xscale('log')
	
	plt.annotate(annotation, xy=(0.7, 0.4), xycoords="axes fraction",  fontsize=10)
	
	plt.legend()
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/Zcuts.pdf')
	
	if graph:
		plt.show()
		
	else:
		plt.close()
	
	return llcuts, llmins
