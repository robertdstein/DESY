import calculatearea as ca
import lightdensity as ld
import math

def run(tradius, r, rayxpos, rayypos, xpos, ypos, Epn, Z, eff):
	distance = math.sqrt((rayxpos - xpos)**2 + (rayypos - ypos)**2)
	
	#~ if tradius > 10:
		#~ n = 10
		#~ 
	#~ else:
		#~ n=3
	#~ 
	#~ if distance > tradius:
		#~ startr = 0.99*(distance-tradius)
		#~ deltar = float(2.1*tradius/n)
	#~ 
	#~ else:
		#~ startr=0
		#~ deltar = float(2.1*r/n)
	#~ 
	#~ Trigger = False
	#~ 
	#~ rawsigcount = 0
	#~ rawbkgcount = 0
	#~ 
	#~ sigslices = 0
	#~ bkgslices = 0
	#~ 
	#~ for i in range (1, n+2):
		#~ 
		#~ currentr = i*deltar + startr
		#~ previousr = (i-1)*deltar + startr
		#~ midr = (i-0.5)*deltar + startr
		#~ 
		#~ newarea = ca.run(tradius, currentr, distance)
		#~ 
		#~ oldarea = ca.run(tradius, previousr, distance)
		#~ 
		#~ areaslice = newarea - oldarea
		#~ 
		#~ [sigdensity, sigerror], [bkgdensity, bkgerror] = ld.run(midr, Epn, Z, r, eff)
		#~ print sigdensity, bkgdensity, sigerror, bkgerror
		#~ 
		#~ if sigdensity > 0:
			#~ sigslices += areaslice
			#~ 
		#~ if bkgdensity > 0:
			#~ bkgslices += areaslice
		#~ 
		#~ rawsigcount += sigdensity*areaslice
		#~ rawbkgcount += bkgdensity*areaslice
		
	[sigdensity, sigerror], [bkgdensity, bkgerror] = ld.run(distance, Epn, Z, r, eff)
	
	rawarea = ca.telarea(tradius)

	rawsigcount = rawarea * sigdensity
	rawbkgcount = rawarea * bkgdensity

	print int(rawsigcount), int(rawbkgcount), sigerror, bkgerror
	return int(rawsigcount), int(rawbkgcount), sigerror, bkgerror
					
