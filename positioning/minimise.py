import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import scipy.optimize

def min(a, gridwidth):
	
	def calculatedifference(x,y,E,Z,x0,y0, sigcount, bkgcount, siglitarea, bkglitarea, rmax, scale):
		r = math.sqrt(((x-x0)**2)+((y-y0)**2))
		sigdensity, bkgd = ld.run(r,E,Z, rmax, scale)
		expectedsig=sigdensity*siglitarea
		expectedbkg = bkgd*bkglitarea
		diff = (expectedsig-sigcount)**2 + (expectedbkg-bkgcount)**2
		return diff
		
	def f(x,y,Z,E, rmax, scale):
		sum = 0
		i = 0
		for entry in a:
			if i == 0:
				i +=1
			else:
				detection = eval(entry)
				x0 = float(detection[0])
				y0 = float(detection[1])
				sigcount = float(detection[2])
				bkgcount = float(detection[3])
				siglitarea=float(detection[4])
				bkglitarea=float(detection[5])
				sum += calculatedifference(x,y,E,Z,x0,y0, sigcount, bkgcount, siglitarea, bkglitarea, rmax, scale)
		return sum
	
	#Runs Minimisation and outputs results
	
	startpos=[0,0]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "Z = 26, limit_Z=(20,26.5), error_Z=100, "
	argumentE = "E = 25, limit_E=(1,250), error_E=10, "
	argumentRmax = "rmax=100, limit_rmax=(50,150), error_rmax=10,  "
	argumentscale = "scale=1.2, fix_scale=True, "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ argumentE + argumentZ + argumentRmax + argumentscale + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['E'], params['Z'], params['rmax']]
	guessfval = m.fval

	xsites = np.linspace(-200, 200, int(gridwidth))
	ysites = np.linspace(-200, 200, int(gridwidth))
	
	for x in xsites:
		for y in ysites:
			m = eval("Minuit(f," + argumentE + argumentRmax + argumentscale+ argumentZ + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
			m.migrad()
			params = m.values
			fval = m.fval
			values = m.get_fmin()
			if values.is_valid:
				if fval < guessfval:
					guess = [params['x'], params['y'], params['E'], params['Z'], params['rmax']]
					guessfval = fval
	
	Zval = int(guess[3]) + int(2*(guess[3]-int(guess[3])))
	print Zval, guess[3]
	argumentZ = "Z = " + str(Zval) +", fix_Z=True, " 
	
	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ argumentZ + argumentE + argumentRmax + argumentscale+argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['E'], params['Z'], params['rmax']]
	guessfval = m.fval
	
	for x in xsites:
		for y in ysites:
			m = eval("Minuit(f, x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumentZ + argumentE + argumentRmax + argumentscale + argumenterror + ")")
			m.migrad()
			params = m.values
			fval = m.fval
			values = m.get_fmin()
			if values.is_valid:
				if fval < guessfval:
					guess = [params['x'], params['y'], params['E'], params['Z'], params['rmax']]
					guessfval = fval
	
	print "Final guess is", guess
	
	#~ guess=[0,0,15,26]
	#~ 
	#~ res = scipy.optimize.minimize(f, guess, options={'disp': True}, method="Powell")
	#~ 
	#~ print res.x
