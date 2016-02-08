import numpy as np
import csv

i=0

with open('atmospheredata/atmprofile.csv','wb') as csvout:
	writer = csv.writer(csvout, delimiter=',', quotechar='|')
	with open('atmospheredata/atmprof10.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in reader:
			newrow=[]
			for i in range(0, len(row)):
				if row[i] != '':
					newrow.append(row[i])
			print row
			print newrow
			writer.writerow(newrow)
	
