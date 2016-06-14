import math
import cherenkovradius as cr

class simulation:
	"""A container for many full simulations
	"""
	def __init__(self):
		self.simulations = []
		
	def generate(self, n):
		for i in range (n):
			

class fullevent:
	"""A Full event simulation"""
	def __init__(self, x, y, Z, N, energy, height, phi, theta):
		self.true = event(x, y, Z, N, energy, height, phi, theta)
		self.detected = None
		self.reconstructed=None
		
class event:
	"""An event class
	"""
	def __init__(self, x=None, y=None, Z=None, N=None, energy=None, height=None, phi=None):
		self.rayxpos = x
		self.rayypos = y
		self.Z = Z
		self.N = N
		self.energy = energy
		self.height = height
		self.phi = phi
		self.theta = theta
		self.getepn()
		
	def getepn(self):
		if (self.energy != None) and (self.N != None):
			self.epn = energy/N
		else:
			self.epn = None
			
	def getrayradius(self):
		self.rayradius, self.theta = cr.run(self.epn, self.height, math.sin(self.phi), text=False)
