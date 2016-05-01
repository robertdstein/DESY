import argparse, os, math, random, time, sys, csv, cmath
import os.path
import numpy as np
from sklearn.externals import joblib
from sklearn import ensemble
import initialisecuts as ic

offset="0"

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="1")
parser.add_argument("-jid", "--jobID", default="2842781")

cfg = parser.parse_args()

nchannels = 2

class fullevent:
	"An event which contains all of the event information for both a full and a hadron-only simulation"
	def __init__(self):
		self.runnumber = cfg.runnumber
		self.jobID = cfg.jobID
		self.simulationcount = 0
		self.simulations = []
		
	def addsimulation(self, simcategory):
		newsim = simulation(simcategory)
		self.simulations.append(newsim)
		self.simulationcount += 1
		return self.simulations[self.simulationcount-1]
	
class simulation:
	"One simulation, which can be either full or hadron simulation"
	def __init__(self, simcategory):
		self.simcategory = simcategory
		self.images=[]
		self.triggerIDs=[]
	
	def addimage(self, size, azimuth, zenith):
		newimage = telescopeimage(size, azimuth, zenith)
		self.images.append(newimage)

	def isbkgfree(self):
		if self.simcategory == "DC":
			return True
		elif self.simcategory == "full":
			return False
		else:
			raise NameError(self.simcategory)
	
	def extractparameters(self):
		print "Something..."
		
	def gettelescope(self, ID):
		return self.images[int(ID)-1]
	
	def settriggerIDs(self):
		triggered = []
		for i in range(len(self.images)):
			image = self.images[i]
			if image.trigger:
				triggered.append(i)
		self.triggerIDs=triggered
	
	def gettriggeredtelescope(self, ID):
		if (ID-1) > len(self.triggerIDs):
			print "Insufficient triggered telescoped!"
			raise ValueError(ID)
		else:
			index = self.triggerIDs[ID-1]
			return self.images[index]

class telescopeimage:
	"An individual telescope image"
	def initialisepixels(self, targetfile):
		with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/data/'+targetfile, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					ID = int(row[0])
					xpos = float(row[1])*self.scale
					ypos=float(row[2])*self.scale
					nn = eval(row[3])
					self.pixels.append(pixel(ID, xpos, ypos, nn))
					
		self.npixels = len(self.pixels)
					
	def __init__(self, size, azimuth, zenith):
		self.size = size
		self.azimuth = azimuth
		self.zenith = size
		self.trigger = False
		self.hillas = container()
		self.addedpedestals = 0
		self.addedgains =0
		if self.size == "HESS2":
			self.pixelfile = "hess2pixels.csv"
			self.angularwidth=1.675
			self.imagewidth=105
		elif self.size == "HESS1":
			self.pixelfile = "hess1pixels.csv"
			self.angularwidth=2.85
			self.imagewidth=70
		else:
			raise NameError(self.size)
		
		self.scale = self.angularwidth/self.imagewidth
		self.pixels = []
		self.initialisepixels(self.pixelfile)
					
	def getpixel(self, ID):
		return self.pixels[int(ID)]
		
	def addpedestals(self, channel, pedestals):
		if self.hasemptypedestals:
			for i in range(len(pedestals)):
				pedestal = float(pedestals[i][:-1])
				currentpixel = self.getpixel(i)
				currentpixel.addpedestal(channel, pedestal)
			self.addedpedestals += 1
		else:
			raise Exception("More than two pedestals!")
	
	def addgains(self, channel, gains):
		if self.hasemptygains:
			for i in range(len(gains)):
				gain= float(gains[i][:-1])
				currentpixel = self.getpixel(i)
				currentpixel.addgain(channel, gain)
			self.addedgains += 1
		else:
			raise Exception("More than two pedestals!")
		
	def sethillasparameters(self, names, values):
		self.trigger = True
		for i in range(len(names)):
			name = names[i]
			value = values[i]
			setattr(self.hillas, name, value)	
			
	def listhillasparameters(self):
		print vars(self.hillas)
		
	def hasemptypedestals(self):
		if self.addedpedestals < nchannels:
			return True
		else:
			return False
			
	def hasemptygains(self):
		if self.addedgains < nchannels:
			return True
		else:
			return False
			
	def findintensities(self):
		if (not self.hasemptygains()) and (not self.hasemptypedestals()):
			for pixel in self.pixels:
				if not pixel.hasemptychannels():
					print "Channel0", 
					pixel.channel0.getintensity()
					print "Channel1", 
					pixel.channel1.getintensity()
				else:
					raise Exception("Not all channels filled!")
		else:
			raise Exception("Not all gains and pedestals filled")
			
