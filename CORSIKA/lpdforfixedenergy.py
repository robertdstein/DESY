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
parser.add_argument("-jid", "--jobID", default="56tev-lpdfull")

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/')
import cherenkovradius as cr
import lightdensity as ld

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

def makesmearBDTentry(pixelentry):
	bdtentry =[]
	for variable in signalbdtvariables:
		varsplit = variable.split('.')
		suffix = pixelentry
		if len(varsplit) > 1:
			for name in varsplit[:-1]:
				if hasattr(suffix, name):
					suffix = getattr(suffix, name)
				else:
					return None
			varname = varsplit[-1]
		else:
			varname = variable
		if hasattr(suffix, varname):
			newval = getattr(suffix, varname)
			if varname == "energy":
				randomfrac = np.random.normal(1, 0.11)
				smearval = randomfrac * newval
				bdtentry.append(smearval)
			elif varname == "core_distance_to_telescope":
				smearval = np.random.normal(newval, 10)
				bdtentry.append(smearval)
			else:
				bdtentry.append(newval)
		else:
			return None
	return bdtentry


filepath = "/nfs/astrop/d6/rstein/data/"

j=2000
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
heights =[[],[]]
rejectedheights=[[],[]]

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
			
			if len(IDs) > 3:
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
						bdtentry = makesmearBDTentry(fullBDT)
						if (fulltel.size=="HESS1") and (bdtentry != None):
							candidatesignal = hess1rgr.predict([bdtentry])[0]
						elif (fulltel.size=="HESS2") and (bdtentry != None):
							candidatesignal = hess2rgr.predict([bdtentry])[0]
						elif bdtentry == None:
							candidatesignal = 0
													
						if (float(ucut) > float(fullBDT.bdtscore) > float(cut)) and (float(simplecandidatesignal) > float(signalcut)) and (float(fulltel.hillas.aspect_ratio_) > arcut):
							truedistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							truesignals1[plotindex].append(DCtel.hillas.image_size_amplitude_/fulltel.mirrorarea)
							truesignals2[plotindex].append(DCpixel.channel1.intensity/fulltel.mirrorarea)						
							accepteddistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							signals[plotindex].append(simplecandidatesignal/fulltel.mirrorarea)
							rgrsignals[plotindex].append(candidatesignal)
							heights[plotindex].append(DCtel.hillas.Hmax_)
						else:
							rejecteddistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							rejectedrgrsignals[plotindex].append(candidatesignal)
							rejectedheights[plotindex].append(DCtel.hillas.Hmax_)


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
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 20)
	sqarea = math.sqrt(areas[i])
	
	ax1=plt.subplot(5,1,1)
	
	plt.xlabel("Core distance to telescope (m)")
	plt.ylabel("Photoelectron Density (m^-2)")
	ax1.set_xlim(left=0)
	ax1.set_ylim(bottom=mindensity)
	ax1.set_yscale("log")
	plt.title("True LPD (Amplitude)")
	
	d=[]
	s=[]
	logs=[]
	h=[]
	
	expd=[]
	exps=[]
	lind=[]
	lins=[]
	extrad = []
	extras=[]
	logextras=[]
	extrah = []
	
	for k in range(len(truedistances[i])):
		value = truedistances[i][k]
		expval = truesignals1[i][k]
		height=heights[i][k]
		rmax , theta = cr.run(epn, height, 1, fit="exp")
		if value < (rmax):	
			d.append(value)
			s.append(expval)
			logs.append(math.log(expval))
			h.append(height)
		else:
			extrad.append(value)
			extras.append(expval)
			logextras.append(math.log(expval))
			extrah.append(height)
			
	plt.scatter(d, s, color="k")
	plt.scatter(extrad, extras, color="red")

			
	#~ extraA, extralogC = np.polyfit(extrad, logextras, 1)
	#~ extraC = math.exp(extralogC)
	#~ print extraA, extralogC, extraC
			
	def f1(x, p1, p2, p3):
		return p1*np.exp(p2*x) + p3

	vf1 =np.vectorize(f1)
	p0=[3.8, 0.015, -4.7]

	popt, pcov = curve_fit(vf1, np.array(d), np.array(s), p0=np.array(p0), maxfev = 100000000)
	print popt
	
	def fit(x):
		return popt[0]*np.exp(popt[1]*x) + popt[2]
	
	vfit = np.vectorize(fit)

	p4s=[]
	for k in range(len(truedistances[i])):
		value = truedistances[i][k]
		expval = truesignals1[i][k]
		height=heights[i][k]
		rmax , theta = cr.run(epn, height, 1, fit="exp")
		if value > (rmax):
			deltar = value-rmax
			expected = math.log(fit(value))
			deltai = math.log(expval)-expected
			gradient = deltai/deltar
			p4s.append(gradient)
		
	p4 = np.mean(p4s)	
	print "Mean p4", p4
	
	Line = "y1(x) =" + str('{0:.3f}'.format(popt[0])) + " e ^ ("+ str('{0:.3f}'.format(popt[1]))+"x) + " + str('{0:.3f}'.format(popt[2])) + "\n"
	Line += "y2(x) = y1(rmax) * e ^ ("+ str('{0:.3f}'.format(p4))+"(x - rmax))"
	print Line
	plt.annotate(Line, xy=(0.05, 0.8), xycoords="axes fraction",  fontsize=15)
	
	def f2(x, rmax):
		return vfit(rmax)*np.exp(p4*(x-rmax))
		
	def fullfit(x, rmax):
		if x > (rmax):
			return f2(x, rmax)
		else:
			return fit(x)
	
	truesigmas=[]
	datasets = [[d, s, h], [extrad, extras, extrah]]
	colors=["green", None]
	
	alldistances=[]
	
	for m in range(len(datasets)): 
		
		data = datasets[m]
		distances = data[0]
		newsignals=data[1]
		currentheights=data[2]
		fillcolor=colors[m]
	
		diffs = []
		lpd=[]
		u=[]
		l=[]
		pu =[]
		pl = []
		
		for n in range(len(newsignals)):
			sig = newsignals[n]
			dist = distances[n]
			height = currentheights[n]
			rmax , theta = cr.run(epn, height, 1, fit="exp")
			fitsig = fullfit(dist, rmax)
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
			if fillcolor != None:
				ax1.fill_between(distances, l, u, color=fillcolor, alpha=0.25)
				ax1.fill_between(distances, pl, pu, color='r', alpha=0.25)
				plt.plot(distances, lpd, color='k')
		else:
			print "Nentries < 3"
		
	
	fd = mpatches.Rectangle((0, 0), 1, 1, fc="g",alpha=0.25)
	pd = mpatches.Rectangle((0, 0), 1, 1, fc="r",alpha=0.25)
	
	figure.legend([fd, pd], ["Fractional Deviation from True Fit","Expected Poissonian Error"], loc="upper right")
	
	message = "Sigma 1: " + str('{0:.2f}'.format(truesigmas[0])) + " \n"
	if len(truesigmas) > 1:
		message += "Sigma 2: " + str('{0:.2f}'.format(truesigmas[1])) + " \n"
	plt.annotate(message, xy=(0.9, 0.6), xycoords="axes fraction",  fontsize=15)
	
	for j in range(0,4):
		ax=plt.subplot(5,1,j+2, sharex=ax1, sharey=ax1)
		sigset = [truesignals2, signals, rgrsignals, rejectedrgrsignals][j]
		diffname = ["True LPD (Max Intensity)", "Simple Estimate LPD", "Regressor Estimate LPD", "REJECTED"][j]
		
		print diffname,
		
		if diffname == "REJECTED":
			pdist=rejecteddistances[i]
			plot=True
			h=rejectedheights[i]
		elif diffname == "True LPD (Max Intensity)":
			pdist=truedistances[i]
			h=heights[i]
			plot=True
		else:
			pdist=accepteddistances[i]
			h=heights[i]
			plot=True
			
		fitd=[]
		fits=[]
		fith=[]
		fitlogs=[]
		
		extrad=[]
		extras=[]
		extrah=[]
			
		
		for l in range(len(sigset[i])):
			dist = pdist[l]
			sig = sigset[i][l]
			height=h[l]
			rmax , theta = cr.run(epn, height, 1, fit="exp")
			if sig > mindensity:
				if dist < rmax:	
					fitd.append(dist)
					fits.append(sig)
					fitlogs.append(math.log(sig))
					fith.append(height)
				else:
					extrad.append(value)
					extras.append(expval)
					extrah.append(height)
				
		if len(fitd) > 0:
			
			if (diffname != "Regressor Estimate LPD") and (diffname != "REJECTED"):
			
				def f1(x, p1, p2, p3):
					return p1*np.exp(p2*x) + p3
			
				vf1 = np.vectorize(f1)
				p0=[3.8, 0.015, -4.7]
			
				popt, pcov = curve_fit(vf1, np.array(fitd), np.array(fits), p0=np.array(p0), maxfev = 100000000)
				print popt
				
				def fit(x):
					return vf1(x, popt[0], popt[1], popt[2])
				
				vfit = np.vectorize(fit)
			
				p4s=[]
				for k in range(len(pdist)):
					value = pdist[k]
					expval = sigset[i][k]
					height=h[k]
					rmax , theta = cr.run(epn, height, 1, fit="exp")
					if value > (rmax):
						deltar = value-rmax
						expected = math.log(fit(value))
						deltai = math.log(expval)-expected
						gradient = deltai/deltar
						p4s.append(gradient)
					
				p4 = np.mean(p4s)	
				print "Mean p4", p4
				
				Line = "y1(x) =" + str('{0:.3f}'.format(popt[0])) + " e ^ ("+ str('{0:.3f}'.format(popt[1]))+"x) + " + str('{0:.3f}'.format(popt[2])) + "\n"
				Line += "y2(x) = y1(rmax) * e ^ ("+ str('{0:.3f}'.format(p4))+"(x - rmax))"
				print Line
				plt.annotate(Line, xy=(0.05, 0.8), xycoords="axes fraction",  fontsize=15)
				
				def f2(x, rmax):
					return vfit(rmax)*np.exp(p4*(x-rmax))
					
			else:
				truep2, truep3, truep4 = ld.pcoeffs()
				print "true p3 is", truep3
	
				def f1(x, p1):
					val = p1*np.exp(truep2*x) + truep3
					if val > 0:
						return math.log(val)
					else:
						return 0.0001
			
				#~ vf1 = np.vectorize(f1)
				#~ p0=[3.8, 6]
			#~ 
				#~ popt, pcov = curve_fit(vf1, np.array(fitd), np.array(fitlogs), p0=np.array(p0), maxfev = 100000000)
				#~ print popt
				
				Avals = []
				
				for l in range(len(fits)):
					sig = fits[l]
					dist = fitd[l]
					yminusc = sig - truep3
					Aval = yminusc * np.exp(-truep2 * dist)
					Avals.append(Aval)
					#~ print "sig", sig,"dist", dist, "y - c", yminusc,"A", Aval
					
				newp1 = np.mean(Avals)
				
				print "Aval", newp1
				
				def fit(x):
					return newp1*np.exp(truep2*x) + truep3
				
				vfit = np.vectorize(fit)
				
				Line = "y1(x) =" + str('{0:.3f}'.format(newp1)) + " e ^ ("+ str('{0:.3f}'.format(truep2))+"x) + " + str('{0:.3f}'.format(truep3)) + "\n"
				Line += "y2(x) = y1(rmax) * e ^ ("+ str('{0:.3f}'.format(truep4))+"(x - rmax))"
				print Line
				plt.annotate(Line, xy=(0.05, 0.8), xycoords="axes fraction",  fontsize=15)
				
				def f2(x, rmax):
					return vfit(rmax)*np.exp(truep4*(x-rmax))
				
				
			def fullfit(x, rmax):
				if x > (rmax):
					return f2(x, rmax)
				else:
					return fit(x)
				
			plt.scatter(fitd, fits, color="k")
			plt.scatter(extrad, extras, color="red")
			
			#~ def vf(x, scale):
				#~ return np.log(fit(x)) * scale
				#~ 
			#~ newpopt, pcov = curve_fit(vf, np.array(fitd), np.array(fitlogs), maxfev = 100000000)
				#~ 
			#~ print "Fitted LPD scale:", newpopt
			#~ 
			#~ def scaledlpd(x, rmax):
				#~ return newpopt[0]*fullfit(x,rmax)
				
			def scaledfit(x):
				return fit(x)
				
			def scaledlpd(x, rmax):
				return fullfit(x, rmax)
				
			
			datasets = [[fitd, fits, fith], [extrad, extras, extrah]]
			colors=["green", None]
		
			alldistances=[]
			truesigmas=[]
			
				
			for m in range(len(datasets)): 
				data = datasets[m]
				distances = data[0]
				newsignals=data[1]
				currentheights=data[2]
				fillcolor=colors[m]
			
				if len(distances) > 0:
			
					diffs = []
					
					for n in range(len(newsignals)):
						sig = newsignals[n]
						dist = distances[n]
						height = currentheights[n]
						rmax , theta = cr.run(epn, height, 1, fit="exp")
						fitsig = scaledlpd(dist, rmax)
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
						truesigma = diffs[integer68]
						
						truesigmas.append(truesigma)
						print "Actual", truesigma, "possonian", 
						
						distances.sort()
						alldistances=[]
						lpd=[]
						u=[]
						l=[]
						pu =[]
						pl = []
						psigmas = []
						for dist in distances:
							sig = scaledfit(dist)
							if sig > mindensity:
								lpd.append(sig)
								ulpd = sig*(1+truesigma)
								u.append(ulpd)
								llpd = sig*(1-truesigma)
								if llpd > 0:
									l.append(llpd)
								else:
									l.append(0.01)
								up = sig + (math.sqrt(sig)/sqarea)
								pu.append(up)
								lp = sig - (math.sqrt(sig)/sqarea)
								pl.append(lp)
								psigmas.append(1./(sqarea*math.sqrt(sig)))
								alldistances.append(dist)
					
						psigmas.sort()
						psigma = psigmas[integer68]
						print psigma
						if fillcolor != None:
							ax.fill_between(alldistances, l, u, color=fillcolor, alpha=0.25)
							ax.fill_between(alldistances, pl, pu, color='r', alpha=0.25)
							plt.plot(alldistances, lpd, color='k')
					
			plt.xlabel("Core distance to telescope (m)")
			plt.ylabel("Photoelectron Density (m^-2)")
			ax.set_xlim(left=0)
			ax.set_ylim(bottom=mindensity)
			plt.title(diffname)
			message=""
			#~ message = "Scale: " + str('{0:.2f}'.format(newpopt[0])) + " \n"
			if truesigmas != []:
				message += "Sigma 1: " + str('{0:.2f}'.format(truesigmas[0])) + " \n"
				if len(truesigmas) > 1:
					message += "Sigma 2: " + str('{0:.2f}'.format(truesigmas[1])) + " \n"
			plt.annotate(message, xy=(0.9, 0.7), xycoords="axes fraction",  fontsize=15)
			#~ print truedistances[i]
			#~ print len(truedistances[0])

	saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/lpd" + str(i+1)+ ".pdf"
	
	print "Saving to", saveto
	
	plt.tight_layout()
	
	plt.savefig(saveto)
	plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/corsikalpd" + str(i+1)+ ".pdf")
	plt.close()


