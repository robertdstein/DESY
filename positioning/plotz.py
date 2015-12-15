import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections):
	with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		zvalues = np.arange(1,9)
		bincount = len(zvalues)
		
		fullcount = []
		
		plt.show()
		
		for val in zvalues:
			
			z = val + 20
			
			plt.subplot(4, 2, val)
			fullcount = []
			
			for i in range (mindetections, detectorcount):
				
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
						
						if detections == i:
							if z == trueZ:
								specificcount.append(reconZ)
								fullcount.append(reconZ)
								
				label = str(i) + "detections"
					
				plt.hist(specificcount, bins=bincount, normed=true, histtype='stepfilled', label=label)
					
			plt.hist(fullcount, bins=bincount, normed=true, histtype='stepfiled', label="All")
			
		plt.show()		
