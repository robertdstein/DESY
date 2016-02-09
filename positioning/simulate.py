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
import looptelescopes as lt
from matplotlib.patches import Ellipse

def run(eff, rowcount, mincount=4, text=False, graph=False, output="default", layout="five", number=1):
	with open("output/" + output + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Event Number", "Category", "Xpos", "Ypos", "Smeared Count", "True X", "True Y", "True Energy per Nucleon", "True Z", "True Height", "Phi", "Epsilon"])
		
		nonDC = 0
		belowThreshold = 0
		metThreshold = 0
		
		for i in range (0, int(number)):
			
			rayxpos, rayypos, epsilon, rayradius, Epn, Z, height, phi, theta = g.run(text=text)
			
			entry, entrytype = lt.run(layout, rayxpos, rayypos, epsilon, rayradius, Epn, Z, height, phi, theta, mincount, eff, metThreshold, graph, text)
					
			if entrytype == "metThreshold":
				metThreshold += 1
				for i in range(0, rowcount):
					if text:
						print i, entry[i]
					writer.writerow(entry[i])
			elif entrytype == "belowThreshold":
				belowThreshold += 1
			elif entrytype == "nonDC":
				nonDC += 1
			else:
				print "ERROR OVER HERE!!!!"
		
		print time.asctime(time.localtime()),"In total there were", number, "Simulated Events. Of these", nonDC, "did not produce Cherenkov Light." 
		print time.asctime(time.localtime()),"A further", belowThreshold, "Events produced Cherenkov Light below Threshold, leaving", metThreshold, "accepted events."
