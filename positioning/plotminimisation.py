import array, math

import time, csv, random
import numpy as np
from iminuit import Minuit
import lightdensity as ld
import calculatearea as ca
import cherenkovradius as cr
import calculateellipse as ce
import telescoperadius as tr
import loglikelihood as ll
import atmosphere as atm
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.mlab as mlab

def run(source, detectorcount, eff, gridwidth):
	with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/data/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i = 0
		for row in reader:
			if i == 0:
				i = 1
			else:
				a=[]
				for j in range (0, detectorcount):
					base = 6*j
					a += [[row[base], row[base+1], row[base+2], row[base+3], row[base+4], row[base+5]]]
				lim = 6*detectorcount
				
				phi = float(row[lim+6])
	
				epsilon = float(row[lim+7])
				
				truex = row[lim]
				truey = row[lim+1]
				trueEpn = row[lim+2]
				trueZ = row[lim+3]
				trueheight = row[lim+4]
				
				true = [truex, truey, trueEpn, trueZ, trueheight, math.degrees(phi), math.degrees(epsilon)]
				
				def f(x,y,Z,Epn, height):
					sum = 0
					for detection in a:
						x0 = float(detection[0])
						y0 = float(detection[1])
						count = float(detection[2])
						category = detection[3]
						dangle = float(detection[4])
						sum += ll.run(x,y,math.fabs(Epn),Z, height, x0,y0, count, category, eff, phi, epsilon)
					return sum
				
				truefval = f(float(row[lim]), float(row[lim+1]), float(row[lim+3]), float(row[lim+2]), float(row[lim+4]))
				print "True Values are", true, "(", truefval, ")"
	
				#Runs Minimisation and outputs results
				
				startpos=[0, 0, 26.0, 1000, 30000]
				argumentx = "limit_x = (-300, 300), error_x = 100000, "
				argumenty = "limit_y = (-300, 300), error_y = 100000, "
				argumentZ = "fix_Z=True, "
				argumentE = "limit_Epn = (232, 4000), error_Epn=100, "
				argumentheight = "limit_height=(17500, 40000), error_height=1000, "
				argumenterror = "print_level=0, errordef = 100"
			
				xsites = np.linspace(-150, 150, int(gridwidth))
				ysites = np.linspace(-150, 150, int(gridwidth))
				
				z=26
				
				minangle = 0
				j = 0
				
				while j < 1:
					coordinates = []
					j = 0
					minangle += 0.1
					for x in xsites:
							for y in ysites:
									n=0
									
									for detection in a:
										x0 = float(detection[0])
										y0 = float(detection[1])
										recordeddangle = float(detection[4])
										
										dangle = ce.dangle(x0, y0, x, y)
										
										if math.fabs(dangle - recordeddangle) < math.radians(minangle):
											n+=1
											
										#~ print dangle, recordeddangle, n
										
									if n > (len(a)-1):
										coordinates.append([x,y])
										j+=1
					if minangle > 10:
						j=10
						
				fix = coordinates[0]
					
				print fix
					
				m = eval("Minuit(f, x="+ str(fix[0]) + ", " + argumentx + "y="+ str(fix[1]) + ", " + argumenty+ "Epn = "+ str(trueEpn) + ", " + argumentE + "Z=" + str(z) + "," +argumentZ + "height = " + str(trueheight) + ", " + argumentheight + argumenterror + ")")
				m.migrad()
				params = m.values
				zguess = [params['x'], params['y'], params['Epn'], params['Z'], params['height']]
				zguessfval = m.fval
				print zguess, zguessfval
				m.hesse()
				
				plotters = ["Epn", "Z", "x", "y",  "height"]
				ranges = [(232, 4000), (20, 32), (-300, 300), (-300, 300), (17500, 40000)]
				
				for i in range (0, len(plotters)):
					ax = plt.subplot(4, 2, i+1)
					bins, f  = m.draw_profile(plotters[i], bins=100, bound=ranges[i], text=False)
					ax.plot(bins, f)
				
				ax = plt.subplot(4, 2, 6)
				levels = np.arange(zguessfval-1, 100, 1)
				cmap = cm.jet_r
				
				xbins, ybins, values = m.contour("x", "y")
				
				cset1 = plt.contourf(xbins, ybins, values, levels, cmap=cmap, origin='lower')
				cbar = plt.colorbar(cset1)
				CS =plt.contour(xbins, ybins, values, colors='k')
				plt.clabel(CS, inline=1, fontsize=10)
					
				ax = plt.subplot(4, 1, 4)
				
				xbins, ybins, values = m.contour("Epn", "height")

				cset2 = plt.contourf(xbins, ybins, values, levels, cmap=cmap, origin='lower')
				cbar = plt.colorbar(cset2)
				plt.xlim(0, 4000)
				CS =plt.contour(xbins, ybins, values, colors='k')
				plt.clabel(CS)
				
				figure = plt.gcf() # get current figure
				figure.set_size_inches(20, 15)
				plt.savefig('graphs/likelihoodprofile.pdf')

run("executeprocessX", 9, 0.06, 100)
