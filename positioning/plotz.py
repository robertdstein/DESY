import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections, graph):

	zvalues = np.arange(1,9)
	bincount = len(zvalues)
	
	for val in zvalues:
		
		z = float(val + 20)
		
		plt.subplot(4, 2, val)
		fullcount = []
		labels=[]
		
		title = "Z is " + str(z)
		
		for j in range (mindetections, detectorcount +1):
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
			
		if fullcount != []:
			plt.hist(fullcount, bins=bincount, histtype='bar', range=[20.5, 28.5], label=labels, stacked=True)
		
		
		plt.title(title)	
		plt.legend()		
	plt.savefig('graphs/Z.pdf')
		
	if graph:
		plt.show()
