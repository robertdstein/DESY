import random, math

p1 = 5.23
p2 = 0.013
oldp3 = -6.508
p3 = 0
p4 = -0.06

def f1(distance, Z):
	#~ print "Distance", distance, "Density", ((Z/26)**2)*(5.23*(math.exp(0.013*distance))-6.508)
	return ((Z/26)**2)*(p1*(math.exp(p2*distance))+p3)
		
def truef1(distance, Z):
	return ((Z/26)**2)*(p1*(math.exp(p2*distance))+oldp3)
		
def f2(distance, Z, rmax):
	return f1(rmax, Z)*math.exp(p4*(distance-rmax))
	
def truef2(distance, Z, rmax):
	return f1(rmax, Z)*math.exp(p4*(distance-rmax))

def run(distance, Epn, Z, rmax, eff, N=56):
	energy=Epn*N/1000
	
	if Epn < 0:
		print distance, Epn, Z, rmax, eff
	
	scale = 73.9 * math.exp(0.025*energy)
	exponent = -0.00004*energy + -0.00692
	
	bkgd = scale * math.e**(distance*exponent)
	
	bkgerror = 0.12

	if distance < rmax:
		density = truef1(distance, Z)
		recondensity = f1(distance, Z)
		dcerror=0.30
		reconerror = 0.12
		if density < 0:
			density=0
		if recondensity < 0:
			recondensity = 0
	else:
		density = truef2(distance, Z, rmax)
		dcerror=0.5
		recondensity = f2(distance, Z, rmax)
		reconerror = 0.21

   	return [density, dcerror], [bkgd, bkgerror], [recondensity, reconerror]
   	
def pcoeffs():
	return p2, p3, p4
   	
def trigger():
	return 20
	
def base(eff):
	return nsbkg * eff
