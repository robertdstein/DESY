import array, math

import time
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import calculatearea as ca
import cherenkovradius as cr
import telescoperadius as tr
import loglikelihood as ll
import atmosphere as atm
import scipy.optimize

def min(a, gridwidth, eff, phi, epsilon):
	
	def f(x,y,Z,Epn, height):
		sum = 0
		for detection in a:
			x0 = float(detection[0])
			y0 = float(detection[1])
			count = float(detection[2])
			category = detection[3]
			sum += ll.run(x,y,Epn,Z, height, x0,y0, count, category, eff, phi, epsilon)
		return sum

	
	#Runs Minimisation and outputs results
	
	startpos=[0, 0, 26.0, 1000]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "fix_Z=True, "
	argumentE = "limit_Epn = (232, 4000), error_Epn=1000, "
	argumentheight = "height=30000, limit_height = (17500, 70000), error_height=(100000), "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ "Epn = "+ str(startpos[3]) + ", " + argumentE + "Z=" + str(startpos[2]) + "," +argumentZ + argumentheight + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
	guessfval = m.fval

	xsites = np.linspace(-100, 100, int(gridwidth))
	ysites = np.linspace(-100, 100, int(gridwidth))
	evals = np.linspace(250, 3500, num=10)
	
	zvalues = np.arange(20.,33.)
	
	#HEY THIS IS ONLY TEMPORARY!!!!!!!!!!!!!!
	
	zvalues = [26]
	
	for z in zvalues:
		
		m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ "Epn = "+ str(startpos[3]) + ", " + argumentE + "Z=" + str(z) + "," +argumentZ + argumentheight + argumenterror + ")")
		m.migrad()
		params = m.values
		zguess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
		zguessfval = m.fval
		
		for x in xsites:
			for y in ysites:
				for e in evals:
					m = eval("Minuit(f," + "Epn=" + str(e) + ", " + argumentE + argumentheight + "Z=" + str(z) + "," +argumentZ + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
					m.migrad()
					params = m.values
					fval = m.fval
					values = m.get_fmin()
					if values.is_valid:
						if fval < zguessfval:
							zguess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
							zguessfval = fval
		
		print zguess, "(", zguessfval, ")"
		
		if zguessfval < guessfval:
			guess = zguess
			guessfval = zguessfval
	
	print "Final guess is", guess, math.degrees(phi), math.degrees(epsilon)
	return guess[0], guess[1], guess[2], guess[3], guess[4]
