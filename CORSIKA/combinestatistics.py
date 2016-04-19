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

oldtotalevents = 0
oldDCpasstotal = 0
oldcorrectevents =0
oldtotalcut=0
oldcorrectcut = 0

cut = 0.9
oldcut = 1.3
DCcut = 6500

right = []
wrong = []

oldright=[]
oldwrong=[]

DCcounts =[]

targetfolder = filepath + cfg.jobID +"/"

while (i < j):
	for k in range(1,5):
		path = targetfolder + "run" + str(i) + "/stats" + str(k) + ".txt"
		if (os.path.isfile(path)):
			print path
			
			DCpath =  targetfolder + "run" + str(i) + "/DCpixel" + str(k) + ".text"
			
			with open(path, 'rb') as f:
				result = float(f.readline())
				score = float(f.readline())
				oldresult = float(f.readline())
				oldQDC = float(f.readline())
				
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
					
					if float(oldresult) == float(1):
						oldcorrectevents += 1
						oldright.append(oldQDC)
						if float(oldQDC) > float(oldcut):
							oldcorrectcut += 1
							oldtotalcut += 1
					elif float(oldresult) == float(0):
						oldwrong.append(oldQDC)
						if float(oldQDC) > float(oldcut):
							oldtotalcut += 1
							
					

	i+=1
	
print "\n \n", totalevents, "Total Events"
print "We define a DC event as one in which the DC pixel has a shower-free count of", DCcut, "or more"
print "We have", DCpasstotal, "DC events \n \n"

print "Of these,", correctevents, "are Correctly Identified Events using BDT"
if DCpasstotal > 0:
	print "Successful BDT DC pixel Identification of", float(100.*correctevents/DCpasstotal), "% \n \n"

print "Of these,", oldcorrectevents, "are Correctly Identified Events using QDC method"
if DCpasstotal > 0:
	print "Old successful DC pixel Identification of", float(100.*oldcorrectevents/DCpasstotal), "% \n \n"
	
print "Our BDT cut requires Signal Probability >", cut
print "We have", totalcut, "events passing this cut"
print "Of these,", correctcut, "are Correctly Identified Events"
if totalcut > 0:
	print "Successful DC pixel Identification after cut is", float(100.*correctcut/totalcut), "% \n \n"
	
print "Our old QDC cut requires QDC >", oldcut
print "We have", oldtotalcut, "events passing this cut"
print "Of these,", oldcorrectcut, "are Correctly Identified Events"
if oldtotalcut > 0:
	print "Successful DC pixel Identification after cut is", float(100.*oldcorrectcut/oldtotalcut), "% \n \n"

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

plt.subplot(3,1,1)
plt.hist(DCcounts, bins=30)
plt.xlabel("DC pixel count")

plt.subplot(3,1,2)
plt.title("Distribution of BDT-reconstructed Events")
plt.hist([right, wrong], color=['g', 'r'], stacked=True, bins=50)
plt.xlabel("BDT score")

plt.subplot(3,1,3)
plt.title("Distribution of QDC-reconstructed Events")
plt.hist([oldright, oldwrong], color=['g', 'r'], stacked=True, bins=50)
plt.xlabel("QDC value")

plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/stats.pdf")
	

