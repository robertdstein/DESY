import argparse, os, math, random, time, sys, csv, cmath
import os.path
import numpy as np
import cPickle as pickle
from sklearn import ensemble
import initialisecuts as ic
import re
import cmath
from telescopeclasses import *

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

arcut, ddireccut, dcogl, dcogu, dlinecut, radiuscut, c1cut = ic.run()
cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

offset="0"

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="1")
parser.add_argument("-jid", "--jobID", default="2842781")

cfg = parser.parse_args()
		
event = fullevent(cfg.runnumber, cfg.jobID)

data_dir = "/nfs/astrop/d6/rstein/data"

result_dir = data_dir + "/" + str(cfg.jobID)
run_dir = os.path.join(result_dir, "run" + str(cfg.runnumber))

for category in ["DC", "full"]:
	base_file_name = os.path.join(run_dir, "run" + str(cfg.runnumber)+ str(category) + "_off" + offset  + "_read_hess_output.txt")
	currentsimulation = event.addsimulation(category)
	print category
	
	if os.path.isfile(base_file_name):
		with open(base_file_name, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			gheader =[]
			hheader = []
			i=1
			for row in reader:
				if len(row) > 4:
					if (row[4] == "Raw:"):
						telaz = row[7]
						telalt = row[11]
						if i < 5:
							currentsimulation.addimage("HESS1", telaz, telalt)
						else:
							currentsimulation.addimage("HESS2", telaz, telalt)
						i+=1
				
				if len(row) > 0:
					if row[0] == "#@+":
						if row[1] == "Lines":
							pass
						elif row[1] == "":
							gheader.append('_'.join(row[3:]))
						else:
							gheader.append('_'.join(row[2::]))
					elif row[0] == "@+":
						gentry = []
						for value in row[1:]:
							if value != "":
								gentry.append(value)
	
						telnumber = gentry[1]
						telescope = currentsimulation.gettelescope(telnumber)
						telescope.sethillasparameters(gheader[2:], gentry[2:])
						currentsimulation.settriggerIDs()
						
					elif row[0] == "#@:":
						if row[1] == "Lines":
							pass
						elif row[1] == "":
							hheader.append('_'.join(row[3:]))
						else:
							hheader.append('_'.join(row[2::]))
					elif row[0] == "@:":				
						hentry = []
						for value in row[1:]:
							if value != "":
								hentry.append(value)
	
						currentsimulation.setshowerparameters(hheader[1:], hentry[1:])
		
		#Add raw count for each pixel in both channels			
		if len(currentsimulation.triggerIDs) > 0:
			with open(base_file_name, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				j = 1
				for row in reader:
					if 8 < len(row) < 15:
						if row[8] == "Pixel":
							pixno = float(row[9][:-1])
							channel = float(row[11][:-1])
							count = float(row[12])
							tel = currentsimulation.gettriggeredtelescope(j)
							if tel.npixels > pixno:
								pass
							else:
								j+=1 
								tel = currentsimulation.gettriggeredtelescope(j)
							
							currentpixel = tel.getpixel(pixno)
							hasempty = currentpixel.hasemptychannels()
		
							if not hasempty:
								j+=1
								tel = currentsimulation.gettriggeredtelescope(j)
								currentpixel = telescope.getpixel(pixno)
								
							currentpixel.addchannelcount(channel, count)
		
			#Add the pedestal and gain for each pixel in both channels
						
			with open(base_file_name, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				j=1
				k=1
				for row in reader:	
					if len(row) > 6 :
						if row[6] == "Pedestals":
							channel = row[8][:-1]
							pedestals = row[10:]
							tel = currentsimulation.gettelescope(j)
							hasemptypedestal = tel.hasemptypedestals()
							if not hasemptypedestal:
								j+=1
								tel = currentsimulation.gettelescope(j)
							tel.addpedestals(channel, pedestals)
							
						elif row[3] == "Gain":
							channel = row[4][:-1]
							gains = row[6:]
							tel = currentsimulation.gettelescope(k)
							hasemptygain = tel.hasemptygains()
							if not hasemptygain:
								k+=1
								tel = currentsimulation.gettelescope(k)
							tel.addgains(channel, gains)
			
			#Calculate the intensity using the count, gain and pedestal for all pixels and both channels
			
			for telID in currentsimulation.triggerIDs:
				tel = currentsimulation.images[telID]
				tel.findintensities()
				print tel.hillas.image_size_amplitude_
			
			currentsimulation.extractpixelhillas()
	
	else:
		print "No files for some reason..."

if event.simulationcount > 0:
	Pickle_dir = os.path.join(run_dir, "pickle")
	if not os.path.exists(Pickle_dir):
		print "Making directory " + Pickle_dir
		os.mkdir(Pickle_dir)
	event.makeplots(run_dir)
	
	print "Saving as pickle file"
	pickle.dump(event, open(Pickle_dir+"/eventdata.p", "wb"))
					
		
					
