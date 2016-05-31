import sys
import os.path
import os
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle

from telescopeclasses import *

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="regressorset")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1
j = 5000

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

hess1candidatepixels = []
hess2candidatepixels = []
hess1DCsignals = []
hess2DCsignals = []

targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"

while (i < j):
	targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
	if (os.path.isfile(targetpath)):
		event = pickle.load(open(targetpath, 'rb'))
		for index in event.simulations.DC.triggerIDs:
			DCtel =  event.simulations.DC.images[index]
			fulltel = event.simulations.full.images[index]
			if fulltel.trueDC != None:
				DCpixel = DCtel.getpixel(DCtel.trueDC)
				fullpixel = fulltel.gettruepixel()
				if fulltel.size == "HESS1":
					hess1candidatepixels.append(fullpixel)
					hess1DCsignals.append(DCtel.hillas.image_size_amplitude_)
				elif fulltel.size == "HESS2":
					hess2candidatepixels.append(fullpixel)
					hess2DCsignals.append(DCtel.hillas.image_size_amplitude_)
				else:
					raise Exception("Name error with size " + fulltel.size)
					
					
	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

pickle_dump_dir = os.path.join(targetfolder, "bdtpickle")
if not os.path.exists(pickle_dump_dir):
	print "Making directory " + pickle_dump_dir
	os.mkdir(pickle_dump_dir)
pickle.dump(hess1candidatepixels,  open(pickle_dump_dir+"/hess1candidatepixels.p", "wb"))
pickle.dump(hess2candidatepixels,  open(pickle_dump_dir+"/hess2candidatepixels.p", "wb"))
pickle.dump(hess1DCsignals,  open(pickle_dump_dir+"/hess1DCsignals.p", "wb"))
pickle.dump(hess2DCsignals,  open(pickle_dump_dir+"/hess2DCsignals.p", "wb"))
