import random, math

p1 = 5.23
p2 = 0.013
p3 = -6.508
p4 = -0.06

def f1(distance, Z):
		#~ print "Distance", distance, "Density", ((Z/26)**2)*(5.23*(math.exp(0.013*distance))-6.508)
		return ((Z/26)**2)*(p1*(math.exp(p2*distance))+p3)
		
def f2(distance, Z, rmax):
	return f1(rmax, Z)*math.exp(p4*(distance-rmax))

def run(distance, Epn, Z, rmax, eff, N=56):
	rmax = 95
	energy=Epn*N/1000
	
	if Epn < 0:
		print distance, Epn, Z, rmax, eff
	
	scale = 73.9 * math.exp(0.025*energy)
	exponent = -0.00004*energy + -0.00692
	
	bkgd = scale * math.e**(distance*exponent)
	
	bkgerror = 0.15

	if distance < rmax:
		density = f1(distance, Z)
		dcerror=0.15
		if density < 0:
			density=0
	else:
		density = f2(distance, Z, rmax)
		dcerror=1.00

   	return [density, dcerror], [bkgd, bkgerror]
   	
def pcoeffs():
	return p2, p3, p4
   	
def trigger():
	return 20
	
def base(eff):
	return nsbkg * eff
