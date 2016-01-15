import argparse, math, random
import csv
import numpy as np

def run(source, outputfile, mincount, detectorcount, text=False):
	with open("data/" + str(outputfile) + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		header = []
		for i in range (1, detectorcount + 1):
			header.append("x"+str(i))
			header.append("y"+str(i))
			header.append("sigcount"+str(i))
			header.append("bkgcount"+str(i))
			header.append("telescope"+str(i))
		header.append("True X")
		header.append("True Y")
		header.append("True Energy Per Nucleon")
		header.append("True Z")
		header.append("True Height")
		header.append("Detecions")
		header.append("Phi")
		writer.writerow(header)
	
		with open("output/"+ str(source) +".csv", 'rb') as csvfile:
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
					sigcount = row[4]
					bkgcount = row[5]
					truex = row[6]
					truey =row[7]
					trueE = row[8]
					trueZ = row[9]
					trueheight = row[10]
					phi = row[11]
					
					j+=1
				
					if (int(event) == int(i)):
						a += [xpos]
						a += [ypos]
						a += [sigcount]
						a += [bkgcount]
						a += [category]
						if ((int(sigcount) == int(0)) & (int(bkgcount) == int(0))):
							pass
						else:
							detections += 1
						
					if j == detectorcount:
						if text:
							print "Total detections:", detections
						if detections >= float(mincount):
							a += [truex]
							a += [truey]
							a += [trueE]
							a += [trueZ]
							a += [trueheight]
							a += [detections]
							a += [phi]
							writer.writerow(a)
						a=[]
						detections=0
						j = 0
						i +=1			
				else:
					i +=1

