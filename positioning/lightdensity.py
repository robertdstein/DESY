import random, math

def run(distance, Energy, Z):
	
	bkgd = 5000 * Energy / 100
	
	if 10 < distance < 100:    
		density = (Z**2)*((0.62*(math.e**(0.014*(distance-100))))-0.173)
	
	else:
		density = 0

   	return density, bkgd
