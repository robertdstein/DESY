import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="1385224")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1
j = 2000

targetfolder = filepath + cfg.jobID +"/"

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
from progressbar import ProgressBar
custom_options = {
	'end': 100,
	'width': 100,
	'format': '%(progress)s%% [%(fill)s%(blank)s]'
}

p = ProgressBar(**custom_options)
print p

with open(targetfolder + "BDTpixels.csv", 'wb') as csvout:
	writer = csv.writer(csvout, delimiter=',')
	writer.writerow(["Channel1", "QDC", "Delta_direction", "Delta_Centre_of_Gravity", "Delta_line", "Energy", "Nearest_Neighbour_Mean", "score", "Channel0"])
	while (i < j) or (os.path.isfile(targetfolder + "run" + str(i) + "/fullpixels1.csv")):
		if (os.path.isfile(targetfolder + "run" + str(i) + "/fullpixels1.csv")):
			for k in range(1,5):
			
				path = targetfolder + "run" + str(i) + "/fullpixels" + str(k) + ".csv"
				
				with open(path, 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					for row in reader:
						if (row[11] == str(0)) or (row[11] == str(1)):
							channel1 = row[1]
							channel0 = row[2]
							QDC = row[7]
							Dd = row[8]
							Dcg = row[9]
							Dline = row[10]
							score = row[11]
							energy = row[12]
							nnmean = row[13]
							
							entry = [channel1, QDC, Dd, Dcg, Dline, energy, nnmean, score, channel0]
							
							writer.writerow(entry)
						else:
							pass
		if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
			print p+1
		i+=1
