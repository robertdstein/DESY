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
					reconEPN = float(row[3])
					reconZ = row[4]
					reconHeight = row[5]
					truex = float(row[6])
					truey = float(row[7])
					trueEPN = float(row[8])
					trueZ = row[9]
					trueHeight = row[10]
					
					if int(detections) == int(j):
						difference = (reconEPN-trueEPN)/trueEPN
						specificcount.append(difference)

		fullcount.append(specificcount)
		label = str(j) + " detections"
		labels.append(label)
			
	plt.hist(fullcount, bins=50, range=[-2,2], label=labels, histtype='bar', stacked=True)

	plt.ylabel("Count")
	plt.xlabel("Fractional diference from True EPN")
	plt.title("Reconstruction of Energy per Nucleon")
	plt.legend()
	plt.savefig('graphs/epn.pdf')
	
	
	if graph:
		plt.show()
