import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import sys
import argparse, math, random, time
import csv
import numpy as np

afspath = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/'
sys.path.append(afspath)

import plotz as pz
import plotposition as pp
import plotepn as pe
import plotangle as pa
import plotheight as ph
import plotlikelihood as pl
import plotlpd as plpd
import optimisez as oz
import categorycounts as cc

import initialise as i
numberofhours, mincount, gridwidth, layout, raweff, flux, area, solidangle, selectionefficiency, hmacceptance = i.run()
sys.path.append('/d6/rstein/Hamburg-Cosmic-Rays/BDT')
import BDT

pickle_dir = "/nfs/astrop/d6/rstein/chargereconstructionpickle/combined/"		
statsdata = pickle_dir + "stats.p"
traindata = pickle_dir + "trainingset.p"

plpd.run(statsdata)

BDT.run(traindata, statsdata, int(mincount))
llcuts = oz.run(statsdata, int(mincount))
print "Log Likelihood Cuts", llcuts

pz.run(statsdata, int(mincount), cuts=None)
pz.run(statsdata, int(mincount), cuts=llcuts)
pl.run(statsdata, int(mincount), cuts=llcuts)
pp.run(statsdata, int(mincount), cuts=llcuts)
pe.run(reconstructdata+ "_BDT", int(mincount), cuts=llcuts)
ph.run(reconstructdata+ "_BDT", int(mincount), cuts=llcuts)
