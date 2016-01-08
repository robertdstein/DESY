import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections, graph):

	zvalues = [26]
	nplots = len(zvalues)
	bincount = 13
	i=1
	
	zrange = [19.5, 32.5]
	
	for val in zvalues:
		
		z = val
		
		plt.subplot(nplots, 1, i)
		
		i+=1
		
		plt.subplots_adjust(hspace = 0.5)
		fullcount = []
		labels=[]
		
		title = "Z is " + str(int(z))
		
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
