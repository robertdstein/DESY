import argparse, math, random
import csv
import numpy as np
import minimise as m
import pltx as px
import ploty as py
import plotepn as pe
import plotz as pz
import plotheight as ph

def run(source, outputfile, detectorcount, variable, mindetections, detectorcount):
	with open("data/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for i in range (mindetections, detectorcount):
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
				
