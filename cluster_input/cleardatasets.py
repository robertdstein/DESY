#!/bin/env python

import sys
import os.path

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'

sys.path.append(afspath)

import argparse, math, random, time
import csv
import numpy as np

nparrallel = 500

targetfolder = "reconstructeddata/"

batchname= "executereconstructed"


with open(afspath + targetfolder + batchname + "_saved.csv", 'wb') as csvout:
	writer1 = csv.writer(csvout, delimiter=',', quotechar='|')
	
	for i in range (1, int(nparrallel)+1):
		filename= batchname + str(i)
		path = afspath + targetfolder + filename + ".csv"
		
		if os.path.isfile(path):
		
			print "Clearing", path
	
			with open(path, 'wb') as csvfile:
				writer2 = csv.writer(csvfile, delimiter=',', quotechar='|')
				writer2.writerow(["Detections","X","Y","Energy Per Nucleon","Z","Height","True X","True Y","True Energy per nucleon","True Z","True Height", "Phi", "Epsilon", "Guess Log Likelihood", "True Log Likelihood"])
			
	#~ filename= batchname + "_combined"
	#~ path = afspath + targetfolder + filename + ".csv"
		
	#~ print "Adding", path
	#~ with open(path, 'rb') as csvfile:
		#~ reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#~ j = 0
		#~ for row in reader:
			#~ writer1.writerow(row)
