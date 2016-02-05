import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
import generate as g
import lightdensity as ld
import calculatearea as ca
import calculateellipse as ce
import countsimulation as cs
import telescoperadius as tr
from matplotlib.patches import Ellipse

def run(eff, text=False, graph=False, output="default", layout="five", number=1):
	with open("output/" + output + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Smeared Count", "True X", "True Y", "True Energy per Nucleon", "True Z", "True Height", "Phi", "Epsilon"])
		
		for i in range (0, int(number)):
			
			if graph:
				fig = plt.figure()
			
			else:
				fig=None
	
			rayxpos, rayypos, epsilon, rayradius, Epn, Energy, Z, scale, height, phi, theta = g.run(text=text)
			
			if graph:
				ra, rp, major, minor, e = ce.coeff(rayradius, theta, phi, epsilon)
				distance = 0.5*(ra - rp)
				xcentre = rayxpos - (distance*math.sin(epsilon))
				ycentre = rayypos + (distance*math.cos(epsilon))
				bigring = Ellipse([xcentre, ycentre], width=scale*2*minor, height=scale*2*major, angle=math.degrees(epsilon))
				bigring.set_facecolor('#99FFFF')
				fig.gca().add_artist(bigring)
				corering = Ellipse([xcentre, ycentre], width=2*minor, height=2*major, angle=math.degrees(epsilon))
				corering.set_facecolor('b')
				fig.gca().add_artist(corering)
				fig.gca().plot(rayxpos,rayypos, 'wx')
				fig.gca().plot(xcentre,ycentre, 'rx')
			
			if text:
				print "Cosmic Ray centre at", rayxpos, rayypos
				print "Major axis is", major
	
			with open("orientations/"+ layout +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					category = row[0]
					xpos = float(row[1])
					ypos = float(row[2])
					
					tradius = tr.run(category)
					r = ce.run(rayradius, theta, phi, epsilon, xpos, ypos, rayxpos, rayypos)
					sigcount, bkgcount= cs.run(tradius, r, rayxpos, rayypos, scale, xpos, ypos, Energy, Z, eff)
					
					count = sigcount + bkgcount
					recorded = random.gauss(count, math.sqrt(count))
					
					if graph:
						if float(recorded) > 0:
							circle = plt.Circle((xpos,ypos),tradius, color='r')
						else:
							circle = plt.Circle((xpos,ypos), tradius, color='k')
						fig.gca().add_artist(circle)
					
					if text:
							print "Radius of ring at this angle is", r
							print "Position", xpos, ypos
							print "Photon Count is", count, "smeared to", recorded
							print "Signal accounts for", sigcount, "Background accounts for", bkgcount	
					
					writer.writerow([int(i+1), category, xpos, ypos, recorded, rayxpos, rayypos, Epn, Z, height, phi, epsilon])					
				    
				if graph:
					plt.xlim(-200, 200)
					plt.ylim(-200, 200)
					plt.show()
	
