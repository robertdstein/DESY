import calculatearea as ca
import lightdensity as ld
import math

def run(radius, r, rayxpos, rayypos, scale, xpos, ypos, Energy, Z, eff):
	distance = math.sqrt((rayxpos - xpos)**2 + (rayypos - ypos)**2)
	n = 100

	deltar = float(r/n)
	
	rawsigcount = 0
	rawbkgcount = 0
	
	sigslices = 0
	bkgslices = 0
	
	for i in range (0, n+1):
		
		currentr = i*deltar
		previousr = (i-1)*deltar
		midr = (i-0.5)*deltar
		
		#~ print radius, currentr, distance, scale, xpos, ypos
		newsigarea, newbkgarea = ca.run(radius, currentr, distance, scale, x0=xpos, y0=ypos)
		
		oldsigarea, oldbkgarea = ca.run(radius, previousr, distance, scale, x0=xpos, y0=ypos)
		
		sigslice = newsigarea - oldsigarea
		bkgslice = newbkgarea - oldbkgarea
		
		sigdensity, bkgdensity = ld.run(midr, Energy, Z, r, scale, eff)
		
		if sigdensity > 0:
			sigslices += sigslice
			
		if bkgdensity > 0:
			bkgslices += bkgslice
		
		rawsigcount += sigdensity*sigslice
		rawbkgcount += bkgdensity*bkgslice
		
		#~ print "N =", i
		#~ print currentr, previousr, midr, deltar
		#~ print newsigarea, oldsigarea, sigslice, newbkgarea, oldbkgarea, bkgslice
		#~ print rawsigcount, rawbkgcount, sigdensity, bkgdensity
		
	testsigarea, testbkgarea = ca.run(radius, r, distance, scale, x0=xpos, y0=ypos)
	testsigdensity, testbkgdensity = ld.run(distance, Energy, Z, r, scale, eff)
	testsig = testsigarea*testsigdensity
	testbkg = testbkgarea*testbkgdensity
	
	#~ print "Rayradius is", r, "Bkgringradius is", r*scale, "distance is", distance, "telescope is", [xpos, ypos]
	#~ print "Sig lit area", testsigarea, sigslices, "Bkg lit area", testbkgarea, bkgslices
	#~ print "new", [rawsigcount, rawbkgcount], "old", [testsig, testbkg]
	#~ print "old sig density", testsigdensity, testbkgdensity
	#~ print "Last new sig density", sigdensity, bkgdensity
	#~ 
	return int(rawsigcount), int(rawbkgcount)
					
