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
import plotcoredistance as pd
import plotlpd as plpd
import optimisez as oz
import categorycounts as cc

import initialise as i
numberofhours, mincount, gridwidth, layout, raweff, flux, area, solidangle, selectionefficiency, hmacceptance = i.run()
sys.path.append('/d6/rstein/Hamburg-Cosmic-Rays/BDT')
import BDT

detectedflux = float(flux)*float(area)*float(solidangle)*float(selectionefficiency)
rateperhour = detectedflux * 60 * 60
n = int(rateperhour*float(numberofhours))
totalhours = numberofhours*5000
totaln = n*5000
print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 
print time.asctime(time.localtime()),"Simulated 500 events, equal to", totalhours, "Simulated Hours. Simulated Events", totaln 



pickle_dir = "/nfs/astrop/d6/rstein/chargereconstructionpickle/combined/"		
statsdata = pickle_dir + "stats.p"
traindata = pickle_dir + "trainingset.p"

plpd.run(statsdata)

BDT.run(traindata, statsdata, int(mincount))
llcuts = oz.run(statsdata, int(mincount))
print "Log Likelihood Cuts", llcuts
llcuts = [0.0, 0.0]

pz.run(statsdata, int(mincount), cuts=None)
pe.run(statsdata, int(mincount), cuts=None)
pd.run(statsdata, int(mincount), cuts=None)
pd.run(statsdata, int(mincount), cuts=llcuts)
pz.run(statsdata, int(mincount), cuts=llcuts)
pl.run(statsdata, int(mincount), cuts=llcuts)
pp.run(statsdata, int(mincount), cuts=llcuts)
pd.run(statsdata, int(mincount), cuts=llcuts)
pe.run(statsdata, int(mincount), cuts=llcuts)
ph.run(statsdata, int(mincount), cuts=llcuts)
