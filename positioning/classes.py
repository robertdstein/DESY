import math, csv, time, random
import generate as g
import cherenkovradius as cr
import atmosphere as atm
import telescoperadius as tr
import lightdensity as ld
import calculatearea as ca
import loglikelihood as ll
import calculateellipse as ce
import countsimulation as cs
import minimise as m
import cPickle as pickle

class simulationset:
	"""A container for many full simulations
	"""
	def __init__(self, raweff, layout, mincount, hmacceptance=[1, 1], gridwidth=300):
		self.simulations = []
		self.raweff = raweff
		self.layout = layout
		self.mincount = mincount
		self.passcount = 0
		self.hmcount = 0
		self.lmcount = 0
		self.nonDC = 0
		self.highmultiplicityacceptance = hmacceptance
		self.gridwidth = gridwidth
		self.rowcount()
		
	def rowcount(self):
		self.ndetectors = 0
		with open("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/orientations/"+ self.layout +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in reader:
				self.ndetectors +=1
		print time.asctime(time.localtime()), "Simulated Array contains", self.ndetectors, "Telescopes." 

		
	def generate(self, n, energy=None, height=None, Z=None):
		print time.asctime(time.localtime()),"Simulating", n, "Events."
		for i in range (n):
			xpos, ypos, epsilon, genergy, gZ, gheight, phi, N = g.run()
			
			if energy == None:
				simenergy = genergy
			if height == None:
				simheight = gheight
			if Z == None:
				simZ = gZ
				
			newsimulation = simulation(xpos, ypos, epsilon, simenergy, simZ, simheight, phi, N, self.layout)
			newsimulation.simulatedetection(self.raweff)
			if newsimulation.detected.DCmultiplicity < self.mincount:
				if newsimulation.detected.DCmultiplicity > 0:
					self.lmcount += 1
				else:
					self.nonDC += 1
			else:
				self.hmcount += 1
				intno = newsimulation.detected.DCmultiplicity - self.mincount
				if random.random() < self.highmultiplicityacceptance[intno]:
					self.passcount += 1
					self.simulations.append(newsimulation)
				
		print time.asctime(time.localtime()),"In total", self.nonDC, "Events did not produce Cherenkov Light." 
		print time.asctime(time.localtime()),"A further", self.lmcount, "Events produced Cherenkov Light below multiplicity Threshold." 
		print time.asctime(time.localtime()),"This leaves", self.hmcount, "high multiplicity events, of which", self.passcount, "were accepted."
		
	def reconstructevents(self):
		print time.asctime(time.localtime()),"Reconstructing", self.passcount, "Events."
		for fullsim in self.simulations:
			fullsim.gettruelikelihood()
			m.min(fullsim, self.layout, self.gridwidth, self.raweff)
			
	def dump(self, n):
		pickle_dump_dir="/nfs/astrop/d6/rstein/chargereconstructionpickle/fullsims/sim" + str(n) +".p" 
		pickle.dump(self, open(pickle_dump_dir,"wb"))
		
class simulation:
	"""A Full event simulation"""
	def __init__(self, xpos, ypos, epsilon, energy, Z, height, phi, N, layout):
		self.true = event(xpos, ypos, epsilon, energy, Z, height, phi, N, layout, smear=False)
		self.detected = event(xpos, ypos, epsilon, energy, Z, height, phi, N, layout, smear=True)
		self.reconstructed=None
	
	def simulatedetection(self, raweff):
		self.true.simulatetelescopes(raweff)
		self.detected.simulatetelescopes(raweff)
			
	def gettruelikelihood(self):
		print "Reconstructing!"
		self.true.calculatedclikelihood(self.detected)
		self.true.calculatefulllikelihood(self.detected)
		#~ print "True guess is [", self.true.rayxpos, self.true.rayypos, self.true.epn, self.true.Z,  self.true.height, "] (", self.true.minusll, ")"
		
	def getreconstructedlikelihood(self):
		if self.reconstructed != None:
			self.reconstructed.calculatedclikelihood(self.detected)
			self.reconstructed.calculatefulllikelihood(self.detected)
		else:
			raise Exception("Event has not been reconstructed!") 
	
class event:
	"""An event class
	"""
	def __init__(self, xpos, ypos, epsilon, energy, Z, height, phi, N, layout, smear):
		self.rayxpos = xpos
		self.rayypos = ypos
		self.energy = energy
		self.Z = Z
		self.height = height
		self.N = N
		self.smear = smear
		
		if smear:
			smearphi = phi + (math.radians(0.5)*(random.random()-0.5))
			smearepsilon = epsilon + (math.radians(0.5)*(random.random()-0.5))
			self.epsilon = smearepsilon
			self.phi = smearphi
		else:
			self.epsilon = epsilon
			self.phi = phi
		
		self.telescopes=[]
		self.addtelescopes(layout)
		self.DCmultiplicity = 0
		self.fullmultiplicity = 0
		self.truemultiplicity = 0
		self.getepn()
		self.getrayradius()
		self.minuslldc = None
		self.minusllfull = None
		self.BDTscore = None
		
	def getepn(self):
		if (self.energy != None) and (self.N != None):
			self.epn = self.energy/self.N
		else:
			self.epn = None
			
	def getrayradius(self):
		self.rayradius, self.theta = cr.run(self.epn, self.height, math.sin(self.phi), text=False)
		
	def getabsorption(self, raweff):
		self.raweff = raweff
		self.absorptionfrac = atm.runabsorption(self.height)
		self.absorptionfrac = 1
		self.efficiency = raweff*self.absorptionfrac/math.sin(self.phi)
		
	def addtelescopes(self, layout):
		if self.telescopes==[]:
			with open("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/orientations/"+ layout +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					category = row[0]
					xpos = float(row[1])
					ypos = float(row[2])
					tel = telescope(category, xpos, ypos)
					self.telescopes.append(tel)
			
	def simulatetelescopes(self, raweff):
		self.getabsorption(raweff)
		for tel in self.telescopes:
			tel.fillcounts(self)
			if tel.DCtrigger:
				self.DCmultiplicity += 1
				if tel.coredistance < tel.scaledrmax:
					self.truemultiplicity += 1
			if tel.fulltrigger:
				self.fullmultiplicity +=1
				
	def calculatedclikelihood(self, detectedevent):
		self.minuslldc = 0
		for i in range(len(self.telescopes)):
			tel = self.telescopes[i]
			detectedtel = detectedevent.telescopes[i]
			likelihood = ll.rundc(tel, detectedtel)
			tel.dclikelihood = likelihood
			self.minuslldc += likelihood
	
	def calculatefulllikelihood(self, detectedevent):
		self.minusllfull = 0
		for i in range(len(self.telescopes)):
			tel = self.telescopes[i]
			detectedtel = detectedevent.telescopes[i]
			likelihood = ll.runfull(tel, detectedtel)
			tel.fulllikelihood = likelihood
			self.minusllfull += likelihood
			
		
class telescope():
	"""A telescope entry
	"""
	threshold = float(ld.trigger())
	
	def __init__(self, telclass, x, y):
		self.telclass = telclass
		self.telradius = tr.run(telclass)
		self.area = ca.telarea(self.telradius)
		self.x = x
		self.y = y
		self.dclikelihood = None
		self.fulllikelihood = None
		
	def fillcounts(self, simulatedevent):
		self.finddistancetocore(simulatedevent)
		self.scaledrmax, dangle = ce.run(simulatedevent, self.x, self.y)
		self.findrecorded(simulatedevent, dangle)
		
	def findrecorded(self, simulatedevent, dangle):
		sigcount, bkgcount, sigerror, bkgerror , reconcount, reconerror = cs.run(self, simulatedevent)
		if simulatedevent.smear:
			DCphotons = int(random.gauss(sigcount, sigerror*sigcount))
			reconphotons = random.gauss(reconcount, reconerror*reconcount)
			fullphotons = int(random.gauss(bkgcount, bkgerror*bkgcount))
			dangle = random.gauss(dangle, 0.01)
		else:
			DCphotons = sigcount				
			fullphotons = bkgcount
			reconphotons = reconcount
			dangle = dangle
			
		self.DCphotons=DCphotons
		self.reconphotons = reconphotons
		self.fullphotons = fullphotons
		self.dangle = dangle
		self.DCfracerror = sigerror
		self.fullfracerror = bkgerror
		self.reconfracerror = reconerror
		
		self.DCtrigger = self.checktrigger(self.DCphotons)
		
		if simulatedevent.smear and not self.DCtrigger:
			self.DCphotons = 0
			
		altDC = ld.altcount(self.coredistance, simulatedevent.Z)
		self.altDCphotons = altDC
		
		self.fulltrigger = self.checktrigger(self.fullphotons)
		
		if simulatedevent.smear and not self.fulltrigger:
			self.fullphotons = 0
					
	def checktrigger(self, count):
		if float(count) > self.threshold:
			return True
		else:
			return False
		
	def finddistancetocore(self, simulatedevent):
		corex = simulatedevent.rayxpos
		corey = simulatedevent.rayypos
		distance = math.sqrt(((corex - self.x)**2) + ((corey - self.y)**2))
		self.coredistance = distance
		
	def finddistancetopoint(self, x, y):
		distance = math.sqrt(((x - self.x)**2) + ((y - self.y)**2))
		return distance
	
		
		
bdtvariables =["epn", "minuslldc", "minusllfull", "fullmultiplicity", "truemultiplicity", "rayxpos", "rayypos", "height"]

def makeBDTentry(simevent):
	bdtentry =[]
	for variable in bdtvariables:
		if hasattr(simevent, variable):
			newval = getattr(simevent, variable)
			bdtentry.append(newval)
		else:
			print "OOPS!", bdtentry, variable
			return None
	return bdtentry
		

