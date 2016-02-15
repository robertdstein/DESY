import random, math

nsbkg = 7

def run(distance, Epn, Z, rmax, eff):
	
	scale = (50 * (10**-3)* Epn *eff)
	
	if distance < 100:
		bkgd = (math.e**((50-distance)/100))*scale + (nsbkg*eff)
	else:
		bkgd = (nsbkg*eff)+(math.e**((90-distance)/20))*scale
	
	if 10 < distance < rmax:
		density = (Z**2)*((0.62*(math.e**(0.014*(distance-100))))-0.173)*eff
	else:
		density = 0

   	return density, bkgd
   	
def trigger(eff):
	return 1.5 * nsbkg * eff
	
def base(eff):
	return nsbkg * eff
