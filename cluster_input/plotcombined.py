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

import initialise as i
numberofhours, mincount, reconstructiongridwidth, orientation, eff, flux, area, solidangle, selectionefficiency = i.run()

with open(afspath + "/orientations/"+ orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1
		
reconstructdata = batchname + "_combined"

llcuts = oz.run(reconstructdata, rowcount, int(mincount), graph=False)
pl.run(reconstructdata, graph=False, llcuts=llcuts)
pz.run(reconstructdata, rowcount, int(mincount), graph=False, llcuts=llcuts)
pp.run(reconstructdata, rowcount, int(mincount), graph=False, llcuts=llcuts)
pe.run(reconstructdata, rowcount, int(mincount), graph=False, llcuts=llcuts)
ph.run(reconstructdata, rowcount, int(mincount), graph=False, llcuts=llcuts)
