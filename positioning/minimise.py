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
		return ll

	#Runs Minimisation and outputs results
	
	fullstartpos=[0, 0, 1000]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "limit_Z = (16,36), error_Z = 2, "
	argumentheight = "limit_height = (17500, 70000), error_height=(100000), "
	argumentE = "limit_Epn = (232, 4000), error_Epn=1000, "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(full, x="+ str(fullstartpos[0]) + ", " + argumentx + "y="+ str(fullstartpos[1]) + ", " + argumenty+ "Epn = "+ str(fullstartpos[2]) + ", " + argumentE + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['Epn']]
	guessfval = m.fval

	xsites = np.linspace(-150, 150, 10)
	ysites = np.linspace(-150, 150, 10)
	
	eraw = np.linspace(0, 1, num=10)
	R = eraw**3.01*(10**-3)
	evals =	((1.7*R/321)+(2411**-1.7))**(-1/1.7)
	
	minangle = 0.0
	j = 0
	
	while j < 10:
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
			j=10
	
	m = eval("Minuit(full, x="+ str(fullstartpos[0]) + ", " + argumentx + "y="+ str(fullstartpos[1]) + ", " + argumenty+ "Epn = "+ str(fullstartpos[2]) + ", " + argumentE + argumenterror + ")")
	m.migrad(resume=False)
	params = m.values
	zguess = [params['x'], params['y'], params['Epn']]
	zguessfval = m.fval
		
	for [x, y] in coordinates:							
			for e in evals:
				m = eval("Minuit(full,  " + "Epn=" + str(e) + ", " + argumentE + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
				m.migrad(resume=False)
				params = m.values
				fval = m.fval
				values = m.get_fmin()
				if fval < zguessfval:
					if values.is_valid:
						guess = [params['x'], params['y'], params['Epn']]
						guessfval = fval						
	
	print "Final guess is", guess, "(", guessfval, ")"
	print "Measured values are", [measured.rayxpos, measured.rayypos, measured.epn], "(", true.minusllfull, ")", true.fullmultiplicity
	
	reconx = guess[0]
	recony = guess[1]
	reconEpn = guess[2]

	
	def dc(Z,height, x, y):
		energy = 56*reconEpn
		testevent = event(x, y, measured.epsilon, energy, Z, height, measured.phi, N=56, layout=layout, smear=False)
		testevent.simulatetelescopes(raweff)
		testevent.calculatedclikelihood(measured)
		testevent.calculatefulllikelihood(measured)
		ll = testevent.minuslldc
		ll += testevent.minusllfull
		return ll

	xsites = np.linspace(-150, 150, int(gridwidth))
	ysites = np.linspace(-150, 150, int(gridwidth))
	
	eraw = np.linspace(0, 1, num=3)
	R = eraw*0.0178
	evals = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)
	hvals = np.linspace(20000, 30000, num=3)
	hvals = [20000]
	
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
		
	print measured.DCmultiplicity, "Detections -> ", xycount, "Valid Core Positions (", minangle, "Degrees from recorded axis)", ehcount, "Valid Height/Epn Combinations", zcount, "Charge Values", xycount*ehcount*zcount, "Total Minimisations"
	
	m = eval("Minuit(dc, x="+ str(reconx) + ", " + argumentx + "y="+ str(recony) + ", " + argumenty+  "Z=26," +argumentZ + "height = 20000, " + argumentheight + argumenterror + ")")
	m.migrad(resume=False)
	params = m.values
	guess = [params['Z'], params['height']]
	guessfval = m.fval
	
	for z in zvalues:
		m = eval("Minuit(dc, Z=" + str(z) + "," +argumentZ + "x="+ str(reconx) + ", " + argumentx + "y="+ str(recony) +", " + argumenty+   "height = 20000, " + argumentheight + argumenterror + ")")
		m.migrad(resume=False)
		params = m.values
		zguess = [params['Z'], params['height']]
		zguessfval = m.fval
		
									
		for [e, h] in ehvals:
			m = eval("Minuit(dc,  x="+ str(reconx) + ", " + argumentx + "y="+ str(recony) + ", " + argumenty+  "height = " + str(h) + ", " + argumentheight + "Z=" + str(z) + "," +argumentZ + argumenterror + ")")
			m.migrad(resume=False)
			params = m.values
			fval = m.fval
			values = m.get_fmin()
			if fval < zguessfval:
				if values.is_valid:
					zguess = [params['x'], params['y'], params['Z'], params['height']]
					zguessfval = fval						
		
		print time.asctime(time.localtime()), zguess, "(", zguessfval, ")"
		
		if zguessfval < guessfval:
			guess = zguess
			guessfval = zguessfval
	
	print "Final guess is", guess, math.degrees(measured.phi), math.degrees(measured.epsilon), "(", guessfval, ")"
	
	reconZ = guess[0]
	reconheight = guess[1]
	
	energy = reconEpn*56
	print [reconx, recony, reconEpn, reconZ, reconheight]
	fullsimulation.reconstructed = event(reconx, recony, measured.epsilon, energy, reconZ, reconheight, measured.phi, N=56, layout=layout, smear=False)
	fullsimulation.reconstructed.simulatetelescopes(raweff)
	fullsimulation.getreconstructedlikelihood()
