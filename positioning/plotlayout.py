import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import generate as g
import lightdensity as ld
import circleoverlap as co
from matplotlib.patches import Ellipse

parser = argparse.ArgumentParser(description='Create a canvas for positions of telescopes')
parser.add_argument("-s", "--source", default="five")
parser.add_argument("-o", "--output", default="default")
parser.add_argument("-t", "--text", action="store_true")
parser.add_argument("-g", "--graph", action="store_true")
parser.add_argument("-n", "--number", default=1)
cfg = parser.parse_args()

#Set Efficiency
eff = 1.0

with open("output/" + cfg.output + ".csv", 'wb') as csvout:
	writer = csv.writer(csvout, delimiter=',', quotechar='|')
	writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Photon Count", "Illuminated Area"])
	
	for i in range (0, int(cfg.number)):
		if cfg.graph:
			fig = plt.figure()

		rayxpos, rayypos, epsilon, rayradius, Energy, major, minor, ra, rp, e, Z = g.run(text=cfg.text)
		
		def frad(angle):
			return major * (1-(e**2))/(1 + (e*math.cos(epsilon- angle)))
		
		if cfg.graph:
			distance = 0.5*(ra - rp)
			xcentre = rayxpos - (distance*math.sin(epsilon))
			ycentre = rayypos + (distance*math.cos(epsilon))
			shape = Ellipse([xcentre, ycentre], width=2*minor, height=2*major, angle=math.degrees(epsilon))
			fig.gca().add_artist(shape)
			fullrange = np.linspace(0, 2*math.pi, 100)
			fig.gca().plot(rayxpos,rayypos, 'ro')
			fig.gca().plot(xcentre,ycentre, 'wo')
			for i in fullrange:
				x = rayxpos + (math.sin(i)*frad(i))
				y = rayypos - (math.cos(i)*frad(i))
				fig.gca().plot(x,y, 'ro')

		if cfg.text:
			print "Cosmic Ray centre at", rayxpos, rayypos

		with open("orientations/"+ cfg.source +".csv", 'rb') as csvfile:
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
            
				density, bkgd = ld.run(distance, Energy, Z)
		
				area = (radius**2) * math.pi
		
				if distance < (radius + r):
					if cfg.graph:
						circle=plt.Circle((xpos,ypos),radius,color='red')
						fig.gca().add_artist(circle)
		
					if distance < (r- radius):
						litarea=area
						if cfg.text:
							print "FULL ILLUMINATION!!!!!", 
						rawsigcount = density*litarea*eff
						sigcount = int(random.gauss(rawsigcount, math.sqrt(rawsigcount)))
						bkgcount = int(bkgd*area*eff)
						count = sigcount+bkgcount

					else:
						litarea = co.run(radius, r, distance)		
						if cfg.text:
							print "PARTIAL ILLUMINATION!!!!!", 
						rawsigcount = density*litarea*eff				
						sigcount = int(random.gauss(rawsigcount, math.sqrt(rawsigcount)))
						bkgcount = int(bkgd*area*eff)
						count = sigcount+bkgcount
			
					if cfg.text:
						print "Angle of location", math.degrees(dangle)
						print "Radius of ring at this angle is", r, "Distance = " + str(distance)
						print "Position", xpos, ypos,  "Illuminated area is", litarea
						print "Density is", density, ", Photon Count is", count
						print "Signal accounts for", rawsigcount, "Smeared to", sigcount, "Background accounts for", bkgcount

				else:
					sigcount = 0
					bkgcount = 0
					litarea=0
					count = sigcount+bkgcount
					if cfg.graph:
						print "Radius of ring at this angle is", r, "Distance = " + str(distance), "Angle of location", math.degrees(dangle)
						circle=plt.Circle((xpos,ypos),radius,color="black")
						fig.gca().add_artist(circle)
						
				writer.writerow([i+1, category, xpos, ypos, count, litarea])					
			    
			if cfg.graph:
				plt.xlim(-300, 300)
				plt.ylim(-300, 300)
				plt.show()
