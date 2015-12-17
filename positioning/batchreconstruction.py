import argparse, math, random
import csv
import numpy as np
import minimise as m

def run(source, outputfile, detectorcount, rgw, eff):
	with open("reconstructeddata/" + str(outputfile) + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Detections","X","Y","Energy Per Nucleon","Z","Height","True X","True Y","True Energy per nucleon","True Z","True Height"])
		with open("data/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			for row in reader:
				if i == 0:
					i = 1
				else:
					a=[]
					for j in range (0, detectorcount):
						base = 5*j
						a += [[row[base], row[base+1], row[base+2], row[base+3], row[base+4]]]
					guessx, guessy, guessEpn, guessZ, guessHeight =m.min(a, rgw, eff)
					lim = 5*detectorcount
					true = [row[lim], row[lim+1], row[lim+2], row[lim+3], row[lim+4]]
					print "True Values are", true
					writer.writerow([row[lim+5], guessx, guessy, guessEpn, guessZ, guessHeight, row[lim], row[lim+1], row[lim+2], row[lim+3], row[lim+4]])
