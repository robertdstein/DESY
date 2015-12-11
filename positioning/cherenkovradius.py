import math

def run(Epn, height, sinphi, text=False):
	nucleonmass= 0.93827 
	gamma = (Epn/nucleonmass) + 1
	beta = math.sqrt(1 - (1/gamma**2))
	
	refractiveindex = 1.000008208
	costheta = 1/(beta*refractiveindex)
	
	theta=math.acos(costheta)
	
	radius = height*math.tan(theta)/sinphi
	
	if text:
		print "Gamma", gamma
		print "Beta is", beta
		print "Cos Theta is", costheta
	
	return radius, theta
