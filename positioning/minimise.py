import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import calculatearea as ca
import cherenkovradius as cr
import calculateellipse as ce
import telescoperadius as tr
import loglikelihood as ll
import atmosphere as atm
import scipy.optimize
from classes import *

def min(fullsimulation, layout, gridwidth, raweff):
	measured = fullsimulation.detected
	true = fullsimulation.true

	def full(x,y, Epn):
		energy = 56*Epn
		testevent = event(x, y, measured.epsilon, energy, 26, 25000, measured.phi, N=56, layout=layout, smear=False)
		testevent.simulatetelescopes(raweff)
		testevent.calculatefulllikelihood(measured)
		ll = testevent.minusllfull
		#~ print "x", x, "y", y, "Epn", Epn, "ll", ll
		return ll

	#Runs Minimisation and outputs results
	
	fullstartpos=[0, 0, 1000, 20000]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "limit_Z = (16,36), error_Z = 2, "
	argumentheight = "limit_height = (17500, 70000), error_height=(100000), "
	argumentE = "limit_Epn = (232, 4000), error_Epn=1000, "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(full, x="+ str(fullstartpos[0]) + ", " + argumentx + "y="+ str(fullstartpos[1]) + ", " + argumenty+ "Epn = "+ str(fullstartpos[2]) + ", " + argumentE + argumenterror + ")")
	m.migrad()
	guessparams = m.values
	guessfval = m.fval

	xsites = np.linspace(-150, 150, 300)
	ysites = np.linspace(-150, 150, 300)
	
	eraw = np.linspace(0, 1, num=50)
	R = eraw**3.01*(10**-3)
	evals =	((1.7*R/321)+(2411**-1.7))**(-1/1.7)
	
	minangle = 0.0
	j = 0
	
	while j < 20:
		coordinates = []
		j = 0
		minangle += 0.1
		for x in xsites:
				for y in ysites:
						n=0
						for tel in measured.telescopes:
							newdangle = ce.dangle(tel.x,tel.y, x, y)
							
							if math.fabs(newdangle - tel.dangle) < math.radians(minangle):
								n+=1
							
						if n > (len(measured.telescopes)-1):
							coordinates.append([x,y])
							j+=1
		if minangle > 20:
			j=200
		
	for [x, y] in coordinates:							
			for e in evals:
				m = eval("Minuit(full,  " + "Epn=" + str(e) + ", " + argumentE + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
				m.migrad(resume=False)
				params = m.values
				fval = m.fval
				values = m.get_fmin()
				if fval < guessfval:
					if values.is_valid:
						guessparams = params
						guessfval = fval						
	
	print "Final guess is", guessparams, "(", guessfval, ")"
	print "Measured values are", [measured.rayxpos, measured.rayypos, measured.epn], "(", true.minusllfull, ")", true.fullmultiplicity
	
	fullreconx = guessparams['x']
	fullrecony = guessparams['y']
	reconEpn = guessparams['Epn']
	
	def dc(Z,height, x, y):
		energy = 56*reconEpn
		testevent = event(x, y, measured.epsilon, energy, Z, height, measured.phi, N=56, layout=layout, smear=False)
		testevent.simulatetelescopes(raweff)
		testevent.calculatedclikelihood(measured)
		testevent.calculatefulllikelihood(measured)
		if math.fabs(Z-26) > 10:
			print "x", x, "y", y, "Height", height, "Z", Z,   
		ll = testevent.minuslldc
		if math.fabs(Z-26) > 10:
			print "ll1",ll, 
		ll += testevent.minusllfull
		if math.fabs(Z-26) > 10:
			print "ll2", ll
		return ll

	xsites = np.linspace(-150, 150, int(gridwidth))
	ysites = np.linspace(-150, 150, int(gridwidth))
	
	eraw = np.linspace(0, 1, num=3)
	R = eraw*0.0178
	evals = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)
	hvals = np.linspace(20000, 30000, num=3)
	
	zvalues = np.arange(20.,33.)
	
	minangle = 0.0
	j = 0
							
	ehvals=[]
	for height in hvals:
		for Epn in evals:
			ri = atm.runindex(height)
			Ethreshold = float(cr.runemin(ri))
			if float(Epn) > float(Ethreshold):
				ehvals.append([Epn, height])
	
	xycount = len(coordinates)			
	ehcount = len(ehvals)
	zcount = len(zvalues)
	line = [0,0]
	
	print ehvals
		
	print measured.DCmultiplicity, "Detections -> ", xycount, "Valid Core Positions (", minangle, "Degrees from recorded axis)", ehcount, "Valid Height/Epn Combinations", zcount, "Charge Values", xycount*ehcount*zcount, "Total Minimisations"
	
	m = eval("Minuit(dc, x="+ str(fullreconx) + ", " + argumentx + "y="+ str(fullrecony) + ", " + argumenty+  "Z=26," +argumentZ + "height = 20000, " + argumentheight + argumenterror + ")")
	m.migrad(resume=False)
	params = m.values
	guessparams = params
	guessfval = m.fval
	
	for z in zvalues:					
		for [e, h] in ehvals:
			m = eval("Minuit(dc,  x="+ str(fullreconx) + ", " + argumentx + "y="+ str(fullrecony) + ", " + argumenty+  "height = " + str(h) + ", " + argumentheight + "Z=" + str(z) + "," +argumentZ + argumenterror + ")")
			m.migrad(resume=False)
			params = m.values
			fval = m.fval
			values = m.get_fmin()
			if fval < guessfval:
				if values.is_valid:							
					if fval < guessfval:
						guessparams = params
						guessfval = fval
	
	print "Final guess is", guessparams, math.degrees(measured.phi), math.degrees(measured.epsilon), "(", guessfval, ")"
	
	reconZ = guessparams["Z"]
	reconheight = guessparams["height"]
	reconx = guessparams["x"]
	recony = guessparams["y"]
	
	energy = reconEpn*56
	print "Recon", [reconx, recony, reconEpn, reconZ, reconheight]
	print "True", [true.rayxpos, true.rayypos, true.epn, true.Z, true.height]
	fullsimulation.reconstructed = event(reconx, recony, measured.epsilon, energy, reconZ, reconheight, measured.phi, N=56, layout=layout, smear=False)
	fullsimulation.reconstructed.simulatetelescopes(raweff)
	fullsimulation.getreconstructedlikelihood()
	fullsimulation.reconstructed.fullrayxpos = fullreconx
	fullsimulation.reconstructed.fullrayypos = fullrecony
