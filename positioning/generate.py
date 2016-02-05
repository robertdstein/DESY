import random, math
import cherenkovradius as cr

def run(text=False):
    	xpos = (random.random()*300)-150
    	ypos = (random.random()*300)-150
	
	R = random.random()*0.0178
	Epn = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)

	Z= 26
	N= Z + 30
	
	height = 30000
	
	Energy = Epn*N/1000
	
	scale=1.2

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
		print "Total Energy is", Energy, "TeV"
    	
	return xpos, ypos, epsilon, radius, Epn, Energy, Z, scale, height, phi, theta
	

