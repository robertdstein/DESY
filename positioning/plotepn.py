import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections, graph):
	with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
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
				
				if int(detections) == int(detectorcount):
					colour = 'b'
				elif int(detections)==int(mindetections):
					colour = 'r'
				else:
					colour = 'g'
				
				plt.scatter(trueEPN,reconEPN, color=colour)

		e=np.linspace(250,3500,1000)
		plt.plot(e,e,color='black')

		plt.xlabel("True Epn")
		plt.ylabel("Reconstructed Epn")
		plt.title("Reconstruction of Energy per Nucleon")
		plt.savefig('graphs/epn.pdf')
		
		if graph:
			plt.show()
