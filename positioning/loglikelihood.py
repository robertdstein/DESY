import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import countsimulation as cs
import cherenkovradius as cr
import telescoperadius as tr
import scipy.optimize

def expected(x,y,Epn,Z, height, x0,y0, category, scale, eff):
	Nucleons= Z+30
	E=Epn*Nucleons/1000
	
	rmax, theta = cr.run(Epn, height, 1)
	tradius = tr.run(category)
	
	expectedsig, expectedbkg= cs.run(tradius, rmax, x, y, scale, x0, y0, E, Z, eff)
	
	expectedcount = int(expectedsig + expectedbkg)
	return expectedcount
	
def stirling(N):
	lognfactorial = ((N*math.log(N))-N + (0.5*math.log(2*N*math.pi)))
	return lognfactorial
	
def run(x,y,Epn,Z, height, x0,y0, sigcount, bkgcount, category, scale, eff):
	N = int(sigcount + bkgcount)
	expectedcount = expected(x,y,Epn,Z, height, x0,y0, category, scale, eff)
	
	
	if N == 0:
		minusll = expectedcount
	elif  expectedcount == 0:
		minusll = 10**10
	else:
		lognfactorial = stirling(N)
		minusll = expectedcount - (N*math.log(float(expectedcount))) + lognfactorial
		
	return minusll
