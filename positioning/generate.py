import random, math

def run(text=False):
    	xpos = (random.random()*300)-150
    	ypos = (random.random()*300)-150
	
	height = random.gauss(30,3)*1000

	theta = math.fabs(random.gauss(0,0.05))

	zenith = random.random()*44

	phi = math.radians(68+zenith)

	epsilon = math.pi*random.random()*2

    	angle = math.radians(theta+0.15)

	radius = height*math.tan(angle)/math.sin(phi)

	ra = radius * math.cos(theta)/math.sin(phi-theta)
	rp = radius * math.sin(phi+theta)/math.cos(theta)

	major = 0.5*(ra+rp)
	minor = math.sqrt(ra*rp)

	e = math.sqrt(1-((minor/major)**2))
	
	if text:
		print "Height is", height
		print "Theta is", theta
		print "Phi is", math.degrees(phi)
		print "Epsilon is", math.degrees(epsilon)
		print "Radius is", radius
		print "Apsis is", ra
		print "Periapsis is", rp	    
		print "Major is", major
		print "Minor is", minor
		print "Eccentrity is", e

	R = random.random()*0.0178
	Epn = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)

	Z=26
	N=56
	
	Energy = Epn*N/1000
	
	print "Total Energy is", Energy, "TeV"
    	
	return xpos, ypos, epsilon, radius, Energy, major, e, Z
	

