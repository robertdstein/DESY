import argparse, math, random, time
import csv
import numpy as np
import simulate as s
import batchprocessing as bp
import batchreconstruction as br
import plotz as pz
import plotposition as pp
import plotepn as pe
import plotangle as pa
import plotheight as ph
import epnstatistics as es
import radiusstatistics as rs
import heightstatistics as hs
import lightstatistics as ls

eff = 0.06
flux = 2.5 * (10**-4)
area = 300**2
solidangle = math.radians(5)
detectedflux = flux*area*solidangle
rateperhour = detectedflux * 60 * 60
n = int(rateperhour*float(cfg.numberofhours))
print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", cfg.numberofhours, "Simulated Events", n 

with open("orientations/"+ cfg.orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1

s.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, output=cfg.sourcedata, layout=cfg.orientation, number = n)
bp.run(cfg.sourcedata, cfg.processdata, int(cfg.mincount), rowcount, text=cfg.text)
br.run(cfg.processdata, cfg.reconstructdata, rowcount, cfg.reconstructiongridwidth, eff)

message = str(time.asctime(time.localtime())) + " Completed simulation of " + str(n) + " events!"
print message
import os, sys
import sendemail as se
name = os.path.basename(__file__)
se.send(name, message)
