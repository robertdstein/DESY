import math

def circleoverlap(tradius, rayradius, distance):
	d=distance
	r=tradius
	R=rayradius
	r2term = (r**2)*math.acos(((d**2) + (r**2) - (R**2))/(2*d*r))
	R2term = (R**2)*math.acos(((d**2) + (R**2) - (r**2))/(2*d*R))
	overlap = 0.5*math.sqrt((-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))

	area = r2term + R2term - overlap
	return area

def run(tradius, rayradius, distance):
	
	area=0
	rawarea = math.pi*(tradius**2)
	
	if rayradius == 0:
		area = 0
	elif (rayradius > tradius):
		if distance < (rayradius - tradius):
			area = rawarea
		elif distance < (rayradius + tradius):
			area = circleoverlap(tradius, rayradius, distance)
	else:
		area=0

	return area
