import calculatearea as ca
import lightdensity as ld
import math

def run(tel, simulatedevent):
	[sigdensity, sigerror], [bkgdensity, bkgerror] = ld.run(tel.coredistance, simulatedevent.epn, simulatedevent.Z, tel.scaledrmax, simulatedevent.efficiency)

	rawsigcount = tel.area * sigdensity
	rawbkgcount = tel.area * bkgdensity

	#~ print int(rawsigcount), int(rawbkgcount), sigerror, bkgerror
	return rawsigcount, rawbkgcount, sigerror, bkgerror
					
