import argparse, math, random
import csv
import numpy as np
import batchprocessing as bp
import batchreconstruction as br

parser = argparse.ArgumentParser(description='Create a canvas for positions of telescopes')
parser.add_argument("-o", "--orientation", default="five")
parser.add_argument("-sd", "--sourcedata", default="default")
parser.add_argument("-pd", "--processdata", default="process")
parser.add_argument("-rd", "--reconstructdata", default="reconstructed")
parser.add_argument("-mc", "--mincount", default=3)
parser.add_argument("-bp", "--batchprocessing", action="store_true")
parser.add_argument("-br", "--batchreconstruction", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
cfg = parser.parse_args()

with open("orientations/"+ cfg.orientation +".csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	rowcount = 0
	for row in reader:
		rowcount +=1

if cfg.batchprocessing:
	bp.run(cfg.sourcedata, cfg.processdata, cfg.mincount, rowcount)
	
if cfg.batchreconstruction:
	br.run(cfg.processdata, cfg.reconstructdata)
