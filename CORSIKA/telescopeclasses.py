import argparse, os, math, random, time, sys, csv, cmath
import os.path
import numpy as np
from sklearn.externals import joblib
from sklearn import ensemble
import cPickle as pickle
import initialisecuts as ic
import re
import cmath

#Enable Plotting on the cluster

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

#Retrieve the cut values for selecting the candidates, stored in a common file initialisecuts.py

arcut, ddireccut, dcogl, dcogu, dlinecut, radiuscut, c1cut = ic.run()
cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

#Define the total number of channels, here 2 (CHannel0/Channel1)
nchannels = 2

#Check to see if the BDT pickle files exist

hess1picklepath = '/nfs/astrop/d6/rstein/BDTpickle/hess1pixelclassifier.p'
hess2picklepath = '/nfs/astrop/d6/rstein/BDTpickle/hess2pixelclassifier.p'
if os.path.isfile(hess1picklepath):
	hess1clf = pickle.load(open(hess1picklepath, "r"))
else:
	print "No hess1 pickle!"
if os.path.isfile(hess2picklepath):
	hess2clf = pickle.load(open(hess2picklepath, "r"))
else:
	print "No hess2 pickle!"
	
#Read in the list of BDT variables top be used for training
	
bdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/pixelBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		bdtvariables.append(row[0])
		
signalbdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/signalBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		signalbdtvariables.append(row[0])

class fullevent:
	"""An event which contains all of the event information 
	for both a full and a hadron-only simulation
	"""
	def __init__(self, runnumber, jobID):
		self.runnumber = runnumber
		self.jobID = jobID
		self.simulationcount = 0
		self.simulations = container()
		
	def addsimulation(self, simcategory):
		"""Add a simulation to the full event. 
		This is either a 'DC simulation' with only hadron interactions, 
		or a full simulation with a background shower
		"""
		newsim = simulation(simcategory)
		setattr(self.simulations, simcategory, newsim)
		self.simulationcount += 1
		return getattr(self.simulations, simcategory)
		
	def makeplots(self, run_dir):
		"""Finds the True DC pixel from the DC simulation, 
		and then produces graphs for both simulations. 
		Graphs are saved to run_dir
		"""
		self.findtrueDCpixel()
		sims = vars(self.simulations)
		for simname in sims:
			sim = getattr(self.simulations, simname)
			sim.plotgraphs(run_dir, self.runnumber)
	
	def findtrueDCpixel(self):
		"""Finds the True DC pixel from the DC simulation, 
		and assigns tel.trueDC to the ID number of this pixel
		in both the full and DC simulation
		"""
		#Checks if there is a DC simulation
		if hasattr(self.simulations, "DC") and hasattr(self.simulations, "full"):
			DCsim = getattr(self.simulations, "DC")
			fullsim = getattr(self.simulations, "full")
			
			#Loops over 'triggered telescopes', identified by Simtel array at those which saw at least 20 p.e
			for index in DCsim.triggerIDs:
				DCtel = DCsim.images[index]
				fulltel = fullsim.images[index]
				bestID = None
				bestsignal = None
				for i in range(len(DCtel.pixels)):
					DCpixelentry = DCtel.pixels[i]
					fullpixelentry = fulltel.pixels[i]
					DCsignal = DCpixelentry.channel1.intensity
					fullpixelentry.truesignal = DCsignal
					if DCsignal > bestsignal:
						bestID=i
						bestsignal=DCsignal
				print bestID
				DCtel.trueDC = bestID
				fulltel.trueDC = bestID
				#Assigns the 'true scores' to each pixel, 1 for the DC pixel and 0 for all other pixels
				#This value is used for BDT training
				if bestID != None:
					fulltel.assignpixelscore()
					DCtel.assignpixelscore()
					
				pix = DCtel.gettruepixel()
				print pix.channel1.intensity,
				pix2 = fulltel.gettruepixel()
				print pix2.truesignal
				
		else:
			raise Exception("Either DC or full simulation missing")
			
	def returnforBDT(self):
		"""Returns a Hess1 and a Hess2 dataset for use in BDT training.
		Also returns a Hess1 and Hess2 true score dataset for use in BDT training
		The results are returned as an array of pixels, without any information
		on the event or telescope
		"""
		if hasattr(self.simulations, "full"):
			fullsim = self.simulations.full
			hess1BDT = []
			hess2BDT = []
			i=0
			j=0
			if hasattr(fullsim.shower, 'shower_azimuth_'):
				for tel in fullsim.images:
					if tel.trueDC != None:
						if tel.size == "HESS1":
							i += 1
						elif tel.size == "HESS2":
							j += 1
						for pixelentry in tel.pixels:
							if tel.size == "HESS1":
								hess1BDT.append(pixelentry)
							elif tel.size == "HESS2":
								hess2BDT.append(pixelentry)
			return hess1BDT, hess2BDT
		else:
			raise Exception("No full simulation exists")
	
