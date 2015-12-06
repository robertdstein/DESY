import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import scipy.optimize

def min(a, gridwidth):
	
	def calculatedifference(x,y,E,Z,x0,y0, sigcount, bkgcount, area):
		r = math.sqrt(((x-x0)**2)+((y-y0)**2))
		sigdensity, bkgd = ld.run(r,E,Z)
		expectedsig=sigdensity*area
		expectedbkg = bkgd*area
		diff = (expectedsig-sigcount)**2 + (expectedbkg-bkgcount)**2
		return diff
		
	def f(x,y,Z,E):
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
				area=float(detection[4])
				sum += calculatedifference(x,y,E,Z,x0,y0, sigcount, bkgcount, area)
		return sum
	
	#Runs Minimisation and outputs results
	
	startpos=[0,0]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "Z = 26, limit_Z=(20,26.5), error_Z=100, "
	argumentE = "E = 42, limit_E=(1,250), error_E=1, "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ argumentZ + argumentE + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['E'], params['Z']]
	guessfval = m.fval

	xsites = np.linspace(-200, 200, int(gridwidth))
	ysites = np.linspace(-200, 200, int(gridwidth))
	
	for x in xsites:
		for y in ysites:
			m = eval("Minuit(f, x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumentZ + argumentE + argumenterror + ")")
			m.migrad()
			params = m.values
			fval = m.fval
			values = m.get_fmin()
			if values.is_valid:
				if fval < guessfval:
					guess = [params['x'], params['y'], params['E'], params['Z']]
					guessfval = fval
	
	Zval = int(guess[3]) + int(2*(guess[3]-int(guess[3])))
	print Zval, guess[3]
	argumentE = "E = " + str(params['E']) +", fix_E=True, " 
	argumentZ = "Z = " + str(Zval) +", fix_Z=True, " 
	
	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ argumentZ + argumentE + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['E'], params['Z']]
	guessfval = m.fval
	
	for x in xsites:
		for y in ysites:
			m = eval("Minuit(f, x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumentZ + argumentE + argumenterror + ")")
			m.migrad()
			params = m.values
			fval = m.fval
			values = m.get_fmin()
			if values.is_valid:
				if fval < guessfval:
					guess = [params['x'], params['y'], params['E'], params['Z']]
					guessfval = fval
	
	print "Final guess is", guess
	
	#~ guess=[0,0,15,26]
	#~ 
	#~ res = scipy.optimize.minimize(f, guess, options={'disp': True}, method="Powell")
	#~ 
	#~ print res.x
