import numpy as np
import csv, math

def runindex(height, text=False):
	with open('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		
		currenth=0
		currentri=0
		
		ri = 1 + (4.12908*(10**-6))
		
		for row in reader:
			i +=1
			if i > 3:
				previousri = currentri
				currentri = float(row[3])
				previoush = currenth
				currenth = float(row[0])*1000
				if currenth < height:
					pass
				else:
					gradient = (float(currentri)-float(previousri))/(float(currenth)-float(previoush))
					deltah = height - currenth
					
					ri = currentri + (deltah*gradient) + 1
					
					if text:
						print float(row[0])*1000, row[3]
						print ri
					return ri
		return ri

def runheight(prob, text=False):
	with open('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		h=30000
		currenth=0
		currentt=0
		
		for row in reader:
			i +=1
			
			t = runlengths(prob)
			
			if i > 3:
				previoust = currentt
				currentt = float(row[2])
				previoush = currenth
				currenth = float(row[0])*1000
				if float(row[2]) > t:
					pass
				else:
					gradient = (float(currenth)-float(previoush))/(float(currentt)-float(previoust))
					deltat = t - previoust
					
					h = currenth + (deltat*gradient)
					
					if text:
						print row, h, t, prob, float(h)
					
					return h
		return h
		
def runlengths(prob):
	scale = 8
	
	lengths = -scale*(math.log(1-prob))
	return lengths
	
def runabsorption(height, text=False):
	with open('/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		
		currenth=0
		currentb=0
		
		b = 0
		frac = 1
		
		for row in reader:
			i +=1
			if i > 3:
				previousb = currentb
				currentb = float(row[7])
				previoush = currenth
				currenth = float(row[0])*1000
				if currenth < height:
					pass
				else:
					gradient = (float(currentb)-float(previousb))/(float(currenth)-float(previoush))
					deltah = height - currenth
					
					b = currentb + (deltah*gradient)
					
					frac = math.e**-b
					
					return frac
		return frac
	
