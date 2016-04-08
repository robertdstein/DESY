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

def run(graph=False):
	
	i = 1
	Evalues = [233, 700, 2000, 3500]
	total = len(Evalues)
	
	for Epn in Evalues:
		
		zenith = 0
	
		phi = math.radians(68+zenith)
		
		hprob = np.linspace(0.001, 0.999, 999)
		
		loc1 = str(total)  + str(2) + str(i)
		loc2 = str(total)  + str(2) + str(i + 1)
		
		ax1 = plt.subplot(loc1)
		ax2 = plt.subplot(loc2)
		
		h=[]
		r=[]
		
		for p in hprob:
		
			height = atm.runheight(p, text=False)
			
			radius, theta = cr.run(Epn, height, math.sin(phi), text=False)
			
			r.append(radius)
			h.append(height)
			
		ax1.plot(r, hprob, '-r')
		ax2.plot(r, h, '-r')

		title = "Epn = " + str(Epn)

		ax1.set_title(title)
		ax1.set_xlabel('Radius')
		ax1.set_xlim(0, 150)
		ax2.set_xlim(0, 150)
		ax1.set_ylim(0, 1)
		ax2.set_ylim(0, 100000)
		ax2.set_xlabel('Radius')
		ax1.set_ylabel('Probability')
		
		ax2.set_ylabel('Height')
		
		i+=2
		
	plt.tight_layout()
	
	plt.suptitle('Radius with Height')
	
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/stats/radius.pdf')
		
	if graph:
		plt.show()

