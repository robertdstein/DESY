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
	
	Rcount = 3
	rlower = 70
	rupper = 130
	Z=26
	
	sdensity=[]
	
	Rmaxrange = np.linspace(rlower, rupper, Rcount)
	
	#Iterate over Energies
	
	
	for Rmax in Rmaxrange:	
		#For a given Energy, iterate over n randomly simulated events
		
		sdensity=[]
		
		rrange = np.linspace(0, 1.2*Rmax, 100)
		
		for r in rrange:
			
			sig, bkg = ld.run(r, 0, Z, Rmax, 1)
			
			if sig > 1:
				sdensity.append(sig)
			else:
				sdensity.append(1)
			
		label= "R = " + str(Rmax)
	
		ax1.plot(rrange, sdensity, label=label)
		
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$')
	plt.xlabel('Radius (m)')
	plt.title('No background, Z=26')
	
	plt.legend(loc=2)
	
	ax2 = plt.subplot(222)
	
	#Define number of bins, maximum Epn
	
	Rmax = 100
	zvalues = np.linspace(20, 32, 5)
	
	sdensity=[]
	
	#Iterate over Energies
	
	for Z in zvalues:	
		#For a given Energy, iterate over n randomly simulated events
		
		sdensity=[]
		
		rrange = np.linspace(0, 1.2*Rmax, 100)
		
		for r in rrange:
			
			sig, bkg = ld.run(r, 0, Z, Rmax, 1)
			
			if sig > 1:
				sdensity.append(sig)
			else:
				sdensity.append(1)
			
		label= "Z = " + str(Z)
	
		ax2.plot(rrange, sdensity, label=label)
	
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$')
	plt.xlabel('Radius (m)')
	plt.title('No background, Rmax=100')
	
	plt.legend(loc=2)
	
	ax3 = plt.subplot(223)
	
	#Define number of bins, maximum Epn
	
	Rmax = 100
	Z = 26
	
	eraw = np.linspace(0.01, 0.99, num=5)
	R = eraw*0.0178
	Erange = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)
	
	for Epn in Erange:

		
		bkgdensity=[]
		
		rrange = np.linspace(0, 1.6*Rmax, 100)
		
		for r in rrange:
			
			sig, bkg = ld.run(r, Epn, Z, Rmax, 1)
			
			if bkg > 1:
				bkgdensity.append(bkg)
			else:
				bkgdensity.append(1)
			
		label= "Epn = " + str(Epn)
	
		ax3.plot(rrange, bkgdensity, label=label)
	
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$')
	plt.xlabel('Radius (m)')
	plt.title('No signal, Rmax = 100m')
	
	plt.legend(loc=3)
	
	ax4 = plt.subplot(224)
	
	#Define number of bins, maximum Epn
	
	height = 22000
	Z = 26
	
	for Epn in Erange:

		rmax, theta = cr.run(Epn, height, sinphi=1, text=False)

		density=[]
		
		rrange = np.linspace(0, 1.6*Rmax, 100)
		
		for r in rrange:
			
			sig, bkg = ld.run(r, Epn, Z, rmax, 1)
			
			count = sig + bkg
			
			if count > 1:
				density.append(count)
			else:
				density.append(1)
			
		label= "Epn = " + str(Epn)
	
		ax4.plot(rrange, density, label=label)
	
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$')
	plt.xlabel('Radius (m)')
	plt.title('Height = ' + str(height) + ', Z = 26')
	
	plt.legend(loc=3)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	title = 'Light Density Statistics'
	plt.suptitle(title, fontsize=20)
	
	plt.savefig('graphs/stats/Light.pdf')
		
	if graph:
		plt.show()

