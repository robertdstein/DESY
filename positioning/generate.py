import random, math
import cherenkovradius as cr
import atmosphere as atm

#Randomly Generates all variables for an event

def run():
	
	#Randomly generates a target centre of -150<x<150m and -150<y<150m
	xpos = (random.random()*300)-150
	ypos = (random.random()*300)-150
	
	#Generates a random probability, and converts this to an Epn value following an E^-1.7 power series
	
	R = random.random()*3.01*(10**-3)
	Epn = ((1.7*R/321)+(2411**-1.7))**(-1/1.7)
	
	#Generates a fixed charge number of Z=26

	Z= 26
	N = 56
	energy = Epn*N
	
	#Randomly generates a height probability, and converts this probability to a set height
	
	hprob = random.random()
	height = atm.runheight(hprob)
	
	#Chooses a zenith angle +- 22 degrees

	zenith = random.random()*44

	phi = math.radians(68+zenith)
	phi = math.radians(90)
	
	#Randomly choose an angle NESW

	epsilon = math.pi*random.random()*2
	
	#~ #Calculate resultant surface radius and angular width of beam
	#~ 
	#~ radius, theta = cr.run(Epn, height, math.sin(phi), text=text)
	#~ 
	#~ if text:
		#~ print "Height is", height
		#~ print "Theta is", math.degrees(theta)
		#~ print "Phi is", math.degrees(phi)
		#~ print "Epsilon is", math.degrees(epsilon)
		#~ print "Radius is", radius
    	
	return xpos, ypos, epsilon, energy, Z, height, phi, N
	

