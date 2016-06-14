import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run(source, detectorcount, mindetections, graph=False, cuts=None, allcounts=None):
	
	print detectorcount, mindetections
	
	ngraphs = 1 + detectorcount-mindetections
	nrows =(ngraphs-int(0.5*ngraphs))

	
	if cuts == None:
		cuts = np.zeros(1 + detectorcount-mindetections)
		
	for j in range (detectorcount, mindetections -1, -1):
		print "Ndetections", j
		
	
		with open("/d6/rstein/Hamburg-Cosmic-Rays/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			
			ax = plt.subplot(nrows, 2, (1+ detectorcount-j))
			
			i = -1
			info = ""
			correct = []
			close = []
			wrong = []
			full = []
			plot = []
			plotcolour = []
			plotlabel = []
			
			bdtmin=cuts[detectorcount-j]
	
			for row in reader:
				if i < 0:
					i += 1
				else:
					detections = row[0]
					reconx = row[1]
					recony = row[2]
					reconEPN = row[3]
					reconZ = row[4]
					reconHeight = row[5]
					truex = row[6]
					truey = row[7]
					trueEPN = row[8]
					trueZ = row[9]
					trueHeight = row[10]
					likelihood = row[13]
					classifier=float(row[15])
					BDT=row[16]
					
					if classifier < 1.5:
						if int(detections) == int(j):
							deltaz = math.fabs(float(trueZ)-float(reconZ))
							full.append(float(BDT))
							
							if float(deltaz) == float(0):
								correct.append(float(BDT))
								
							elif float(deltaz) == float(1):
								close.append(float(BDT))
								
							elif float(deltaz) > 1:
								wrong.append(float(BDT))
			
			total = len(correct)
			info += "For BDT > " + str(bdtmin) + " Values \n"
			for i in range(0, 3):
				category = [correct, close, wrong][i]
				name = ["correct", "close", "wrong"][i]
				color = ["green", "orange", "red"][i]
				label=["Delta Z = 0", "Delta Z = 1", "Delta Z > 1"][i]
				passno = 0
				totalno = len(category)
				for entry in category:
					if float(bdtmin) < float(entry):
						passno +=1
				if totalno > 0:
					passfrac = passno/float(totalno)
					plot.append(category)
					plotcolour.append(color)
					plotlabel.append(label)
				else:
					passfrac = 0
				info += ('For ' + str(name) + ' then ' + str(passfrac) + " events pass \n")
		
		if len(plot) > 0:
			plt.hist(plot, color = plotcolour, bins = 50, stacked=True, label=plotlabel, histtype='bar')
			plt.axvline(x=bdtmin,  color='r')
		
		#~ for val in llcuts:
			#~ plt.axvline(x=(val+0.01), linestyle='--', color='m', label="LL Cut")
		
		plt.xlabel('BDT Score')
		plt.ylabel('Count', labelpad=0)
		plt.legend()
		plt.annotate(info, xy=(0.65, 0.45), xycoords="axes fraction",  fontsize=10)
		title = str(j) + " Telescope Detections"
		plt.title(title)
	
	figure = plt.gcf() # get current figure
	figure.set_size_inches(20, 15)
	plt.suptitle('BDT prediction of signal probability', fontsize=20)
	
	plt.savefig('/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/Likelihood.pdf')
		
	if graph:
		plt.show()
	else:
		plt.close()
