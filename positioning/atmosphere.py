import numpy as np
import csv, math

def runindex(height, text=False):
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		
		currenth=0
		currentri=0
		
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

def runheight(prob, text=False):
	with open('atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i=0
		h=30000
		currenth=0
		currentt=0
		
		for row in reader:
			i +=1
			t = - 12 * math.log(1 - (prob))
			
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

#~ print runheight(0.001)
#~ print runheight(0.01)
#~ print runheight(0.1)
#~ print runheight(0.5)
#~ print runheight(0.9)
#~ print runheight(0.99)
#~ print runheight(0.999)

	
