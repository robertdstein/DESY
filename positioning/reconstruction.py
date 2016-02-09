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
import plotstatistics as ps

parser = argparse.ArgumentParser(description='Create a canvas for positions of telescopes')
parser.add_argument("-o", "--orientation", default="five")
parser.add_argument("-sd", "--sourcedata", default="default")
parser.add_argument("-pd", "--processdata", default="process")
parser.add_argument("-rd", "--reconstructdata", default="reconstructed")
parser.add_argument("-mc", "--mincount", default=4)
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-s", "--simulate", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-e", "--email", action="store_true")
parser.add_argument("-pz", "--plotz", action="store_true")
parser.add_argument("-pp", "--plotposition", action="store_true")
parser.add_argument("-pe", "--plotepn", action="store_true")
parser.add_argument("-ph", "--plotheight", action="store_true")
parser.add_argument("-pa", "--plotangle", action="store_true")
parser.add_argument("-ps", "--plotstatistics", action="store_true")
parser.add_argument("-nh", "--numberofhours", default=1)
parser.add_argument("-rgw", "--reconstructiongridwidth", default=25)
cfg = parser.parse_args()

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
		
if cfg.simulate:
	s.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, output=cfg.sourcedata, layout=cfg.orientation, number = n)
	bp.run(cfg.sourcedata, cfg.processdata, int(cfg.mincount), rowcount, text=cfg.text)
	br.run(cfg.processdata, cfg.reconstructdata, rowcount, cfg.reconstructiongridwidth, eff)
	
if cfg.plotz:
	pz.run(cfg.reconstructdata, rowcount, int(cfg.mincount), cfg.graph)
	
if cfg.plotposition:
	pp.run(cfg.reconstructdata, rowcount, int(cfg.mincount), cfg.graph)
	
if cfg.plotepn:
	pe.run(cfg.reconstructdata, rowcount, int(cfg.mincount), cfg.graph)
	
if cfg.plotangle:
	pa.run(cfg.reconstructdata, rowcount, int(cfg.mincount), cfg.graph)
	
if cfg.plotheight:
	ph.run(cfg.reconstructdata, rowcount, int(cfg.mincount), cfg.graph)
	
if cfg.plotstatistics:
	ps.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, output=cfg.sourcedata, layout=cfg.orientation, number = n)

if cfg.email:
	message = str(time.asctime(time.localtime())) + " Completed simulation of " + str(n) + " events!"
	print message
	import os, sys
	import sendemail as se
	name = os.path.basename(__file__)
	se.send(name, message)
