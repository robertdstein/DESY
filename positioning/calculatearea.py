import math
import matplotlib.pyplot as plt

def circleoverlap(tradius, rayradius, distance):
	d=distance
	r=tradius
	R=rayradius
	r2term = (r**2)*math.acos(((d**2) + (r**2) - (R**2))/(2*d*r))
	R2term = (R**2)*math.acos(((d**2) + (R**2) - (r**2))/(2*d*R))
	overlap = 0.5*math.sqrt((-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R))

	area = r2term + R2term - overlap
	return area

def run(tradius, rayradius, distance, scale, x0=0, y0=0, fig=None, graph=False):
	if distance < (tradius + (rayradius*scale)):
		if graph:
			circle=plt.Circle((x0,y0),tradius,color='red')
			fig.gca().add_artist(circle)
		
		area = math.pi*(tradius**2)
		
		if distance < math.fabs(rayradius- tradius):
			siglitarea=area
		elif distance == 0:
			siglitarea=area
		elif distance < (rayradius+ tradius):
			siglitarea = circleoverlap(tradius, rayradius, distance)
		else:
			siglitarea=0
				
		if distance < math.fabs(((rayradius*scale)- tradius)):
			bkglitarea=area
		elif distance == 0:
			bkglitarea=area
		else:
			bkglitarea = circleoverlap(tradius, (rayradius*scale), distance)

	else:
		siglitarea=0
		bkglitarea=0
		if graph:
			circle=plt.Circle((x0,y0),tradius,color="black")
			fig.gca().add_artist(circle)
	
	return siglitarea, bkglitarea