class simulation:
	"""One simulation, which can be either full 
	or DC (hadron only) simulation
	"""
	def __init__(self, simcategory):
		self.simcategory = simcategory
		self.images=[]
		self.triggerIDs=[]
		self.shower = container()
		self.filled = False
	
	def addimage(self, size, azimuth, altitude):
		"""Adds a new image to the simulation.
		Takes the size as an argument (HESS1 or HESS2)
		also takes the telescope Azimuth and Zenith angle, as
		found in the SImtel Array output.
		"""
		newimage = telescopeimage(size, azimuth, altitude)
		self.images.append(newimage)

	def gettelescope(self, ID):
		"""Returns the telescope with a specified ID number
		The telescopes are numbered 1-5 by simtelarray
		""" 
		return self.images[int(ID)-1]
	
	def settriggerIDs(self):
		"""Checks each image in the simulation, to see if it was triggered
		creates self.triggerIDS, an array containing the ID number of each 
		telescope that was triggered.
		""" 
		triggered = []
		for i in range(len(self.images)):
			image = self.images[i]
			if image.trigger:
				triggered.append(i)
		self.triggerIDs=triggered
	
	def gettriggeredtelescope(self, ID):
		"""Returns the nth triggered telescope. Numbering is
		assigned by 1-5 if all telescopes are triggered, or
		1-N for N triggered telescopes
		"""
		if (ID-1) > len(self.triggerIDs):
			print "Insufficient triggered telescoped!"
			raise ValueError(ID)
		else:
			index = self.triggerIDs[ID-1]
			return self.images[index]
	
	def setshowerparameters(self, names, values):
		"""For a list of shower parameter names and their values,
		sets the shower parameters as attributes for the event.
		The simtelarray readout gives the parameters/values, which 
		are stored under self.shower.parameter
		""" 
		for i in range(len(names)):
			name = re.sub('[.()]', '', names[i])
			name += "["
			writename = name[:name.find("[")]
			value = float(values[i])
			setattr(self.shower, writename, value)
			
	def extractpixelhillas(self, findBDT):
		"""Using the general shower azimuth and altitude, the hillas parameters
		for each image are calculated. 
		""" 
		if hasattr(self.shower, 'shower_azimuth_') and hasattr(self.shower, 'shower_altitude_'):
			for index in self.triggerIDs:
				tel = self.images[index]
				tel.generatepixelhillasparameters(self.shower.shower_azimuth_, self.shower.shower_altitude_, findBDT)
		else:
			print "No Shower Azimuth and Altitude"
			
	def plotgraphs(self, run_dir, runnumber):
		"""Makes a pdf for a given simulation, comatining a
		plotted image from each camera.
		"""
		figure = plt.figure()
		for i in range(len(self.images)):
			tel = self.images[i]
			tel.plotimage(i, self.simcategory)
		figure.set_size_inches(10, 20)
		plt.subplots_adjust(wspace=0, hspace=0)
		plt.savefig(run_dir + "/graph" + str(runnumber)+ self.simcategory + ".pdf")
		plt.close()
				
		
