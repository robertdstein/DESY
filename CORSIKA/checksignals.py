import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="2567181")

cfg = parser.parse_args()

hess1rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess1signalregressor.p'
hess2rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess2signalregressor.p'
if os.path.isfile(hess1rgrpath):
	hess1rgr = pickle.load(open(hess1rgrpath, "r"))
else:
	print "No hess1 pickle!"
if os.path.isfile(hess2rgrpath):
	hess2rgr = pickle.load(open(hess2rgrpath, "r"))
else:
	print "No hess2 pickle!"
	
signalbdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/signalBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		signalbdtvariables.append(row[0])
print signalbdtvariables

def makeBDTentry(pixelentry):
	bdtentry =[]
	for variable in signalbdtvariables:
		varsplit = variable.split('.')
		suffix = pixelentry
		if len(varsplit) > 1:
			for name in varsplit[:-1]:
				 suffix = getattr(suffix, name)
			varname = varsplit[-1]
		else:
			varname = variable
		if hasattr(suffix, varname):
			newval = getattr(suffix, varname)
			bdtentry.append(newval)
		else:
			return None
	return bdtentry

filepath = "/nfs/astrop/d6/rstein/data/"
i = 1
j = 100
totalimages = [0, 0]
DCpasstotal = [0, 0]
correctimages =[0, 0]
totalcut=[0, 0]
correctcut = [0, 0]

oldtotalimages =[0, 0]
oldDCpasstotal = [0, 0]
oldcorrectimages =[0, 0]
oldtotalcut=[0, 0]
oldcorrectcut = [0, 0]

altcorrectimages =[0, 0]
alttotalcut=[0, 0]
altcorrectcut = [0, 0]

combinedtotal = [0, 0]
combinedcorrect = [0, 0]

cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

right = [[], []]
wrong = [[], []]

oldright=[[], []]
oldwrong=[[], []]

combinedright = [[], []]
combinedwrong = [[], []]
DCcounts =[[], []]
rightscores =[[], []]
wrongscores = [[], []]
rightsignals =[[], []]
wrongsignals = [[], []]

passed = [[[], []], [[], []]]
rejected = [[[], []], [[], []]]
passeddiff=[[], []]
rejecteddiff=[[], []]

passedcsignals= [[[], []], [[], []]]
passedDCsignals = [[[], []], [[], []]]
rejectedcsignals = [[[], []], [[], []]]
rejectedDCsignals =[[[], []], [[], []]]



