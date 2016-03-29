import argparse, math, random, time
import csv
import numpy as np
import generate as g
import lightdensity as ld
import calculatearea as ca
import calculateellipse as ce
import countsimulation as cs
import cherenkovradius as cr
import telescoperadius as tr
import looptelescopes as lt
import atmosphere as atm
import matplotlib.pyplot as plt

radii = []
weights = []
labels=[]
colors=[]
		
Epns = [50000./56., 40000./56., 30000./56., 20000./56.]
height = 25000

wl=450*(10**-9)
Z = 26
alpha=float(1)/float(137)
ewidth = 1.6*(10**-19)
scaling= (Z**2) * alpha * ewidth * math.pi * 2/(wl**2)

for Epn in Epns:
	
	r=[]
	w=[]

	print Epn, height
	
	h = 65000
	
	heights = []
	ris = []
	linears=[]
	
	while h > height:
		h += -1
		
		beta, ri = cr.runbetaeta(Epn, h)
		heights.append(h)
		ris.append(ri-1)
		linearri=atm.linearri(h)
		linears.append(linearri - 1)
		
		if float(beta) > (float(1)/float(ri)):
			radius, theta = cr.run(Epn, h, sinphi=1)
			
			n = (1-(1/(ri*beta)**2))
			
			oldradius, oldtheta = cr.run(Epn, h+1, sinphi=1)
			
			deltar =  float(radius)- float(oldradius)
			
			area= deltar * math.pi * ((2*radius) + deltar) 
			
			density = scaling*n/area
			
			r.append(radius)
			w.append(density)
			rmax=radius
			
	radii.append(r)
	weights.append(w)
	labels.append(str(Epn))
	colors.append("k")
		
plt.subplot(2,1,1)
plt.plot(heights, ris, label="Exponential")
plt.plot(heights, linears, label="Linear", color='r')
plt.yscale("Log")
plt.legend()
plt.subplot(2,1,2)

n, bins, patches = plt.hist(radii, weights=weights,  bins=100, histtype='bar', alpha=0.0, color=colors)
#~ plt.yscale("Log", nonposy='clip')

mid = (bins[1:] + bins[:-1])*0.5

for i in range(0, len(labels)):
	plt.plot(mid, n[i], label=labels[i])
plt.legend(loc=2)

figure = plt.gcf() # get current figure
figure.set_size_inches(20, 15)

path = '/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/stats/lpd.pdf'
print "saving to", path
plt.savefig(path)
