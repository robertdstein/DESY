import random, math

def run(distance, Energy, Z, rmax, scale, eff):
	if distance < rmax*scale:    
		bkgd = 5 * Energy *eff
	else:
		bkgd = 0
	
	if 10 < distance < rmax:    
		density = (Z**2)*((0.62*(math.e**(0.014*(distance-100))))-0.173)*eff
	else:
		density = 0

   	return density, bkgd
