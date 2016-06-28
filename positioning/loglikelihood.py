import array, math

import time
import numpy as np
import lightdensity as ld
import countsimulation as cs
import cherenkovradius as cr
import calculateellipse as ce
import telescoperadius as tr
import atmosphere as atm
from classes import *

threshold = ld.trigger()

#~ def expected(simulated):
	#~ 
	#~ rayradius, theta = cr.run(Epn, height, math.sin(phi))
	#~ tradius = tr.run(category)
	#~ 
	#~ frac = atm.runabsorption(height)
	#~ 
	#~ eff = raweff*frac/math.sin(phi)
	#~ 
	#~ if rayradius > 0:
		#~ r=0
		#~ 
	#~ r, dangle = ce.run(rayradius, theta, phi, epsilon, x0, y0, x, y)
	#~ 
	#~ expectedcount, expectedbkgcount, dcerror, bkgerror= cs.run(tradius, r, x, y, x0, y0, Epn, Z, eff)
	#~ 
	#~ return expectedcount, expectedbkgcount, dcerror, bkgerror
	
#~ def stirling(N):
	#~ lognfactorial = ((N*math.log(N))-N + (0.5*math.log(2*N*math.pi)))
	#~ return lognfactorial
	
def rundc(tel, detectedtel):
	if str(detectedtel.DCtrigger) == str(False):
		return 0
		count = detectedtel.altDCphotons
		expectedcount = tel.altDCphotons
	else:
		expectedcount = tel.reconphotons
		count = math.fabs(detectedtel.reconphotons)
	dcerror = tel.reconfracerror

	if expectedcount < 0:
		expectedcount = 0
		
	
	dcsigma = 0.5*(dcerror*(expectedcount))
		
	minusll=0
	
	minusll += math.log(dcsigma)
	minusll += ((count-expectedcount)/(math.sqrt(2)*dcsigma))**2
	
	return minusll
	
def runfull(tel, detectedtel):
	expectedbkgcount = tel.fullphotons
	bkgerror = tel.fullfracerror
	
	bkgcount = detectedtel.fullphotons
		
	if expectedbkgcount < 0:
		expectedbkgcount = 0
	
	bkgsigma = 0.5*(bkgerror*(expectedbkgcount))
		
	minusll=0
	
	minusll += math.log(bkgsigma)			
	minusll += ((bkgcount-expectedbkgcount)/(math.sqrt(2)*bkgsigma))**2
	
	return minusll
