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
from classes import *

def run(eff, rowcount, mincount=4, text=False, graph=False, output="default", layout="five", number=1, nh=1):
	
	#Define number of bins, stepcount
	
	bincount = 20
	stepcount = 1000
	
	lower = float(1)/float(stepcount)
	upper = float(1-lower)
	
	Rrange = np.linspace(lower, upper, stepcount)
	
	#~ ax1 = plt.subplot(321)
	#~ 
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

	#~ ax1.plot(survivallengths, Rrange, label="survived")
	#~ ax1.plot(decaylengths, Rrange, label = "decayed")
	#~ plt.ylabel('Fraction')
	#~ plt.xlabel('Interaction Lengths', labelpad=0)
	#~ plt.legend()
	
	ax2 = plt.subplot(311)
	
	rawheights=[]
	opticallengths = []
	
	with open('/d6/rstein/Hamburg-Cosmic-Rays/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		for row in reader:
			i +=1
			
			if i > 3:
				opticallengths.append(float(row[2]))
				rawheights.append(float(row[0])*1000)
	
	ax2.plot(rawheights, opticallengths, 'r', label="Sum")
	plt.ylabel('Integrated Interaction Lengths')
	plt.yscale('log')
	plt.xlabel('Height', labelpad=0)
	ax2.invert_xaxis()
	
	ax3 = plt.subplot(312, sharex=ax2)
	
	ax3.plot(survivalheights, Rrange, label="survived")
	ax3.plot(decayheights, Rrange, label = "interacted")
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
	emith = []
	
	#Iterate over Energies
	simset = simulationset(eff, layout, mincount=0, hmacceptance = [1,1,1,1,1,1])
	
	simset.generate(number)
	
	for sim in simset.simulations:
		true = sim.true
		height = true.height
		multiplicity = int(true.truemultiplicity)
		
		hrange.append(height)
		
		if multiplicity == int(0):
			nDC.append(height)

		elif multiplicity < int(mincount):
			bT.append(height)
			emith.append(height)

		else:
			mT.append(height)
			emith.append(height)
			
	print "High Multiplicity DC emission is", float(len(mT))/float(number)
	print "Low Multiplicity DC emission is", float(len(bT))/float(number)
	print "Non-DC emission is", float(len(nDC))/float(number)

	#Create labels for each bin

	labels = ["metThreshold", "belowThreshold", "nonDC"]
	
	hrange.sort()
		
	hcount = len(hrange)

	limits = [hrange[0], hrange[hcount - 1]]
	
	hbins = np.linspace(limits[0], limits[1], bincount)
	
	#~ extent = ax1.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('decay.png', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax2.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('Decay Lengths.pdf', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax3.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('Fraction with Height.pdf', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax4.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('first interaction height.pdf', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax5.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('interaction category.pdf', bbox_inches=extent.expanded(1.2, 1.2))

		
	ax4 = plt.subplot(313, sharex=ax2)
	
	tweights = np.ones_like(decayheights)/len(decayheights)
	#~ mcweights = np.ones_like(hrange)/len(hrange)
	
	plt.hist([decayheights], weights=[tweights])
	plt.ylabel('Fraction')
	plt.xlabel('First Interaction Height', labelpad=0)
	ax4.invert_xaxis()
	
	fig = plt.gcf() # get current figure
	
	st = fig.suptitle("Atmospheric Interaction", fontsize=20)
	st.set_y(0.98)
	fig.set_size_inches(10, 15)
	fig.tight_layout()
	fig.subplots_adjust(top=0.95)
	
	
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/stats/generalheight.pdf')
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/generalheight.png')
	#Plot the unscaled histogram
	
	ax5 = plt.subplot(211, sharex=ax2)
	
	plt.hist([mT, bT, nDC], bins=20, log=True, histtype='bar', range=limits, label=labels)
	
	print "Overall mean first interaction height is", np.mean(hrange)
	hrange.sort()
	nhrange = len(hrange)
	halfin = int(nhrange/2.)
	hmedian = hrange[halfin]
	print "Overall median first interaction height is", hmedian
	
	tscale = atm.runlengthswithh(hmedian)
	print "Corresponding Median Interaction Lengths", tscale
	texpectation = tscale/math.log(2)
	print "Resultant Expectation Interaction Lengths", texpectation
	
	emith.sort()
	ehrange = len(emith)
	ehalfin = int(ehrange/2.)
	ehmedian = emith[ehalfin]
	
	print "Cherenkov-Emission mean first interaction height is", np.mean(emith)
	print "Cherenkov-Emission median first interaction height is", ehmedian
	etscale = atm.runlengthswithh(ehmedian)
	print "Corresponding Median Interaction Lengths", etscale
	etexpectation = etscale/math.log(2)
	print "Resultant Expectation Interaction Lengths", etexpectation
	
	plt.xlim(limits)
	plt.ylabel('Recorded Count')
	plt.xlabel('First Interaction Height', labelpad=0)
	plt.legend(loc=2)
	ax5.invert_xaxis()
	
	#plot the histogram scaled with E^-1.7 distribution to the second subplot
	
	ax6 = plt.subplot(212)
	
	if len(mT) > 0:
	
		n, bins, _ = plt.hist([mT], bins=20, label=labels)
		
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
	
	print "For Ntel > ", mincount, ", mean first interaction height is", np.mean(mT)
	
	ax6.invert_xaxis()
	
	
	title = 'Height Statistics for ' + str(nh) + " hours"

	fig = plt.gcf() # get current figure
	
	st = fig.suptitle(title, fontsize=20)
	st.set_y(0.98)
	fig.set_size_inches(10, 15)
	fig.tight_layout()
	fig.subplots_adjust(top=0.95)
	#~ extent = ax1.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('decay.png', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax2.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('Decay Lengths.pdf', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax3.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('Fraction with Height.pdf', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax4.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('first interaction height.pdf', bbox_inches=extent.expanded(1.2, 1.2))
	#~ 
	#~ extent = ax5.get_window_extent().transformed(figure.dpi_scale_trans.inverted())
	#~ plt.savefig('interaction category.pdf', bbox_inches=extent.expanded(1.2, 1.2))

	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/hessheight.png')

	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/stats/Height.pdf')
	
		
	if graph:
		plt.show()

