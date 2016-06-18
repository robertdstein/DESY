#!/bin/env python

import sys
import os.path

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'

sys.path.append(afspath)

import argparse, math, random, time
import csv
import numpy as np

nparrallel = 5000

targetfolder = "reconstructeddata/"

batchname= "executereconstructed"

combinedstatspath = afspath + targetfolder + batchname + "_combined.csv"
combinedbdtpath = afspath + targetfolder + batchname + "_trainingset.csv"

with open(combinedstatspath, 'wb') as csvout1:
	writer1 = csv.writer(csvout1, delimiter=',', quotechar='|')
	
	with open(combinedbdtpath, 'wb') as csvout2:
		writer2 = csv.writer(csvout2, delimiter=',', quotechar='|')
	
		j=-1
		
		for i in range (1, int(nparrallel)+1):
			filename= batchname + str(i)
			path = afspath + targetfolder + filename + ".csv"
			
			if os.path.isfile(path):
			
				print "Adding", path
				
				if random.random() > 0.5:
					writer = writer1
				else:
					writer = writer2
		
				with open(path, 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					
					for row in reader:
						if j == -1:
							writer.writerow(row)
							j = 1
						elif j == 1:
							writer.writerow(row)
						elif j == 0:
							j = 1
							pass
					
				j = 0
			
	#~ filename= batchname + "_saved"
	#~ path = afspath + targetfolder + filename + ".csv"
		#~ 
	#~ print "Adding", path
	#~ with open(path, 'rb') as csvfile:
		#~ reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		#~ j = 0
		#~ for row in reader:
			#~ if j == 1:
				#~ writer.writerow(row)
			#~ elif j == 0:
				#~ j = 1
