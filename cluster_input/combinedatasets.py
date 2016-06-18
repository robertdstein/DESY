#!/bin/env python

import sys
import os.path

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'

sys.path.append(afspath)

import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from classes import *

nparrallel = 5000

pickle_dir = "/nfs/astrop/d6/rstein/chargereconstructionpickle/"

targetfolder = pickle_dir + "fullsims/"
dump_dir = pickle_dir + "/combined/"

stats=[]
bdt = []
		
for i in range (1, int(nparrallel)+1):
	path = targetfolder + "sim" + str(i) +".p"
	
	if os.path.isfile(path):
	
		print "Adding", path
		
		simset = pickle.load(open(path, 'rb'))
		
		if random.random() > 0.5:
			stats.append(simset)
		else:
			bdt.append(simset)

bdtpath = dump_dir + "trainingset.p"
statspath = dump_dir + "stats.p"

pickle.dump(bdt, open(bdtpath,"wb"))
pickle.dump(stats, open(statspath,"wb"))
