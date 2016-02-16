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
	
	#Define number of bins, stepcount
	
	bincount = 20
	stepcount = 1000
	
	lower = float(1)/float(stepcount)
	upper = float(1-lower)
	
	Rrange = np.linspace(lower, upper, stepcount)
	
	ax1 = plt.subplot(321)
	
	decaylengths = []
	survivallengths = []
	decayheights = []
	survivalheights = []
	for R in Rrange:
		dl = atm.runlengths(R)
		decaylengths.append(dl)
		sl = atm.runlengths(1-R)
		survivallengths.append(sl)
		
		dh = atm.runheight(R)
		decayheights.append(dh)
		sh = atm.runheight(1-R)
		survivalheights.append(sh)

	ax1.plot(survivallengths, Rrange, label="survived")
	ax1.plot(decaylengths, Rrange, label = "decayed")
	plt.ylabel('Fraction')
	plt.xlabel('Decay Length', labelpad=0)
	plt.legend()
	
	ax2 = plt.subplot(322)
	
	rawheights=[]
	opticallengths = []
	
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		for row in reader:
			i +=1
			
			if i > 3:
				opticallengths.append(float(row[2]))
				rawheights.append(float(row[0])*1000)
	
	ax2.plot(rawheights, opticallengths, 'r', label="Sum")
	plt.ylabel('Integrated Decay Lengths')
	plt.yscale('log')
	plt.xlabel('Height', labelpad=0)
	ax2.invert_xaxis()
	
	ax3 = plt.subplot(323, sharex=ax2)
	
	ax3.plot(survivalheights, Rrange, label="survived")
	ax3.plot(decayheights, Rrange, label = "decayed")
	plt.ylabel('Fraction')
	plt.xlabel('First Interaction Height', labelpad=0)
	ax3.invert_xaxis()
	plt.legend(loc=2)
		
	#Create a subplot for the fractional abundance

	hrange=[]
	
	fullcount = []
	nDC = []
	wnDC = []
	bT = []
	wbT = []
	mT = []
	wmT = []
	
	#Iterate over Energies
	

	for i in range (0, int(number)):
		
		Rand = random.random()
		height = atm.runheight(Rand, text)
		
		#As in generate.py, randomly generate all variables (expect Epn)
		
		xpos = (random.random()*300)-150
		ypos = (random.random()*300)-150
	
		Z= 26
		
		Re = random.random()*0.0178
		Epn = ((1.7*Re/321)+(3571**-1.7))**(-1/1.7)
		
		weight = Epn ** (-1.7)
		
		hrange.append(height)
	
		zenith = random.random()*44
	
		phi = math.radians(68+zenith)
	
		epsilon = math.pi*random.random()*2
		
		radius, theta = cr.run(Epn, height, math.sin(phi), text=text)
		
		#Determine what category the event was
		
		entry, entrytype = lt.run(layout, xpos, ypos, epsilon, radius, Epn, Z, height, phi, theta, mincount, eff, 1, graph=False, text=False)
		
		#append the energy value to the appropriate category
		
		if entrytype == "metThreshold":
			mT.append(height)
			wmT.append(R)
		elif entrytype == "belowThreshold":
			bT.append(height)
			wbT.append(R)
		elif entrytype == "nonDC":
			nDC.append(height)
			wnDC.append(R)
		else:
			print "ERROR OVER HERE!!!!"

	#Create labels for each bin

	labels = ["metThreshold", "belowThreshold", "nonDC"]
	
	hrange.sort()
		
	hcount = len(hrange)

	limits = [hrange[0], hrange[hcount - 1]]
	
	hbins = np.linspace(limits[0], limits[1], bincount)
		
	ax4 = plt.subplot(324, sharex=ax2)
	
	tweights = np.ones_like(decayheights)/len(decayheights)
	mcweights = np.ones_like(hrange)/len(hrange)
	
	plt.hist([decayheights, hrange], weights=[tweights, mcweights], label=["Theoretical", "Recorded"])
	plt.ylabel('Fraction')
	plt.xlabel('First Interaction Height', labelpad=0)
	ax4.invert_xaxis()
	plt.legend(loc=2)
	
	#Plot the unscaled histogram
	
	ax5 = plt.subplot(325, sharex=ax2)
	
	plt.hist([mT, bT, nDC], bins=hbins, log=True, histtype='bar',range=limits, label=labels)
	
	plt.xlim(limits)
	plt.ylabel('Recorded Count')
	plt.xlabel('First Interaction Height', labelpad=0)
	plt.legend(loc=2)
	ax5.invert_xaxis()
	
	#plot the histogram scaled with E^-1.7 distribution to the second subplot
	
	ax6 = plt.subplot(326)
	
	n, bins, _ = plt.hist([mT], label=labels)
	
	mid = (bins[1:] + bins[:-1])*0.5
	errors = []
	for count in n:
		errors.append(math.sqrt(count))
	
	plt.errorbar(mid, n, yerr=errors, fmt='kx')
	
	nmax = np.amax(n)
	
	uplim = nmax + 2*(math.sqrt(nmax))
	
	plt.ylim(0, uplim)
	
	plt.xlabel('First Interaction Height', labelpad=0)
	
	plt.ylabel('Recorded Count')
	plt.legend()
	
	ax6.invert_xaxis()
	
	title = 'Height Statistics for ' + str(nh) + " hours"
	
	plt.suptitle(title, fontsize=20)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.savefig('graphs/stats/Height.pdf')
		
	if graph:
		plt.show()
