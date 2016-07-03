import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
from classes import *

def run(statsset, mindetections, cuts):
	
	datasimset = pickle.load(open(statsset, 'rb'))
	detectorcount = datasimset[0].ndetectors
	
	fig = plt.figure()
	
	k=0
	cutset = [cuts,None]
	for currentcuts in cutset: 
		for j in range (detectorcount, mindetections -1, -1):
			print "Ndetections", j
			plt.subplot(2,2, 4-k)
			if currentcuts == None:
				bdtmin = -0.01
			else:
				bdtmin = currentcuts[k]
				
			base = datasimset[0].simulations[0].true
			for tel in base.telescopes:
				x = tel.x
				y=tel.y
				area = tel.area
				r = tel.telradius
				#~ plt.scatter(x,y, s =area, linewidth='2', facecolors='white', zorder=2)
				circle=plt.Circle((x,y),r, linewidth="3", alpha=0.5, color='white', zorder=2)
				circle=plt.Circle((x,y),r,linewidth='1', edgecolor="k", facecolor='none', zorder=3)
				fig = plt.gcf()
				fig.gca().add_artist(circle)
			
			for simset in datasimset:
				for sim in simset.simulations:	
					recon = sim.reconstructed
					observed = sim.detected
					true = sim.true
					if int(observed.DCmultiplicity) == int(j):
						if recon.BDTscore != None:
							if float(bdtmin) < float(recon.BDTscore):
								x = recon.rayxpos
								y = recon.rayypos
								score = recon.BDTscore
								plt.scatter(x,y, s =50, alpha = 0.5, c=score, zorder=1, linewidth='0', vmin=0, vmax = 1)
						
			plt.colorbar()			
			plt.xlim(-150, 150)
			plt.ylim(-150, 150)
			if currentcuts == None:
				plt.title("Reconstructed position and BDT score for all "  + str(j) +  "-telescope events", fontsize = 10)
			else:
				plt.title("Reconstructed position and BDT score for accepted "  + str(j) +  "-telescope events", fontsize = 10)
			k +=1
		
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)

	plt.tight_layout()
	
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/bdtmap.pdf')
	path = '/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/bdtmap.pdf'
	
	plt.savefig(path)
	print "saving to", path
	plt.close()
	
