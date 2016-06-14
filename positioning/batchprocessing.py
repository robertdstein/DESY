import argparse, math, random
import csv
import numpy as np
import telescoperadius as tr

def run(source, outputfile, mincount, detectorcount, text=False):
	with open("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/data/" + str(outputfile) + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		header = []
		for i in range (1, detectorcount + 1):
			header.append("x "+str(i))
			header.append("y "+str(i))
			header.append("Count "+str(i))
			header.append("Bkg Count "+str(i))
			header.append("Telescope "+str(i))
			header.append("Dangle "+str(i))
			header.append("Altitude "+str(i))
		header.append("True X")
		header.append("True Y")
		header.append("True Energy Per Nucleon")
		header.append("True Z")
		header.append("True Height")
		header.append("Detecions")
		header.append("Phi")
		header.append("Epsilon")
		
		header.append("Theta")
		writer.writerow(header)
	
		with open("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/output/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			j = 0
			detections = 0
			a=[]
			for row in reader:
				if i > 0:
					event = row[0]
					category = row[1]
					xpos = float(row[2])
					ypos = float(row[3])
					smearcount = float(row[4])
					smearbkgcount = float(row[5])
					truex = row[6]
					truey =row[7]
					trueE = row[8]
					trueZ = row[9]
					trueheight = row[10]
					phi = row[11]
					epsilon=row[12]
					Trigger = row[13]
					smeardangle = row[14]
					smearamplitude = row[15]
					
					j+=1
				
					if (int(event) == int(i)):
						a += [xpos]
						a += [ypos]
						a += [smearcount]
						a += [smearbkgcount]
						a += [category]
						a += [smeardangle]
						a += [smearamplitude]
						if str(Trigger) == str(True):
							detections += 1
						else:
							pass
						
					if j == detectorcount:
						
						if detections >= float(mincount):
							a += [truex]
							a += [truey]
							a += [trueE]
							a += [trueZ]
							a += [trueheight]
							a += [detections]
							a += [phi]
							a += [epsilon]
							
							writer.writerow(a)
							if text:
								print a
						a=[]
						detections=0
						j = 0
						i +=1			
				else:
					i +=1

