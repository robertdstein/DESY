import sys

afspath = '/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/'

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

sys.path.append('/home/steinrob/Documents/DESY/BDT')
import BDT

with open(afspath + "/orientations/"+ orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1
		
reconstructdata = batchname + "_combined"

allcounts = cc.run(reconstructdata, rowcount, int(mincount))
print allcounts


BDT.run(reconstructdata, rowcount, int(mincount), allcounts)

llcuts = oz.run(reconstructdata + "_BDT", rowcount, int(mincount), graph=False, allcounts=allcounts)
print llcuts
pz.run(reconstructdata + "_BDT", rowcount, int(mincount), graph=False, cuts=None, allcounts=allcounts)	

pl.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts, allcounts=allcounts)
pz.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts, allcounts=allcounts)
pp.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts, allcounts=allcounts)
pe.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts, allcounts=allcounts)
ph.run(reconstructdata+ "_BDT", rowcount, int(mincount), graph=False, cuts=llcuts, allcounts=allcounts)
