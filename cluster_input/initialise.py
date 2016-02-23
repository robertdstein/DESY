import math

numberofhours = 0.05
mincount=5
reconstructiongridwidth=301
orientation="ideal"
eff = 0.06
flux = 2.0 * (10**-4)
area = 300**2
solidangle = math.radians(5)
selectionefficiency = 0.50

def run():
	return numberofhours, mincount, reconstructiongridwidth, orientation, eff, flux, area, solidangle, selectionefficiency
	
