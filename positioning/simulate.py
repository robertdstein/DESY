import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import generate as g
import lightdensity as ld
import circleoverlap as co
from matplotlib.patches import Ellipse

def run(eff, text=False, graph=False, output="default", layout="five", number=1):
	with open("output/" + output + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Sig Count", "Background Count", "Illuminated Signal Area", "Illuminated Background Area"])
		
		for i in range (0, int(number)):
			if graph:
				fig = plt.figure()
	
			rayxpos, rayypos, epsilon, rayradius, Energy, major, minor, ra, rp, e, Z, scale = g.run(text=text)
			
			def frad(angle):
				return major * (1-(e**2))/(1 + (e*math.cos(epsilon- angle)))
			
			if graph:
				distance = 0.5*(ra - rp)
				xcentre = rayxpos - (distance*math.sin(epsilon))
				ycentre = rayypos + (distance*math.cos(epsilon))
				bigshape = Ellipse([xcentre, ycentre], width=scale*2*minor, height=scale*2*major, angle=math.degrees(epsilon))
				fig.gca().add_artist(bigshape)
				fullrange = np.linspace(0, 2*math.pi, 100)
				fig.gca().plot(rayxpos,rayypos, 'ro')
				fig.gca().plot(xcentre,ycentre, 'wo')
				for j in fullrange:
					x = rayxpos + (math.sin(j)*frad(j))
					y = rayypos - (math.cos(j)*frad(j))
					fig.gca().plot(x,y, 'ro')
	
			print "Cosmic Ray centre at", rayxpos, rayypos
			print "Major axis is", major
	
			with open("orientations/"+ layout +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					category = row[0]
					xpos = float(row[1])
					ypos = float(row[2])
					if category == "lst":
						diameter = 23
						colour = 'r'
					elif category == "mst":
						diameter = 12
						colour = 'b'
					elif category == "sst":
						diameter = 4
						colour = 'g'
			
					rawangle = math.atan((math.fabs(xpos-rayxpos))/math.fabs((ypos-rayypos)))
					
					if ((xpos-rayxpos) < 0) & ((ypos-rayypos) > 0):
						dangle = rawangle
					elif ((xpos-rayxpos) < 0) & ((ypos-rayypos) < 0):
						dangle = math.pi - rawangle
					elif ((xpos-rayxpos) > 0) & ((ypos-rayypos) < 0):
						dangle = math.pi + rawangle				
					elif ((xpos-rayxpos) > 0) & ((ypos-rayypos) > 0):
						dangle = (2*math.pi) - rawangle
	
					r = frad(dangle + math.pi)
			
					radius = diameter/2
	            
					distance = math.sqrt((rayxpos - xpos)**2 + (rayypos - ypos)**2)
	            
					density, bkgd = ld.run(distance, Energy, Z, r, scale)
			
					area = (radius**2) * math.pi
			
					if distance < (radius + (r*scale)):
						if graph:
							circle=plt.Circle((xpos,ypos),radius,color='red')
							fig.gca().add_artist(circle)
			
						if distance < (r- radius):
							siglitarea=area
						elif distance < (r+ radius):
							siglitarea = co.run(radius, r, distance)
						else:
							siglitarea=0
								
						if distance < ((r*scale)- radius):
							bkglitarea=area
						else:
							bkglitarea = co.run(radius, (r*scale), distance)

					else:
						siglitarea=0
						bkglitarea=0
						if graph:
							circle=plt.Circle((xpos,ypos),radius,color="black")
							fig.gca().add_artist(circle)
					
					rawsigcount = density*siglitarea*eff
					sigcount = int(random.gauss(rawsigcount, math.sqrt(rawsigcount)))
					bkgcount = int(bkgd*bkglitarea*eff)
					
					if text:
							print "Angle of location", math.degrees(dangle)
							print "Radius of ring at this angle is", r, "Distance = " + str(distance)
							print "Position", xpos, ypos,  "Illuminated signal area is", siglitarea,  "Illuminated Background area is", bkglitarea
							print "Density is", density, ", Photon Count is", count
							print "Signal accounts for", rawsigcount, "Smeared to", sigcount, "Background accounts for", bkgcount	
					writer.writerow([int(i+1), category, xpos, ypos, sigcount, bkgcount, siglitarea, bkglitarea])					
				    
				if graph:
					plt.xlim(-200, 200)
					plt.ylim(-200, 200)
					plt.show()
	
