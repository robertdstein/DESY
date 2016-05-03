import sys
import os.path
import os
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle

hess1picklepath = '/nfs/astrop/d6/rstein/BDTpickle/hess1pixelclassifier.p'
hess2picklepath = '/nfs/astrop/d6/rstein/BDTpickle/hess2pixelclassifier.p'
for picklepath in [hess1picklepath, hess2picklepath]:
	if os.path.isfile(picklepath):
		remove_old_BDT = "rm " + picklepath 
		os.system(remove_old_BDT)

from telescopeclasses import *

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

hess1set = []
hess2set = []

hess1scores = []
hess2scores = []

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
			bdtentry.append(newval)
		else:
			print("No variable named " +variable)
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
				hess1set.append(bdtentry)
				hess1scores.append(truescore)
		for hess2pixel in hess2pixels:
			bdtentry, truescore = makeBDTentry(hess2pixel)
			if (bdtentry != None) and (truescore != None):
				hess2set.append(bdtentry)
				hess2scores.append(truescore)
	
	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

pickle_dump_dir = os.path.join(targetfolder, "bdtpickle")
if not os.path.exists(pickle_dump_dir):
	print "Making directory " + pickle_dump_dir
	os.mkdir(pickle_dump_dir)
pickle.dump(hess1set,  open(pickle_dump_dir+"/hess1bdtdata.p", "wb"))
pickle.dump(hess2set,  open(pickle_dump_dir+"/hess2bdtdata.p", "wb"))
pickle.dump(hess1scores,  open(pickle_dump_dir+"/hess1bdtscores.p", "wb"))
pickle.dump(hess2scores,  open(pickle_dump_dir+"/hess2bdtscores.p", "wb"))
