import math

numberofhours = 357
mincount=4
reconstructiongridwidth=13
orientation="five"
eff = 0.06
flux = 2.0 * (10**-4)
area = 300**2
solidangle = math.radians(5)
selectionefficiency = 0.50

def run():
	return numberofhours, mincount, reconstructiongridwidth, orientation, eff, flux, area, solidangle, selectionefficiency
	
