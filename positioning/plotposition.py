import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections, graph, cuts, allcounts=None):
	fullcount=[]
	labels=[]
	info = ""
	k=0
	for j in range (detectorcount, mindetections -1, -1):
		specificcount=[]
		
		if allcounts != None:
			count = allcounts[detectorcount-j]
			testcount = int(float(count)/4.) 
					
		else:
			testcount = 0
		
		with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			specificcount = []
			
			full=0
			passing=0
			
			i = -1
			
			bdtmin = cuts[k]

			for row in reader:
				if i < (2*testcount):
					i += 1
				else:
					detections = row[0]
					reconx = float(row[1])
					recony = float(row[2])
					reconEPN = row[3]
					reconZ = row[4]
					reconHeight = row[5]
					truex = float(row[6])
					truey = float(row[7])
					trueEPN = row[8]
					trueZ = row[9]
					trueHeight = row[10]
					likelihood = row[13]
					classifier = float(row[15])
					BDT = row[16]
					
					if int(detections) == int(j):
						full += 1
						if float(bdtmin) < float(BDT):
							if float(classifier) < float(1.5):
								passing += 1
								distance = math.sqrt(((reconx-truex)**2)+(recony-truey)**2)
								specificcount.append(distance)

		total = len(specificcount)
		
		if float(total) > float(0):
			fullcount.append(specificcount)
			label = str(j) + " detections"
			labels.append(label)

			specificcount.sort()
		
			lower = int(0)
			mid = int(total*0.5)
			upper = int(total*0.68)
			
			lowerz = 0
			meanz = specificcount[mid]
			upperz = specificcount[upper]
			sigma = (upperz-lowerz) * 0.5
			
			fraction = float(passing)/float(full)
			info += str("For N = " + str(j) + " we require BDT >  " + str(bdtmin) + "\n ")
			info += str("Fraction passing is " + str(fraction) + "\n")
			
			info += ('Upper bound = ' + str(upperz) + " \n")
			info += ('Median = ' + str(meanz) + " \n")
			info += ('Sigma = ' + str(sigma) + "\n \n")
	
		k +=1
	
	plt.annotate(info, xy=(0.6, 0.3), xycoords="axes fraction",  fontsize=15)
	
	n, bins, _ = plt.hist(fullcount, bins=30, range=[0,30], label=labels, histtype='bar', stacked=True)

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
	
	uplim = nmax + 2*(math.sqrt(nmax))
	
	plt.ylim(0, uplim)
	
	nmax = np.amax(n)
	
	uplim = nmax + (math.sqrt(nmax))
	
	plt.ylim(0, uplim)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)

	plt.xlabel("Distance from True Position")
	plt.ylabel("Count")
	plt.title("Distance Reconstruction")
	plt.legend()
	
	path = '/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/position.pdf'
	plt.savefig(path)
	print "saving to", path
	
	if graph:
		plt.show()
		
	else:
		plt.close()
