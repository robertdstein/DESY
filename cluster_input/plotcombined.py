import sys

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'

sys.path.append(afspath)

import argparse, math, random, time
import csv
import numpy as np

nparrallel = 10

targetfolder = "reconstructeddata/"

batchname= "executereconstructed"

import plotz as pz
import plotposition as pp
import plotepn as pe
import plotangle as pa
import plotheight as ph
import plotlikelihood as pl
import optimisez as oz
import categorycounts as cc

import initialise as i
numberofhours, mincount, reconstructiongridwidth, orientation, eff, flux, area, solidangle, selectionefficiency = i.run()

sys.path.append('/d6/rstein/Hamburg-Cosmic-Rays/BDT')
import BDT

with open(afspath + "/orientations/"+ orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1
		
reconstructdata = batchname + "_combined"
traindata = batchname + "_trainingset"

#~ allcounts = cc.run(reconstructdata, rowcount, int(mincount))
#~ print "All Counts", allcounts

#~ BDT.run(traindata, reconstructdata, rowcount, int(mincount))
#~ 
#~ llcuts = oz.run(reconstructdata + "_BDT", rowcount, int(mincount), graph=False)
#~ print "Log Likelihood Cuts", llcuts
#~ pz.run(reconstructdata + "_BDT", rowcount, int(mincount), graph=False, cuts=None)	
llcuts=[0,0]
pl.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts)
pz.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts)
pp.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts)
pe.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts)
ph.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts)
