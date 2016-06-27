import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time, math
from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
import csv
import random
from classes import *
import cPickle as pickle

plt.ioff()

def run(statsset):
	
	distances=[]
	truesignals=[]
	signals=[]
	fulltrue=[]
	fullsmear=[]
	
	
	fullsimsets = pickle.load(open(statsset, 'rb'))
	
	for simset in fullsimsets:
		for sim in simset.simulations:
			recon = sim.reconstructed
			observed = sim.detected
			true = sim.true
			if 36000 > true.energy > 35000:
				for i in range(len(true.telescopes)):
					ttel = true.telescopes[i]
					dtel = observed.telescopes[i]
					
					coredistance = ttel.coredistance
					truesignal = ttel.DCphotons/ttel.area
					signal = dtel.DCphotons/dtel.area
					full = ttel.fullphotons/dtel.area
					smear = dtel.fullphotons/dtel.area
					distances.append(coredistance)
					truesignals.append(truesignal)
					signals.append(signal)
					fulltrue.append(full)
					fullsmear.append(smear)
	
	data = [truesignals, signals, fulltrue, fullsmear]
	headings = ["True LPD", "Received LPD", "True Full LPD" "Received Full LPD"]
	for i in range(len(data)):
		plt.subplot(4,1, i+1)
		plotdata = data[i]
		plt.scatter(distances, plotdata)
		plt.xlabel("Distance")
		plt.ylabel("Photoelectron density")
		
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 20)
	
	plt.savefig("/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/stats/lpd.pdf")
	
	plt.close()

				
