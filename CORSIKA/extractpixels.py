import argparse, os, math, random, time, sys, csv, cmath
import numpy as np

offset="0"

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="1")
parser.add_argument("-jid", "--jobID", default="1174879")

cfg = parser.parse_args()

data_dir = "/nfs/astrop/d6/rstein/data"

result_dir = data_dir + "/" + str(cfg.jobID)

run_dir = os.path.join(result_dir, "run" + str(cfg.runnumber))
base_file_name = os.path.join(run_dir, "run" + str(cfg.runnumber) + "_off" + offset + "_read_hess_output.txt")

full=[]

g=open(run_dir + "/hillasparameters.csv", "w+")
gwriter = csv.writer(g, delimiter=',')
gheader = []

with open(base_file_name, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	test=False
	new=False
	current=[]
	for row in reader:
		
		if test:
			new=True
			test=False

		if len(row) > 8:
			if row[8] == "Pixel":
				if str(row[11]) == "1:":
					pixno = float(row[9][:-1])
					channel = float(row[11][:-1])
					count = float(row[12])
					current.append([pixno, count, channel])
					new=False
					test=True
		
		if len(row) > 0:
			if row[0] == "#@+":
				if row[1] == "Lines":
					pass
				elif row[1] == "":
					gheader.append(' '.join(row[3:]))
				else:
					gheader.append(' '.join(row[2::]))
			if row[0] == "@+":
				if 'gheader' in locals():
					 gwriter.writerow(gheader)
					 del gheader
				
				gentry = []
				for value in row[1:]:
					if value != "":
						gentry.append(value)
				
				gwriter.writerow(gentry)
						
		if new:
			full.append(current)
			current=[]
			new=False
			test=False
			
g.close()
	
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

arcut = 0.75
ddireccut = 0.45
dcogl = 0.17
dcogu = 0.91
dlinecut = 0.23
radiuscut = 40
QDCcut = 1

with open(run_dir + "/hillasparameters.csv", 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	
	for row in reader:
		if row[0] == "event":
			pass
		else:
			i = int(row[1]) - 1
			
			if i < 4 :
				targetfile = "hess1pixels.csv"
				imagewidth=70
				angularwidth=2.85
				size=100
				fig = plt.subplot(4,2,i+1)
				
			elif i == 4:
				targetfile = "hess2pixels.csv"
				imagewidth=105
				angularwidth=1.675
				size=180
				fig = plt.subplot(2,1,2)
			
			scale = angularwidth/imagewidth
			
			cogx = float(row[13])
			cogy = float(row[14])
			angle = math.radians(float(row[11]))
			coredistance=float(row[3])
			
			showerx=0
			showery=0
			
			width=float(row[6])
			length=float(row[7])
			distance = float(row[8])
			
			aspectratio = width/length
			
			end=distance + (2*length)

			numrange = np.linspace(-end, end, 2)
			
			sm = cmath.rect(1, angle).imag/cmath.rect(1, angle).real
			sc = showery - (sm * showerx)

			current = full[i]
			
			x=[]
			y=[]
			color=[]
			selectx=[]
			selecty=[]
			bestQDC=0.0
			bestID=None

			with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/'+targetfile, 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in reader:
					ID = int(row[0])
					xpos = float(row[1])*scale
					ypos=float(row[2])*scale
					
					nn = eval(row[3])
					nncounts=[]
					for nID in nn:
						neighbourentry = current[int(nID)]
						ncount = neighbourentry[1]
						nncounts.append(ncount)
						
					
					entry = current[ID]
					value = entry[1]
					
					QDC = float(value)/max(nncounts)

					ddirec = math.sqrt((xpos-showerx)**2 + (ypos-showery)**2)
					dcog = math.sqrt((xpos-cogx)**2 + (ypos-cogy)**2)
					
					intersectionangle = angle + math.pi/2
					
					m = cmath.rect(1, intersectionangle).imag/cmath.rect(1, intersectionangle).real
					c = ypos - (m*xpos)
					
					intersectionx = (sc - c)/(m-sm)
					intersectiony = (m * intersectionx) + c
					
					dline = math.sqrt((xpos-intersectionx)**2 + (ypos-intersectiony)**2)
					
					#~ if (float(ID)/400)-(int(float(ID)/400)) > 0:
						#~ pass
					#~ else:
						#~ plt.plot([intersectiony, ypos], [intersectionx, xpos], color='w')
						#~ plt.scatter(intersectiony, intersectionx, c='pink', s=100, marker="x", zorder=2)
						#~ plt.scatter(ypos, xpos, c='pink', s=100, marker="*", zorder=2)
					
					if ddirec < ddireccut:				
						if dcogl < dcog < dcogu:
							if dline < dlinecut:
								selectx.append(xpos)
								selecty.append(ypos)
								if QDC > bestQDC:
									bestID=ID
									bestQDC=QDC

					entry.append(xpos)
					entry.append(ypos)
					entry.append(nn)
					entry.append(nncounts)
					entry.append(QDC)
					entry.append(ddirec)
					entry.append(dcog)
					entry.append(dline)
					x.append(xpos)
					y.append(ypos)
					color.append(value)
			
			
			plt.plot((numrange*sm)+sc, numrange, color='w', linestyle='dashed')
			
			#~ coordinates = [[(showery,showerx), ddireccut], [(cogy, cogx), dcogl], [(cogy, cogx), dcogu]]
			#~ 
			#~ for cset in coordinates:
				#~ e = Circle(xy=cset[0], radius=cset[1])
				#~ fig.add_artist(e)
				#~ e.set_edgecolor('w')
				#~ e.set_facecolor("none")
				#~ e.set_linestyle('dashed')
					
			plt.scatter(y, x, s=size, c=color, linewidth='0', marker="H", zorder=1)
			plt.scatter(selecty, selectx, s=size, facecolors='none', edgecolors='w', marker="H", zorder=2)
			plt.xlim(-angularwidth, angularwidth)
			plt.ylim(-angularwidth, angularwidth)
			
			plt.axis('off')
			
			plt.scatter(cogy, cogx, c='w', s=100, marker="x")

			message="REJECTED!"
			
			if aspectratio > arcut:
				message += " \n Aspect Ratio too large, A.R = " + str(aspectratio) + " Cut requires A.R < " + str(arcut)
				
			if bestQDC < QDCcut:	
				message += " \n QDC too low, Q =" + str(bestQDC) + " Cut requires Q > "+ str(QDCcut)

			if coredistance < radiuscut:
				message += " \n Too close, r = " + str(coredistance) + " Cut requires r > " + str(radiuscut)
				
			if message == "REJECTED!":
				status="Accepted"
				ringcolor="pink"
				print "PASSED!"
			else:	
				ringcolor = "red"
				status = "Rejected"
				print message

			plt.annotate(status, xy=(0.0, 0.0), xycoords="axes fraction",  fontsize=10)
			
			if bestID != None:
				plt.scatter(current[bestID][4], current[bestID][3], facecolors='none', edgecolors=ringcolor, s=(size*1.2), marker="o", linewidth=2, zorder=3)
			
			current=full[i]
			path = run_dir + "/pixels" +str(i+1)+".csv"
			print path
			f=open(path, 'w+')
			writer = csv.writer(f, delimiter=',')
			writer.writerow(["PixelID", "Count", "Channel", "Xpos(Deg)", "Ypos(Deg)", "Neighbour IDs", "Neighbour Counts", "QDC", "Delta Direction", "Delta C.o.g"])
			for entry in current:
				writer.writerow(entry)
			f.close()	

figure = plt.gcf()
figure.set_size_inches(10, 20)
plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig(run_dir + "/graph" + str(cfg.runnumber) + ".pdf")
	
