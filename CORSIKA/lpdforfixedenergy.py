import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="4894324")

cfg = parser.parse_args()


filepath = "/nfs/astrop/d6/rstein/data/"

j=500
i=0

distances=[[],[]]
signals=[[],[]]
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
				DCtrue = DCtel.getpixel(trueID)
				DCcount = DCtrue.channel1.intensity
				
				if fulltel.BDTID != None:
					fullBDT = fulltel.getBDTpixel()
					
					if (fullBDT.bdtscore != None):				
						candidatesignal = fullBDT.channel1.intensity - fullBDT.nnmean
							
						difference = (candidatesignal - DCcount)
						

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
						truesignals[plotindex].append(DCcount)
						signals[plotindex].append(candidatesignal)


	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1
	
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

for i in [0, 1]:
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 20)
	
	ax1=plt.subplot(2,1,1)
	
	plt.scatter(distances[0], signals[0])
	plt.xlabel("Core distance to telescope (m)")
	plt.ylabel("Photoelectrons")
	ax1.set_xlim(left=0)
	ax1.set_ylim(bottom=1)
	ax1.set_yscale("log")
	plt.title("Reconstruction LPD")
	
	ax2=plt.subplot(2,1,2)
	
	plt.scatter(distances[0], truesignals[0])
	plt.xlabel("Core distance to telescope (m)")
	plt.ylabel("Photoelectrons")
	ax2.set_xlim(left=0)
	ax2.set_ylim(bottom=1)
	ax2.set_yscale("log")
	plt.title("True LPD")
	
	
	saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/lpd" + str(i+1)+".pdf"
	
	print "Saving to", saveto
	
	plt.savefig(saveto)
	plt.close()
	