class telescopeimage:
	"An individual telescope image"
	def initialisepixels(self, targetfile):
		"""Opens a csv file containing either the hess1 or hess2 pixels.
		Each entry containsthe pixel ID, it's x and y position, and the ID
		numbers of it's nearest neighbours
		"""
		with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/data/'+targetfile, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					ID = int(row[0])
					xpos = float(row[1])*self.scale
					ypos=float(row[2])*self.scale
					nn = eval(row[3])
					self.pixels.append(pixel(ID, xpos, ypos, nn))
					
		self.npixels = len(self.pixels)
					
	def __init__(self, size, azimuth, altitude):
		self.size = size
		self.azimuth = azimuth
		self.altitude= altitude
		self.trigger = False
		self.hillas = container()
		self.addedpedestals = 0
		self.addedgains =0
		if self.size == "HESS2":
			self.pixelfile = "hess2pixels.csv"
			self.angularwidth=1.675
			self.imagewidth=105
			self.plotscale =180
			self.mirrorarea=614
		elif self.size == "HESS1":
			self.pixelfile = "hess1pixels.csv"
			self.angularwidth=2.85
			self.imagewidth=70
			self.plotscale =100
			self.mirrorarea=108
		else:
			raise NameError(self.size)
		
		self.scale = self.angularwidth/self.imagewidth
		self.pixels = []
		self.initialisepixels(self.pixelfile)
		self.QDCID = None
		self.BDTID = None
		self.trueDC = None
		self.rawQDCID = None
					
	def getpixel(self, ID):
		"""Returns the pixel with a given ID number
		"""
		return self.pixels[int(ID)]
		
	def addpedestals(self, channel, pedestals):
		"""Adds pedestal values to each pixel.
		The pedestal values are read from Simtelarray as a list
		and the sccript assigns each pedestal to the correct pixel.
		"""
		if self.hasemptypedestals:
			for i in range(len(pedestals)):
				pedestal = float(pedestals[i][:-1])
				currentpixel = self.getpixel(i)
				currentpixel.addpedestal(channel, pedestal)
			self.addedpedestals += 1
		else:
			raise Exception("More than two pedestals!")
	
	def addgains(self, channel, gains):
		"""Adds gain values to each pixel.
		The gain values are read from Simtelarray as a list
		and the sccript assigns each pedestal to the correct pixel.
		"""
		if self.hasemptygains:
			for i in range(len(gains)):
				gain= float(gains[i][:-1])
				currentpixel = self.getpixel(i)
				currentpixel.addgain(channel, gain)
			self.addedgains += 1
		else:
			raise Exception("More than two pedestals!")
		
	def sethillasparameters(self, names, values):
		"""For a list of Hillas parameter names and their values,
		sets the hillas parameters as attributes for the telescope.
		The simtelarray readout gives the parameters/values, which
		are stored under self.hillas.parameter
		""" 
		self.trigger = True
		for i in range(len(names)):
			name = re.sub('[.()]', '', names[i])
			name += "["
			writename = name[:name.find("[")]
			value = float(values[i])
			setattr(self.hillas, writename, value)	
			
	def listhillasparameters(self):
		"""Prints a list of all variables assigned in the
		container self.hillas
		"""
		print vars(self.hillas)
		
	def hasemptypedestals(self):
		"""Checks to see whether both channels have been assigned
		pedestal values. Returns true if not or false if both channels are filled.
		"""
		if self.addedpedestals < nchannels:
			return True
		else:
			return False
			
	def hasemptygains(self):
		"""Checks to see whether both channels have been assigned
		gain values. Returns true if not or false if both channels are filled.
		"""
		if self.addedgains < nchannels:
			return True
		else:
			return False
			
	def findintensities(self):
		"""Checks to see if each pixel has two full channels, containing
		a gain, pedestal and raw count. If so, calculates the intensity
		for each pixel.
		"""
		if (not self.hasemptygains()) and (not self.hasemptypedestals()):
			for pixel in self.pixels:
				if not pixel.hasemptychannels():
					pixel.channel0.getintensity()
					pixel.channel1.getintensity()
				else:
					raise Exception("Not all channels filled!")
		else:
			raise Exception("Not all gains and pedestals filled")
			
	def fillnearestneighbours(self):
		"""For each pixel in the telescope, the Nearest Neaighbour IDs are read.
		Each Neighbour Entry is found, and the Channel 1 intensities are appended to
		an array. This array forms the pixel.nnc1s attribute. The same is done for the Neighbour
		Channel1 raw count, forming the pixel.rawnnc1s attribute.
		"""
		for pixelentry in self.pixels:
			nnIDs = pixelentry.nearestneighbourIDs
			nnc1s = []
			rawnnc1s =[]
			for index in nnIDs:
				neighbour = self.pixels[index]
				c1 = neighbour.channel1.intensity
				nnc1s.append(c1)
				rawc1 = neighbour.channel1.count
				rawnnc1s.append(rawc1)
			pixelentry.nnc1s = nnc1s
			pixelentry.rawnnc1s = rawnnc1s
	
	def plotimage(self, i, simcategory):
		"""Plots each telescope image in a pdf file. The intensity of each pixel
		is illustated in a colour scale, and the x/y axis are swapped to match the
		graphical output of Simtelarray. In addition, the Shower Direction, Center of Gravity
		and QDC/BDT/True pixels are illustrated.
		""" 
		if self.size == "HESS1":
			fig = plt.subplot(4,2,i+1)
		else:
			fig = plt.subplot(2,1,2)
		y=[]
		x=[]
		color = []
		for pixelentry in self.pixels:
			y.append(pixelentry.y)
			x.append(pixelentry.x)
			color.append(pixelentry.channel1.intensity)
		plt.scatter(y, x, s=self.plotscale, c=color, linewidth='0', marker="H", zorder=1, vmin=-1, vmax = 800)
		if not self.trigger:
			plt.annotate("Not \n Triggered", xy=(0.2, 0.5), xycoords="axes fraction", zorder=2, color='w', fontsize=(0.3*self.plotscale))
		
		if simcategory == "full":
			#~ if hasattr(self.hillas, "showery"):
				#~ plt.scatter(self.hillas.showery, self.hillas.showerx, c='w', s=100, marker="o")			
			if hasattr(self.hillas, "image_cog_y_"):
				plt.scatter(self.hillas.image_cog_y_, self.hillas.image_cog_x_, c='w', s=100, marker="x")
			#~ if self.QDCID != None:
				#~ QDCpixel = self.getQDCpixel()
				#~ plt.scatter(QDCpixel.y, QDCpixel.x, facecolors='none', edgecolors="r", s=(self.plotscale*1.2), marker="o", linewidth=2, zorder=4)
			#~ if self.BDTID != None:
				#~ BDTpixel = self.getBDTpixel()
				#~ plt.scatter(BDTpixel.y, BDTpixel.x, facecolors='none', edgecolors="white", s=(self.plotscale*1.2), marker="*", linewidth=2, zorder=3)	
		
		if self.trueDC != None:
			truepixel = self.gettruepixel()
			print truepixel.ID
			plt.scatter(truepixel.y, truepixel.x, facecolors='none', edgecolors="white", s=(self.plotscale*1.2), marker="o", linewidth=2, zorder=3)
			plt.annotate("",
			            xy=(truepixel.y+0.05, truepixel.x+0.05), xycoords='data',
			            xytext=(-0.5, 0.0), textcoords='data',
			            size=20, va="center", ha="center",
			            arrowprops=dict(arrowstyle="simple",
			                            connectionstyle="arc3,rad=-0.2", color="white"), 
			            )
		plt.xlim(-self.angularwidth, self.angularwidth)
		plt.ylim(-self.angularwidth, self.angularwidth)
		plt.axis('off')
		
	def findQDCpixel(self):
		"""Each pixel is checked to see if it passes the HESS cuts.
		Of those that do, the ID of the pixel with the largets QDC value is 
		assigned as the telescope attribute self.QDCID
		""" 
		bestID = None
		bestQDC = 5.0
		if hasattr(self.hillas, "aspect_ratio_"):
			if self.hillas.aspect_ratio_ < arcut:
				for i in range(len(self.pixels)):
					pixelentry = self.pixels[i]
					if pixelentry.ddirec < ddireccut:				
						if dcogl < pixelentry.dcog < dcogu:
							if pixelentry.dline < dlinecut:
								if pixelentry.channel1.intensity < c1cut:
									if pixelentry.QDC < self.qdccut:
										if pixelentry.QDC < bestQDC:
											bestID=i
											bestQDC=pixelentry.QDC
		self.QDCID = bestID
		
	def getQDCpixel(self):
		"""Returns the pixel with the ID matching self.QDCID.
		This is the 'QDC candidate pixel'
		"""
		if self.QDCID != None:
			return self.getpixel(self.QDCID)
		else:
			raise Exception("No QDC pixel!")
			
	def findrawQDCpixel(self):
		"""Each pixel is checked to see if it passes the HESS cuts.
		Of those that do, the ID of the pixel with the largest rawQDC value is 
		assigned as the telescope attribute self.rawQDCID
		""" 
		bestID = None
		bestrawQDC = None
		if hasattr(self.hillas, "aspect_ratio_"):
			if self.hillas.aspect_ratio_ < arcut:
				for i in range(len(self.pixels)):
					pixelentry = self.pixels[i]
					if pixelentry.ddirec < ddireccut:				
						if dcogl < pixelentry.dcog < dcogu:
							if pixelentry.dline < dlinecut:
								if pixelentry.rawQDC > bestrawQDC:
									bestID=i
									bestrawQDC=pixelentry.rawQDC
		self.rawQDCID = bestID
		
	def getrawQDCpixel(self):
		"""Returns the pixel with the ID matching self.rawQDCID
		This is the 'altQDC candidate pixel'.
		"""
		if self.rawQDCID != None:
			return self.getpixel(self.rawQDCID)
		else:
			raise Exception("No raw QDC pixel!")
	
	def gettruepixel(self):
		"""Returns the pixel with the ID matching self.rawQDCID
		This is the 'True DC pixel'.
		"""
		if self.trueDC != None:
			return self.getpixel(self.trueDC)
		else:
			raise Exception("No true DC pixel!")
			
	def findBDTpixel(self):
		"""Each pixel is loaded, and a BDT-format entry is formed
		by using the BDT variable names listed above. Then, if a BDT has been trained for 
		telescopes of the same self.size as the telescope the pixels belong to (HESS1 or HESS2),
		the BDT classifier is used to assign a signal probability. This probability is set
		as the attribute pixelentry.bdtscore. In addition, the pixel with the largest BDT score
		in the telescope image is found, and is selected as the BDT pixel. 
		Its ID is used as the value of self.BDTID
		
		""" 
		bestID = None
		bestscore = None
		if os.path.isfile(hess1picklepath):
			for i in range(len(self.pixels)):
				pixelentry = self.pixels[i]
				bdtentry=[]
				include=True
				for variable in bdtvariables:
					varsplit = variable.split('.')
					suffix = pixelentry
					if len(varsplit) > 1:
						for name in varsplit[:-1]:
							 suffix = getattr(suffix, name)
						varname = varsplit[-1]
					else:
						varname = variable
					if hasattr(suffix, varname):
						newval = getattr(suffix, varname)
						if newval != None:
							bdtentry.append(newval)
						else:
							include=False
					else:
						raise Exception("No variable named " +variable)
				if self.size == "HESS2" and os.path.isfile(hess2picklepath) and include:
					bdtvalues = hess2clf.predict_proba([bdtentry])[0]
					bdtscore = bdtvalues[1]
				elif self.size == "HESS1" and os.path.isfile(hess1picklepath) and include:
					bdtvalues = hess1clf.predict_proba([bdtentry])[0]
					bdtscore = bdtvalues[1]
				else:
					print "self.size error, self.size=" + self.size
					bdtscore = None
				pixelentry.bdtscore = bdtscore
				bdtsum = bdtvalues[0] + bdtvalues[1]
				if bdtsum != 1.0:
					print bdtsum 
				if bdtscore > bestscore:
					bestID=i
					bestscore= bdtscore
		self.BDTID = bestID
		
	def getBDTpixel(self):
		"""Returns the pixel with the ID matching self.BDTID
		This is the 'BDT candidate pixel'.
		"""
		if self.BDTID != None:
			pixelentry = self.getpixel(self.BDTID)
			#~ bdtentry=[]
			#~ for variable in bdtvariables:
				#~ varsplit = variable.split('.')
				#~ suffix = pixelentry
				#~ if len(varsplit) > 1:
					#~ for name in varsplit[:-1]:
						 #~ suffix = getattr(suffix, name)
					#~ varname = varsplit[-1]
				#~ else:
					#~ varname = variable
				#~ if hasattr(suffix, varname):
					#~ newval = getattr(suffix, varname)
					#~ if newval != None:
						#~ bdtentry.append(newval)
					#~ else:
						#~ include=False
				#~ else:
					#~ raise Exception("No variable named " +variable)
			#~ print bdtvariables
			#~ print bdtentry
			return pixelentry
		else:
			raise Exception("No BDT pixel!")
		
	def generatepixelhillasparameters(self, showerazimuth, showeraltitude, findBDT):
		"""Uses the general shower azimuth and altitude to form the various Hillas parameters.
		Firstly the nearest neighbour entries are found. Then the image-specific shower direction is found.
		This is recorded as self.hillas.showerx/y. In addition the aspect ration is found.
		The cog/shower positions are passed as an argument to each pixel, to find the hillas parameters 
		for every pixel.
		"""
		self.fillnearestneighbours()
		cogx = self.hillas.image_cog_x_
		cogy = self.hillas.image_cog_y_
		angle = math.radians(float(self.hillas.orientation_))

		deltaaz = float(showerazimuth) - float(self.azimuth)
		deltaalt= float(showeraltitude) - float(self.altitude) 
		showery=cmath.rect(deltaalt, math.radians(180 - float(showerazimuth))).imag
		showerx=cmath.rect(deltaalt, math.radians(180 - float(showerazimuth))).real
		self.hillas.showery = showery
		self.hillas.showerx = showerx
		
		width=self.hillas.width_
		length=self.hillas.length_
		distance = self.hillas.distance_
		aspectratio = width/length
		self.hillas.aspect_ratio_ = aspectratio
		
		sm = (cogy-showery)/(cogx - showerx)
		sc = showery - (sm * showerx)
		
		itot = self.hillas.image_size_amplitude_
		
		for pixelentry in self.pixels:
			pixelentry.hillas(cogx, cogy, showerx, showery, sm, sc)
			pixelentry.image_size_amplitude_=itot
		
		arg = itot / (math.sin(math.radians(float(self.altitude)))*161)
		self.qdccut = 0.14 * math.log(arg)
				
		self.findQDCpixel()
		self.findrawQDCpixel()
		print "FindBDT is", findBDT,
		if findBDT == "True":
			print True
			self.findBDTpixel()
		else:
			print False
		
	def assignpixelscore(self):
		"""The pixelentry.truescore value is assigned as 0 for every pixel in the
		image, except for the true DC pixel, which has a truescore of 1.
		"""
		if self.trueDC != None:
			for pixelentry in self.pixels:
				pixelentry.truescore = 0
			dcpixel = self.gettruepixel()
			dcpixel.truescore = 1
		else:
			raise Exception("No DC pixel has been identified!")
	
			
