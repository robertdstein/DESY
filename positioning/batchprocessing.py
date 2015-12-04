import argparse, math, random
import csv
import numpy as np

def run(source, outputfile, mincount, detectorcount):
	with open("data/" + str(outputfile) + ".csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow("a")
	
		with open("output/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			i = 0
			j = 1
			a=[]
			for row in reader:
				if i > 0:
					event = row[0]
					category = row[1]
					xpos = float(row[2])
					ypos = float(row[3])
					count = row[4]
					area = row[5]
					
					j+=1
				
					if (int(event) == int(i)):
						if int(count) != int(0):
							a += [[xpos, ypos, count, area]]
						
					if j == detectorcount:
						if len(a) >= float(mincount):
							writer.writerow(a)
						j = 1
						i +=1			
				else:
					i +=1

