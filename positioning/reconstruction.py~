import array, math
#from scipy.optimize import fmin

def run(x,y,E,Z,x0,y0, count):
	r = math.sqrt(((x-x0)**2)+((y-y0)**2)
	expectedcount = ((Z**2)*((0.62*(math.e**(0.014*(r-100))))-0.173)+(50*E))
	diff = (expectedcount-count)**2
	return diff

def f(x, y, E, Z, a):
	sum = 0	
	for detection in a:
		x0 = a[2]
		y0 = a[3]
		count = a[4]
		sum +=run(x,y,E,Z,x0,y0, count)
	return sum
		

#fmin(run,array.array([0,0]))

