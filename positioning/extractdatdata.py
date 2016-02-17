import numpy as np
import csv

i=0

setwavelength = 400

with open('atmospheredata/atmabs.csv','wb') as csvout:
	writer = csv.writer(csvout, delimiter=',', quotechar='|')
	with open('atmospheredata/atmabs.dat', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		j = -1
		newrow=[]
		wavelength = 0
		
		for row in reader:
			j +=1
			
			if j == 0:
				pass
			
			else:
				for i in range(0, len(row)):
					if row[i] != '':
						newentry = row[i]
						if float(wavelength) == float(setwavelength):
							print newentry
							writer.writerow([newentry])
							
				if j == 1:
					wavelength = newentry
				
				if j > 6:
					j=0
	
