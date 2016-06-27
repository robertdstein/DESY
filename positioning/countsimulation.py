import calculatearea as ca
import lightdensity as ld
import math

def run(tel, simulatedevent):
	[sigdensity, sigerror], [bkgdensity, bkgerror], [recondensity, reconerror] = ld.run(tel.coredistance, simulatedevent.epn, simulatedevent.Z, tel.scaledrmax, simulatedevent.efficiency)

	rawsigcount = tel.area * sigdensity
	rawbkgcount = tel.area * bkgdensity
	rawreconcount = tel.area * recondensity

	#~ print int(rawsigcount), int(rawbkgcount), sigerror, bkgerror
	return rawsigcount, rawbkgcount, sigerror, bkgerror, rawreconcount, reconerror
					
