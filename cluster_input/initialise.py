import math

sim="HESS"

if sim == "HESS":
	numberofhours = 0.15
	mincount=4
	reconstructiongridwidth=30.1
	layout="five"
	raweff = 1.0
	flux = 2.0 * (10**-4)
	flux = 2.86 * (10**-5)
	area = 300**2
	solidangle = 0.006
	selectionefficiency = 0.50
	hmacceptance = [0.35, 0.09]

def run():
	return numberofhours, mincount, reconstructiongridwidth, layout, raweff, flux, area, solidangle, selectionefficiency, hmacceptance
	
