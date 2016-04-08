#!/bin/env python

import sys
import os.path

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'

sys.path.append(afspath)

import argparse, math, random, time
import csv
import numpy as np

nparrallel = 50

targetfolder = "reconstructeddata/"

batchname= "executereconstructed"


with open(afspath + targetfolder + batchname + "_combined.csv", 'wb') as csvout:
	writer = csv.writer(csvout, delimiter=',', quotechar='|')
	
	j=-1
	
	for i in range (1, int(nparrallel)+1):
		filename= batchname + str(i)
		path = afspath + targetfolder + filename + ".csv"
		
		if os.path.isfile(path):
		
			print "Adding", path
	
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
			
	filename= batchname + "_saved"
	path = afspath + targetfolder + filename + ".csv"
		
	print "Adding", path
	with open(path, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		j = 0
		for row in reader:
			if j == 1:
				writer.writerow(row)
			elif j == 0:
				j = 1
