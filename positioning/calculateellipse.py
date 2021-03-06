import math

def dangle(xpos, ypos, rayxpos, rayypos):
	
	deltax = math.fabs(xpos-rayxpos)
	deltay = math.fabs(ypos-rayypos)
	
	if deltay == 0:
		if deltax == 0:
			rawangle = math.atan(1)
		else:
			rawangle = 0.5*math.pi
	else:
		rawangle = math.atan(deltax/deltay)
	
	dangle=0
		
	if ((xpos-rayxpos) < 0) & ((ypos-rayypos) > 0):
		dangle = rawangle
	elif ((xpos-rayxpos) < 0) & ((ypos-rayypos) < 0):
		dangle = math.pi - rawangle
	elif ((xpos-rayxpos) > 0) & ((ypos-rayypos) < 0):
		dangle = math.pi + rawangle				
	elif ((xpos-rayxpos) > 0) & ((ypos-rayypos) > 0):
		dangle = (2*math.pi) - rawangle
		
	return dangle

def frad(angle, major, e, epsilon):
	return major * (1-(e**2))/(1 + (e*math.cos(epsilon- angle)))
	
def coeff(radius, theta, phi, epsilon):
	ra = radius * math.cos(theta)/math.sin(phi-theta)
	rp = radius * math.sin(phi+theta)/math.cos(theta)

	major = 0.5*(ra+rp)
	minor = math.sqrt(ra*rp)

	if major > minor > 0:
		e = math.sqrt(1-((minor/major)**2))
	else:
		e = 0
	
	return ra, rp, major, minor, e

def run(simulatedevent, xpos, ypos):
	
	ra, rp, major, minor, e = coeff(simulatedevent.rayradius, simulatedevent.theta, simulatedevent.phi, simulatedevent.epsilon)
	
	newdangle=dangle(xpos, ypos, simulatedevent.rayxpos, simulatedevent.rayypos)

	r = frad(newdangle + math.pi, major, e, simulatedevent.epsilon)
	
	return r, newdangle
	
