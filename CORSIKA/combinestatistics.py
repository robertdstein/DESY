import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import os.path
import initialisecuts as ic

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="1957737")

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

combinedtotal = 0
combinedcorrect = 0

cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

right = []
wrong = []

oldright=[]
oldwrong=[]

combinedright = []
combinedwrong = []

DCcounts =[]

targetfolder = filepath + cfg.jobID +"/"

custom_options = {
	'end': 100,
	'width': 100,
	'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

p = ProgressBar(**custom_options)
print p


while (i < j):
	for k in range(1,5):
		path = targetfolder + "run" + str(i) + "/stats" + str(k) + ".txt"
		if (os.path.isfile(path)):
			
			DCpath =  targetfolder + "run" + str(i) + "/DCpixel" + str(k) + ".text"
			
			with open(path, 'rb') as f:
				result = float(f.readline())
				score = float(f.readline())
				oldresult = float(f.readline())
				oldQDC = float(f.readline())
				raw = str(f.readline()).rstrip()
				entry = eval(raw)
				count = entry[1]
				nnmean= entry[13]
				signal = count-nnmean
				
				with open(DCpath, 'rb') as g:
					g.readline()
					entry = eval(g.readline())
					DCcount = entry[1]
					DCcounts.append(DCcount)
				
				totalevents += 1
				
				if DCcount > DCcut:
					
					DCpasstotal += 1
					
				combined=False
				
				if float(result) == float(1):
					correctevents += 1
					right.append(score)
					if float(ucut) > float(score) > float(cut):
						correctcut += 1
						totalcut += 1
						combined=True
				elif float(result) == float(0):
					wrong.append(score)
					if float(ucut) > float(score) > float(cut):
						totalcut += 1
						combined=True
				
				if float(oldresult) == float(1):
					oldcorrectevents += 1
					oldright.append(oldQDC)
					if float(oldQDC) > float(QDCcut):
						oldcorrectcut += 1
						oldtotalcut += 1
						combined=True
				elif float(oldresult) == float(0):
					oldwrong.append(oldQDC)
					if float(oldQDC) > float(QDCcut):
						oldtotalcut += 1
						combined=True
						
				if combined:
					if float(oldQDC) > float(QDCcut):
						if float(oldresult) == float(1):
							combinedcorrect += 1
							combinedtotal += 1
						else:
							combinedtotal += 1
					elif float(signal) > float(signalcut):
						if float(result) == float(1):
							combinedcorrect += 1
							combinedtotal += 1
							combinedright.append(score)
						else:
							combinedtotal += 1
							combinedwrong.append(score)

	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1
	
message = []
	
message += "\n \n", str(totalevents), "Total Events. "
message += "We define a DC event as one in which the DC pixel has a shower-free count of", str(DCcut), "or more."
message += "We have", str(DCpasstotal), "DC events. \n"

message += "Of these,", str(oldcorrectevents), "are Correctly Identified Events using QDC method."
if DCpasstotal > 0:
	message += "Old successful ID rate of", str('{0:.1f}'.format(float(100.*oldcorrectevents/DCpasstotal))), "%. \n"

message += "Of these,", str(correctevents), "are Correctly Identified Events using BDT method."
if DCpasstotal > 0:
	message += "Successful ID rate  of", str('{0:.1f}'.format(float(100.*correctevents/DCpasstotal))), "% \n \n"

message += "Our QDC cut requires QDC >", str(QDCcut), ". "
message += "We have", str(oldtotalcut), "events passing this cut. "
message += "Of these,", str(oldcorrectcut), "are Correctly Identified Events. \n "
if oldtotalcut > 0:
	message += "Successful ID rate after cut is", str('{0:.1f}'.format(float(100.*oldcorrectcut/oldtotalcut))),  "% "
	message += "Fraction of DC pixels correctly identified is", str('{0:.1f}'.format(float(100.*oldcorrectcut/DCpasstotal))), "% \n \n"
	
message += "Our BDT cut requires Signal Probability >", str(cut), ". "
message += "We have", str(totalcut), "events passing this cut. "
message += "Of these,", str(correctcut), "are Correctly Identified Events.\n  "
if totalcut > 0:
	message += "Successful ID rate after cut is", str('{0:.1f}'.format(float(100.*correctcut/totalcut))), "% "
	message += "Fraction of DC pixels correctly identified is", str('{0:.1f}'.format(float(100.*correctcut/DCpasstotal))), "% \n \n"
	
message += "We check for an event that has QDC >", str(QDCcut), ", or if not, \n "
message += "require Signal Probability >", str(cut), "and signal >", str(signalcut), ". \n"
message += "We have", str(combinedtotal), "events passing this cut. "
message += "Of these,", str(combinedcorrect), "are Correctly Identified Events. \n "
if oldtotalcut > 0:
	message += "Successful ID rate after cut is", str('{0:.1f}'.format(float(100.*combinedcorrect/combinedtotal))), "% "
	message += "Fraction of DC pixels correctly identified is", str('{0:.1f}'.format(float(100.*combinedcorrect/DCpasstotal))), "% \n \n"
	
toprint = ' '.join(message)
print toprint

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

for rows in [2, 3]:

	ax1 = plt.subplot(rows,2,1)
	plt.title("Signal in pure DC pixel without shower")
	plt.hist(DCcounts, bins=30)
	plt.xlabel("DC pixel count")
	
	ax2 = plt.subplot(rows,2,2)
	
	plt.title("Distribution of QDC-reconstructed Events")
	plt.hist([oldright, oldwrong], color=['g', 'r'], stacked=True, bins=50)
	plt.xlabel("QDC value")
	
	ax3 = plt.subplot(rows,2,3)
	plt.title("Distribution of BDT-reconstructed Events")
	plt.hist([right, wrong], color=['g', 'r'], stacked=True, bins=50)
	plt.xlabel("BDT score")
	
	ax4 = plt.subplot(rows,2,4)
	plt.title("Distribution of BDT-reconstructed Events, after cuts")
	plt.hist([combinedright, combinedwrong], color=['g', 'r'], stacked=True, bins=50)
	plt.xlabel("BDT score")
	
	figure = plt.gcf() # get current figure
	if rows == 2:
		figure.set_size_inches(15, 15)
		plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/cutdistribution.pdf")
		
	elif rows ==3:
		figure.set_size_inches(20, 15)
		ax5 = plt.subplot(3,1,3)
		plt.axis('off')
		plt.annotate(toprint, xy=(0.0, 0.25), xycoords="axes fraction",  fontsize=10)
		plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/stats.pdf")
	

