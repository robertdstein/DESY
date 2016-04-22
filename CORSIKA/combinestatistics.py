import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import os.path

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar

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

combinedtotal = 0
combinedcorrect = 0

cut = 0.45
oldcut = 1.3
DCcut = 5500

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
						if float(score) > float(cut):
							correctcut += 1
							totalcut += 1
							combined=True
					elif float(result) == float(0):
						wrong.append(score)
						if float(score) > float(cut):
							totalcut += 1
							combined=True
					
					if float(oldresult) == float(1):
						oldcorrectevents += 1
						oldright.append(oldQDC)
						if float(oldQDC) > float(oldcut):
							oldcorrectcut += 1
							oldtotalcut += 1
							combined=True
					elif float(oldresult) == float(0):
						oldwrong.append(oldQDC)
						if float(oldQDC) > float(oldcut):
							oldtotalcut += 1
							combined=True
							
					if combined:
						if float(oldQDC) > float(oldcut):
							if float(oldresult) == float(1):
								combinedcorrect += 1
								combinedtotal += 1
							else:
								combinedtotal += 1
						else:
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
message += "We have", str(DCpasstotal), "DC events \n \n"

message += "Of these,", str(oldcorrectevents), "are Correctly Identified Events using QDC method."
if DCpasstotal > 0:
	message += "Old successful DC pixel Identification of", str('{0:.1f}'.format(float(100.*oldcorrectevents/DCpasstotal))), "% \n \n"

message += "Of these,", str(correctevents), "are Correctly Identified Events using BDT."
if DCpasstotal > 0:
	message += "Successful BDT DC pixel Identification of", str('{0:.1f}'.format(float(100.*correctevents/DCpasstotal))), "% \n \n"

message += "Our old QDC cut requires QDC >", str(oldcut), ". "
message += "We have", str(oldtotalcut), "events passing this cut. "
message += "Of these,", str(oldcorrectcut), "are Correctly Identified Events. "
if oldtotalcut > 0:
	message += "Successful DC pixel Identification after cut is", str('{0:.1f}'.format(float(100.*oldcorrectcut/oldtotalcut))), "% \n \n"
	
message += "Our BDT cut requires Signal Probability >", str(cut), ". "
message += "We have", str(totalcut), "events passing this cut. "
message += "Of these,", str(correctcut), "are Correctly Identified Events. "
if totalcut > 0:
	message += "Successful DC pixel Identification after cut is", str('{0:.1f}'.format(float(100.*correctcut/totalcut))), "% \n \n"
	
message += "We check for an event that has QDC >", str(oldcut), ", and if not, require Signal Probability >", str(cut), ". "
message += "We have", str(combinedtotal), "events passing this cut. "
message += "Of these,", str(combinedcorrect), "are Correctly Identified Events. "
if oldtotalcut > 0:
	message += "Successful DC pixel Identification after cut is", str('{0:.1f}'.format(float(100.*combinedcorrect/combinedtotal))), "% \n \n"
	
toprint = ' '.join(message)
print toprint

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

plt.subplot(3,2,1)
plt.hist(DCcounts, bins=30)
plt.xlabel("DC pixel count")

plt.subplot(3,2,2)

plt.title("Distribution of QDC-reconstructed Events")
plt.hist([oldright, oldwrong], color=['g', 'r'], stacked=True, bins=50)
plt.xlabel("QDC value")

plt.subplot(3,2,3)
plt.title("Distribution of BDT-reconstructed Events")
plt.hist([right, wrong], color=['g', 'r'], stacked=True, bins=50)
plt.xlabel("BDT score")

plt.subplot(3,2,4)
plt.title("Distribution of BDT-reconstructed Events, after QDC cuts")
plt.hist([combinedright, combinedwrong], color=['g', 'r'], stacked=True, bins=50)
plt.xlabel("BDT score")

plt.subplot(3,1,3)
plt.axis('off')
plt.annotate(toprint, xy=(0.0, 0.25), xycoords="axes fraction",  fontsize=10)

figure = plt.gcf() # get current figure
figure.set_size_inches(20, 15)

plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/stats.pdf")
	

