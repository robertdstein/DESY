import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import generate as g
import lightdensity as ld
import calculatearea as ca
import countsimulation as cs
import telescoperadius as tr
from matplotlib.patches import Ellipse

def run(eff, text=False, graph=False, output="default", layout="five", number=1):
	with open("output/" + output + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Sig Count", "Background Count", "True X", "True Y", "True Energy per Nucleon", "True Z", "True Height", "Phi"])
		
		for i in range (0, int(number)):
			
			if graph:
				fig = plt.figure()
			
			else:
				fig=None
	
			rayxpos, rayypos, epsilon, rayradius, Energy, Epn, major, minor, ra, rp, e, Z, scale, height, phi = g.run(text=text)
			
			def frad(angle):
				return major * (1-(e**2))/(1 + (e*math.cos(epsilon- angle)))
			
			if graph:
				distance = 0.5*(ra - rp)
				xcentre = rayxpos - (distance*math.sin(epsilon))
				ycentre = rayypos + (distance*math.cos(epsilon))
				bigshape = Ellipse([xcentre, ycentre], width=scale*2*minor, height=scale*2*major, angle=math.degrees(epsilon))
				fig.gca().add_artist(bigshape)
				fullrange = np.linspace(0, 2*math.pi, 100)
				fig.gca().plot(rayxpos,rayypos, 'wo')
				fig.gca().plot(xcentre,ycentre, 'ro')
				for j in fullrange:
					x = rayxpos + (math.sin(j)*frad(j))
					y = rayypos - (math.cos(j)*frad(j))
					fig.gca().plot(x,y, 'wo')
			
			if text:
				print "Cosmic Ray centre at", rayxpos, rayypos
				print "Major axis is", major
	
			with open("orientations/"+ layout +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					category = row[0]
					xpos = float(row[1])
					ypos = float(row[2])
					
					radius = tr.run(category)
			
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
					
					sigcount, bkgcount= cs.run(radius, r, rayxpos, rayypos, scale, xpos, ypos, Energy, Z, eff)
					
					count = sigcount + bkgcount
					#recorded = math.gauss(count, math.sqrt(count))
					
					if text:
							print "Angle of location", math.degrees(dangle)
							print "Radius of ring at this angle is", r
							print "Position", xpos, ypos
							print "Photon Count is", count, "smeared to", recorded
							print "Signal accounts for", sigcount, "Background accounts for", bkgcount	
					
					writer.writerow([int(i+1), category, xpos, ypos, sigcount, bkgcount, rayxpos, rayypos, Epn, Z, height, phi])					
				    
				if graph:
					plt.xlim(-200, 200)
					plt.ylim(-200, 200)
					plt.show()
	
