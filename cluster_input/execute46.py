n = 46

import initialise as i
numberofhours, mincount, reconstructiongridwidth, orientation, eff, flux, area, solidangle, selectionefficiency = i.run()

import sys

sys.path.append('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/')

import argparse, math, random, time
import csv
import numpy as np
import simulate as s
import batchprocessing as bp
import batchreconstruction as br

sourcedata="executedefault" + str(n)
processdata="executeprocess" + str(n)
reconstructdata="executereconstructed" + str(n)


detectedflux = float(flux)*float(area)*float(solidangle)*float(selectionefficiency)
rateperhour = detectedflux * 60 * 60
n = int(rateperhour*float(numberofhours))
print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 

with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/orientations/"+ orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1

s.run(eff, rowcount, mincount=mincount, text=False, graph=False, output=sourcedata, layout=orientation, number = n)
bp.run(sourcedata, processdata, int(mincount), rowcount, text=False)
br.run(processdata, reconstructdata, rowcount, reconstructiongridwidth, eff)

message = str(time.asctime(time.localtime())) + " Completed simulation of " + str(n) + " events!"
import os, sys
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message, False)
