import argparse, os, math, random, time, sys, csv, cmath
import os.path
import numpy as np
from sklearn.externals import joblib
from sklearn import ensemble
import initialisecuts as ic

offset="0"

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="1")
parser.add_argument("-jid", "--jobID", default="2842781")
parser.add_argument("-cn", "--cardname", default="full")


cfg = parser.parse_args()

data_dir = "/nfs/astrop/d6/rstein/data"

result_dir = data_dir + "/" + str(cfg.jobID)

run_dir = os.path.join(result_dir, "run" + str(cfg.runnumber))
base_file_name = os.path.join(run_dir, "run" + str(cfg.runnumber)+ str(cfg.cardname) + "_off" + offset  + "_read_hess_output.txt")

full=[]

f=open(run_dir + "/telescopedirections.csv", "w+")
fwriter = csv.writer(f, delimiter=',')
fheader = []

g=open(run_dir + "/hillasparameters" + cfg.cardname + ".csv", "w+")
gwriter = csv.writer(g, delimiter=',')
gheader = []

h=open(run_dir + "/eventparameters" + cfg.cardname + ".csv", "w+")
hwriter = csv.writer(h, delimiter=',')
hheader = []

with open(base_file_name, 'rb') as csvfile:
	i = 1
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
				if str(row[11]) == "0:":
					pixno = float(row[9][:-1])
					channel = float(row[11][:-1])
					count = float(row[12])
					current.append([pixno, count])
					new=False
					test=True
				elif str(row[11]) == "1:":
					pixno = int(row[9][:-1])
					channel = float(row[11][:-1])
					count = float(row[12])
					entry = current[pixno]
					oldpixno = entry[0]
					oldcount = entry[1]
					current[pixno] = [pixno, count, oldcount]
					new=False
					test=True
		
		if len(row) > 0:
			
			if len(row) > 4:
				if (row[4] == "Raw:"):
					telaz = row[7]
					telalt = row[11]
					fwriter.writerow([i, telaz, telalt])
					i+=1
			
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
			
			if row[0] == "#@:":
				if row[1] == "Lines":
					pass
				elif row[1] == "":
					hheader.append('_'.join(row[3:]))
				else:
					hheader.append('_'.join(row[2::]))
			if row[0] == "@:":
				if 'hheader' in locals():
					 hwriter.writerow(hheader)
					 del hheader
				
				hentry = []
				for value in row[1:]:
					if value != "":
						hentry.append(value)

				showerazimuth = hentry[4]
				showeraltitude = hentry[5]
				
				hwriter.writerow(hentry)
						
		if new:
			full.append(current)
			current=[]
			new=False
			test=False

f.close()			
g.close()
h.close()
	
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

arcut, ddireccut, dcogl, dcogu, dlinecut, radiuscut = ic.run()
cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()

picklepath = '/nfs/astrop/d6/rstein/BDTpickle/DCpixelclassifier.pkl'
if os.path.isfile(picklepath):
	clf=joblib.load(picklepath)		
else:
	print "No pickle!"

