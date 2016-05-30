import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="56tev-lpd")

cfg = parser.parse_args()

hess1rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess1signalregressor.p'
hess2rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess2signalregressor.p'
if os.path.isfile(hess1rgrpath):
	hess1rgr = pickle.load(open(hess1rgrpath, "r"))
else:
	print "No hess1 pickle!"
if os.path.isfile(hess2rgrpath):
	hess2rgr = pickle.load(open(hess1rgrpath, "r"))
else:
	print "No hess2 pickle!"
	
signalbdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/signalBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		signalbdtvariables.append(row[0])
print signalbdtvariables

minmultiplicity=3

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



j=2000
i=0

distances=[[],[]]
signals=[[],[]]
rgrsignals=[[],[]]
rgrdiffs=[[],[]]
simplediffs=[[],[]]
truesignals=[[],[]]

cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

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

				if fulltel.BDTID != None:
					fullBDT = fulltel.getBDTpixel()
								
					simplecandidatesignal = fullBDT.channel1.intensity -fullBDT.nnmean

					bdtentry = makeBDTentry(fullBDT)
					if (fulltel.size=="HESS1") and (bdtentry != None):
						candidatesignal = hess1rgr.predict([bdtentry])[0]
					elif (fulltel.size=="HESS2") and (bdtentry != None):
						candidatesignal = hess2rgr.predict([bdtentry])[0]
					elif bdtentry == None:
						candidatesignal = 0
						
					if float(ucut) > float(fullBDT.bdtscore) > float(cut):
						if float(simplecandidatesignal) > float(signalcut):

							if fulltel.BDTID == trueID:
								result = 1
							elif fulltel.BDTID == None:
								print "None!!!"
							else:
								result = 0
								
							if fulltel.size == "HESS1":
								plotindex = 0
							elif fulltel.size == "HESS2":
								plotindex = 1
							else:
								raise Exception("Telescope.size error, size is " +fulltel.size)
							
							distances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							truesignals[plotindex].append(DCtel.hillas.image_size_amplitude_)
							signals[plotindex].append(simplecandidatesignal)
							rgrsignals[plotindex].append(candidatesignal)


	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

for i in [0, 1]:
	print "HESS"+str(i+1)
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 20)
	
	ax1=plt.subplot(3,1,1)
	
	plt.scatter(distances[i], truesignals[i])
	plt.xlabel("Core distance to telescope (m)")
	plt.ylabel("Photoelectrons")
	ax1.set_xlim(left=0)
	ax1.set_ylim(bottom=10)
	#~ ax1.set_yscale("log")
	plt.title("True LPD")
	
	d=[]
	s=[]
	
	for k in range(len(distances[i])):
		value = distances[i][k]
		if value < 90:
			lpdval = truesignals[i][k]
			d.append(value)
			s.append(math.log(lpdval))
	
	A, logC = np.polyfit(d, s, 1)
	C = math.exp(logC)
	print A, logC, C
	
	diffs = []
	
	for l in range(len(s)):
		sig = math.exp(s[l])
		dist = d[l]
		fitsig = C*math.exp(A*dist)
		diff = math.fabs((sig-fitsig)/fitsig)
		diffs.append(diff)

	diffs.sort()
	nentries = len(diffs)
	halfinteger = int(0.5*nentries)
	lowerinteger = int(0.16*nentries)
	upperinteger = int(0.84*nentries)
	integer68 = int(0.68*nentries)
	
	lower = diffs[lowerinteger]
	upper = diffs[upperinteger]
	
	sigma = 0.5*(upper-lower)
	sigma = diffs[integer68]
	print "Actual", lower, diffs[halfinteger], sigma, upper, sigma
	
	d.sort()
	
	lpd=[]
	u=[]
	l=[]
	for dist in d:
		sig = C*math.exp(A*dist)
		lpd.append(sig)
		ulpd = sig*(1+sigma)
		u.append(ulpd)
		llpd = sig*(1-sigma)
		l.append(llpd)
		
	plt.plot(d, lpd, color='k')
	plt.fill_between(d, l, u, color='g', alpha=0.25)
	
	for j in range(0,2):
		
		sigset = [signals, rgrsignals][j]
		diffname = ["Simple", "Regressor"][j]
		
		diffs=[]
		
		for l in range(len(sigset[i])):
			sig = sigset[i][l]
			dist = distances[i][l]
			fitsig = C*math.exp(A*dist)
			diff = math.fabs((sig-fitsig)/fitsig)
			diffs.append(diff)
		
		diffs.sort()
		nentries = len(diffs)
		halfinteger = int(0.5*nentries)
		lowerinteger = int(0.16*nentries)
		upperinteger = int(0.84*nentries)
		integer68 = int(0.68*nentries)
		
		lower = diffs[lowerinteger]
		upper = diffs[upperinteger]
		
		sigma = 0.5*(upper-lower)
		sigma = diffs[integer68]
		print diffname, lower, diffs[halfinteger], sigma, upper, sigma
		
		ax=plt.subplot(3,1,j+2, sharex=ax1, sharey=ax1)
		
		plt.scatter(distances[i], sigset[i])
		
		u=[]
		l=[]
		for sig in lpd:
			ulpd = sig*(1+sigma)
			u.append(ulpd)
			llpd = sig*(1-sigma)
			l.append(llpd)

		plt.plot(d, lpd, color='k')
		plt.fill_between(d, l, u, color='g', alpha=0.25)
		
		plt.xlabel("Core distance to telescope (m)")
		plt.ylabel("Photoelectrons")
		ax.set_xlim(left=0)
		ax.set_ylim(bottom=10)
		plt.title(diffname+ " Estimate LPD")

	saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/lpd" + str(i+1)+ ".pdf"
	
	print "Saving to", saveto
	
	plt.savefig(saveto)
	plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/corsikalpd" + str(i+1)+ ".pdf")
	plt.close()
	
