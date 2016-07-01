import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="testdata")

cfg = parser.parse_args()

minmultiplicity=3


filepath = "/nfs/astrop/d6/rstein/data/"
i = 1
j = 15000
	
energy=[]

cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()
arcut = ic.runar()

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

while (i < j):
	targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
	if (os.path.isfile(targetpath)):
		event = pickle.load(open(targetpath, 'rb'))
		if hasattr(event.simulations, "DC") and hasattr(event.simulations, "full"):
			DCsim =event.simulations.DC
			fullsim = event.simulations.full
			
			kar=0
			
			for fulltel in fullsim.images:
				if fulltel.BDTID != None:
					fullBDT = fulltel.getBDTpixel()
					candidatesignal = fullBDT.channel1.intensity - fullBDT.nnmean
					if float(ucut) > float(fullBDT.bdtscore) > float(cut):
							if float(candidatesignal) > float(signalcut):
								if float(fulltel.hillas.aspect_ratio_) > arcut:
									kar +=1
									
			if kar > minmultiplicity:
				tel = fullsim.gettriggeredtelescope(0)
				energy.append(tel.hillas.energy)
				
	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1
	
print energy

print cfg.jobID.split("full")[1]

plt.hist(energy, histtype='bar')
figure = plt.gcf() # get current figure
figure.set_size_inches(20, 10)
plt.xlabel("True Energy (TeV)", fontsize=20)
plt.ylabel("Count", fontsize=20)
plt.title("Energy Distribution of Accepted " + cfg.jobID.split("full")[1], fontsize=25)
plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/energy"+str(cfg.jobID)+".pdf")
plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/energy"+str(cfg.jobID)+".pdf")
plt.close()
					
