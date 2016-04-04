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
import matplotlib.colors as colors
import matplotlib.mlab as mlab

def run(source, detectorcount, eff, gridwidth):
	with open("/d6/rstein/Hamburg-Cosmic-Rays/positioning/data/"+ str(source) +".csv", 'rb') as csvfile:
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
				argumenterror = "print_level=0, errordef = 10"
					
				m = eval("Minuit(f, x="+ str(truex) + ", " + argumentx + "y="+ str(truey) + ", " + argumenty+ "Epn = "+ str(trueEpn) + ", " + argumentE + "Z=" + str(trueZ) + "," +argumentZ + "height = " + str(trueheight) + ", " + argumentheight + argumenterror + ")")
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
					plt.yscale('log')
					
				ax = plt.subplot(4, 2, 6)
				
				cmap = cm.jet_r
				
				xbins, ybins, values = m.contour("x", "y", bound=[(float(truex)-50, float(truex)+50), (float(truey)-50, float(truey)+50)])
				levels = np.arange(zguessfval-1, np.amax(values), 10)
				norm=colors.LogNorm(vmin=zguessfval-1, vmax=np.amax(values))
				
				cset1 = plt.contourf(xbins, ybins, values, levels, cmap=cmap, norm=norm, origin='lower')
				CS =plt.contour(xbins, ybins, values, colors='k')
				plt.clabel(CS, inline=1, fontsize=10)
				plt.scatter(truex, truey, marker='x', color='k')
				plt.ylabel("Y")
				plt.xlabel("X")
					
				ax = plt.subplot(4, 2, 7)
				
				xbins, ybins, values = m.contour("Epn", "height", bound=[(232, 3000),(17500, 40000)])
				levels = np.arange(zguessfval-1, np.amax(values), 10)
				norm=colors.LogNorm(vmin=zguessfval-1, vmax=np.amax(values))

				cset2 = plt.contourf(xbins, ybins, values, levels,  cmap=cmap, norm=norm, origin='lower')
				CS =plt.contour(xbins, ybins, values, colors='k')
				plt.clabel(CS)
				plt.scatter(trueEpn, trueheight, marker='x', color='k')
				plt.ylabel("height")
				plt.xlabel("Epn")
				
				ax = plt.subplot(4, 2, 8)
				
				xbins, ybins, values = m.contour("Epn", "Z", bound=[(232, 3000),(20, 32)])
				
				levels = np.arange(zguessfval-1, np.amax(values), 10)
				norm=colors.LogNorm(vmin=zguessfval-1, vmax=np.amax(values))

				cset3 = plt.contourf(xbins, ybins, values, levels,  norm=norm, cmap=cmap, origin='lower')
				CS =plt.contour(xbins, ybins, values, colors='k')
				plt.clabel(CS)
				plt.scatter(trueEpn, trueZ, marker='x', color='k')
				plt.gca().set_xlim(left=232)
				plt.ylabel("Z")
				plt.xlabel("Epn")
				
				figure = plt.gcf() # get current figure
				figure.set_size_inches(20, 15)
				plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/likelihoodprofile.pdf')
				plt.close()

run("executeprocessX", 9, 0.06, 100)
