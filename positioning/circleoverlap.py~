import math

def run(tradius, rayradius, distance):
	d=distance
	r=tradius
	R=rayradius
	r2term = (r**2)*math.acos(((d**2) + (r**2) - (R**2))/(2*d*r))
	R2term = (R**2)*math.acos(((d**2) + (R**2) - (r**2))/(2*d*R))
	overlap = 0.5*math.sqrt((-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))

	area = r2term + R2term - overlap
	return area
