import sys

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'

sys.path.append(afspath)

import argparse, math, random, time
import csv
import numpy as np

nparrallel = 10

targetfolder = "reconstructeddata/"

reconstructdata= "archive/9gridarchive"

import plotz as pz
import plotposition as pp
import plotepn as pe
import plotangle as pa
import plotheight as ph
import plotlikelihood as pl
import optimisez as oz
import categorycounts as cc

import initialise as i
orientation="ideal"
mincount=5

sys.path.append('/d6/rstein/Hamburg-Cosmic-Rays/BDT')
import BDT

with open(afspath + "/orientations/"+ orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1

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
