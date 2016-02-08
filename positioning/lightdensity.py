import random, math

nsbkg = 7

def run(distance, Epn, Z, rmax, eff):
	if distance < rmax*1.2:
		bkgd = (5 * (10**-3)* Epn * Z *eff) + (nsbkg*eff)
	else:
		bkgd = (nsbkg*eff)
	
	if 10 < distance < rmax:    
		density = (Z**2)*((0.62*(math.e**(0.014*(distance-100))))-0.173)*eff
	else:
		density = 0

   	return density, bkgd
   	
def trigger(eff):
	return 1.5 * nsbkg * eff
	
def base(eff):
	return nsbkg * eff
