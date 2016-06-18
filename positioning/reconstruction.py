import argparse, math, random, time, sys
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
import plotlikelihood as pl
import optimisez as oz
import optimiselayout as ol
import categorycounts as cc

parser = argparse.ArgumentParser(description='Create a canvas for positions of telescopes')
parser.add_argument("-o", "--orientation", default="five")
parser.add_argument("-d", "--data", default="default")
parser.add_argument("-mc", "--mincount", default=4)
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-s", "--simulate", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-e", "--email", action="store_true")
parser.add_argument("-p", "--plot", action="store_true")
parser.add_argument("-pc", "--plotcut", action="store_true")
parser.add_argument("-es", "--epnstatistics", action="store_true")
parser.add_argument("-rs", "--radiusstatistics", action="store_true")
parser.add_argument("-hs", "--heightstatistics", action="store_true")
parser.add_argument("-ls", "--lightstatistics", action="store_true")
parser.add_argument("-ol", "--optimiselayout", action="store_true")
parser.add_argument("-nh", "--numberofhours", default=1)
parser.add_argument("-rgw", "--reconstructiongridwidth", default=75)

cfg = parser.parse_args()

eff = 1.0
selectionefficiency = 1.0
flux = 2.0 * (10**-4)
area = 300**2
solidangle = math.radians(5)
detectedflux = flux*area*solidangle*selectionefficiency
rateperhour = detectedflux * 60 * 60
n = int(rateperhour*float(cfg.numberofhours))

defaultcuts = [500, 500]

if cfg.data == "default":
	sourcedata="executesimulated_combined"
	processdata = "executeprocessed_combined"
	reconstructdata = "executereconstructed_combined"
	
else:
	sourcedata= str(cfg.data) + "simulated" + str(cfg.mincount)
	processdata = str(cfg.data) + "processed"+ str(cfg.mincount)
	reconstructdata = str(cfg.data) + "reconstructed"+ str(cfg.mincount)

with open("orientations/"+ cfg.orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1
		
if cfg.simulate:
	print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
	print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", cfg.numberofhours, "Simulated Events", n 
	s.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, output=sourcedata, layout=cfg.orientation, number = n)
	bp.run(sourcedata, processdata, int(cfg.mincount), rowcount, text=cfg.text)
	br.run(processdata, reconstructdata, rowcount, cfg.reconstructiongridwidth, eff)
	message = str(time.asctime(time.localtime())) + " Completed simulation of " + str(n) + " events!"
	print message
	import os, sys
	import sendemail as se
	name = os.path.basename(__file__)
	se.send(name, message)
	
if cfg.plotcut:
	allcounts = cc.run(reconstructdata, rowcount, int(cfg.mincount))
	
	sys.path.append('/d6/rstein/Hamburg-Cosmic-Rays/BDT')
	import BDT
	BDT.run(reconstructdata, rowcount, int(cfg.mincount), allcounts)
	
	llcuts = oz.run(reconstructdata + "_BDT", rowcount, int(cfg.mincount), cfg.graph, allcounts)
	print llcuts
	pl.run(reconstructdata+ "_BDT", rowcount, int(cfg.mincount), cfg.graph, llcuts, allcounts)
	pz.run(reconstructdata+ "_BDT", rowcount, int(cfg.mincount), cfg.graph, llcuts, allcounts)
	pp.run(reconstructdata+ "_BDT", rowcount, int(cfg.mincount), cfg.graph, llcuts)
	pe.run(reconstructdata+ "_BDT", rowcount, int(cfg.mincount), cfg.graph, llcuts)
	ph.run(reconstructdata+ "_BDT", rowcount, int(cfg.mincount), cfg.graph, llcuts)
	
if cfg.plot:
	pz.run(reconstructdata, rowcount, int(cfg.mincount), cfg.graph, defaultcuts)
	pp.run(reconstructdata, rowcount, int(cfg.mincount), cfg.graph, defaultcuts)
	pe.run(reconstructdata, rowcount, int(cfg.mincount), cfg.graph, defaultcuts)
	ph.run(reconstructdata, rowcount, int(cfg.mincount), cfg.graph, defaultcuts)

#~ if cfg.plotangle:
	#~ pa.run(cfg.reconstructdata, rowcount, int(cfg.mincount), cfg.graph)

if cfg.radiusstatistics:
	rs.run(cfg.graph)
	
if cfg.optimiselayout:
	ol.run(cfg.numberofhours)
	
if cfg.epnstatistics:
	es.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, layout=cfg.orientation, number = n, nh=cfg.numberofhours)
	
if cfg.heightstatistics:
	hs.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, layout=cfg.orientation, number = n, nh=cfg.numberofhours)
	
if cfg.lightstatistics:
	ls.run(eff, rowcount, mincount=cfg.mincount, text=cfg.text, graph=cfg.graph, layout=cfg.orientation, number = n, nh=cfg.numberofhours)
