import random, math
import cherenkovradius as cr
import atmosphere as atm

def run(text=False):
    	xpos = (random.random()*300)-150
    	ypos = (random.random()*300)-150
	
	R = random.random()*0.0178
	Epn = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)

	Z= 26
	
	hprob = random.random()
	height = atm.runheight(hprob, text)

	zenith = random.random()*44

	phi = math.radians(68+zenith)

	epsilon = math.pi*random.random()*2
	
	radius, theta = cr.run(Epn, height, math.sin(phi), text=text)
	
	if text:
		print "Height is", height
		print "Theta is", math.degrees(theta)
		print "Phi is", math.degrees(phi)
		print "Epsilon is", math.degrees(epsilon)
		print "Radius is", radius
    	
	return xpos, ypos, epsilon, radius, Epn, Z, height, phi, theta
	

