import argparse, math, random, time
import csv
import numpy as np
import generate as g
import lightdensity as ld
import calculatearea as ca
import calculateellipse as ce
import countsimulation as cs
import telescoperadius as tr
				
def run(layout, rayxpos, rayypos, epsilon, rayradius, Epn, Z, height, phi, theta, mincount, eff, metThreshold=0, graph=False, text=False):
	
	j=1
	
	entry = []
	entrytype = ""

	if graph:
		import matplotlib.pyplot as plt
		from matplotlib.patches import Ellipse		
		fig = plt.figure()
		ra, rp, major, minor, e = ce.coeff(rayradius, theta, phi, epsilon)
		distance = 0.5*(ra - rp)
		xcentre = rayxpos - (distance*math.sin(epsilon))
		ycentre = rayypos + (distance*math.cos(epsilon))
		ring = Ellipse([xcentre, ycentre], width=2*minor, height=2*major, angle=math.degrees(epsilon))
		ring.set_facecolor('b')
		fig.gca().add_artist(ring)
		fig.gca().plot(rayxpos,rayypos, 'wx')
		fig.gca().plot(xcentre,ycentre, 'rx')
	else:
		fig=None
	
	if text:
		print "Cosmic Ray centre at", rayxpos, rayypos
		print "Rayradius is", rayradius

	if rayradius > 0:
		with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/orientations/"+ layout +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')

			for row in reader:
				Trigger = False
				category = row[0]
				xpos = float(row[1])
				ypos = float(row[2])
				
				tradius = tr.run(category)
				r, dangle = ce.run(rayradius, theta, phi, epsilon, xpos, ypos, rayxpos, rayypos)
				sigcount, bkgcount= cs.run(tradius, r, rayxpos, rayypos, xpos, ypos, Epn, Z, eff)
				
				count = sigcount + bkgcount
				recorded = random.gauss(count, math.sqrt(count))
				
				recordeddangle = random.gauss(dangle, 0.01)
				
				if sigcount > 0:
					distance = math.sqrt(((rayxpos-xpos)**2) + ((rayypos-ypos)**2))
					frac = distance/r
					altitude = frac*((math.pi/2)-theta)
					recordedaltitude = random.gauss(altitude, 0.01)

				else:
					recordedaltitude = "None"

				thresholdfrac = ld.trigger()
				threshold = float(bkgcount)*thresholdfrac
				
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
				
				
				if float(sigcount) > float(threshold):
					j+=1
					Trigger=True
					if text:
						print j-1, "Trigger Warning!",  recorded, area, recondensity, threshold
				
				elif text:
					print j-1, "No Trigger!",  recorded, area, recondensity, threshold
					
				entry.append([int(metThreshold+1), category, xpos, ypos, recorded, rayxpos, rayypos, Epn, Z, height, phi, epsilon, Trigger, recordeddangle, recordedaltitude])
				
				if float(j) > float(mincount):
					entrytype = "metThreshold"
				else:
					entrytype = "belowThreshold"

	else:
		entrytype = "nonDC"

	if graph:
		plt.xlim(-200, 200)
		plt.ylim(-200, 200)
		plt.show()
			
	return entry, entrytype
