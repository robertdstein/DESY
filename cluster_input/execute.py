#!/bin/env python

import initialise as i
numberofhours, mincount, gridwidth, layout, raweff, flux, area, solidangle, selectionefficiency, hmacceptance = i.run()

import sys

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/')

import argparse, math, random, time
import csv
import numpy as np
import simulate as s
import batchprocessing as bp
import batchreconstruction as br
from classes import *

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", default=1)

cfg = parser.parse_args()

sourcedata="executedefault" + str(cfg.number)
processdata="executeprocess" + str(cfg.number)
reconstructdata="executereconstructed" + str(cfg.number)


detectedflux = float(flux)*float(area)*float(solidangle)*float(selectionefficiency)
rateperhour = detectedflux * 60 * 60
n = int(rateperhour*float(numberofhours))
print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 

simset = simulationset(raweff, layout, mincount, hmacceptance, gridwidth)
simset.generate(n)
simset.reconstructevents()
simset.dump(cfg.number)

#~ message = str(time.asctime(time.localtime())) + " Completed simulation of " + str(n) + " events!"
#~ import os, sys
#~ import sendemail as se
#~ name = os.path.basename(__file__)
#~ se.send(name, message, False)
