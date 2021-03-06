#!/bin/env python

import argparse, math, random, time
import csv
import numpy as np
import simulate as s
import batchprocessing as bp
import batchreconstruction as br

sourcedata="testing"
processdata="testing"
reconstructdata="testing"

numberofhours = 10
mincount=4
reconstructiongridwidth=3
orientation="five"
eff = 0.06
flux = 2.5 * (10**-4)
area = 300**2
solidangle = math.radians(5)

detectedflux = float(flux)*float(area)*float(solidangle)
rateperhour = detectedflux * 60 * 60
n = int(rateperhour*float(numberofhours))
print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 

with open("/d6/rstein/Hamburg-Cosmic-Rayspositioning/orientations/"+ orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1

s.run(eff, rowcount, mincount=mincount, text=False, graph=False, output=sourcedata, layout=orientation, number = n)
bp.run(sourcedata, processdata, int(mincount), rowcount, text=False)
br.run(processdata, reconstructdata, rowcount, reconstructiongridwidth, eff)
