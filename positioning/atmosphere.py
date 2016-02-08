import numpy as np
import csv, math

def runindex(height, text=False):
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		for row in reader:
			i +=1		
			
			if height is None:
				print row
			
			if i > 4:
				if float(row[0])*1000 < height:
					pass
				else:
					ri = float(row[3])+1
					if text:
						print float(row[0])*1000, row[3]
						print ri
					return ri

def runheight(prob, text=False):
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		h=30000
		
		for row in reader:
			i +=1
			t = - 6 * math.log(1 - (prob))
			
			if i > 3:
				if float(row[2]) > t:
					pass
				else:
					h = float(row[0])*1000
					
					if text:
						print 
						
					if h > 2000:
						pass
					else:
						print row, h, t
					
					return h
	
