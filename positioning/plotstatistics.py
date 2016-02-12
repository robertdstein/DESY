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

def run(eff, rowcount, mincount=4, text=False, graph=False, output="default", layout="five", number=1, nh=1):
	
	#Create a subplot for the fractional abundance

	ax1 = plt.subplot(221)
	
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
		
		weight = Epn ** (-2.7)
		
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
	
	mweights = np.ones_like(mT)/len(mT)
	bweights=np.ones_like(bT)/len(bT)
	nDCweights=np.ones_like(nDC)/len(nDC)
	
	#Plot the histogram

	plt.hist([mT, bT, nDC], bins=Erange, log=True, histtype='bar',range=limits, label=labels)

	plt.xlim(limits)
	plt.xscale('log')
	plt.setp(ax1.get_xticklabels(), visible=False)
	plt.ylabel('Abundance')
	
	#plot the histogram scaled with E^-2.7 distribution to the second subplot
	
	ax2 = plt.subplot(222, sharex=ax1)
		
	plt.hist([mT, bT, nDC], weights=[wmT, wbT, wnDC], log=True, bins=Erange, histtype='bar',range=limits, label=labels)

	plt.xlim(limits)
	plt.xscale('log')
	plt.xticks(bin_centers, xlabels, rotation=90)
	plt.xlabel('Epn', labelpad=0)
	plt.ylabel('Scaled Count')
	plt.legend()
	
	ax3 = plt.subplot(212)
	
	rawheights=[]
	thetamax = []
	emin=[]
	rmax = []
	refractiveindex = []
	
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		for row in reader:
			i +=1
			if i > 3:
				height = float(row[0])*1000
				ri = float(row[3]) + float(1)
				theta = math.acos(float(1)/float(ri))
				Ethreshold = cr.runemin(ri)
				r = theta*height
				rawheights.append(height)
				thetamax.append(theta)
				emin.append(Ethreshold)
				rmax.append(r)
				refractiveindex.append(float(row[3]))
	
	ax3.plot(rawheights, thetamax, label="Maximum Theta")
	ax3.plot(rawheights, emin, label="Threshold Energy (GeV per Nucleon)")
	ax3.plot(rawheights, rmax, label="Maximum Radius (m)")
	ax3.plot(rawheights, refractiveindex, label="Refractive Index - 1")
	plt.yscale('log')
	
	plt.xlabel('Height', labelpad=0)
	plt.legend(loc=4)
	
	ax3.invert_xaxis()
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	title = 'Epn Statistics for ' + str(float(nh)*float(bincount)) + " hours"
	plt.suptitle(title, fontsize=20)
	
	plt.savefig('graphs/EnergyStats.pdf')
		
	if graph:
		plt.show()

