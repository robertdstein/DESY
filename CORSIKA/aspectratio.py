import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="bigtestdata")

cfg = parser.parse_args()

minmultiplicity=3

files = [cfg.jobID, "protons"]
hess1ars = [[],[]]
hess2ars =[[],[]]

for f in range(len(files)):
	filepath = "/nfs/astrop/d6/rstein/data/"
	i = 1
	j = 15000
	
	folder = files[f]
	
	print "COMPLETING JOB", folder
	
	cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

	targetfolder = filepath + folder +"/"
	
	sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
	from progressbar import ProgressBar
	custom_options = {
		'end': 100,
		'width': 100,
		'format': '%(progress)s%% [%(fill)s%(blank)s]'
	}
	
	p = ProgressBar(**custom_options)
	print p
	
	while (i < j):
		targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
		if (os.path.isfile(targetpath)):
			event = pickle.load(open(targetpath, 'rb'))
			if hasattr(event.simulations, "DC") and hasattr(event.simulations, "full"):
				DCsim =event.simulations.DC
				fullsim = event.simulations.full
				
				k=0
				
				for index in DCsim.triggerIDs:
					fulltel =  fullsim.images[index]
					
					if fulltel.BDTID != None:
						fullBDT = fulltel.getBDTpixel()
						candidatesignal = fullBDT.channel1.intensity - fullBDT.nnmean
						if float(ucut) > float(fullBDT.bdtscore) > float(cut):
								if float(candidatesignal) > float(signalcut):
									k+=1
									
				if k > minmultiplicity:
					for index in DCsim.triggerIDs:
						fulltel =  fullsim.images[index]
						
						if hasattr(fulltel.hillas, "aspect_ratio_"):	
							ar = fulltel.hillas.aspect_ratio_
							if fulltel.BDTID != None:
								fullBDT = fulltel.getBDTpixel()
								candidatesignal = fullBDT.channel1.intensity - fullBDT.nnmean
								if (float(ucut) > float(fullBDT.bdtscore) > float(cut)) and (float(candidatesignal) > float(signalcut)):
									if fulltel.size == "HESS1":
										hess1ars[f].append(ar)					
									elif fulltel.size == "HESS2":
										hess2ars[f].append(ar)
									else:
										raise Exception("Telescope.size error, size is " +fulltel.size)
										
	
		if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
			print p+1
		i+=1
		
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
		
ax1 = plt.subplot(2,1,1)
plt.title("HESS1 Image Aspect Ratio", y=1.15)
plt.hist(hess1ars, color=['g', "white"], label=["Iron passing all cuts", "Proton passing all cuts"], stacked=True, bins=25)
plt.xlabel("Aspect Ratio")

ax2 = plt.subplot(212, sharex=ax1)
plt.title("HESS2 Image Aspect Ratio", y=1.15)
plt.hist(hess2ars, color=['g', "white"], label=["Iron passing all cuts", "Proton passing all cuts"], stacked=True, bins=25)
plt.xlabel("Aspect Ratio")

figure = plt.gcf() # get current figure
handles, labels = ax1.get_legend_handles_labels()
figure.legend(handles, labels, loc="upper right")

plt.subplots_adjust(hspace = 0.5)

figure.set_size_inches(10, 15)
plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/aspectratio.pdf")
saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/aspectratio.pdf"
print "Saving To", saveto
plt.savefig(saveto)
plt.close() 
				
