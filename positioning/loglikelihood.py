import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import countsimulation as cs
import cherenkovradius as cr
import calculateellipse as ce
import telescoperadius as tr
import scipy.optimize

def expected(x,y,Epn,Z, height, x0,y0, category, eff, phi, epsilon):
	
	rayradius, theta = cr.run(Epn, height, math.sin(phi))
	tradius = tr.run(category)
	
	if rayradius > 0:
		r = ce.run(rayradius, theta, phi, epsilon, x0, y0, x, y)
		
		expectedsig, expectedbkg= cs.run(tradius, r, x, y, x0, y0, Epn, Z, eff)
		
		expectedcount = int(expectedsig + expectedbkg)
	
	else:
		expectedcount = math.pi*(tradius**2)*ld.base(eff)
	
	return expectedcount
	
def stirling(N):
	lognfactorial = ((N*math.log(N))-N + (0.5*math.log(2*N*math.pi)))
	return lognfactorial
	
def run(x,y,Epn,Z, height, x0,y0, count, category, eff, phi, epsilon):
	N = int(count)
	expectedcount = expected(x,y,Epn,Z, height, x0,y0, category, eff, phi, epsilon)
	
	if N == 0:
		minusll = expectedcount
	elif  expectedcount == 0:
		minusll = 10**10
	else:
		lognfactorial = stirling(N)
		minusll = expectedcount - (N*math.log(float(expectedcount))) + lognfactorial
		
	return minusll
