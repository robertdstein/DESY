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

altitude = 1800

def run(eff, rowcount, mincount=4, text=False, graph=False, layout="five", number=1, nh=1):
	
	#Create a subplot for the fractional abundance

	ax1 = plt.subplot(211)
	
	#Define number of bins, maximum Epn
	
	bincount = 20
	nmax = 1
	emax = 35720
	
	Rrange = np.linspace(0, nmax, bincount)
	k = math.log(emax/232)/float(nmax)
	
	Erange=[]
	
	fullcount = []
	nDC = []
	wnDC = []
	bT = []
	wbT = []
	mT = []
	wmT = []
	
	#Iterate over Energies
	
	for R in Rrange:

		Epn = 232*(math.e**(k*R))
		
		Erange.append(Epn)
		
		weight = Epn ** (-2.7)
		
		#For a given Energy, iterate over n randomly simulated events

		for i in range (0, int(number)):
			
			#As in generate.py, randomly generate all variables (expect Epn)
			
			xpos = (random.random()*300)-150
			ypos = (random.random()*300)-150
		
			Z= 26
			
			hprob = random.random()
			height = atm.runheight(hprob, text)
		
			zenith = random.random()*44
		
			phi = math.radians(68+zenith)
		
			epsilon = math.pi*random.random()*2
			
			radius, theta = cr.run(Epn, height, math.sin(phi), text=text)
			
			#Determine what category the event was
			
			entry, entrytype = lt.run(layout, xpos, ypos, epsilon, radius, Epn, Z, height, phi, theta, mincount, eff, 1, graph=False, text=False)
			
			#append the energy value to the appropriate category
			
			if entrytype == "metThreshold":
				mT.append(Epn)
				wmT.append(weight)
			elif entrytype == "belowThreshold":
				bT.append(Epn)
				wbT.append(weight)
			elif entrytype == "nonDC":
				nDC.append(Epn)
				wnDC.append(weight)
			else:
				print "ERROR OVER HERE!!!!"
	
	#Create labels for each bin

	labels = ["metThreshold", "belowThreshold", "nonDC"]
	
	xlabels=[]
	
	for i in Erange:
		xlabels.append(int(i))
	
	Erange.append(emax + 1)
	bin_centers = 0.5 * np.diff(Erange) + Erange[:-1]
	
	limits = [Erange[0], Erange[bincount]]
	
	mweights = np.ones_like(mT)/len(mT)
	bweights=np.ones_like(bT)/len(bT)
	nDCweights=np.ones_like(nDC)/len(nDC)
	
	#Plot the histogram

	plt.hist([mT, bT, nDC], bins=Erange, log=True, histtype='bar',range=limits, label=labels)

	plt.xlim(limits)
	plt.xscale('log')
	plt.xticks(bin_centers, xlabels, rotation=90)
	plt.xlabel('Epn', labelpad=0)
	plt.ylabel('Abundance')
	plt.gca().set_ylim(bottom=0.1)
	
	#plot the histogram scaled with E^-2.7 distribution to the second subplot
	
	ax2 = plt.subplot(212)
		
	plt.hist([mT, bT, nDC], weights=[wmT, wbT, wnDC], log=True, bins=Erange, histtype='bar',range=limits, label=labels)

	plt.xlim(limits)
	plt.xscale('log')
	plt.xticks(bin_centers, xlabels, rotation=90)
	plt.xlabel('Epn', labelpad=0)
	plt.ylabel('Scaled Count')
	plt.legend()
	
	fig = plt.gcf() # get current figure
	title = 'Epn Statistics for ' + str(float(nh)*float(bincount)) + " hours"
	st = plt.suptitle(title, fontsize=20)
	st.set_y(0.98)
	fig.set_size_inches(10, 15)
	fig.tight_layout()
	fig.subplots_adjust(top=0.95)
	
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/report/graphs/energystats.png')
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/stats/energystats.pdf')
	
	plt.close()

	
	#Plot variables Etheshold and Ring Radius againist height
	
	ax3 = plt.subplot(211)
	
	rawheights=[]
	emin=[]
	rmax = []
	
	Erange = [3521, 750, 232]
	
	labels = [" = Infinity "]
	for e in Erange:
		labels.append(" = " + str(e))
		
	colors=["k", "r", "g", "m", "c", "b"]
	
	nucleonmass = 0.93827 
	
	betarange = [1.0]
	for E in Erange:
		gamma = float(E)/nucleonmass
		betarange.append(math.sqrt(1-(float(1)/(gamma**2))))
	
	print Erange
	print betarange
	
	curves=[]
	for j in range (0, len(betarange)):
		curves.append([])
		rawheights.append([])

	#Look up values from atmprofile10.csv
	
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		for row in reader:
			i +=1
			
			#Skip the first three rows
			
			if i > 3:
				
				#Loads the height and Refractive Index
				
				height = float(row[0])*1000
				ri = float(row[3]) + float(1)
				
				#Calculate the maximum Cherenkov Angle as 1/eta
				
				for j in range (0, len(betarange)):
					beta = betarange[j]
					costheta = float(1)/((float(ri))*float(beta))
					if costheta < 1:
						theta = math.acos(float(1)/((float(ri))*float(beta)))
						r = theta*(height-altitude)
						curves[j].append(r)
						rawheights[j].append(height)
				
				#Calculates the Threshold Energy using Refractive Index
				
				Ethreshold = float(cr.runemin(ri))*(10**-3)
				
				#Calculate the Maximum Ring Size, and appends these values to arrays
				
				emin.append(Ethreshold)

	for j in range (0, len(betarange)):
		print j, len(curves[j]), len(rawheights[j])
		label = "Radius (m) for E" + str(labels[j])
		ax3.plot(curves[j], rawheights[j], color = colors[j], label=label, linewidth=3.0)
	#~ plt.axhspan(19000, 26000, color='m', alpha=0.5)
	ax3.plot(emin,rawheights[0],  color='b', linewidth=3.0, label="Threshold Energy (TeV per Nucleon)")	
	
	plt.xscale('log')
	
	plt.ylabel('Height', labelpad=0)
	plt.legend(loc=3)
	
	print "Maximum Radius is", max(curves[0])
	
	ax4 = plt.subplot(212)
	
	plots = []
	weighting = []
	labels = []

	requiredfracs=np.linspace(0.6, 0.9, 3)
	
	for requiredfrac in requiredfracs:
		heights = []	
		
		probrange = []
		normweight = []
		
		stepcount = 1000
		
		lower = float(1)/float(stepcount)
		upper = float(1-lower)
		
		Rrange = np.linspace(lower, upper, stepcount)
	
		for R in Rrange:
			h = atm.runheight(1-R)
			ri = atm.runindex(h)
			thetamax = math.acos(float(1)/(float(ri)))
			rmax = thetamax * (h - altitude)
			
			if rmax > 60:
				
				rthreshold = 0.5*rmax
				
				hthreshold = 20000
				r = 120000
				
				while r > rthreshold:
					ri = atm.runindex(hthreshold)
					thetamax = math.acos(float(1)/(float(ri)))
					r = thetamax * (hthreshold - altitude)
					hthreshold += 1000
				
				requiredr = (requiredfrac*rthreshold)
	
				etrial = 250
				r = 0
				ri = atm.runindex(hthreshold)
				while r < requiredr:
					gamma = float(etrial)/nucleonmass
					beta = math.sqrt(1-(float(1)/(gamma**2)))
					costheta = float(1)/((float(ri))*beta)
					
					if costheta < 1:
						theta = math.acos(costheta)
						r = theta * (hthreshold - altitude)
					
					etrial += 100
					
			
				N = ((etrial**(-1.7)))*(float(321)/1.7)
				#~ print "For the Saturation Threshold of", etrial, "we have a probability of", N, "that an event will meet this" 
				#~ 
				#~ print "For a height", h, "rmax is", rmax, "our threshold is", rthreshold, "(and the an angle is", thetamax, ")" 
				#~ print "We examine", hthreshold, "where the max radius is", r, "and the threshold was", rthreshold
				#~ print "For beta = 1, we have", rthreshold, "we require",  requiredr, "at an energy", etrial, "we have", r
				#~ print "For a height", h, "Our Probability is", R, "that an event will reach this height or further"
				heights.append(h)
				normweight.append(N)
				
		
		label = "For half Rmax, we require r=" + str(round(requiredfrac, 2))
		labels.append(label)
		
		plots.append(heights)
		weighting.append(normweight/np.sum(normweight))
	
	plots.append(heights)
	weighting.append(np.ones(len(heights))/len(heights))
	labels.append("All Events")
	
	print len(plots), len(weighting), len(labels)	
	
	plt.hist(plots, bins=20, weights=weighting, histtype='bar', label=labels)
	
	plt.xlabel('Height', labelpad=0)
	plt.ylabel('Normalised Fraction of Events', labelpad=0)
		
	plt.legend(loc=2)
	fig = plt.gcf() # get current figure
	
	st = fig.suptitle("Threshold Energy and Cherenkov Ring Radii", fontsize=20)
	st.set_y(0.98)
	fig.set_size_inches(10, 15)
	fig.tight_layout()
	fig.subplots_adjust(top=0.95)
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/stats/logenergyradius.pdf')
	plt.savefig('/afs/desy.de/user/s/steinrob/Documents/DESY/report/graphs/logenergyradius.png')
	title = 'Epn Statistics for ' + str(float(nh)*float(bincount)) + " hours"
	plt.suptitle(title, fontsize=20)
	
	plt.savefig('graphs/stats/Energy.pdf')
	
		
	if graph:
		plt.show()

