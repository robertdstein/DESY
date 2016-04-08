import math
import atmosphere as atm

nucleonmass= 0.93827 

def run(Epn, height, sinphi, fit="linear", text=False):
	
	theta = runtheta(Epn, height, fit)

	if height is None:
		print refractiveindex, height, sinphi, gamma, costheta
	
	radius = (float(height)-1800)*math.tan(theta)/float(sinphi)
	
	if text:
		print "Gamma", gamma
		print "Beta is", beta
		print "Cos Theta is", costheta
	
	return radius, theta

def runtheta(Epn, height, fit="linear"):
	
	gamma = (Epn/nucleonmass) + 1
	beta = math.sqrt(1 - (1/gamma**2))
	
	if fit == "linear":	
		refractiveindex = atm.runindex(height)
	elif fit == "exp":
		refractiveindex = atm.expindex(height)
	
	
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
	
def runbetaeta(Epn, height, fit="linear"):
	gamma = (Epn/nucleonmass) + 1
	beta = math.sqrt(1 - (1/gamma**2))
	
	if fit == "linear":	
		refractiveindex = atm.runindex(height)
	elif fit == "exp":
		refractiveindex = atm.expindex(height)
	
	return beta, refractiveindex
	
	
	
