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
	
	ax1 = plt.subplot(212)
	
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
			
			sig, bkg = ld.run(r, 0, Z, Rmax, eff)
			
			if sig > 1:
				sdensity.append(sig)
			else:
				sdensity.append(1)
			
		label= "Z = " + str(Z)
	
		ax1.plot(rrange, sdensity, label=label)
	
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$', fontsize=20)
	plt.xlabel('Radius (m)', fontsize=20)
	plt.title('No background, Rmax=100', fontsize=20)
	
	plt.legend(loc=2)
	
	ax2 = plt.subplot(211)
	
	#Define number of bins, maximum Epn
	
	Rmax = 100
	Z = 26
	
	eraw = np.linspace(0.0, 1.0, num=3)
	R = eraw*0.0178
	Erange = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)
	
	Erange = [3571, 850]
	
	height = 22000
	Z = 26
	
	colors=['r', 'g', 'b']
	
	for i in range(0, len(Erange)):
		
		Epn = Erange[i]

		rmax, theta = cr.run(Epn, height, sinphi=1, text=False)
		
		color=colors[i]

		density=[]
		
		sigdensity = []
		
		bkgdensity=[]
		
		rrange = np.linspace(0, 1.6*Rmax, 100)
		
		for r in rrange:
			
			sig, bkg = ld.run(r, Epn, Z, rmax, eff)
			
			count = sig + bkg
			
			if count > 1:
				density.append(count)
			else:
				density.append(1)
				
			if sig > 1:
				sigdensity.append(sig)
			else:
				sigdensity.append(1)
			
			if bkg > 1:
				bkgdensity.append(bkg)
			else:
				bkgdensity.append(1)
			
		label= "Epn = " + str(Epn)
	
		ax2.plot(rrange, bkgdensity, 'x', color=color)
		ax2.plot(rrange, sigdensity, '--', color=color)
		ax2.plot(rrange, density, color=color, label=label, linewidth=3.0)
	
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$', fontsize=20)
	plt.xlabel('Radius (m)', fontsize=20)
	plt.title('Height = ' + str(height) + ', Z = 26', fontsize=20)
	
	plt.legend()
	
	ax1.tick_params(labelsize=20)
	ax2.tick_params(labelsize=20)
	
	plt.suptitle("Lateral Photon Distribution in DC pixel", fontsize=20)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	
	plt.savefig('graphs/stats/Light.pdf')
		
	if graph:
		plt.show()