targetfolder = filepath + cfg.jobID +"/"

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar
custom_options = {
	'end': 100,
	'width': 100,
	'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

p = ProgressBar(**custom_options)
print p

hessstatus=[False, False]
if os.path.isfile(hess1picklepath):
	hessstatus[0] = True
if os.path.isfile(hess2picklepath):
	hessstatus[1] = True
if not os.path.isfile(hess1picklepath) and not os.path.isfile(hess2picklepath):
	raise Exception("No BDT saved, so no results to plot!")

while (i < j):
	targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
	if (os.path.isfile(targetpath)):
		event = pickle.load(open(targetpath, 'rb'))
		if hasattr(event.simulations, "DC") and hasattr(event.simulations, "full"):
			DCsim =event.simulations.DC
			fullsim = event.simulations.full
			
			for index in DCsim.triggerIDs:
				DCtel = DCsim.images[index]
				fulltel =  fullsim.images[index]
				
				trueID = DCtel.trueDC
				DCtrue = DCtel.getpixel(trueID)
				DCcount = DCtrue.channel1.intensity
				
				if fulltel.size == "HESS1":
					plotindex = 0
					toplot = hessstatus[0]
				elif fulltel.size == "HESS2":
					plotindex = 1
					toplot = hessstatus[1]
				else:
					raise Exception("Telescope.size error, size is " +fulltel.size) 

				DCcounts[plotindex].append(DCcount)
				
				fullBDT = fulltel.getpixel(trueID)
				
				if fullBDT.bdtscore != None:
											
					candidatesignal = fullBDT.channel1.intensity
						
					
					difference = (candidatesignal - DCcount)
					absd = math.fabs(difference)
				
					totalimages[plotindex] += 1
					
					if DCcount > DCcut:
						DCpasstotal[plotindex] += 1
					
					if fulltel.BDTID == trueID:
						result = 1
						rightscores[plotindex].append(fullBDT.bdtscore)
						rightsignals[plotindex].append(candidatesignal)
					elif fulltel.BDTID == None:
						print "None!!!"
					else:
						result = 0
						wrongscores[plotindex].append(fullBDT.bdtscore)
						wrongsignals[plotindex].append(candidatesignal)
					
					passcut = False
					
					if float(result) == float(1):
						correctimages[plotindex] += 1
						right[plotindex].append(fullBDT.bdtscore)
						if float(ucut) > float(fullBDT.bdtscore) > float(cut):
							correctcut[plotindex] += 1
							totalcut[plotindex] += 1
							if float(candidatesignal) > float(signalcut):
								passcut = True	
								combinedcorrect[plotindex] += 1
								combinedtotal[plotindex] += 1
								combinedright[plotindex].append(fullBDT.bdtscore)
					elif float(result) == float(0):
						wrong[plotindex].append(fullBDT.bdtscore)
						if float(ucut) > float(fullBDT.bdtscore) > float(cut):
							totalcut[plotindex] += 1
							if float(candidatesignal) > float(signalcut):	
								passcut = True	
								combinedtotal[plotindex] += 1
								combinedwrong[plotindex].append(fullBDT.bdtscore)
					
					if passcut:
						passed[plotindex][result].append(difference)
						passeddiff[plotindex].append(absd)
						passedcsignals[plotindex][result].append(candidatesignal)
						passedDCsignals[plotindex][result].append(DCcount)
					else:
						rejected[plotindex][result].append(difference)
						rejecteddiff[plotindex].append(absd)
						rejectedcsignals[plotindex][result].append(candidatesignal)
						rejectedDCsignals[plotindex][result].append(DCcount)			

	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1
	
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

for i in [0, 1]:
	if hessstatus[i]:
			
		colors =['r', 'g']

		ax2 = plt.subplot(2,2,2)
		plt.hist([rejected[i][0], rejected[i][1]], color=colors, stacked=True, bins=50)
		plt.title("DC pixel error for rejected events")
		plt.xlabel("Difference from true count")
		
		ax1 = plt.subplot(221, sharex=ax2)
		plt.hist(passed[i], color=colors, stacked=True, bins=50)
		plt.title("DC pixel error for events passing cuts")
		plt.xlabel("Difference from true count")

		linear = np.linspace(1, 3000, 1000)
		plotcut = []
		for entry in linear:
			plotcut.append(signalcut/entry)
		
		
		ax4 = plt.subplot(2,2,4)
		for j in range(2):
			plt.scatter( rejectedDCsignals[i][j],rejectedcsignals[i][j], color=colors[j], marker="o")
		plt.plot([0,2500], [0, 2500], color="k")
		plt.title("True vs. reconstructed signal for rejected events")
		plt.ylabel("Total pixel intensity")
		
		ax3 = plt.subplot(223, sharex = ax4, sharey=ax4)
		for j in range(2):
			plt.scatter( passedDCsignals[i][j],passedcsignals[i][j], color=colors[j], marker="o")
		plt.plot([0,2500], [0, 2500], color="k")
		plt.xlabel("True signal")
		plt.title("True vs. reconstructed signal for accepted events")
		plt.ylabel("Total pixel intensity")
		
		k=1
		
		for category in ["passed", "rejected"]:
		
			allevents = eval(category +"[i][0]")
			allevents.extend(eval(category +"[i][1]"))
			allevents.sort()

			alldiff= eval(category + "diff[i]")
			
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
			
			eval("ax" + str(k) + ".annotate(toprint, xy=(0.02, 0.75), xycoords='axes fraction',  fontsize=10)")
			
			print k, toprint
			
			k+=1
		
		figure = plt.gcf() # get current figure
		figure.set_size_inches(20, 20)
		
		saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/signalchecks" + str(i+1)+".pdf"
		
		print "Saving to", saveto
		
		plt.savefig(saveto)
		plt.close()
	
