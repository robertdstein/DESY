import time, math
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import matplotlib.pyplot as plt
import argparse
import csv
from sklearn.externals import joblib

def run(source, detectorcount, mindetections):
	
	allcounts=[]
	
	for k in range (detectorcount, mindetections -1, -1):

		count = 0
		
		with open("/d6/rstein/Hamburg-Cosmic-Rays/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			
			j = 0
	
			for row in reader:
				if j == 0:
					j = 1
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
					likelihood = row[13]
					
					if int(detections) == int(k):
						count +=1
						
			allcounts.append(count)
			
	return allcounts
							
