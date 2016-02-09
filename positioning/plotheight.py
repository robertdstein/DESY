import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections, graph):
	fullcount=[]
	labels=[]
	
	for j in range (detectorcount, mindetections -1, -1):
		specificcount=[]
		
		with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			for row in reader:
				if i == 0:
					i = 1
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
					
					if int(detections) == int(j):
						difference= float(reconHeight) - float(trueHeight)
						specificcount.append(difference)

		fullcount.append(specificcount)
		label = str(j) + " detections"
		labels.append(label)
			
	plt.hist(fullcount, bins=30, range=[-30000,20000], label=labels, histtype='bar', stacked=True)

	plt.xlabel("Distance from True Height")
	plt.ylabel("Count")
	plt.title("Height Reconstruction")
	plt.legend()
	
	plt.savefig('graphs/height.pdf')
	
	if graph:
		plt.show()	
