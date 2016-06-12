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

def min(a, gridwidth, eff, phi, epsilon, detections):
	
	def f(x,y,Z,Epn, height):
		sum = 0
		for detection in a:
			x0 = float(detection[0])
			y0 = float(detection[1])
			count = float(detection[2])
			bkgcount = float(detection[3])
			category = detection[4]
			sum += ll.run(x,y,Epn,Z, height, x0,y0, count, bkgcount, category, eff, phi, epsilon)
		return sum

	
	#Runs Minimisation and outputs results
	
	startpos=[0, 0, 26.0, 1000, 30000]
	argumentx = "limit_x = (-300, 300), error_x = 100000, "
	argumenty = "limit_y = (-300, 300), error_y = 100000, "
	argumentZ = "fix_Z=True, "
	argumentE = "limit_Epn = (232, 4000), error_Epn=1000, "
	argumentheight = "limit_height = (17500, 70000), error_height=(100000), "
	argumenterror = "print_level=0, errordef = 100"

	m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ "Epn = "+ str(startpos[3]) + ", " + argumentE + "Z=" + str(startpos[2]) + "," +argumentZ + "height = " + str(startpos[4]) + ", " + argumentheight + argumenterror + ")")
	m.migrad()
	params = m.values
	guess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
	guessfval = m.fval

	xsites = np.linspace(-150, 150, int(gridwidth))
	ysites = np.linspace(-150, 150, int(gridwidth))
	
	eraw = np.linspace(0, 1, num=25)
	R = eraw*0.0178
	evals = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)
	hvals = np.linspace(20000, 30000, num=3)
	
	zvalues = np.arange(20.,33.)
	
	minangle = 0
	j = 0
	
	while j < 8:
		coordinates = []
		j = 0
		minangle += 0.5
		for x in xsites:
				for y in ysites:
						n=0
						
						for detection in a:
							x0 = float(detection[0])
							y0 = float(detection[1])
							recordeddangle = float(detection[4])
							
							dangle = ce.dangle(x0, y0, x, y)
							
							if math.fabs(dangle - recordeddangle) < math.radians(minangle):
								n+=1
							
						if n > (len(a)-1):
							coordinates.append([x,y])
							j+=1
		if minangle > 10:
			j=10
							
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
	
	#~ rg = guess
	#~ rf = guessfval
		
	print detections, "Detections -> ", xycount, "Valid Core Positions (", minangle, "Degrees from recorded axis)", ehcount, "Valid Height/Epn Combinations", zcount, "Charge Values", xycount*ehcount*zcount, "Total Minimisations"
	
	for z in zvalues:
		
		m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty+ "Epn = "+ str(startpos[3]) + ", " + argumentE + "Z=" + str(z) + "," +argumentZ + "height = " + str(startpos[4]) + ", " + argumentheight + argumenterror + ")")
		m.migrad(resume=False)
		params = m.values
		zguess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
		zguessfval = m.fval
		
		for [x, y] in coordinates:							
				for [e, h] in ehvals:
					m = eval("Minuit(f,  " + "Epn=" + str(e) + ", " + argumentE + "height = " + str(h) + ", " + argumentheight + "Z=" + str(z) + "," +argumentZ + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
					m.migrad(resume=False)
					params = m.values
					fval = m.fval
					values = m.get_fmin()
					if fval < zguessfval:
						if values.is_valid:
							zguess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
							zguessfval = fval
							#~ print zguess, "(", zguessfval, ") Valid!" 
						#~ elif fval < rf:
							#~ rf = fval
							#~ rg = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
							#~ print rg, "(", rf, ") Rejected!"
							
							
		
		print time.asctime(time.localtime()), zguess, "(", zguessfval, ")"
		#~ print rg, "(", rf, ") Rejected!"
		
		if zguessfval < guessfval:
			guess = zguess
			guessfval = zguessfval
	
	print "Final guess is", guess, math.degrees(phi), math.degrees(epsilon), "(", guessfval, ")"
	return guess[0], guess[1], guess[2], guess[3], guess[4], guessfval
