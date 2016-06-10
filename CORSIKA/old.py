import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc
from scipy.optimize import curve_fit

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="56tev-lpd")

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/')
import cherenkovradius as cr

cfg = parser.parse_args()

hess1rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess1signalregressor.p'
hess2rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess2signalregressor.p'
if os.path.isfile(hess1rgrpath):
	hess1rgr = pickle.load(open(hess1rgrpath, "r"))
else:
	print "No hess1 pickle!"
if os.path.isfile(hess2rgrpath):
	hess2rgr = pickle.load(open(hess2rgrpath, "r"))
else:
	print "No hess2 pickle!"
	
signalbdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/signalBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		signalbdtvariables.append(row[0])
print signalbdtvariables

minmultiplicity=3

def makeBDTentry(pixelentry):
	bdtentry =[]
	for variable in signalbdtvariables:
		varsplit = variable.split('.')
		suffix = pixelentry
		if len(varsplit) > 1:
			for name in varsplit[:-1]:
				 suffix = getattr(suffix, name)
			varname = varsplit[-1]
		else:
			varname = variable
		if hasattr(suffix, varname):
			newval = getattr(suffix, varname)
			bdtentry.append(newval)
		else:
			return None
	return bdtentry


filepath = "/nfs/astrop/d6/rstein/data/"

j=200
i=0

accepteddistances=[[],[]]
signals=[[],[]]
rgrsignals=[[],[]]
rgrdiffs=[[],[]]
simplediffs=[[],[]]
truesignals1=[[],[]]
truesignals2=[[],[]]
truedistances=[[],[]]
rejecteddistances=[[],[]]
rejectedrgrsignals=[[],[]]

cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()
arcut = ic.runar()

