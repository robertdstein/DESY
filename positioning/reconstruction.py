import array, math

import time
import numpy as np
from iminuit import Minuit

def min(a):
    
    print "a", a
    
    argument = "Z = 26, limit_Z = (20, 26), error_Z=1, x=0, limit_x = (-300, 300), error_x = 0, y=0, limit_y = (-300, 300), error_y = 1, E = 10, limit_E = (1, 150), error_E = 1, a = " + str(a) +", fix_a=True, errordef = 10**-3"
    
    print argument
    
    def run(x,y,E,Z,x0,y0, count):
	r = math.sqrt(((x-x0)**2)+((y-y0)**2))
	expectedcount = ((Z**2)*((0.62*(math.e**(0.014*(r-100))))-0.173)+(50*E))
	diff = (expectedcount-count)**2
	return diff

    def f(x, y, E, Z):
	sum = 0
	print "a", a
	for detection in a:
		x0 = detection[2]
		y0 = detection[3]
		count = detection[4]
		sum +=run(x,y,E,Z,x0,y0, count)
	return sum
    
    #Runs Minimisation and outputs results
    
    m = Minuit(f,Z = 26, limit_Z = (20, 26), error_Z=1, x=0, limit_x = (-300, 300), error_x = 0, y=0, limit_y = (-300, 300), error_y = 1, E = 10, limit_E = (1, 150), error_E = 1, errordef = 10**-3)
    
    m.migrad()

    print m.print_param()
    print('fval', m.fval)
    
    message = str(time.asctime(time.localtime())) + " Finished minimisation with output "  + str(m.print_param())
    print message
    
a=[[7.2831853072,"lst",0,0,380815],[7.2831853072,"lst",60,60,346688],[7.2831853072,"lst",60,-60,403627],[7.2831853072,"lst",-60,60,323913]]

min(a)



