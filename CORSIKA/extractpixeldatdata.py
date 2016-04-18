import numpy as np
import csv, math

combos = [["hess1pixels.csv", "hess/hess_camera.dat"], ["hess2pixels.csv", "hess2/large_drawer_camera.dat"]]

radius = 4.3

for entry in combos:
	pixels=[]
	
	#Extract pixel locations
	
	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/data/' + entry[0], 'w+') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		with open('/nfs/astrop/d6/rstein/corsika_simtelarray/sim_telarray/cfg/' + entry[1], 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in reader:
				if len(row) > 0:
					if row[0] == "Pixel":
						newentry = []
						i=1
						while len(newentry) < 4:
							if row[i] != "":
								newentry.append(row[i])
							i+=1
						writer.writerow([newentry[0], newentry[2], newentry[3]])
						pixels.append([newentry[0], newentry[2], newentry[3]])
	
	#Identify nearest neighbours for each pixel
						
	for pixel in pixels:
		xpos = float(pixel[1])
		ypos = float(pixel[2])
		
		nearestneighbours = []
		
		with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/data/' + entry[0], 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in reader:
				ID = int(row[0])
				currentxpos = float(row[1])
				currentypos=float(row[2])
				
				if math.fabs(currentxpos - xpos) < radius:
					if math.fabs(currentypos - ypos) < radius:
						if math.fabs(currentypos - ypos) + math.fabs(currentxpos - xpos) > 0:
							nearestneighbours.append(ID)
		
		pixel.append(nearestneighbours)
		
	#Rewrite csvfile with nearest neightbour ID numbers

	with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/data/' + entry[0], 'w+') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		for pixel in pixels:
			writer.writerow(pixel)
		

		
