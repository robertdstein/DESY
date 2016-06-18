import argparse, math, random, time
import csv
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
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

def run(eff, rowcount=5, mincount=4, text=False, graph=False, output="default", layout="five", number=1, nh=1):
	
	ax3 = plt.subplot(313)
	
	#Define number of bins, maximum Epn
	
	Rmax = 100
	zvalues = np.linspace(20, 32, 3)

	#Iterate over Energies
	
	for Z in zvalues:	
		#For a given Energy, iterate over n randomly simulated events
		
		sdensity=[]
		sigupper=[]
		siglower=[]
	
		
		rrange = np.linspace(0, 2*Rmax, 100)
		
		for r in rrange:
			
			[sig, sigerror], [bkg,  bkgerror] = ld.run(r, 0, Z, Rmax, eff)
			
			if sig > 0:
				sdensity.append(sig)
			else:
				sdensity.append(0.01)
				
			su = sig*(1+sigerror)
			sl = sig*(1-sigerror)
			sigupper.append(su)
			siglower.append(sl)
			
		label= "Z = " + str(Z)
	
		line = ax3.plot(rrange, sdensity, label=label)
		linecolor = line[0].get_color()
		ax3.fill_between(rrange, siglower, sigupper, color=linecolor, alpha=0.25)
		
		
	ax3.set_ylim(bottom=0.1)
	ax3.tick_params(labelsize=20)
	plt.yscale('log')
	plt.ylabel('Photons per m$^2$', fontsize=20)
	plt.xlabel('Radius (m)', fontsize=20)
	plt.title('No background DC light, Rmax=100', fontsize=20)
	
	plt.legend(loc=2)
	
	ax1 = plt.subplot(311)
	ax2 = plt.subplot(312)
	
	#Define number of bins, maximum Epn
	
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
		sigupper=[]
		siglower=[]
		
		bkgdensity=[]
		bkgupper=[]
		bkglower=[]
		
		rrange = np.linspace(0, 2.0*rmax, 100)
		
		for r in rrange:
			
			[sig, sigerror], [bkg,  bkgerror] = ld.run(r, Epn, Z, rmax, eff)
				
			if sig > 0.0:
				sigdensity.append(sig)
			else:
				sigdensity.append(0.01)
				
			su = sig*(1+sigerror)
			sl = sig*(1-sigerror)
			sigupper.append(su)
			siglower.append(sl)
			
			if bkg > 0:
				bkgdensity.append(bkg)
			else:
				bkgdensity.append(0.01)
			
			bu = bkg*(1+bkgerror)
			bl = bkg*(1-bkgerror)
			bkgupper.append(bu)
			bkglower.append(bl)
			
		label= "Epn = " + str(Epn)
	
		ax1.plot(rrange, bkgdensity, 'x', color=color)
		ax1.fill_between(rrange, bkglower, bkgupper, color=color, alpha=0.25)
		ax2.plot(rrange, sigdensity, '--', color=color)
		ax2.fill_between(rrange, siglower, sigupper, color=color, alpha=0.25)

	for ax in [ax1, ax2]:
		ax.set_yscale('log')
		ax.set_ylabel('Photons per m$^2$', fontsize=20)
		ax.set_xlabel('Radius (m)', fontsize=20)
		ax.set_title('Height = ' + str(height) + ', Z = 26', fontsize=20)
		ax.tick_params(labelsize=20)
		ax.set_ylim(bottom=0.1)
	
	
	plt.suptitle("Lateral Photon Distribution in DC pixel", fontsize=20)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(15, 25)
	
	saveto = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/stats/Light.pdf'
	print "Saving to", saveto
	plt.savefig(saveto)
		
	if graph:
		plt.show()
	plt.close()
