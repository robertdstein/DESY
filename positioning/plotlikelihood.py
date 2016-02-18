import argparse, math, random
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run(source, graph, llcuts):

	i=1
	zrange = [19.5, 32.5]
	
	i+=1
	
	correct = []
	close = []
	wrong = []
	full = []
	
	with open("reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		
		i = 0

		for row in reader:
			if i == 0:
				i = 1
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

				deltaz = math.fabs(float(trueZ)-float(reconZ))
				
				full.append(float(likelihood))
				
				if float(deltaz) == float(0):
					correct.append(float(likelihood))
					
				elif float(deltaz) == float(1):
					close.append(float(likelihood))
					
				elif float(deltaz) > 1:
					wrong.append(float(likelihood))
		
		total = len(correct)
		
		correct.sort()
		
		lower = int(0)
		mid = int(total*0.5)
		sigmai = int(total*0.68)
		
		lowerz = float(correct[lower])
		meanz = float(correct[mid])
		sigma = float(correct[sigmai])
		
		info = "For correct Z Values \n"
		info += ('Lower bound = ' + str(lowerz) + " \n")
		info += ('Mean = ' + str(meanz) + " \n")
		info += ('One Sigma Bound= ' + str(sigma) + "\n \n")
		
		for i in range(0, 3):
			category = [correct, close, wrong][i]
			name = ["correct", "close", "wrong"][i]
			passno = 0
			totalno = len(category)
			for entry in category:
				if entry < sigma:
					passno +=1
			passfrac = passno/float(totalno)
			info += ('For ' + str(name) + ' we have ' + str(passfrac) + " events passing \n")
		
	bincount = 50
	
	limits = [correct[0], correct[total-1]]
	
	plt.hist([correct, close, wrong], color = ["green", "orange", "red"], bins = bincount, stacked=True, label=["Delta Z = 0", "Delta Z = 1", "Delta Z > 1"], histtype='bar')
	
	for val in llcuts:
		plt.axvline(x=(val+0.01), linestyle='--', color='m', label="LL Cut")
	
	plt.xlabel('Log Likelihood')
	plt.ylabel('Count', labelpad=0)
	plt.legend()
	
	plt.annotate(info, (1300, 10),  fontsize=10)
	plt.suptitle('Likelihood', fontsize=20)
	
	plt.savefig('graphs/Likelihood.pdf')
		
	if graph:
		plt.show()
	else:
		plt.close()
