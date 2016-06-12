import random, math

def run(distance, Epn, Z, rmax, eff, N=56):
	
	energy=Epn*N/1000
	
	if Epn < 0:
		print distance, Epn, Z, rmax, eff
	
	scale = (9.4*energy + -204.1)
	exponent = -0.00004*energy + -0.00692
	
	bkgd = scale * math.e**(distance*exponent)
	
	bkgerror = 0.15
	
	def f1(distance):
		#~ print "Distance", distance, "Density", ((Z/26)**2)*(5.23*(math.exp(0.013*distance))-6.508)
		return ((Z/26)**2)*(5.23*(math.exp(0.013*distance))-6.508)
		
	def f2(distance):
		return f1(rmax)*math.exp(-rmax-(0.06*distance))
	
	if distance < rmax:
		density = f1(distance)
		dcerror=0.19
		if density < 0:
			density=0
	else:
		density = f2(distance)
		dcerror=0.85

	print "Density", density, "Distance", distance 

   	return [density, dcerror], [bkgd, bkgerror]
   	
def trigger():
	return 1.5
	
def base(eff):
	return nsbkg * eff