with open(run_dir + "/hillasparameters" + cfg.cardname + ".csv", 'rb') as csvfile:
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
			energy=float(row[2])
			
			telaz=0
			telalt=0			
			with open(run_dir + "/telescopedirections.csv", 'r') as nf:
				telreader = csv.reader(nf, delimiter=',', quotechar='|')
				for telrow in telreader:
					if int(telrow[0]) == int(row[1]):
						telazimuth = telrow[1]
						telaltitude = telrow[2]
					else:
						pass
			
			deltaaz = float(showerazimuth) - float(telazimuth)
			deltaalt= float(showeraltitude) - float(telaltitude)
			
			showery=cmath.rect(deltaalt, math.radians(180 - float(showerazimuth))).imag
			showerx=cmath.rect(deltaalt, math.radians(180 - float(showerazimuth))).real

			width=float(row[6])
			length=float(row[7])
			distance = float(row[8])
			
			aspectratio = width/length
			end=distance + (2*length)

			numrange = np.linspace(-end, end, 2)
			
			sm = (cogy-showery)/(cogx - showerx)
			sc = showery - (sm * showerx)

			current = full[i]
			
			x=[]
			y=[]
			color=[]
			selectx=[]
			selecty=[]
			bestQDC=0.0
			bestcount=0.0
			bestID=None
			
			if os.path.isfile(picklepath):
				bestscore=0.0
				clfID=None
				

			with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/data/'+targetfile, 'rb') as csvfile:
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
					channel1 = entry[1]
					channel0 = entry[2]
					
					QDC = float(channel1)/max(nncounts)
					nnmean = np.mean(nncounts)
					
					signal = channel1-nnmean
					print QDC, nnmean, signal

					ddirec = math.sqrt((xpos-showerx)**2 + (ypos-showery)**2)
					dcog = math.sqrt((xpos-cogx)**2 + (ypos-cogy)**2)
					
					m = -1./sm
					c = ypos - (m*xpos)
					
					intersectionx = (sc - c)/(m-sm)
					intersectiony = (m * intersectionx) + c
					
					dline = math.sqrt((xpos-intersectionx)**2 + (ypos-intersectiony)**2)
					
					includeinBDT = 0
					
					if cfg.cardname =="full":
						if ddirec < ddireccut:				
							if dcogl < dcog < dcogu:
								if dline < dlinecut:
									selectx.append(xpos)
									selecty.append(ypos)
									
									if QDC > bestQDC:
										bestID=ID
										bestQDC=QDC
					
					elif cfg.cardname == "DC":
						if channel1 > bestcount:
							bestID=ID
							bestcount=channel1
							
					if os.path.isfile(picklepath):
						bdtentry = [channel1, QDC, ddirec, dcog, dline, nnmean, signal]
						bdtscore = clf.predict_proba([bdtentry])[0]
						bdtscore = clf.predict_proba([bdtentry])[0][1]
						if bdtscore > bestscore:
							clfID=ID
							bestscore= bdtscore

					entry.append(xpos)
					entry.append(ypos)
					entry.append(nn)
					entry.append(nncounts)
					entry.append(QDC)
					entry.append(ddirec)
					entry.append(dcog)
					entry.append(dline)
					entry.append(includeinBDT)
					entry.append(energy)
					entry.append(nnmean)
					if os.path.isfile(picklepath):
						entry.append(bdtscore)
					x.append(xpos)
					y.append(ypos)
					color.append(channel1)
			
			
			plt.plot((numrange*sm)+sc, numrange, color='w', linestyle='dashed')
			
			coordinates = [[(showery,showerx), ddireccut], [(cogy, cogx), dcogl], [(cogy, cogx), dcogu]]
			
			plt.scatter(y, x, s=size, c=color, linewidth='0', marker="H", zorder=1, vmin=3800, vmax=7800)
			plt.xlim(-angularwidth, angularwidth)
			plt.ylim(-angularwidth, angularwidth)
			
			plt.axis('off')
			
			plt.scatter(cogy, cogx, c='w', s=100, marker="x")
			plt.scatter(showery, showerx, c='w', s=100, marker="o")

			message="REJECTED!"
			
			if aspectratio > arcut:
				message += " \n Aspect Ratio too large, A.R = " + str(aspectratio) + " Cut requires A.R < " + str(arcut)
				
			if bestQDC < QDCcut:	
				message += " \n QDC too low, Q =" + str(bestQDC) + " Cut requires Q > "+ str(QDCcut)

			if coredistance < radiuscut:
				message += " \n Too close, r = " + str(coredistance) + " Cut requires r > " + str(radiuscut)
			
			if (cfg.cardname == "full"):
				if message == "REJECTED!":
					status="Accepted"
					ringcolor="pink"
				else:	
					ringcolor = "red"
					status = "Rejected"
				
				plt.annotate(status, xy=(0.0, 0.0), xycoords="axes fraction",  fontsize=10)	
				
			elif (cfg.cardname == "DC"):
				ringcolor = "white"
			
			DCpath = run_dir + "/DCpixel" + str(i+1) + ".text"
			csvpath = run_dir + "/" + cfg.cardname + "pixels" + str(i+1) + ".csv"
			
			if (cfg.cardname == "full") & os.path.isfile(DCpath):
					with open(DCpath) as g:
						trueID = g.readline()
						print "DC pixel", trueID
						plt.scatter(current[int(trueID)][4], current[int(trueID)][3], facecolors='none', edgecolors="orange", s=(size*1.2), marker="o", linewidth=2, zorder=3)
						trueevent = current[int(trueID)]
						truecount = trueevent[1]
						if truecount > signalcut:
							current[int(trueID)][14] = 1
						else:
							current[int(trueID)][14] = -1
						trueQDC = current[7]
						
						if bestID != None:
							if int(trueID) == int(bestID):
								status += " \n MATCHED!"
								
						if os.path.isfile(picklepath):	
							statspath = run_dir + "/stats" + str(i+1) + ".txt"
							with open(statspath, 'w+') as h:
								if int(clfID) == int(trueID):
									h.write("1 \n")
								else:
									h.write("0 \n")
								h.write(str(bestscore) + "\n")
								bestIDval = 0
								if bestID != None:
									if int(bestID) == int(trueID):
										bestIDval = 1

								h.write(str(bestIDval) + " \n")
								h.write(str(bestQDC) + "\n")
								h.write(str(current[clfID]) + "\n")
						
							countpath = run_dir + "/candidate" + str(i+1) + ".txt"
							with open(countpath, 'w+') as f:
								candidateID = 0
								passcut = False
								if bestID != None:
									if float(bestQDC) > float(QDCcut):
										candidateID = bestID
										passcut = True
										
								if not passcut:
									candidateID = clfID
									passcut = False
								
								candidate = current[int(candidateID)]
								
								f.write(str(passcut) + " \n")
								f.write(str(candidate) + "\n")
				
			elif (cfg.cardname =="DC"):
				g=open(DCpath, 'w+')
				g.write(str(bestID) + " \n")

				g.write(str(current[bestID]) + " \n")
				g.close()
			
			with open(csvpath, 'w+') as f:
				writer = csv.writer(f, delimiter=',', quotechar='|')
				writer.writerow(["PixelID", "Channel1", "Channel0", "Xpos(Deg)", "Ypos(Deg)", "Neighbour IDs", "Neighbour Counts", "QDC", "Delta Direction", "Delta C.o.g", "Delta Line", "DC?"])
				for entry in current:	
					writer.writerow(entry)
			
			if bestID != None:
				plt.scatter(current[bestID][4], current[bestID][3], facecolors='none', edgecolors=ringcolor, s=(size*1.2), marker="o", linewidth=2, zorder=3)
				
			if os.path.isfile(picklepath) and (cfg.cardname == "full"):
				plt.scatter(current[clfID][4], current[clfID][3], facecolors='none', edgecolors="white", s=(size*1.2), marker="*", linewidth=2, zorder=3)

figure = plt.gcf()
figure.set_size_inches(10, 20)
plt.subplots_adjust(wspace=0, hspace=0)

plt.savefig(run_dir + "/graph" + str(cfg.runnumber) + cfg.cardname + ".pdf")
plt.close()
