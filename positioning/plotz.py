import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run(source, detectorcount, mindetections, graph):

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
		
		for j in range (detectorcount, mindetections -1, -1):
			with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				specificcount = []
				
				
				i = 0

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
						
						if int(detections) == int(j):
							if int(z) == int(trueZ):
								specificcount.append(float(reconZ))
								
								
				label = str(j) + " detections"
					
				fullcount.append(specificcount)
				labels.append(label)
				
				hist, bin_edges = np.histogram(specificcount, bins=bincount, range=zrange)
				bin_centres = (bin_edges[:-1] + bin_edges[1:])/2
				
				total = len(specificcount)
				print total
				
				specificcount.sort()
				
				lower = int(total*0.16)
				mid = int(total*0.5)
				upper = int(total*0.84)
				
				print lower, upper, mid
				
				lowerz = specificcount[lower]
				meanz = specificcount[mid]
				upperz = specificcount[upper]
				sigma = (upperz-lowerz) * 0.5
				
				print lowerz, meanz, upperz, sigma
				
				def gauss(x, A, mu, sigma):
				    return A*np.exp(-(x-mu)**2/(2.*sigma**2))
				
				# p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
				p0 = [1., 26., 1.]
				
				coeff, var_matrix = curve_fit(gauss, reconvalues, hist, p0=p0)
				
				# Get the fitted curve
				hist_fit += gauss(bin_centres, *coeff)
				
				plt.plot(bin_centres, hist_fit, color='k')
				
				# Finally, lets get the fitting parameters, i.e. the mean and standard deviation:
				
				info += str("For N = " + str(j) + " \n ")
				info += str("Count = " + str(coeff[0])+ " \n ")
				info += str('Mean = ' + str(coeff[1])+ " \n ")
				info += str('Sigma = ' + str(coeff[2])+ "\n \n")
				info += ('Lower bound = ' + str(lowerz) + " \n")
				info += ('Upper bound = ' + str(upperz) + " \n")
				info += ('Mean = ' + str(meanz) + " \n")
				info += ('Sigma = ' + str(sigma) + "\n \n")
			
		plt.annotate(info, (30, 6),  fontsize=10)
			
		if fullcount != []:
			plt.hist(fullcount, bins=bincount, histtype='bar', range=zrange, label=labels, stacked=True)
			
		
		plt.xlim(zrange)
		plt.xlabel('Reconstructed Z', labelpad=0)
		plt.title(title)
		handles, labels = plt.subplot(nplots, 1, i).get_legend_handles_labels()	
	plt.suptitle('True Z reconstruction', fontsize=20)
	plt.figlegend(handles, labels, 'upper right')
	
	plt.savefig('graphs/Z.pdf')
		
	if graph:
		plt.show()
