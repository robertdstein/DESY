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
	
	ax1 = plt.subplot(221)
	
	upperlim = 200
	bincount = 10
	
	telescopegap = np.linspace(5, upperlim, bincount)
	
	simlim = (upperlim + 150)
	
	category = "lst"
					
	tradius = tr.run(category)
	
	raweff = 0.06
	selectionefficiency = 0.50
	flux = 2.0 * (10**-4)
	area = 4*(simlim**2)
	solidangle = math.radians(5)
	detectedflux = flux*area*solidangle*selectionefficiency
	rateperhour = detectedflux * 60 * 60
	n = int(rateperhour*float(numberofhours))
	
	print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
	print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 
	
	fullcount = []
	
	for i in range (0, 10):
		fullcount.append([])
	
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
	
	for i in range (0, 10):
		if len(fullcount[i]) > int(0):
			plotcount.append(fullcount[i])
			label = str(i)
			labels.append(label)
	n, bins, _ = ax1.hist(plotcount, label=labels, bins=bincount, stacked=True)
	plt.legend(loc=2)
	plt.xlabel('Grid width (m)', labelpad=0)
	plt.ylabel('Count', labelpad=0)
	
	ax2 = plt.subplot(222)
	
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
	print mid
	
	for k in range (0, len(lines)):
		line = lines[k]
		label = linelabels[k]
		plt.plot(mid, line, label=label)
		
	plt.legend()
	
	plt.xlabel('Grid width (m)', labelpad=0)
	plt.ylabel('Count', labelpad=0)
	
	title = "Telescope Observations for " +str(numberofhours) + " hours"
	
	plt.suptitle(title, fontsize=20)
	
	ax3 = plt.subplot(223)
	
	upperlim = 44
	bincount = 30
	
	telescopegap = np.linspace(14, upperlim, bincount)
	
	simlim = (upperlim + 150)
	
	area = 4*(simlim**2)
	detectedflux = flux*area*solidangle*selectionefficiency
	rateperhour = detectedflux * 60 * 60
	n = int(rateperhour*float(numberofhours))
	
	print time.asctime(time.localtime()),"Cosmic Ray Iron Flux is", flux, "Simulated Area is", area, "Field of View is", solidangle, "Detected Flux is", detectedflux
	print time.asctime(time.localtime()),"Rate per hour", rateperhour, "Simulated Hours", numberofhours, "Simulated Events", n 
	
	fullcount = []
	
	for i in range (0, 10):
		fullcount.append([])
	
	for gap in telescopegap:
		
		specificcount = []
		
		coordinates = []
		points = np.linspace(-gap, gap, 3)
		
		for x in points:
			for y in points:
				coordinates.append([x,y])
		
		for i in range (0,n):
			
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
	
	for i in range (0, 10):
		if len(fullcount[i]) > int(0):
			plotcount.append(fullcount[i])
			label = str(i)
			labels.append(label)
	n, bins, _ = ax3.hist(plotcount, label=labels, bins=(bincount), stacked=True)
	plt.legend(loc=2)
	plt.xlabel('Grid width (m)', labelpad=0)
	plt.ylabel('Count', labelpad=0)
	
	ax4 = plt.subplot(224)
	
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
	print mid
	
	for k in range (0, len(lines)):
		line = lines[k]
		label = linelabels[k]
		ax4.plot(mid, line, label=label)
		
	plt.legend()
	
	plt.xlabel('Grid width (m)', labelpad=0)
	plt.ylabel('Count', labelpad=0)
	
	plt.gca().set_ylim(bottom=0)
	
	title = "Telescope Observations for " +str(numberofhours) + " hours"
	
	plt.suptitle(title, fontsize=20)

	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)	
	
	plt.savefig('graphs/stats/optimiselayout.pdf')
