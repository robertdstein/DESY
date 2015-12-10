import random, math

def run(text=False):
    	xpos = (random.random()*300)-150
    	ypos = (random.random()*300)-150
	
	R = random.random()*0.0178
	Epn = ((1.7*R/321)+(3571**-1.7))**(-1/1.7)

	nucleonmass= 0.93827 
	gamma = (Epn/nucleonmass) + 1
	
	beta = math.sqrt(1 - (1/gamma**2))

	Z=26
	N=56
	
	Energy = Epn*N/1000
	
	refractiveindex = 1.000292
	
	height = random.gauss(30,3)*1000

	costheta = 1/(beta*refractiveindex)
	
	theta=math.acos(costheta)
	
	scale=1.2

	zenith = random.random()*44

	phi = math.radians(68+zenith)

	epsilon = math.pi*random.random()*2
	
	angle = math.radians(theta+0.15)

	radius = height*math.tan(angle)/math.sin(phi)

	ra = radius * costheta/math.sin(phi-theta)
	rp = radius * math.sin(phi+theta)/costheta

	major = 0.5*(ra+rp)
	minor = math.sqrt(ra*rp)

	e = math.sqrt(1-((minor/major)**2))
	
	if text:
		print "gamma", gamma
		print "Cos theta", costheta
		print "Beta is", beta
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
    	
	return xpos, ypos, epsilon, radius, Energy, major, minor, ra, rp, e, Z, scale
	

