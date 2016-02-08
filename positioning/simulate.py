import argparse, math, random, time
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

def run(eff, rowcount, mincount=4, text=False, graph=False, output="default", layout="five", number=1):
	with open("output/" + output + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Smeared Count", "True X", "True Y", "True Energy per Nucleon", "True Z", "True Height", "Phi", "Epsilon"])
		
		nonDC = 0
		belowThreshold = 0
		metThreshold = 0
		
		for i in range (0, int(number)):
			
			j=1
			
			entry = []
			
			if graph:
				fig = plt.figure()
			
			else:
				fig=None
	
			rayxpos, rayypos, epsilon, rayradius, Epn, Z, height, phi, theta = g.run(text=text)
			
			if graph:
				ra, rp, major, minor, e = ce.coeff(rayradius, theta, phi, epsilon)
				distance = 0.5*(ra - rp)
				xcentre = rayxpos - (distance*math.sin(epsilon))
				ycentre = rayypos + (distance*math.cos(epsilon))
				ring = Ellipse([xcentre, ycentre], width=2*minor, height=2*major, angle=math.degrees(epsilon))
				ring.set_facecolor('b')
				fig.gca().add_artist(ring)
				fig.gca().plot(rayxpos,rayypos, 'wx')
				fig.gca().plot(xcentre,ycentre, 'rx')
			
			if text:
				print "Cosmic Ray centre at", rayxpos, rayypos
				print "Rayradius is", rayradius
	
			if rayradius > 0:
				with open("orientations/"+ layout +".csv", 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')

					for row in reader:
						Trigger = False
						category = row[0]
						xpos = float(row[1])
						ypos = float(row[2])
						
						tradius = tr.run(category)
						r = ce.run(rayradius, theta, phi, epsilon, xpos, ypos, rayxpos, rayypos)
						sigcount, bkgcount= cs.run(tradius, r, rayxpos, rayypos, xpos, ypos, Epn, Z, eff)
						
						count = sigcount + bkgcount
						recorded = random.gauss(count, math.sqrt(count))
						
						area = math.pi*(tradius**2)
						recondensity=(recorded/area)
						threshold = ld.trigger(eff)
						
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
						
						if float(recondensity) > float(threshold):
							j+=1
							Trigger=True
							if text:
								print j-1, "Trigger Warning!",  recorded, area, recondensity, threshold
						
						elif text:
							print j-1, "No Trigger!",  recorded, area, recondensity, threshold
							
						entry.append([int(metThreshold+1), category, xpos, ypos, recorded, rayxpos, rayypos, Epn, Z, height, phi, epsilon, Trigger])
						
					if float(j) > float(mincount):
						metThreshold += 1
						for i in range(0, rowcount):
							if text:
								print i, entry[i]
							writer.writerow(entry[i])
					else:
						belowThreshold += 1
	
			else:
				nonDC +=1
				pass
				
			if graph:
				plt.xlim(-200, 200)
				plt.ylim(-200, 200)
				plt.show()
		
		print time.asctime(time.localtime()),"In total there were", number, "Simulated Events. Of these", nonDC, "did not produce Cherenkov Light." 
		print time.asctime(time.localtime()),"A further", belowThreshold, "Events produced Cherenkov Light below Threshold, and", metThreshold, "accepted events."
