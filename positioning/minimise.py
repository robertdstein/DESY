import array, math

import time
import numpy as np
from iminuit import Minuit

def min(a):
	argument = "Z = 26, limit_Z = (20, 26), error_Z=1, x=0, limit_x = (-300, 300), error_x = 0, y=0, limit_y = (-300, 300), error_y = 1, E = 10, limit_E = (1, 150), error_E = 1, a = " + str(a) +", fix_a=True, errordef = 10**-3"
	print argument
	
	def run(x,y,E,Z,x0,y0, count, area):
		r = math.sqrt(((x-x0)**2)+((y-y0)**2))
		if 10 < r < 100:
			expectedcount = ((Z**2)*((0.62*(math.e**(0.014*(r-100))))-0.173)+(50*E))*area
		else:
			expectedcount = 0
		diff = (expectedcount-count)**2
		print expectedcount, count, diff
		return diff
		
	def f(x, y, E, Z):
		sum = 0
		i = 0
		for entry in a:
			if i == 0:
				i +=1
			else:
				detection = eval(entry)
				x0 = float(detection[0])
				y0 = float(detection[1])
				count = float(detection[2])
				area = float(detection[3])
				sum +=run(x,y,E,Z,x0,y0, count, area)
		return sum
	
	#Runs Minimisation and outputs results
    
	m = Minuit(f,Z = 26, fix_Z=True, x=-30, limit_x = (-300, 300), error_x = 1000, y=-50, limit_y = (-300, 300), error_y = 1000, E = 42, limit_E=(1,150), error_E=1, errordef = 1000000)
    
	m.migrad()

	print m.print_param()
	print('fval', m.fval)
	print(m.values)
	print(m.errors)
    
	message = str(time.asctime(time.localtime())) + " Finished minimisation with output "  + str(m.print_param())
	print message



