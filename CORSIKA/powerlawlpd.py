import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc
from scipy.optimize import curve_fit

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

data=np.arange(36, 57, 10)
print data

nrows = len(data)-int(len(data)/2)
print nrows


areas = [108., 614.]

mindensity = 0.1
height = 25000

filepath = "/nfs/astrop/d6/rstein/data/"


cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()
arcut = ic.runar()



sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar
custom_options = {
	'end': 100,
	'width': 100,
	'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

for k in range(4):
	
	Cvalues=[]
	sigmas=[]

	Avalues=[]
	Aerrors=[]
	
	hmax=[]

	Cdeviation =[]

	for energy in data:
		jobID= str(energy) + "tev-lpdfull"
		targetfolder = filepath + jobID +"/"
		truesignals1=[[],[]]
		truedistances=[[],[]]
		hcurrent=[]
		hdist=[]
		hsigs=[]
		energyindex = int((energy-26)/10)
		p = ProgressBar(**custom_options)
		print p
		j=20
		i=0
		

		
		if k == 0:
			gradient = -0.0095
		else:
			gradient = Afit(energy)
		
		while (i < j):
			targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
			if (os.path.isfile(targetpath)):
				event = pickle.load(open(targetpath, 'rb'))
				if hasattr(event.simulations, "DC") and hasattr(event.simulations, "full"):
					DCsim =event.simulations.DC
					fullsim = event.simulations.full
					
					IDs=0
					interactionheight=None
				
					for fulltel in fullsim.images:	
						if fulltel.BDTID != None:
							fullBDT = fulltel.getBDTpixel()
										
							simplecandidatesignal = fullBDT.channel1.intensity -fullBDT.nnmean
							
							if float(ucut) > float(fullBDT.bdtscore) > float(cut):
								if float(simplecandidatesignal) > float(signalcut):
									if float(fulltel.hillas.aspect_ratio_) > arcut:
										IDs+=1
					
					if DCsim.triggerIDs != []:
						DCtel = DCsim.gettriggeredtelescope(0)
						if hasattr(DCtel.hillas, "Hmax_"):
							interactionheight = float(DCtel.hillas.Hmax_)
									
					if IDs > 0:
		
						for l in range(len(fullsim.images)):
							fulltel	= fullsim.images[l]
							
							if fulltel.size == "HESS1":
								plotindex = 0
							elif fulltel.size == "HESS2":
								plotindex = 1
							else:
								raise Exception("Telescope.size error, size is " +fulltel.size)
			
							truedistances[plotindex].append(fulltel.hillas.core_distance_to_telescope)
							truesignals1[plotindex].append(fulltel.hillas.image_size_amplitude_/fulltel.mirrorarea)
							
							if interactionheight != None:
								hsigs.append(fulltel.hillas.image_size_amplitude_/fulltel.mirrorarea)
								hdist.append(fulltel.hillas.core_distance_to_telescope)
								hcurrent.append(interactionheight)
		
			if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
				print p+1
			i+=1
			
		if k==2:
			print "hmax", hcurrent
			for n in range(len(hdist)):
				sig = hsigs[n]
				dist = hdist[n]
				fitsig = fit(dist)
				diff = (sig-fitsig)/fitsig
				Cdeviation.append(diff)
			
			hmax.extend(hcurrent)
			
			print "Len(hcurrent)", len(hcurrent), "Len(Hmax)", len(hmax), "Len(Cdev)", len(Cdeviation)
			
			
		
		for index in [0]:
			print "HESS"+str(index+1)
			epn=1000 * energy/56
			print energy, "TeV", epn, "GeV per nucleon"
			print height, "m"
			
			s=[]
			sigs=[]
		
			for l in range(len(truedistances[index])):
				value = truedistances[index][l]
				expval = truesignals1[index][l]
				logval = math.log(expval)
				diffval = logval-(gradient*value)
				s.append(diffval)
				sigs.append(logval)
				
			if k==0:			
				[A, logC], cov = np.polyfit(x=truedistances[index], y=sigs, deg=1, cov=True)
				C = math.exp(logC)
				Avar = math.sqrt(cov[0][0])
				print A, logC, C, C/(energy**2), cov, Avar
				
				Avalues.append(A)
				Aerrors.append(Avar)
			
			elif k==1:
				logC=np.mean(s)
				C = np.exp(logC)
				print logC, C, C/(energy**2)
				
				Cvalues.append(C)
				
			elif k > 1:
				C = Cfit(energy)
				
				
			if k > 0:
				if k ==3:
					ax=plt.subplot(nrows,2,energyindex)
					plt.scatter(truedistances[index], truesignals1[index])	
				
				def fit(x):
					return C*np.exp(x*gradient)
					
				lpd=[]
				u=[]
				l=[]
				pu =[]
				pl = []
			
				diffs = []
				alldistances=[]
				
				sqarea = math.sqrt(areas[index])
				
				for n in range(len(truedistances[index])):
					sig = truesignals1[index][n]
					dist = truedistances[index][n]
					fitsig = fit(dist)
					diff = math.fabs((sig-fitsig)/fitsig)
					diffs.append(diff)
			
				diffs.sort()
				print diffs
				nentries = len(diffs)
				distances=truedistances[index]
				distances.sort()
				if nentries > 3:
					halfinteger = int(0.5*nentries)
					lowerinteger = int(0.16*nentries)
					upperinteger = int(0.84*nentries)
					integer68 = int(0.68*nentries)
					
					lower = diffs[lowerinteger]
					upper = diffs[upperinteger]
					
					truesigma = diffs[integer68]
					fiterror= truesigma*C
					sigmas.append(fiterror)
					print "Actual", truesigma, "possonian", 
		
					psigmas = []
					for dist in distances:
						sig = fit(dist)
						lpd.append(sig)
						ulpd = sig*(1+truesigma)
						u.append(ulpd)
						llpd = sig*(1-truesigma)
						l.append(llpd)
						up = sig + (math.sqrt(sig)/sqarea)
						pu.append(up)
						lp = sig - (math.sqrt(sig)/sqarea)
						pl.append(lp)
						psigmas.append(1./(sqarea*math.sqrt(sig)))
				
					psigmas.sort()
					psigma = psigmas[integer68]
					print psigma, "Fiterror", fiterror
					
					
					if k ==3:
					
						plt.plot(distances, lpd, color='k')
						plt.fill_between(distances, l, u, color='g', alpha=0.25)
						ax.fill_between(distances, pl, pu, color='r', alpha=0.25)
						message = "Sigma: " + str('{0:.2f}'.format(truesigma)) + " \n"
						plt.annotate(message, xy=(0.6, 0.8), xycoords="axes fraction",  fontsize=15)
						fd = mpatches.Rectangle((0, 0), 1, 1, fc="g",alpha=0.25)
						pd = mpatches.Rectangle((0, 0), 1, 1, fc="r",alpha=0.25)
						
						figure = plt.gcf() # get current figure
						figure.set_size_inches(20, 20)
						figure.legend([fd, pd], ["Fractional Deviation from True Fit","Expected Poissonian Error"], loc="upper right")
					
						title= str(energy)+ " TeV HESS " + str(index+1)
						plt.title(title)
						
						print len(truedistances[index]), "points"
						print truedistances[index], truesignals1[index]
						
						
						plt.xlabel("Core distance to telescope (m)")
						plt.ylabel("Photoelectron Density (m^-2)")
						ax.set_xlim(left=0)
						ax.set_yscale("log")
						plt.title(str(energy) + " TeV")
				
	print data
	print Cvalues
	print sigmas
	print Avalues
	print "MEAN GRADIENT:", np.mean(Avalues)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 20)
	
	if k==0:

		Am, Ac = np.polyfit(data, Avalues, 1)
		
		def Afit(x):
			return Am*x + Ac
		plt.subplot(3,1,1)
		plt.errorbar(data, Avalues, yerr=Aerrors, fmt='o')
		plt.xlabel("Energy (Tev)")
		plt.ylabel("Fitted Exponent")
		
		plt.plot(data, Afit(data), color="k")
		Line = "y =" + str('{0:.5f}'.format(Am)) + " x + " + str('{0:.5f}'.format(Ac))
		plt.annotate(Line, xy=(0.85, 0.9), xycoords="axes fraction",  fontsize=15)
		
	elif k==1:
		plt.subplot(3,1,2)
		plt.errorbar(data, Cvalues, yerr=sigmas, fmt='o')
		plt.xlabel("Energy (Tev)")
		plt.ylabel("Fitted Amplitude")
		
		Cm, Cc = np.polyfit(data, Cvalues, 1)
		
		def Cfit(x):
			return Cm*x + Cc
		
		logcvals=[]
		for cval in Cvalues:
			logcvals.append(math.log(cval))
		
		cexponent, logcamplitude = np.polyfit(data, logcvals, 1)
		camplitude = np.exp(logcamplitude)
		
		def Cfit(x):
			return camplitude*np.exp(x*cexponent)
			
		plt.plot(data, Cfit(data), color="k")
		plt.yscale("log")
		Line = "y =" + str('{0:.1f}'.format(camplitude)) + " e ^ ( " + str('{0:.3f}'.format(cexponent)) + " x)"
		plt.annotate(Line, xy=(0.05, 0.9), xycoords="axes fraction",  fontsize=15)
		
	elif k==2:
		plt.subplot(3,1,3)
		plt.scatter(hmax, Cdeviation)
		plt.xlabel("First Interaction Height (m)")
		plt.ylabel("Fitted Amplitude")
		
		print "Final!", hmax, Cdeviation
		
		Chm, Chc = np.polyfit(hmax, Cdeviation, 1)
		
		print "Fitted", Chm, Chc
		print "Chm", Chm
		
		def Chfit(x):
			return Chm*x + Chc
		
		logcvals=[]
		for cval in Cvalues:
			logcvals.append(math.log(cval))
		
		#~ cexponent, logcamplitude = np.polyfit(data, logcvals, 1)
		#~ camplitude = np.exp(logcamplitude)
		#~ 
		#~ def Cfit(x):
			#~ return camplitude*np.exp(x*cexponent)
			
		print "Fittted", hmax, Chfit(hmax) 
		
		chfitteddata=[]
		for h in hmax:
			chfitteddata.append(Chfit(h))
			
		plt.plot(hmax,chfitteddata, color="k")
		#~ plt.yscale("log")
		Line = "y =" + str('{0:.5f}'.format(Chm)) + " x + " + str('{0:.5f}'.format(Chc))
		plt.annotate(Line, xy=(0.05, 0.9), xycoords="axes fraction",  fontsize=15)
		
		figure = plt.gcf() # get current figure
		figure.set_size_inches(20, 20)
		
		saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/lpdpowerlaw.pdf"
		
		print "Saving to", saveto
		
		plt.savefig(saveto)
		plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/lpdpowerlaw.pdf")
		plt.close()
		
	else:
		saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/fullshowerlpd.pdf"
		
		print "Saving to", saveto
		
		plt.tight_layout()
		
		plt.savefig(saveto)
		plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/corsikafullshowerlpd.pdf")
		plt.close()
		
	
