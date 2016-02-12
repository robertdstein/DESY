import math
import atmosphere as atm

nucleonmass= 0.93827 

def run(Epn, height, sinphi, text=False):
	
	theta = runtheta(Epn, height)

	if height is None:
		print refractiveindex, height, sinphi, gamma, costheta
	
	radius = float(height)*math.tan(theta)/float(sinphi)
	
	if text:
		print "Gamma", gamma
		print "Beta is", beta
		print "Cos Theta is", costheta
	
	return radius, theta

def runtheta(Epn, height):
	
	gamma = (Epn/nucleonmass) + 1
	beta = math.sqrt(1 - (1/gamma**2))
	
	refractiveindex = atm.runindex(height)
	
	costheta = 1/(beta*refractiveindex)
	
	if costheta < 1:	
		theta=math.acos(costheta)
	else:
		theta=0
		
	return theta


def runemin(ri):
	
	costheta = 1
	
	beta = costheta/ri
	gamma = math.sqrt(1/(1 - (beta**2)))
	
	Epn = nucleonmass*(gamma-1)
	
	return Epn
	
	
	
