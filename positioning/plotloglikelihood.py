import argparse, math, random
import csv
import numpy as np
import loglikelihood as ll
from iminuit import Minuit
import matplotlib.pyplot as plt
from matplotlib  import cm

def run(source, outputfile, detectorcount, rgw, eff):
	with open("data/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i = 0
		for row in reader:
			if i == 0:
				i = 1
			else:
				a=[]
				for j in range (0, detectorcount):
					base = 5*j
					a += [[row[base], row[base+1], row[base+2], row[base+3], row[base+4]]]
		
				def f(x,y,Epn, height, scale):
					sum = 0
					for detection in a:
						x0 = float(detection[0])
						y0 = float(detection[1])
						sigcount = float(detection[2])
						bkgcount = float(detection[3])
						category = detection[4]
						sum += ll.run(x,y,Epn,26, height, x0,y0, sigcount, bkgcount, category, scale, eff)
					return sum
				
				startpos=[0, 0, 26.0]
				argumentx = "fix_x=True, "
				argumenty = "fix_y=True, "
				argumentZ = "Z=26, fix_Z=True,"
				argumentE = "Epn = 300, limit_Epn = (232, 4000), error_Epn=1, "
				argumentheight = "height=30000, fix_height=True, "
				argumentscale = "scale=1.2, fix_scale=True, "
				argumenterror = "print_level=0, errordef = 100"
			
				m = eval("Minuit(f, x="+ str(startpos[0]) + ", " + argumentx + "y="+ str(startpos[1]) + ", " + argumenty + argumentE + argumentheight + argumentscale + argumenterror + ")")
				m.migrad()
				params = m.values
				guess = [params['x'], params['y'], params['Epn'], params['height']]
				print guess
				guessfval = m.fval
			
				xsites = np.linspace(-200, 200, int(rgw))
				ysites = np.linspace(-200, 200, int(rgw))
				
				col = []
				colmax = 0
				
				for x in xsites:
					row = []
					for y in ysites:
						m = eval("Minuit(f," + argumentE + argumentheight + argumentscale + "x="+ str(x) + ", " + argumentx + "y="+ str(y) + ", " + argumenty+ argumenterror + ")")
						m.migrad()
						params = m.values
						fval = m.fval
						values = m.get_fmin()
						
						colorval = math.log(fval)
						row.append(colorval)
						
						if colorval > colmax:
							colmax = colorval
						
						if values.is_valid:
							if fval < guessfval:
								guess = [params['x'], params['y'], params['Epn'], params['height']]
								guessfval = fval
								
					col.append(row)
				print col
				grid = col/colmax
				print grid
						
				plt.scatter(x, y, c=(col/colmax), marker='s', cmap = cm.jet )
				
				lim = 5*detectorcount
				true = [row[lim], row[lim+1], row[lim+2], row[lim+3], row[lim+4]]
				print "True Values are", true
				print "Final guess is", guess 
				plt.colorbar()
				plt.show()
