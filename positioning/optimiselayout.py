import argparse, math, random, time
import csv
import numpy as np
import matplotlib.pyplot as plt
import telescoperadius as tr
import atmosphere as atm
import lightdensity as ld
import calculatearea as ca
import calculateellipse as ce
import countsimulation as cs
import telescoperadius as tr
import cherenkovradius as cr

def run(numberofhours):
	
	ax1 = plt.subplot(211)
	
	category = "lst"
	tradius = tr.run(category)
	
	raweff = 0.06
	selectionefficiency = 0.50
	flux = 2.0 * (10**-4)
	solidangle = math.radians(5)
	
	ranges = []
	
	lowerlim = 15
	midlim = 50
	upperlim = 200
	lowerbincount = 20
	upperbincount = 10
	
	lowerrange = [lowerlim, midlim, lowerbincount]
	ranges.append(lowerrange)
	
	upperrange = [midlim, upperlim, upperbincount]
	ranges.append(upperrange)
	
	fullcount = []
	edges = []
	
	for i in range (0, 10):
		fullcount.append([])
		
	for i in range(0, 2):
		
		entry = ranges[i]
		
		lower = entry[0]
		upper = entry[1]
		bins = entry[2]
		
		
		edge = np.linspace(lower, upper, bins)
		edges.extend(edge)
		telescopegap = (edge[1:] + edge[:-1])*0.5
		
		print edge
		print telescopegap
		
		
		simlim = (upper + 150)
		
		area = 4*(simlim**2)
		detectedflux = flux*area*solidangle*selectionefficiency
		rateperhour = detectedflux * 60 * 60
		n = int(rateperhour*float(numberofhours))
		
		print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
		print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 
	
		for gap in telescopegap:
			
			specificcount = []
			
			coordinates = []
			points = np.linspace(-gap, gap, 3)
			
			for x in points:
				for y in points:
					coordinates.append([x,y])
			
			for i in range (0, n):
				
				#Randomly generates a target centre of -150<x<150m and -150<y<150m
				rayxpos = (random.random()*2 * simlim)-simlim
				rayypos = (random.random()*2 * simlim)-simlim
				
				#Generates a random probability, and converts this to an Epn value following an E^-1.7 power series
				
				R = random.random()*0.0178
				Epn = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)
				
				#Generates a fixed charge number of Z=26
			
				Z= 26
				
				#Randomly generates a height probability, and converts this probability to a set height
				
				hprob = random.random()
				height = atm.runheight(hprob, text=False)
				
				#Chooses a zenith angle +- 22 degrees
			
				zenith = random.random()*44
			
				phi = math.radians(68+zenith)
				
				#Randomly choose an angle NESW
			
				epsilon = math.pi*random.random()*2
				
				#Calculate resultant surface radius and angular width of beam
				
				radius, theta = cr.run(Epn, height, math.sin(phi), text=False)
				
				frac = atm.runabsorption(height)
			
				eff = raweff*frac/math.sin(phi)
			
				j=0
				
				if radius > 0:
					for [xpos, ypos] in coordinates:
						r, dangle = ce.run(radius, theta, phi, epsilon, xpos, ypos, rayxpos, rayypos)
						sigcount, bkgcount= cs.run(tradius, r, rayxpos, rayypos, xpos, ypos, Epn, Z, eff)
						
						count = sigcount + bkgcount
						recorded = random.gauss(count, math.sqrt(count))
						thresholdfrac = ld.trigger()
						threshold = float(bkgcount)*thresholdfrac
	
						if float(sigcount) > float(threshold):
							j+=1
							
					if j > 0:
						fullcount[j].append(gap)
	
	plotcount = []
	labels = []
	
	edges.remove(midlim)
	
	print edges
	
	for i in range (0, 10):
		if len(fullcount[i]) > int(0):
			plotcount.append(fullcount[i])
			label = str(i)
			labels.append(label)
	n, bins, _ = ax1.hist(plotcount, label=labels, bins=edges, stacked=True)
	
	print n
	print bins

	plt.legend(loc=2)
	plt.xlabel('Grid width (m)', fontsize=20, labelpad=0)
	plt.ylabel('Count', fontsize=20, labelpad=0)
	
	ax2 = plt.subplot(212)
	
	f = 0
	for label in labels:
		if float(label) < float(4):
			fourlim = f
			
		if float(label) < float(5):
			fivelim = f
			
		if float(label) <  float(6):
			sixlim = f
		
		f += 1
	
	lines =[]
	for i in range (0,len(n)):
		if i == fourlim:
			subfourline = n[i]
			
		if i == fivelim:
			subfiveline = n[i]
			
		if i == sixlim:
			subsixline = n[i]
			
		if i == (len(n)-1):
			
			if i > fourlim:
				fourline = n[i] - subfourline
				lines.append(fourline)
	
			if i > fivelim:
				fiveline = n[i] - subfiveline
				lines.append(fiveline)
			if i > sixlim:
				sixline = n[i] - subsixline
				lines.append(sixline)

	linelabels = ["Detections > 3", "Detections > 4", "Detections > 5"]
	
	mid = (bins[1:] + bins[:-1])*0.5
	#~ print mid
	
	for k in range (0, len(lines)):
		line = lines[k]
		label = linelabels[k]
		plt.plot(mid, line, label=label)
		
	plt.legend()
	
	plt.xlabel('Grid width (m)', fontsize=20, labelpad=0)
	plt.ylabel('Count', fontsize=20, labelpad=0)
	plt.yscale('log')
	
	ax1.tick_params(labelsize=20)
	ax2.tick_params(labelsize=20)
	
	title = "Telescope Observations for " +str(numberofhours) + " hours"
	
	plt.suptitle(title, fontsize=20)

	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)	
	
	plt.savefig('graphs/stats/optimiselayout.pdf')
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/report/graphs/logenergyradius.png')