class pixel:
	"A single pixel in a telescope image"
	def __init__(self, ID, x, y, nn):
		self.ID = ID
		self.x = x
		self.y = y
		self.nearestneighbourIDs = nn
		self.imagedata = False
		self.channel0 = channelentry()
		self.channel1 = channelentry()
		
	def getentry(self):
		return [self.ID, self.x, self.y, self.nearestneighbourIDs]
		
	def addchannelcount(self, channel, count):
		if int(channel) == (0):
			self.channel0.count = count
		elif int(channel) == int(1):
			self.channel1.count = count
		else:
			print "Channel does not exist!"
			raise NameError(channel)
			
	def hasemptychannels(self):
		if (self.channel0.count != None) and (self.channel1.count != None):
			return False
		else:
			return True
			
	def addpedestal(self, channel, pedestal):
		if int(channel) == (0):
			self.channel0.pedestal = pedestal
		elif int(channel) == int(1):
			self.channel1.pedestal = pedestal
		else:
			print "Channel does not exist!"
			raise NameError(channel)
			
	def addgain(self, channel, gain):
		if int(channel) == (0):
			self.channel0.gain = gain
		elif int(channel) == int(1):
			self.channel1.gain = gain
		else:
			print "Channel does not exist!"
			raise NameError(channel)

class channelentry:
	"One channel entry in a pixel"
	def __init__(self):
		self.count = None
		self.gain = None
		self.pedestal = None
		self.intensity = None
		
	def getintensity(self):
		if (self.count != None) and (self.gain != None) and (self.pedestal != None):
			self.intensity = (self.count - self.pedestal) * self.gain
			#~ print self.count, self.gain, self.pedestal, self.intensity
		else:
			print self.count, self.gain, self.pedestal
			raise Exception("Not all channels initialised!")
			
class container():
	pass
		
event = fullevent()

data_dir = "/nfs/astrop/d6/rstein/data"

result_dir = data_dir + "/" + str(cfg.jobID)
run_dir = os.path.join(result_dir, "run" + str(cfg.runnumber))

Pickle_dir = os.path.join(run_dir, "pickle")
if not os.path.exists(Pickle_dir):
	print "Making directory " + Pickle_dir
	os.mkdir(Pickle_dir)

for category in ["DC", "full"]:
	base_file_name = os.path.join(run_dir, "run" + str(cfg.runnumber)+ str(category) + "_off" + offset  + "_read_hess_output.txt")
	currentsimulation = event.addsimulation(category)
	print category
	
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
				if row[0] == "@+":
					gentry = []
					for value in row[1:]:
						if value != "":
							gentry.append(value)

					telnumber = gentry[1]
					telescope = currentsimulation.gettelescope(telnumber)
					telescope.sethillasparameters(gheader[2:], gentry[2:])
					currentsimulation.settriggerIDs()
	
	with open(base_file_name, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		j = 1
		for row in reader:
			if 8 < len(row) < 15:
				if row[8] == "Pixel":
					pixno = float(row[9][:-1])
					channel = float(row[11][:-1])
					count = float(row[12])
					telescope = currentsimulation.gettriggeredtelescope(j)
					if telescope.npixels > pixno:
						pass
					else:
						j+=1 
						telescope = currentsimulation.gettriggeredtelescope(j)
					
					currentpixel = telescope.getpixel(pixno)
					hasempty = currentpixel.hasemptychannels()

					if not hasempty:
						j+=1
						telescope = currentsimulation.gettriggeredtelescope(j)
						currentpixel = telescope.getpixel(pixno)
						
					currentpixel.addchannelcount(channel, count)
					
	with open(base_file_name, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		j=1
		k=1
		for row in reader:	
			if len(row) > 6 :
				if row[6] == "Pedestals":
					channel = row[8][:-1]
					pedestals = row[10:]
					telescope = currentsimulation.gettelescope(j)
					hasemptypedestal = telescope.hasemptypedestals()
					if not hasemptypedestal:
						j+=1
						telescope = currentsimulation.gettelescope(j)
					print "Channel", channel, len(row), len(pedestals), j, "Pedestal"
					telescope.addpedestals(channel, pedestals)
					
				elif row[3] == "Gain":
					channel = row[4][:-1]
					gains = row[6:]
					telescope = currentsimulation.gettelescope(k)
					hasemptygain = telescope.hasemptygains()
					if not hasemptygain:
						k+=1
						telescope = currentsimulation.gettelescope(k)
					print "Channel", channel, len(row), len(gains), k, "Gain"
					telescope.addgains(channel, gains)
	
	for telID in currentsimulation.triggerIDs:
		print telID
		telescope = currentsimulation.images[telID]
		telescope.findintensities()
					
					
					
		
					
