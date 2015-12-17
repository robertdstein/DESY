import argparse, math, random
import csv
import numpy as np
import simulate as s
import batchprocessing as bp
import batchreconstruction as br
import plotz as pz
import plotx as px
import ploty as py
import plotepn as pe

parser = argparse.ArgumentParser(description='Create a canvas for positions of telescopes')
parser.add_argument("-o", "--orientation", default="five")
parser.add_argument("-sd", "--sourcedata", default="default")
parser.add_argument("-pd", "--processdata", default="process")
parser.add_argument("-rd", "--reconstructdata", default="reconstructed")
parser.add_argument("-mc", "--mincount", default=3)
parser.add_argument("-bp", "--batchprocessing", action="store_true")
parser.add_argument("-br", "--batchreconstruction", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-s", "--simulate", action="store_true")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-pz", "--plotz", action="store_true")
parser.add_argument("-px", "--plotx", action="store_true")
parser.add_argument("-py", "--ploty", action="store_true")
parser.add_argument("-pe", "--plotepn", action="store_true")
parser.add_argument("-ph", "--ploth", action="store_true")
parser.add_argument("-n", "--number", default=int(1))
parser.add_argument("-rgw", "--reconstructiongridwidth", default=25)
cfg = parser.parse_args()

eff = 0.08

with open("orientations/"+ cfg.orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1
		
if cfg.simulate:
	s.run(eff, text=cfg.text, graph=cfg.graph, output=cfg.sourcedata, layout=cfg.orientation, number = int(cfg.number))

if cfg.batchprocessing:
	bp.run(cfg.sourcedata, cfg.processdata, cfg.mincount, rowcount, text=cfg.text)
	
if cfg.batchreconstruction:
	br.run(cfg.processdata, cfg.reconstructdata, rowcount, cfg.reconstructiongridwidth, eff)
	
if cfg.plotz:
	pz.run(cfg.reconstructdata, rowcount, cfg.mincount, cfg.graph)
	
if cfg.plotx:
	px.run(cfg.reconstructdata, rowcount, cfg.mincount, cfg.graph)

if cfg.ploty:
	py.run(cfg.reconstructdata, rowcount, cfg.mincount, cfg.graph)
	
if cfg.plotepn:
	pe.run(cfg.reconstructdata, rowcount, cfg.mincount, cfg.graph)
