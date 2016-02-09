import argparse, math, random, time
import csv
import numpy as np
import matplotlib.pyplot as plt
import generate as g
import lightdensity as ld
import calculatearea as ca
import calculateellipse as ce
import countsimulation as cs
import telescoperadius as tr
import looptelescopes as lt
import atmosphere as atm
import cherenkovradius as cr
from matplotlib.patches import Ellipse

def run(eff, rowcount, mincount=4, text=False, graph=False, output="default", layout="five", number=1):
	
	#Create a subplot for the fractional abundance

	ax1 = plt.subplot(211)
	
	#Define number of bins, maximum Epn
	
	bincount = 20
	nmax = 1
	emax = 35720
	
	Rrange = np.linspace(0, nmax, bincount)
	k = math.log(emax/232)/float(nmax)
	
	Erange=[]
	
	fullcount = []
	nDC = []
	wnDC = []
	bT = []
	wbT = []
	mT = []
	wmT = []
	
	#Iterate over Energies
	
	for R in Rrange:

		Epn = 232*(math.e**(k*R))
		
		Erange.append(Epn)
		
		weight = Epn ** (-1.7)
		
		#For a given Energy, iterate over n randomly simulated events

		for i in range (0, int(number)):
			
			#As in generate.py, randomly generate all variables (expect Epn)
			
			xpos = (random.random()*300)-150
			ypos = (random.random()*300)-150
		
			Z= 26
			
			hprob = random.random()
			height = atm.runheight(hprob, text)
		
			zenith = random.random()*44
		
			phi = math.radians(68+zenith)
		
			epsilon = math.pi*random.random()*2
			
			radius, theta = cr.run(Epn, height, math.sin(phi), text=text)
			
			#Determine what category the event was
			
			entry, entrytype = lt.run(layout, xpos, ypos, epsilon, radius, Epn, Z, height, phi, theta, mincount, eff, 1, graph=False, text=False)
			
			#append the energy value to the appropriate category
			
			if entrytype == "metThreshold":
				mT.append(Epn)
				wmT.append(weight)
			elif entrytype == "belowThreshold":
				bT.append(Epn)
				wbT.append(weight)
			elif entrytype == "nonDC":
				nDC.append(Epn)
				wnDC.append(weight)
			else:
				print "ERROR OVER HERE!!!!"
	
	#Create labels for each bin

	labels = ["metThreshold", "belowThreshold", "nonDC"]
	
	xlabels=[]
	
	for i in Erange:
		xlabels.append(int(i))
	
	Erange.append(emax + 1)
	bin_centers = 0.5 * np.diff(Erange) + Erange[:-1]
	
	limits = [Erange[0], Erange[bincount]]
	
	print limits
	
	#Plot the unscaled histogram

	plt.hist([mT, bT, nDC], bins=Erange, histtype='bar',range=limits, label=labels, stacked=True)

	plt.xlim(limits)
	plt.xscale('log')
	plt.setp(ax2.get_xticklabels(), visible=False)
	plt.ylabel('Fractional Abundance')
	plt.legend()
	
	#plot the histogram scaled with E^-1.7 distribution to the second subplot
	
	ax1 = plt.subplot(212, sharex=ax2)
		
	plt.hist([mT], weights=[wmT], bins=Erange, histtype='bar',range=limits, label=labels, stacked=True)

	plt.xlim(limits)
	plt.xscale('log')
	plt.xticks(bin_centers, xlabels, rotation=90)
	plt.xlabel('Epn', labelpad=0)
	plt.ylabel('Normalised Adunbance')
	plt.legend()
	
	plt.suptitle('Epn Statistics', fontsize=20)
	
	plt.savefig('graphs/EnergyStats.pdf')
		
	if graph:
		plt.show()

