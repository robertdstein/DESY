import numpy as np
import csv, math
from scipy.optimize import curve_fit

#Provides the Refractive Index for a given Height

def expindex(height, fit=False, text=False):
	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		#Provides starting values to avoid errors in extreme cases
		
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
				
				#Finds nearest height entry above given height
				
				if currenth < height:
					pass
				else:
					
					#Interpolates refractive Index given Index and Height step size from previous entry

					K, A_log = np.polyfit([currenth, previoush], [math.log(currentri), math.log(previousri)], 1)
					A = np.exp(A_log)
					
					ri =  1 + (A * math.e**(K*height))
					
					if text:
						print float(row[0])*1000, row[3]
						print ri
					return ri
		return ri
		
#Provides a Height corresponding to a given Probability

def runheight(prob, text=False):
	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		#Provides starting values to avoid errors in extreme cases

		i=0
		h=30000
		currenth=0
		currentt=0
		
		for row in reader:
			i +=1
			
			t = runlengths(prob)
			
			if i > 3:
				
				#Finds nearest decay length entry above given decay lengths
				
				previoust = currentt
				currentt = float(row[2])
				previoush = currenth
				currenth = float(row[0])*1000
				
				if float(row[2]) > t:
					pass
				else:
					
					#Interpolates height given Decay Lengths and Height step size from previous entry
					
					gradient = (float(currenth)-float(previoush))/(float(currentt)-float(previoust))
					deltat = t - previoust
					
					h = currenth + (deltat*gradient)
					
					if text:
						print row, h, t, prob, float(h)
					
					return h
		return h
		
#Convert a Probability to a number of decay Lengths, with a mean of 8
#Assumes with P=0 for immediate decay at top of atmosphere and P=1 for survival to ground
		
def runlengths(prob):
	scale = 12.0
	
	lengths = -scale*(math.log(1-prob))
	return lengths
	
def runlengthswithh(h, text=False):
	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		#Provides starting values to avoid errors in extreme cases

		i=0
		currenth=0
		currentt=0
		t=0
		
		for row in reader:
			i +=1
			
			if i > 3:
				
				#Finds nearest decay length entry above given decay lengths
				
				previoust = currentt
				currentt = float(row[2])
				previoush = currenth
				currenth = float(row[0])*1000
				
				if currenth < h:
					pass
				else:
					
					#Interpolates height given Decay Lengths and Height step size from previous entry
					
					gradient =(float(currentt)-float(previoust))/(float(currenth)-float(previoush))
					deltah = h - previoush
					
					t = currentt + (deltah*gradient)
					
					if text:
						print row, h, t, prob, float(h)
					
					return t
		return t
	
#Calculates the fraction of Transmitted Light from a given height that will reach the ground
#Assumes absorbtion fraction at first interaction covers preceding emission too (this is reasonable as f~54% for almost all decay height)
	
def runabsorption(height, text=False):
	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
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
		
def runindex(height, fit=False, text=False):
	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/atmospheredata/atmprofile.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		#Provides starting values to avoid errors in extreme cases
		
		i=0
		
		currenth=0
		currentri=0
		
		ri=1
		
		for row in reader:
			i +=1
			if i > 3:
				
				previousri = currentri
				currentri = float(row[3])
				previoush = currenth
				currenth = float(row[0])*1000
				
				#Finds nearest height entry above given height
				
				if currenth < height:
					pass
				else:
					#~ print "Height", height, currenth, previoush, currentri, previousri
					#Interpolates refractive Index given Index and Height step size from previous entry
					#~ print currentri, previousri, previoush, height, currenth, ri
					gradient = (float(currentri)-float(previousri))/(float(currenth)-float(previoush))
					deltah = height - previoush
					
					ri = previousri + (deltah*gradient) + 1
					
					
					
					#~ m, c = np.polyfit([currenth, previoush], [currentri, previousri], 1)
					
					#~ ri =  1 + (m*height) + c
					
					if text:
						print float(row[0])*1000, row[3]
						print ri
					return ri
		return ri
	
