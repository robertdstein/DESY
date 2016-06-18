import argparse, math, random, time
import csv
import numpy as np
import generate as g
import lightdensity as ld
import calculatearea as ca
import calculateellipse as ce
import countsimulation as cs
import telescoperadius as tr
				
def run(layout, rayxpos, rayypos, epsilon, rayradius, Epn, Z, height, phi, theta, mincount, eff):
	
	j=1
	
	entry = []
	entrytype = ""

	if rayradius > 0:
		with open("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/orientations/"+ layout +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')

			for row in reader:
				Trigger = False
				category = row[0]
				xpos = float(row[1])
				ypos = float(row[2])
				
				tradius = tr.run(category)
				r, dangle = ce.run(rayradius, theta, phi, epsilon, xpos, ypos, rayxpos, rayypos)
				sigcount, bkgcount, sigerror, bkgerror= cs.run(tradius, r, rayxpos, rayypos, xpos, ypos, Epn, Z, eff)
				
				recorded = int(random.gauss(sigcount, sigerror*sigcount))
				
				bkgrecorded = int(random.gauss(bkgcount, bkgerror*bkgcount))
				
				recordeddangle = random.gauss(dangle, 0.01)
				
				if sigcount > 0:
					distance = math.sqrt(((rayxpos-xpos)**2) + ((rayypos-ypos)**2))
					frac = distance/r
					altitude = frac*((math.pi/2)-theta)
					recordedaltitude = random.gauss(altitude, 0.01)

				else:
					recordedaltitude = "None"

				threshold = ld.trigger()
				
				if float(recorded) > float(threshold):
					j+=1
					Trigger=True
				else:
					recorded=0
						
				if float(bkgrecorded) < float(threshold):
					bkgrecorded=0
					
				#~ print  "Signal", sigcount,"Recorded Signal", recorded, "Background", bkgcount,"Recorded Background", bkgrecorded, "multiplicity", j-1	
				
				entry.append([int(metThreshold+1), category, xpos, ypos, recorded, bkgrecorded, rayxpos, rayypos, Epn, Z, height, phi, epsilon, Trigger, recordeddangle, recordedaltitude])
				
				if float(j) > float(mincount):
					entrytype = "metThreshold"
				else:
					entrytype = "belowThreshold"

	else:
		entrytype = "nonDC"

	return entry, entrytype
