import argparse, os, math, random, time, sys, csv, cmath
import os.path
import numpy as np
from sklearn.externals import joblib
from sklearn import ensemble
import cPickle as pickle
import initialisecuts as ic
import re
import cmath

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

arcut, ddireccut, dcogl, dcogu, dlinecut, radiuscut = ic.run()
cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

nchannels = 2

hess1picklepath = '/nfs/astrop/d6/rstein/BDTpickle/hess1pixelclassifier.p'
hess2picklepath = '/nfs/astrop/d6/rstein/BDTpickle/hess2pixelclassifier.p'
if os.path.isfile(hess1picklepath):
	hess1clf = pickle.load(open(hess1picklepath, "r"))
if os.path.isfile(hess2picklepath):
	hess2clf = pickle.load(open(hess2picklepath, "r"))
else:
	print "No pickle!"
	
bdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/pixelBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		bdtvariables.append(row[0])

class fullevent:
	"An event which contains all of the event information for both a full and a hadron-only simulation"
	def __init__(self, runnumber, jobID):
		self.runnumber = runnumber
		self.jobID = jobID
		self.simulationcount = 0
		self.simulations = container()
		
	def addsimulation(self, simcategory):
		newsim = simulation(simcategory)
		setattr(self.simulations, simcategory, newsim)
		self.simulationcount += 1
		return getattr(self.simulations, simcategory)
		
	def makeplots(self, run_dir):
		self.findtrueDCpixel()
		sims = vars(self.simulations)
		for simname in sims:
			sim = getattr(self.simulations, simname)
			sim.plotgraphs(run_dir, self.runnumber)
	
	def findtrueDCpixel(self):
		if hasattr(self.simulations, "DC"):
			DCsim = getattr(self.simulations, "DC")
			for index in DCsim.triggerIDs:
				tel = DCsim.images[index]
				bestID = None
				bestsignal = None
				for i in range(len(tel.pixels)):
					pixelentry = tel.pixels[i]
					if pixelentry.channel1.intensity > bestsignal:
						bestID=i
						bestsignal=pixelentry.channel1.intensity 
				tel.trueDC = bestID
				if bestID != None:
					tel.assignpixelscore()
			
			if hasattr(self.simulations, "full"):
				fullsim = getattr(self.simulations, "full")
				for index in DCsim.triggerIDs:
					DCtel = DCsim.images[index]
					trueID = DCtel.trueDC
					fulltel = fullsim.images[index]
					fulltel.trueDC = trueID
					if trueID != None:
						fulltel.assignpixelscore()
			else:
				print "No full simulations for some reason!"

		else:
			raise Exception("No pure DC simulation exists")
			
	def returnforBDT(self):
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
	"One simulation, which can be either full or hadron simulation"
	def __init__(self, simcategory):
		self.simcategory = simcategory
		self.images=[]
		self.triggerIDs=[]
		self.shower = container()
		self.filled = False
	
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
	
	def setshowerparameters(self, names, values):
		for i in range(len(names)):
			name = re.sub('[.()]', '', names[i])
			name += "["
			writename = name[:name.find("[")]
			value = float(values[i])
			setattr(self.shower, writename, value)
			
	def extractpixelhillas(self):
		if hasattr(self.shower, 'shower_azimuth_') and hasattr(self.shower, 'shower_altitude_'):
			for index in self.triggerIDs:
				tel = self.images[index]
				tel.generatepixelhillasparameters(self.shower.shower_azimuth_, self.shower.shower_altitude_)
		else:
			print "No Shower Azimuth and Altitude"
			
	def plotgraphs(self, run_dir, runnumber):
		figure = plt.figure()
		for i in range(len(self.images)):
			tel = self.images[i]
			tel.plotimage(i)
		figure.set_size_inches(10, 20)
		plt.subplots_adjust(wspace=0, hspace=0)
		plt.savefig(run_dir + "/graph" + str(runnumber)+ self.simcategory + ".pdf")
		plt.close()
				
		
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
		elif self.size == "HESS1":
			self.pixelfile = "hess1pixels.csv"
			self.angularwidth=2.85
			self.imagewidth=70
			self.plotscale =100
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
			name = re.sub('[.()]', '', names[i])
			name += "["
			writename = name[:name.find("[")]
			value = float(values[i])
			setattr(self.hillas, writename, value)	
			
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
					pixel.channel0.getintensity()
					pixel.channel1.getintensity()
				else:
					raise Exception("Not all channels filled!")
		else:
			raise Exception("Not all gains and pedestals filled")
			
	def fillnearestneighbours(self):
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
	
	def plotimage(self, i):
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
		if hasattr(self.hillas, "image_cog_y_"):
			plt.scatter(self.hillas.image_cog_y_, self.hillas.image_cog_x_, c='w', s=100, marker="x")
		if hasattr(self.hillas, "showery"):
			plt.scatter(self.hillas.showery, self.hillas.showerx, c='w', s=100, marker="o")
		if self.QDCID != None:
			QDCpixel = self.getQDCpixel()
			plt.scatter(QDCpixel.y, QDCpixel.x, facecolors='none', edgecolors="r", s=(self.plotscale*1.2), marker="o", linewidth=2, zorder=4)
		if self.BDTID != None:
			BDTpixel = self.getBDTpixel()
			plt.scatter(BDTpixel.y, BDTpixel.x, facecolors='none', edgecolors="white", s=(self.plotscale*1.2), marker="*", linewidth=2, zorder=3)	
		if self.trueDC != None:
			truepixel = self.gettruepixel()
			plt.scatter(truepixel.y, truepixel.x, facecolors='none', edgecolors="orange", s=(self.plotscale*1.2), marker="o", linewidth=2, zorder=3)
		plt.xlim(-self.angularwidth, self.angularwidth)
		plt.ylim(-self.angularwidth, self.angularwidth)
		plt.axis('off')
		
	def findQDCpixel(self):
		bestID = None
		bestQDC = None
		if hasattr(self.hillas, "aspect_ratio_"):
			if self.hillas.aspect_ratio_ < arcut:
				for i in range(len(self.pixels)):
					pixelentry = self.pixels[i]
					if pixelentry.ddirec < ddireccut:				
						if dcogl < pixelentry.dcog < dcogu:
							if pixelentry.dline < dlinecut:
								if pixelentry.QDC > bestQDC:
									bestID=i
									bestQDC=pixelentry.QDC
		self.QDCID = bestID
		
	def getQDCpixel(self):
		if self.QDCID != None:
			return self.getpixel(self.QDCID)
		else:
			raise Exception("No QDC pixel!")
			
	def findrawQDCpixel(self):
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
		if self.rawQDCID != None:
			return self.getpixel(self.rawQDCID)
		else:
			raise Exception("No raw QDC pixel!")
	
	def gettruepixel(self):
		if self.trueDC != None:
			return self.getpixel(self.trueDC)
		else:
			raise Exception("No true DC pixel!")
			
	def findBDTpixel(self):
		bestID = None
		bestscore = None
		if os.path.isfile(hess1picklepath):
			for i in range(len(self.pixels)):
				pixelentry = self.pixels[i]
				bdtentry=[]
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
						bdtentry.append(newval)
					else:
						raise Exception("No variable named " +variable)
				if self.size == "HESS2" and os.path.isfile(hess2picklepath):
					bdtscore = hess2clf.predict_proba([bdtentry])[0][1]
				elif self.size == "HESS1" and os.path.isfile(hess1picklepath):
					bdtscore =  hess1clf.predict_proba([bdtentry])[0][1]
				else:
					print "self.size error, self.size=" + self.size
					bdtscore = None
				pixelentry.bdtscore = bdtscore
				if bdtscore > bestscore:
					bestID=i
					bestscore= bdtscore
		self.BDTID = bestID
		
	def getBDTpixel(self):
		if self.BDTID != None:
			return self.getpixel(self.BDTID)
		else:
			raise Exception("No BDT pixel!")
		
	def generatepixelhillasparameters(self, showerazimuth, showeraltitude):
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
		
		for pixelentry in self.pixels:
			pixelentry.hillas(cogx, cogy, showerx, showery, sm, sc)
		
		self.findQDCpixel()
		self.findrawQDCpixel()
		self.findBDTpixel()
		
	def assignpixelscore(self):
		if self.trueDC != None:
			for pixelentry in self.pixels:
				pixelentry.truescore = 0
			dcpixel = self.gettruepixel()
			dcpixel.truescore = 1
		else:
			raise Exception("No DC pixel has been identified!")
	
			
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
		self.nnc1s = None
		self.bdtscore = None
		self.truescore = None
		
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
			
	def hillas(self, cogx, cogy, showerx, showery, sm, sc):
		self.dcog = math.sqrt((self.x-cogx)**2 + (self.y-cogy)**2)
		self.ddirec = math.sqrt((self.x-showerx)**2 + (self.y-showery)**2)
		
		m = -1./sm
		c = self.y - (m*self.x)
		intersectionx = (sc - c)/(m-sm)
		intersectiony = (m * intersectionx) + c
		self.dline = math.sqrt((self.x-intersectionx)**2 + (self.y-intersectiony)**2)
		
		self.QDC = math.fabs(self.channel1.intensity/max([ abs(i) for i in self.nnc1s]))
		self.rawQDC = math.fabs(self.channel1.count/max([ abs(i) for i in self.rawnnc1s]))
		self.nnmean = np.mean(self.nnc1s)
		self.signalguess = self.channel1.intensity-self.nnmean
		self.imagedata = True

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
