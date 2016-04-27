import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import os.path
import initialisecuts as ic
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="1957737")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1
j = 500

passed = [[], []]
rejected = [[], []]
passeddiff=[]
rejecteddiff=[]

passedcsignals= [[], [], [], []]
passedDCsignals = [[], [], [], []]
rejectedcsignals = [[], [], [], []]
rejectedDCsignals =[[], [], [], []]

targetfolder = filepath + cfg.jobID +"/"

cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

custom_options = {
	'end': 100,
	'width': 100,
	'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

p = ProgressBar(**custom_options)
print p

while (i < j):
	for k in range(1,5):
		path = targetfolder + "run" + str(i) + "/candidate" + str(k) + ".txt"
		if (os.path.isfile(path)):
			
			DCpath =  targetfolder + "run" + str(i) + "/DCpixel" + str(k) + ".text"
			
			with open(path, 'rb') as f:
				result = str(f.readline()).rstrip()
				candidateentry = eval(str(f.readline()))
				candidatecount = candidateentry[1]
				candidatennmean = candidateentry[13]
				candidatesignal = candidatecount-candidatennmean
				score = candidateentry[14]
				
				candidatenn = candidateentry[6]
				nnmax = np.max(candidatenn)
				nnmin = np.min(candidatenn)
				bkg = 0.5* (nnmax + nnmin)
				newsig = candidatecount - bkg
				
				passcut = False
				
				if (str(result) == str(True)):
					markerindex = 2
					passcut = True
				else:
					markerindex = 0
					if float(cut) < float(score) < float(ucut):
						if float(candidatesignal) > float(signalcut):
							passcut = True
							
				#~ candidatesignal=newsig

				with open(DCpath, 'rb') as g:
					g.readline()
					DCentry = eval(g.readline())
					DCcount = DCentry[1]
					DCnnmean = DCentry[13]
					DCsignal = DCcount-DCnnmean 
					
					difference = (candidatesignal - DCsignal)
					absd = math.fabs(difference)
					
					if int(DCentry[0]) == int(candidateentry[0]):
						colorindex=0
					else:
						colorindex = 1
						
					index =  int(colorindex + markerindex)

					if passcut:
						passed[colorindex].append(difference)
						passeddiff.append(absd)
						passedcsignals[index].append(candidatesignal)
						passedDCsignals[index].append(DCsignal)
						
					else:
						rejected[colorindex].append(difference)
						rejecteddiff.append(absd)
						rejectedcsignals[index].append(candidatesignal)
						rejectedDCsignals[index].append(DCsignal)			
				
	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

colors =['g', 'r']

ax2 = plt.subplot(2,2,2)
plt.hist(rejected, color=colors, stacked=True, bins=50)
plt.title("DC pixel error for rejected events")
plt.xlabel("Difference from true count")

ax1 = plt.subplot(221, sharex=ax2)
plt.hist(passed, color=colors, stacked=True, bins=50)
plt.title("DC pixel error for events passing cuts")
plt.xlabel("Difference from true count")

markers=["o", "*"]

ax4 = plt.subplot(2,2,4)
for i in range(2):
	for j in range(2):
		plt.scatter(rejectedcsignals[int(2*float(j) + i)], rejectedDCsignals[int(2*float(j) + i)], color=colors[i], marker=markers[j])
plt.plot([0,8000], [0, 8000], color='k')
plt.xlabel("Candidate reconstructed signal")
plt.title("True vs. reconstructed signal for rejected events")
plt.ylabel("Pure DC signal")

ax3 = plt.subplot(223, sharex = ax4, sharey=ax4)
for i in range(2):
	for j in range(2):
		plt.scatter(passedcsignals[int(2*float(j) + i)], passedDCsignals[int(2*float(j) + i)], color=colors[i], marker=markers[j])
plt.plot([0,8000], [0, 8000], color='k')
plt.xlabel("Candidate reconstructed signal")
plt.title("True vs. reconstructed signal for accepted events")
plt.ylabel("Pure DC signal")

i=1

for category in ["passed", "rejected"]:

	allevents = eval(category +"[0]")
	allevents.extend(eval(category +"[1]"))
	allevents.sort()
	
	alldiff= eval(category + "diff")
	
	alldiff.sort()
	
	nentries = len(allevents)
	halfinteger = int(0.5*nentries)
	lowerinteger = int(0.16*nentries)
	upperinteger = int(0.84*nentries)
	integer68 = int(0.68*nentries)
	
	lower = allevents[lowerinteger]
	upper = allevents[upperinteger]
	
	toprint= "Mean = " + str('{0:.1f}'.format(np.mean(allevents)))
	toprint += ". Median = " + str('{0:.1f}'.format(allevents[halfinteger])) + "\n"
	toprint += "Lower = " + str('{0:.1f}'.format(lower))
	toprint += ". Upper = " + str('{0:.1f}'.format(upper)) + "\n"
	toprint += "Sigma = " + str('{0:.1f}'.format(0.5*(upper-lower))) + "\n"
	
	toprint += "Mean absolute difference = "+ str('{0:.1f}'.format(np.mean(alldiff))) + "\n"
	toprint += "Median absolute difference = " + str('{0:.1f}'.format(alldiff[halfinteger])) + "\n"
	toprint += "Sigma = " + str('{0:.1f}'.format(alldiff[integer68])) + "\n"
	
	eval("ax" + str(i) + ".annotate(toprint, xy=(0.02, 0.75), xycoords='axes fraction',  fontsize=10)")
	
	i+=1


figure = plt.gcf() # get current figure
figure.set_size_inches(20, 20)

plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/errorstats.pdf")
plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/DCcounterror.pdf")
	