targetfolder = filepath + cfg.jobID +"/"

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar
custom_options = {
	'end': 100,
	'width': 100,
	'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

p = ProgressBar(**custom_options)
print p

hessstatus=[False, False]
if os.path.isfile(hess1picklepath):
	hessstatus[0] = True
if os.path.isfile(hess2picklepath):
	hessstatus[1] = True
if not os.path.isfile(hess1picklepath) and not os.path.isfile(hess2picklepath):
	raise Exception("No BDT saved, so no results to plot!")

while (i < j):
	targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
	if (os.path.isfile(targetpath)):
		event = pickle.load(open(targetpath, 'rb'))
		if hasattr(event.simulations, "DC") and hasattr(event.simulations, "full"):
			DCsim =event.simulations.DC
			fullsim = event.simulations.full
			
			IDs=[]
			
			for index in DCsim.triggerIDs:
				fulltel =  fullsim.images[index]

				if fulltel.BDTID != None:
					fullBDT = fulltel.getBDTpixel()
								
					simplecandidatesignal = fullBDT.channel1.intensity -fullBDT.nnmean
					
					if float(ucut) > float(fullBDT.bdtscore) > float(cut):
						if float(simplecandidatesignal) > float(signalcut):
							if float(fulltel.hillas.aspect_ratio_) > arcut:
								IDs.append(index)
			
			if len(IDs) > 0:
				for index in DCsim.triggerIDs:
					DCtel = DCsim.images[index]
					fulltel =  fullsim.images[index]
					trueID = DCtel.trueDC
					DCpixel = DCtel.gettruepixel()
						
					if fulltel.size == "HESS1":
						plotindex = 0
					elif fulltel.size == "HESS2":
						plotindex = 1
					else:
						raise Exception("Telescope.size error, size is " +fulltel.size)
					

					if fulltel.BDTID != None:
						fullBDT = fulltel.getBDTpixel()
									
						simplecandidatesignal = (fullBDT.channel1.intensity -fullBDT.nnmean)
	
						bdtentry = makeBDTentry(fullBDT)
						if (fulltel.size=="HESS1") and (bdtentry != None):
							candidatesignal = hess1rgr.predict([bdtentry])[0]/fulltel.mirrorarea
						elif (fulltel.size=="HESS2") and (bdtentry != None):
							candidatesignal = hess2rgr.predict([bdtentry])[0]/fulltel.mirrorarea
						elif bdtentry == None:
							candidatesignal = 0
							
						truedistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
						truesignals1[plotindex].append(DCtel.hillas.image_size_amplitude_/fulltel.mirrorarea)
						truesignals2[plotindex].append(DCpixel.channel1.intensity/fulltel.mirrorarea)
							
						if (float(ucut) > float(fullBDT.bdtscore) > float(cut)) and (float(simplecandidatesignal) > float(signalcut)) and (float(fulltel.hillas.aspect_ratio_) > arcut):						
							accepteddistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							signals[plotindex].append(simplecandidatesignal/fulltel.mirrorarea)
							rgrsignals[plotindex].append(candidatesignal)
						else:
							rejecteddistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							rejectedrgrsignals[plotindex].append(candidatesignal)


	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

areas = [108., 614.]

mindensity = 0.1
height = 25000

for i in [0, 1]:
	print "HESS"+str(i+1)
	energy = float(cfg.jobID[:cfg.jobID.find("tev-lpd")])
	epn=1000 * energy/56
	print energy, "TeV", epn, "GeV per nucleon"
	print height, "m"
	rmax , theta = cr.run(epn, height, 1, fit="exp")
	print rmax, "m"
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 20)
	sqarea = math.sqrt(areas[i])
	
	ax1=plt.subplot(5,1,1)
	
	plt.scatter(truedistances[i], truesignals1[i])
	plt.xlabel("Core distance to telescope (m)")
	plt.ylabel("Photoelectron Density (m^-2)")
	ax1.set_xlim(left=0)
	ax1.set_ylim(bottom=mindensity)
	ax1.set_yscale("log")
	plt.title("True LPD (Amplitude)")
	
	d=[]
	s=[]
	
	expd=[]
	exps=[]
	lind=[]
	lins=[]
	extrad = []
	extras=[]
	
	for k in range(len(truedistances[i])):
		value = truedistances[i][k]
		expval = truesignals1[i][k]
		if value < rmax:	
			d.append(value)
			s.append(expval)
		elif value > rmax:
			extrad.append(value)
			extras.append(math.log(expval))
				
	def f1(x, p1, p2, p3, p4):
		if x < rmax:
			return p1*np.exp(p2*x) + p3
		else:
			return (p1*np.exp(p2*rmax) + p3)*np.exp(p4*(x-rmax))
			
	vf1 = np.vectorize(f1)
	p0=[3.8, 0.015, -4.7, -0.06]

	popt, pcov = curve_fit(vf1, np.array(d), np.array(s), p0=np.array(p0), maxfev = 100000000)
	print popt

	def fit(x):
		return vf1(x, popt[0], popt[1], popt[2], popt[3])
	
	truesigmas=[]
	datasets = [[d, s], [extrad, extras]]
	
	alldistances=[]
	lpd=[]
	u=[]
	l=[]
	pu =[]
	pl = []
	
	for m in range(len(datasets)): 
		
		data = datasets[m]
		distances = data[0]
		newsignals=data[1]
	
		diffs = []
		
		for n in range(len(newsignals)):
			sig = newsignals[n]
			dist = distances[n]
			fitsig = fit(dist)
			if fitsig > mindensity:
				diff = math.fabs((sig-fitsig)/fitsig)
				diffs.append(diff)
	
		diffs.sort()
		nentries = len(diffs)
		if nentries > 3:
			halfinteger = int(0.5*nentries)
			lowerinteger = int(0.16*nentries)
			upperinteger = int(0.84*nentries)
			integer68 = int(0.68*nentries)
			
			lower = diffs[lowerinteger]
			upper = diffs[upperinteger]
			
			truesigmas.append(diffs[integer68])
			print "Actual", truesigmas[m], "possonian", 
			
			distances.sort()
			psigmas = []
			for dist in distances:
				sig = fit(dist)
				if sig > mindensity:
					lpd.append(sig)
					ulpd = sig*(1+truesigmas[m])
					u.append(ulpd)
					llpd = sig*(1-truesigmas[m])
					l.append(llpd)
					up = sig + (math.sqrt(sig)/sqarea)
					pu.append(up)
					lp = sig - (math.sqrt(sig)/sqarea)
					pl.append(lp)
					psigmas.append(1./(sqarea*math.sqrt(sig)))
					alldistances.append(dist)
		
			psigmas.sort()
			psigma = psigmas[integer68]
			print psigma
		else:
			print "Nentries < 3"
		
	plt.plot(alldistances, lpd, color='k')
	plt.fill_between(alldistances, l, u, color='g', alpha=0.25)
	ax1.fill_between(alldistances, pl, pu, color='r', alpha=0.25)
	fd = mpatches.Rectangle((0, 0), 1, 1, fc="g",alpha=0.25)
	pd = mpatches.Rectangle((0, 0), 1, 1, fc="r",alpha=0.25)
	
	figure.legend([fd, pd], ["Fractional Deviation from True Fit","Expected Poissonian Error"], loc="upper right")
			
	truesigma=truesigmas[0]
	
	for j in range(0,4):
		
		sigset = [truesignals2, signals, rgrsignals, rejectedrgrsignals][j]
		diffname = ["True LPD (Max Intensity)", "Simple Estimate LPD", "Regressor Estimate LPD", "REJECTED"][j]
		
		print diffname,
		
		if diffname == "REJECTED":
			pdist=rejecteddistances[i]
			plot=True
		elif diffname == "True LPD (Max Intensity)":
			pdist=truedistances[i]
			plot=True
		else:
			pdist=accepteddistances[i]
			plot=True
		
		fitdistances=[]
		fitsignals=[]
		for l in range(len(sigset[i])):
			dist = pdist[l]
			if dist < rmax:
				sig = sigset[i][l]
				fitdistances.append(dist)
				fitsignals.append(sig)
		
		def vf(x, scale):
			return fit(x) * scale
			
		newpopt, pcov = curve_fit(vf, np.array(fitdistances), np.array(fitsignals), maxfev = 100000000)
			
		print "Fitted LPD scale:", newpopt
		
		def scaledlpd(x):
			#~ return vf(x, newpopt[0])
			return vf(x, 1)
		
		alldiffs=[[],[]]
		allfracdiffs=[[],[]]
		for l in range(len(fitsignals)):
			sig = sigset[i][l]
			dist = pdist[l]
			fitsig = scaledlpd(dist)
			if fitsig > mindensity:	
				diff = (sig-fitsig)
				fracdiff=math.fabs((sig-fitsig)/fitsig)	
				if dist < rmax:
					alldiffs[0].append(diff)
					allfracdiffs[0].append(fracdiff)
				else:
					alldiffs[1].append(diff)
					allfracdiffs[1].append(fracdiff)
			
					
		print len(sigset[i]), len(alldiffs[0]), len(alldiffs[1])			
		
		fracsigmas=[]
		
		for m in range (len(alldiffs)):
			#~ print "Making fracdiff", m,
			diffs = alldiffs[m]
			fracdiffs=allfracdiffs[m]
			diffs.sort()
			fracdiffs.sort()
			nentries = len(diffs)
			if nentries > 3:
				halfinteger = int(0.5*nentries)
				lowerinteger = int(0.16*nentries)
				upperinteger = int(0.84*nentries)
				integer68 = int(0.68*nentries)
				
				lower = diffs[lowerinteger]
				upper = diffs[upperinteger]
				
				sigma = 0.5*(upper-lower)
				
				fracsigma=fracdiffs[integer68]
				fracsigmas.append(fracsigma)
				
				#~ print m, diffname, lower, diffs[halfinteger], diffs[integer68], upper, sigma, fracsigma, 
				
				#~ if fracsigma > truesigmas[m]:
					#~ effsigma = math.sqrt(fracsigma**2 - truesigmas[m]**2)
					#~ print effsigma
				#~ else:
					#~ print ""
			else:
				print "nentries < 3"
		
		print fracsigmas
		
		if plot:
			ax=plt.subplot(5,1,j+2, sharex=ax1, sharey=ax1)
			
			plt.scatter(pdist, sigset[i])
			
			currentlpd=[]
			currentdistances=[]
			u=[]
			l=[]
			pdist.sort()
						
			for dist in alldistances:
				sig = scaledlpd(dist)
				if sig > mindensity:
					currentlpd.append(sig)
					currentdistances.append(dist)
					
					if (dist > rmax) and len(fracsigmas)> 1:
						fracsigma=fracsigmas[1]
					else:
						fracsigma=fracsigmas[0]
					
					llpd = sig*(1-fracsigma)
					if llpd < 0:
						llpd=mindensity
					ulpd = sig*(1+fracsigma)
	
					l.append(llpd)
					u.append(ulpd)
					
		
			plt.plot(alldistances, lpd, color='k')
			plt.fill_between(alldistances, l, u, color='g', alpha=0.25)
			ax.fill_between(alldistances, pl, pu, color='r', alpha=0.25)
			
			plt.xlabel("Core distance to telescope (m)")
			plt.ylabel("Photoelectron Density (m^-2)")
			ax.set_xlim(left=0)
			ax.set_ylim(bottom=mindensity)
			plt.title(diffname)
			plt.annotate("Scale:" + str('{0:.2f}'.format(newpopt[0])), xy=(0.8, 0.9), xycoords="axes fraction",  fontsize=15)

	saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/lpd" + str(i+1)+ ".pdf"
	
	print "Saving to", saveto
	
	plt.tight_layout()
	
	plt.savefig(saveto)
	plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/corsikalpd" + str(i+1)+ ".pdf")
	plt.close()
	
