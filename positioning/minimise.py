import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import calculatearea as ca
import cherenkovradius as cr
import telescoperadius as tr
import scipy.optimize

def min(a, gridwidth, eff):
	def calculatedifference(x,y,Epn,Z, height, x0,y0, sigcount, bkgcount, category, scale):
		Nucleons= Z+30
		E=Epn*Nucleons/1000
		
		rmax, theta = cr.run(Epn, height, 1)
		
		distance = math.sqrt(((x-x0)**2)+((y-y0)**2))
		
		sigdensity, bkgd = ld.run(distance, E, Z, rmax, scale, eff)
		
		tradius = tr.run(category)
		
		siglitarea, bkglitarea = ca.run(tradius, rmax, distance, scale)
		
		expectedsig=sigdensity*siglitarea
		expectedbkg = bkgd*bkglitarea
		
		diff = (((sigcount- expectedsig)**2)/(sigcount+1)) + (((expectedbkg - bkgcount)**2)/(bkgcount+1))
		return diff
		
	def f(x,y,Z,Epn, height, scale):
		sum = 0
		i = 0
		for detection in a:
			x0 = float(detection[0])
			y0 = float(detection[1])
			sigcount = float(detection[2])
			bkgcount = float(detection[3])
			category = detection[4]
			sum += calculatedifference(x,y,Epn,Z, height, x0,y0, sigcount, bkgcount, category, scale)
		return sum
	
	#Runs Minimisation and outputs results
	
	startpos=[0, 0, 26.0]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "fix_Z=True, "
	argumentE = "Epn = 300, limit_Epn = (232, 4000), error_Epn=1, "
	argumentheight = "height=30000, fix_height=True, "
	argumentscale = "scale=1.2, fix_scale=True, "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ argumentE + "Z=" + str(startpos[2]) + "," +argumentZ + argumentheight + argumentscale + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
	guessfval = m.fval

	xsites = np.linspace(-200, 200, int(gridwidth))
	ysites = np.linspace(-200, 200, int(gridwidth))
	
	zvalues = np.arange(21.,29.)
	
	for z in zvalues:
		for x in xsites:
			for y in ysites:
				m = eval("Minuit(f," + argumentE + argumentheight + argumentscale+ "Z=" + str(z) + "," +argumentZ + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
				m.migrad()
				params = m.values
				fval = m.fval
				values = m.get_fmin()
				if values.is_valid:
					if fval < guessfval:
						guess = guess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
						guessfval = fval
		print "for Z=", z, guess
	
	print "Final guess is", guess
	return guess[0], guess[1], guess[2], guess[3], guess[4]
