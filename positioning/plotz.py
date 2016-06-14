import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

def run(source, detectorcount, mindetections, graph, cuts=None):

	i=1

	zvalues = [26]
	nplots = len(zvalues)
	bincount = 13
	zrange = [19.5, 32.5]
	reconvalues = np.linspace(zrange[0]+0.5, zrange[1]-0.5, bincount)
	
	if cuts == None:
		cuts = np.zeros(1 + detectorcount-mindetections)
		classifiermax=8.5
		path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/rawZ.pdf'
	else:
		classifiermax=1.5
		path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Z.pdf'
	
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
						
			with open("/d6/rstein/Hamburg-Cosmic-Rays/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				specificcount = []
				differences = []
				
				full=0
				passing=0
				
				i = -1
				
				bdtmin = cuts[k]

				for row in reader:
					if i < 0:
						i += 1
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
						classifier = float(row[15])
						BDT=row[16]
						
						if int(detections) == int(j):
							if int(z) == int(trueZ):
								full += 1
								if float(bdtmin) < float(BDT):
									if float(classifier) < float(classifiermax):
										passing += 1
										specificcount.append(float(reconZ))
										diff = math.fabs(float(reconZ)-26)
										differences.append(diff)
											
				label = str(j) + " detections"

				fullcount.append(specificcount)
				labels.append(label)
				
				hist, bin_edges = np.histogram(specificcount, bins=bincount, range=zrange)
				bin_centres = (bin_edges[:-1] + bin_edges[1:])/2
				
				total = len(specificcount)
				
				if float(full) > 0:
					fraction = float(passing)/float(full)
					info += str("For N = " + str(j) + " we require BDT >  " + str(bdtmin) + "\n ")
					info += str("Fraction passing is " + str(fraction) + "\n")
				
				if float(total) > float(0):
				
					meanz = np.mean(specificcount)
					meansigma = np.mean(differences)
					
					info += ('Mean = ' + str('{0:.2f}'.format(meanz)) + " \n")
					
					if float(meansigma) == float(0):
						differences.append(1)
						limitsigma = np.mean(differences)
						info += ('Sigma < ' + str(limitsigma) + "\n")

					else:
						info += ('Sigma = ' + str(meansigma) + "\n")
				
				info += "\n"
				
				
			k +=1
		print info	
				
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
		
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.annotate(info, xy=(0.8, 0.8), xycoords="axes fraction",  fontsize=10)
	plt.suptitle("True Z reconstruction", fontsize=20)
	plt.legend()
	
	plt.savefig(path)
	print "saving to", path
		
	if graph:
		plt.show()
		
	else:
		plt.close()
