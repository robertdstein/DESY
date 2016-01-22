import calculatearea as ca
import lightdensity as ld
import math

def run(tradius, r, rayxpos, rayypos, scale, xpos, ypos, Energy, Z, eff):
	distance = math.sqrt((rayxpos - xpos)**2 + (rayypos - ypos)**2)
	
	if tradius > 10:
		n = 10
		
	else:
		n=3
	
	if distance > tradius:
		startr = distance-tradius
		deltar = float(2*tradius*scale/n)
	
	else:
		startr=0
		deltar = float(2*r*scale/n)
	
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
		
		sigdensity, bkgdensity = ld.run(midr, Energy, Z, r, scale, eff)
		
		if sigdensity > 0:
			sigslices += areaslice
			
		if bkgdensity > 0:
			bkgslices += areaslice
		
		rawsigcount += sigdensity*areaslice
		rawbkgcount += bkgdensity*areaslice
		
		if newarea < oldarea:
			print "N =", i
			print currentr, previousr, midr, deltar, startr
			print newarea, oldarea, areaslice, distance, tradius
			print sigslices, bkgslices
			print rawsigcount, rawbkgcount, sigdensity, bkgdensity
			Trigger = True

	testsigarea, testbkgarea = ca.oldrun(tradius, r, distance, scale, x0=xpos, y0=ypos)
	testsigdensity, testbkgdensity = ld.run(distance, Energy, Z, r, scale, eff)
	testsig = testsigarea*testsigdensity
	testbkg = testbkgarea*testbkgdensity
	
	if Trigger:
		print "Rayradius is", r, "Bkgringradius is", r*scale, "distance is", distance, "telescope is", [xpos, ypos]
		print "Sig lit area", testsigarea, sigslices, "Bkg lit area", testbkgarea, bkgslices
		print "new", [rawsigcount, rawbkgcount], "old", [testsig, testbkg]
		print "old sig density", testsigdensity, testbkgdensity
		print "Last new sig density", sigdensity, bkgdensity
		Trigger = False
	
	return int(rawsigcount), int(rawbkgcount)
					
