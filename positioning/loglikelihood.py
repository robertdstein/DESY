import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import calculatearea as ca
import cherenkovradius as cr
import telescoperadius as tr
import scipy.optimize

def expected(x,y,Epn,Z, height, x0,y0, category, scale, eff):
	Nucleons= Z+30
	E=Epn*Nucleons/1000
	
	rmax, theta = cr.run(Epn, height, 1)
	
	distance = math.sqrt(((x-x0)**2)+((y-y0)**2))
	
	sigdensity, bkgd = ld.run(distance, E, Z, rmax, scale, eff)
	
	tradius = tr.run(category)
	
	siglitarea, bkglitarea = ca.run(tradius, rmax, distance, scale)
	
	expectedsig=sigdensity*siglitarea
	expectedbkg = bkgd*bkglitarea
	
	expectedcount = int(expectedsig + expectedbkg)
	return expectedcount
	
def stirling(N):
	lognfactorial = ((N*math.log(N))-N + (0.5*math.log(2*N*math.pi)))
	return lognfactorial
	
def run(x,y,Epn,Z, height, x0,y0, sigcount, bkgcount, category, scale, eff):
	N = int(sigcount + bkgcount)
	expectedcount = expected(x,y,Epn,Z, height, x0,y0, category, scale, eff)
	lognfactorial = stirling(N)
	
	if N == 0:
		minusll = expectedcount
	elif  expectedcount == 0:
		minusll = 10**10
	else:
		minusll = expectedcount - (N*math.log(float(expectedcount))) + lognfactiorial
