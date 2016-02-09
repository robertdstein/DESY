import math
import atmosphere as atm

def run(Epn, height, sinphi, text=False):
	nucleonmass= 0.93827 
	gamma = (Epn/nucleonmass) + 1
	beta = math.sqrt(1 - (1/gamma**2))
	
	refractiveindex = atm.runindex(height)
	
	#~ print Epn, height, sinphi, refractiveindex
	
	costheta = 1/(beta*refractiveindex)
	
	if costheta < 1:	
		theta=math.acos(costheta)
	else:
		theta=0
		
	if height is None:
		print refractiveindex, height, sinphi, gamma, costheta
	
	radius = float(height)*math.tan(theta)/float(sinphi)
	
	if text:
		print "Gamma", gamma
		print "Beta is", beta
		print "Cos Theta is", costheta
	
	return radius, theta
