import argparse, math, random
import csv
import numpy as np
import minimise as m
import loglikelihood as ll

def run(source, outputfile, detectorcount, rgw, eff):
	with open("reconstructeddata/" + str(outputfile) + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Detections","X","Y","Energy Per Nucleon","Z","Height","True X","True Y","True Energy per nucleon","True Z","True Height", "Phi", "Epsilon"])
		with open("data/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			for row in reader:
				if i == 0:
					i = 1
				else:
					a=[]
					for j in range (0, detectorcount):
						base = 4*j
						a += [[row[base], row[base+1], row[base+2], row[base+3]]]
					lim = 4*detectorcount
					
					phi = float(row[lim+6])
					smearphi = phi + (math.radians(0.5)*(random.random()-0.5))

					epsilon = float(row[lim+7])
					smearepsilon = epsilon + (math.radians(0.5)*(random.random()-0.5))
					
					true = [row[lim], row[lim+1], row[lim+2], row[lim+3], row[lim+4], math.degrees(phi), math.degrees(epsilon)]
					
					def f(x,y,Z,Epn, height):
						sum = 0
						for detection in a:
							x0 = float(detection[0])
							y0 = float(detection[1])
							count = float(detection[2])
							category = detection[3]
							sum += ll.run(x,y,Epn,Z, height, x0,y0, count, category, eff, smearphi, smearepsilon)
						return sum
					
					guessx, guessy, guessEpn, guessZ, guessHeight =m.min(a, rgw, eff, smearphi, smearepsilon)

					print "True Values are", true, "(", f(float(row[lim]), float(row[lim+1]), float(row[lim+3]), float(row[lim+2]), float(row[lim+4])), ")"
					
					writer.writerow([row[lim+5], guessx, guessy, guessEpn, guessZ, guessHeight, row[lim], row[lim+1], row[lim+2], row[lim+3], row[lim+4], row[lim+6], row[lim+7]])
