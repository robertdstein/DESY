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

	ra = radius * math.cos(theta)/math.sin(phi-theta)
	rp = radius * math.sin(phi+theta)/math.cos(theta)

	major = 0.5*(ra+rp)
	minor = math.sqrt(ra*rp)

	e = math.sqrt(1-((minor/major)**2))
	
	if text:
		print "Height is", height
		print "Theta is", math.degrees(theta)
		print "Phi is", math.degrees(phi)
		print "Epsilon is", math.degrees(epsilon)
		print "Radius is", radius
		print "Apsis is", ra
		print "Periapsis is", rp	    
		print "Major is", major
		print "Minor is", minor
		print "Eccentrity is", e
		print "Total Energy is", Energy, "TeV"
    	
	return xpos, ypos, epsilon, radius, Energy, Epn, major, minor, ra, rp, e, Z, scale, height, phi
	

