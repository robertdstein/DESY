import array, math

import time
import numpy as np
import lightdensity as ld
import countsimulation as cs
import cherenkovradius as cr
import calculateellipse as ce
import telescoperadius as tr
import atmosphere as atm

threshold = ld.trigger()

def expected(x,y,Epn,Z, height, x0,y0, category, raweff, phi, epsilon):
	
	rayradius, theta = cr.run(Epn, height, math.sin(phi))
	tradius = tr.run(category)
	
	frac = atm.runabsorption(height)
	
	eff = raweff*frac/math.sin(phi)
	
	if rayradius > 0:
		r=0
		
	r, dangle = ce.run(rayradius, theta, phi, epsilon, x0, y0, x, y)
	
	expectedcount, expectedbkgcount, dcerror, bkgerror= cs.run(tradius, r, x, y, x0, y0, Epn, Z, eff)
	
	return expectedcount, expectedbkgcount, dcerror, bkgerror
	
#~ def stirling(N):
	#~ lognfactorial = ((N*math.log(N))-N + (0.5*math.log(2*N*math.pi)))
	#~ return lognfactorial
	
def run(x,y,Epn,Z, height, x0,y0, count, bkgcount, category, eff, phi, epsilon):
	N = int(count)
	Nbkg = int(bkgcount)
	expectedcount, expectedbkgcount, dcerror, bkgerror = expected(x,y,Epn,Z, height, x0,y0, category, eff, phi, epsilon)\
	
	minusll=0
	
	if expectedcount < 0:
		expectedcount = 0
		
	if expectedbkgcount < 0:
		expectedbkgcount = 0
	dcsigma = dcerror*(expectedcount + 0.0001)
	bkgsigma = bkgerror*(expectedbkgcount+0.0001)
	
		
	#~ print "Likelihood", 
	
	if (N > 0):
		minusll += math.log(dcsigma)
		#~ print "DC", minusll,
		minusll += ((N-expectedcount)/(math.sqrt(2)*dcsigma))**2
		#~ print minusll,
	
	if Nbkg > 0:
		minusll += math.log(bkgsigma)			
		#~ print "Full", minusll,
		minusll += ((Nbkg-expectedbkgcount)/(math.sqrt(2)*bkgsigma))**2
		#~ print minusll,
	
	#~ print ""
	
	return minusll
