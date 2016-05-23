import sys
import os.path
import os
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle

from telescopeclasses import *

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False
	except TypeError:
		return False

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="2842781")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1
j = 2000

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

hess1testset = []
hess1trainset = []
hess2testset = []
hess2trainset = []

hess1testscores = []
hess1trainscores = []
hess2testscores = []
hess2trainscores = []

hess1candidatepixels = []
hess2candidatepixels = []
hess1DCsignals = []
hess2DCsignals = []

targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"

def makeBDTentry(pixelentry):
	bdtentry =[]
	for variable in bdtvariables:
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
			if isfloat(newval):
				if float(newval) != float("inf"):
					bdtentry.append(newval)
				else:
					return None, None
			else:
					return None, None
		else:
			return None, None
	return bdtentry, pixelentry.truescore

while (i < j):
	targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
	if (os.path.isfile(targetpath)):
		event = pickle.load(open(targetpath, 'rb'))
		hess1pixels, hess2pixels = event.returnforBDT()
		for hess1pixel in hess1pixels:
			bdtentry, truescore = makeBDTentry(hess1pixel)
			if (bdtentry != None) and (truescore != None):
				if random.random() < 0.9:
					hess1trainset.append(bdtentry)
					hess1trainscores.append(truescore)
				else:
					hess1testset.append(bdtentry)
					hess1testscores.append(truescore)
		for hess2pixel in hess2pixels:
			bdtentry, truescore = makeBDTentry(hess2pixel)
			if (bdtentry != None) and (truescore != None):
				if random.random() < 0.9:
					hess2trainset.append(bdtentry)
					hess2trainscores.append(truescore)
				else:
					hess2testset.append(bdtentry)
					hess2testscores.append(truescore)
		for index in event.simulations.DC.triggerIDs:
			DCtel =  event.simulations.DC.images[index]
			fulltel = event.simulations.full.images[index]
			if fulltel.trueDC != None:
				DCpixel = DCtel.getpixel(DCtel.trueDC)
				fullpixel = fulltel.gettruepixel()
				if fulltel.size == "HESS1":
					hess1candidatepixels.append(fullpixel)
					hess1DCsignals.append(DCpixel.channel1.intensity)
				elif fulltel.size == "HESS2":
					hess2candidatepixels.append(fullpixel)
					hess2DCsignals.append(DCpixel.channel1.intensity)
				else:
					raise Exception("Name error with size " + fulltel.size)
					
					
	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

pickle_dump_dir = os.path.join(targetfolder, "bdtpickle")
if not os.path.exists(pickle_dump_dir):
	print "Making directory " + pickle_dump_dir
	os.mkdir(pickle_dump_dir)
pickle.dump(hess1trainset,  open(pickle_dump_dir+"/hess1trainbdtdata.p", "wb"))
pickle.dump(hess1testset,  open(pickle_dump_dir+"/hess1testbdtdata.p", "wb"))
pickle.dump(hess2trainset,  open(pickle_dump_dir+"/hess2trainbdtdata.p", "wb"))
pickle.dump(hess2testset,  open(pickle_dump_dir+"/hess2testbdtdata.p", "wb"))
pickle.dump(hess1trainscores,  open(pickle_dump_dir+"/hess1trainbdtscores.p", "wb"))
pickle.dump(hess1testscores,  open(pickle_dump_dir+"/hess1testbdtscores.p", "wb"))
pickle.dump(hess2trainscores,  open(pickle_dump_dir+"/hess2trainbdtscores.p", "wb"))
pickle.dump(hess2testscores,  open(pickle_dump_dir+"/hess2testbdtscores.p", "wb"))
pickle.dump(hess1candidatepixels,  open(pickle_dump_dir+"/hess1candidatepixels.p", "wb"))
pickle.dump(hess2candidatepixels,  open(pickle_dump_dir+"/hess2candidatepixels.p", "wb"))
pickle.dump(hess1DCsignals,  open(pickle_dump_dir+"/hess1DCsignals.p", "wb"))
pickle.dump(hess2DCsignals,  open(pickle_dump_dir+"/hess2DCsignals.p", "wb"))
