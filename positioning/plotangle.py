import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt

def run(source, detectorcount, mindetections, graph):
	fig = plt.figure()
	plt1 = fig.add_subplot(2,1,1)
	plt2 = fig.add_subplot(2,1,2)
	
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
				phi = row[11]
				
				deviation = math.degrees(math.fabs((0.5*math.pi)-float(phi)))

				if int(detections) == int(detectorcount):
					color = "b"
				elif int(detections) == int(mindetections):
					color = "r"
				else:
					color = "g"
				
				distance = math.sqrt(((reconx-truex)**2)+(recony-truey)**2)
				
				zerror=math.fabs(float(trueZ)-float(reconZ))
				
				plt1.scatter(deviation, distance, color=color)
				plt2.scatter(deviation, zerror, color=color) 

	plt1.set_ylabel("Distance from True Position")
	plt1.set_xlabel("Zenith Angle Deviation")
	plt1.set_title("Distance Reconstruction with Zenith angle")

	plt2.set_ylabel("Error in True Z")
	plt2.set_xlabel("Zenith Angle Deviation")
	plt2.set_title("Z Reconstruction with Zenith angle")
	
	fig.savefig('graphs/zenithangle.pdf')
	
	if graph:
		fig.show()
		raw_input("prompt")
