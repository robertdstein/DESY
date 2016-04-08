import calculatearea as ca
import lightdensity as ld
import math

def run(tradius, r, rayxpos, rayypos, xpos, ypos, Epn, Z, eff):
	distance = math.sqrt((rayxpos - xpos)**2 + (rayypos - ypos)**2)
	
	if tradius > 10:
		n = 10
		
	else:
		n=3
	
	if distance > tradius:
		startr = 0.99*(distance-tradius)
		deltar = float(2.1*tradius/n)
	
	else:
		startr=0
		deltar = float(2.1*r/n)
	
	Trigger = False
	
	rawsigcount = 0
	rawbkgcount = 0
	
	sigslices = 0
	bkgslices = 0
	
	for i in range (1, n+2):
		
		currentr = i*deltar + startr
		previousr = (i-1)*deltar + startr
		midr = (i-0.5)*deltar + startr
		
		newarea = ca.run(tradius, currentr, distance)
		
		oldarea = ca.run(tradius, previousr, distance)
		
		areaslice = newarea - oldarea
		
		sigdensity, bkgdensity = ld.run(midr, Epn, Z, r, eff)
		
		if sigdensity > 0:
			sigslices += areaslice
			
		if bkgdensity > 0:
			bkgslices += areaslice
		
		rawsigcount += sigdensity*areaslice
		rawbkgcount += bkgdensity*areaslice
		
		#~ if newarea < oldarea:
			#~ print "Possible error!"
			#~ print "N =", i
			#~ print currentr, previousr, midr, deltar, startr
			#~ print newarea, oldarea, areaslice, distance, tradius
			#~ print sigslices, bkgslices
			#~ print rawsigcount, rawbkgcount, sigdensity, bkgdensity
			#~ Trigger = True
	
	#~ if Trigger:
		#~ print "Rayradius is", r, "Bkgringradius is", r*scale, "distance is", distance, "telescope is", [xpos, ypos]
		#~ print "Sig lit area", testsigarea, sigslices, "Bkg lit area", testbkgarea, bkgslices
		#~ print "new", [rawsigcount, rawbkgcount], "old", [testsig, testbkg]
		#~ print "old sig density", testsigdensity, testbkgdensity
		#~ print "Last new sig density", sigdensity, bkgdensity
		#~ Trigger = False
	#~ 
	return int(rawsigcount), int(rawbkgcount)
					