class pixel:
	"""A single pixel in a telescope image
	"""
	def __init__(self, ID, x, y, nn):
		self.ID = ID
		self.x = x
		self.y = y
		self.nearestneighbourIDs = nn
		self.channel0 = channelentry()
		self.channel1 = channelentry()
		self.nnc1s = None
		self.bdtscore = None
		self.truescore = None
		
	def addchannelcount(self, channel, count):
		"""Adds the raw count to either Channel 0 or Channel 1
		"""
		if int(channel) == (0):
			self.channel0.count = count
		elif int(channel) == int(1):
			self.channel1.count = count
		else:
			print "Channel does not exist!"
			raise NameError(channel)
			
	def hasemptychannels(self):
		"""Checks to see if a count has been asssigned for
		the pixel channel 0 and channel 1.
		"""
		if (self.channel0.count != None) and (self.channel1.count != None):
			return False
		else:
			return True
			
	def addpedestal(self, channel, pedestal):
		"""Adds the pedestal value to either channel 0 or Channel 1
		"""
		if int(channel) == (0):
			self.channel0.pedestal = pedestal
		elif int(channel) == int(1):
			self.channel1.pedestal = pedestal
		else:
			print "Channel does not exist!"
			raise NameError(channel)
			
	def addgain(self, channel, gain):
		"""Adds the gain value to either Channel 0 or Channel 1.
		"""
		if int(channel) == (0):
			self.channel0.gain = gain
		elif int(channel) == int(1):
			self.channel1.gain = gain
		else:
			print "Channel does not exist!"
			raise NameError(channel)
			
	def hillas(self, cogx, cogy, showerx, showery, sm, sc):
		""" Finds various hillas parameters for the pixel, using the telescope-wide shower
		direction and c.o.g positions.
		"""
		self.dcog = math.sqrt((self.x-cogx)**2 + (self.y-cogy)**2)
		self.ddirec = math.sqrt((self.x-showerx)**2 + (self.y-showery)**2)
		
		m = -1./sm
		c = self.y - (m*self.x)
		intersectionx = (sc - c)/(m-sm)
		intersectiony = (m * intersectionx) + c
		self.dline = math.sqrt((self.x-intersectionx)**2 + (self.y-intersectiony)**2)
		
		if float(self.channel1.intensity) != float(0):
			self.QDC = math.fabs(max([ abs(i) for i in self.nnc1s])/self.channel1.intensity)
		else:
			self.QDC=None
		
		self.rawQDC = math.fabs(max([ abs(i) for i in self.rawnnc1s])/self.channel1.count)
		self.nnmean = np.mean(self.nnc1s)
		self.signalguess = self.channel1.intensity-self.nnmean
		self.nnmax = np.max(self.nnc1s)
		self.nnmin = np.min(self.nnc1s)
		nns=0
		for neighbour in self.nnc1s:
			nns += (neighbour**2)
		self.nnrms = math.sqrt(nns/float(len(self.nnc1s)))
		
class channelentry:
	"""One channel entry in a pixel.
	"""
	def __init__(self):
		self.count = None
		self.gain = None
		self.pedestal = None
		self.intensity = None
		
	def getintensity(self):
		"""If count, pedestal and gain are found, then calculates the intensity.
		I = (count-pedestal)*gain.
		"""
		if (self.count != None) and (self.gain != None) and (self.pedestal != None):
			self.intensity = (self.count - self.pedestal) * self.gain
			#~ print self.count, self.gain, self.pedestal, self.intensity
		else:
			print self.count, self.gain, self.pedestal
			raise Exception("Not all channels initialised!")
			
class container():
	"""An empty container class
	"""
	pass
