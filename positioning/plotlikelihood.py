import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cPickle as pickle
from classes import *

def run(statsset, mindetections, cuts=None):
	
	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors
	
	print detectorcount, mindetections
	
	ngraphs = 1 + detectorcount-mindetections
	nrows =(ngraphs-int(0.5*ngraphs))

	
	if cuts == None:
		cuts = np.zeros(1 + detectorcount-mindetections)
		
	for j in range (detectorcount, mindetections -1, -1):
		print "Ndetections", j
		
		ax = plt.subplot(nrows, 2, (1+ detectorcount-j))
		
		i = -1
		info = ""
		correct = []
		close = []
		wrong = []
		full = []
		plot = []
		plotcolour = []
		plotlabel = []
		
		bdtmin=cuts[detectorcount-j]
		
		for simset in datasimset:
				for sim in simset.simulations:	
					recon = sim.reconstructed
					observed = sim.detected
					true = sim.true
					

					if int(observed.DCmultiplicity) == int(j):
						if recon.BDTscore != None:
							deltaz = int(math.fabs(float(true.Z)-float(recon.Z)))
							full.append(float(recon.BDTscore))
							
							if float(deltaz) == float(0):
								correct.append(float(recon.BDTscore))
								
							elif float(deltaz) == float(1):
								close.append(float(recon.BDTscore))
								
							elif float(deltaz) > 1:
								wrong.append(float(recon.BDTscore))
			
		total = len(correct)
		info += "For BDT > " + str('{0:.2f}'.format(bdtmin)) + " Values \n"
		for i in range(0, 3):
			category = [correct, close, wrong][i]
			name = ["correct", "close", "wrong"][i]
			color = ["green", "orange", "red"][i]
			label=["Delta Z = 0", "Delta Z = 1", "Delta Z > 1"][i]
			passno = 0
			totalno = len(category)
			for entry in category:
				if float(bdtmin) < float(entry):
					passno +=1
			if totalno > 0:
				passfrac = passno/float(totalno)
				plot.append(category)
				plotcolour.append(color)
				plotlabel.append(label)
			else:
				passfrac = 0
			info += (str(label) + ' - ' + str('{0:.0f}'.format(100*passfrac)) + "% pass \n")
	
		if len(plot) > 0:
			plt.hist(plot, color = plotcolour, range=[0,1], bins = 25, stacked=True, label=plotlabel, histtype='stepfilled')
			plt.axvline(x=bdtmin,  color='k', linewidth=4)
		
		#~ for val in llcuts:
			#~ plt.axvline(x=(val+0.01), linestyle='--', color='m', label="LL Cut")
		
		plt.xlabel('BDT Score')
		plt.ylabel('Count', labelpad=0)
		plt.legend()
		plt.annotate(info, xy=(0.65, 0.75), xycoords="axes fraction",  fontsize=10)
		title = str(j) + " Telescope Detections"
		plt.title(title)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(15, 10)
	plt.suptitle('BDT prediction of signal probability', fontsize=20)
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/Likelihood.pdf')
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Likelihood.pdf')
	plt.close()
