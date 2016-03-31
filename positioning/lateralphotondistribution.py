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

eff=1.0

radii = []
weights = []
labels=[]
colors=[]
		
Epns = np.linspace(15, 65, 5)
height = 25000

wl=450*(10**-9)
Z = 26
alpha=float(1)/float(137)
ewidth = 0.7
#~ scaling= (Z**2) * alpha * ewidth * math.pi * 2/(wl**2)
scaling = 370 * (Z**2) * 100 * ewidth

for tev in Epns:
	
	Epn = tev*1000./56.
	
	r=[]
	w=[]

	print tev, "TeV", height, Epn
	
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
			
			n = scaling*(math.sin(theta)**2)
			
			DeltaE = (10**-9)*(n*2.74)/56.
			
			oldradius, oldtheta = cr.run(Epn, h+1, sinphi=1)
			
			deltar =  float(radius)- float(oldradius)
			
			area= math.pi * ((radius**2) -(oldradius**2))
			
			frac = atm.runabsorption(h)
			frac=1
			
			density = frac*eff*n/area
			
			r.append(radius)
			w.append(density)
			rmax=radius
			
			Epn += -DeltaE
	
	r.append(radius+0.01)
	w.append(1)
		
	radii.append(r)
	weights.append(w)
	labels.append(str(tev) + " TeV")
	colors.append("k")
		
plt.subplot(3,1,1)
plt.plot(heights, ris, label="Exponential")
plt.plot(heights, linears, label="Linear", color='r')
plt.yscale("Log")
plt.legend()

plt.subplot(3,1,2)

plt.yscale("Log", nonposy='clip')

for i in range(0, len(labels)):
	plt.plot(radii[i], weights[i], label=labels[i])
plt.legend(loc=2)
plt.gca().set_ylim(bottom=1)

plt.subplot(3,1,3)

for i in range(0, len(labels)):
	plt.plot(radii[i], weights[i], label=labels[i])
plt.legend(loc=2)

plt.gca().set_ylim(bottom=1)
figure = plt.gcf() # get current figure
figure.set_size_inches(15, 25)

path = '/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/stats/lpd.pdf'
print "saving to", path
plt.savefig(path)
