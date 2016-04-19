import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="1385224")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1
j = 2000
totalevents = 0
DCpasstotal = 0
correctevents =0
totalcut=0
correctcut = 0

cut = 0.9
DCcut = 6500

right = []
wrong = []
DCcounts =[]

targetfolder = filepath + cfg.jobID +"/"

while (i < j):
	if (os.path.isfile(targetfolder + "run" + str(i) + "/stats1.txt")):
		for k in range(1,5):
		
			path = targetfolder + "run" + str(i) + "/stats" + str(k) + ".txt"
			print path
			
			DCpath =  targetfolder + "run" + str(i) + "/DCpixel" + str(k) + ".text"
			
			with open(path, 'rb') as f:
				result = float(f.readline())
				score = float(f.readline())
				regularmethodscore = float(f.readline())
				
				with open(DCpath, 'rb') as g:
					g.readline()
					entry = eval(g.readline())
					DCcount = entry[1]
					DCcounts.append(DCcount)
				
				totalevents += 1
				
				if DCcount > DCcut:
					
					DCpasstotal += 1
					
					if float(result) == float(1):
						correctevents += 1
						right.append(score)
						if float(score) > float(cut):
							correctcut += 1
							totalcut += 1
					elif float(result) == float(0):
						wrong.append(score)
						if float(score) > float(cut):
							totalcut += 1
							
					

	i+=1
	
print totalevents, "Total Events"
print correctevents, "Correct Events"
if totalevents > 0:
	print "Successful DC pixel Identification of", float(100.*correctevents/totalevents), "%"
	
print "Cut requires BDT >", cut
print totalcut, "Total Events"
print correctcut, "Correct Events"
if totalcut > 0:
	print "Successful DC pixel Identification after cut is ", float(100.*correctcut/totalcut), "%"

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.subplot(2,1,1)
plt.hist(DCcounts, bins=30)
plt.xlabel("DC pixel count")
plt.subplot(2,1,2)
plt.hist([right, wrong], color=['g', 'r'], stacked=True, bins=50)
plt.xlabel("BDT score")
plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/stats.pdf")
	

