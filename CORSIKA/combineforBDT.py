import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="1385224")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1
j = 1500

targetfolder = filepath + cfg.jobID +"/"

with open(targetfolder + "BDTpixels.csv", 'wb') as csvout:
	writer = csv.writer(csvout, delimiter=',')
	while (i < j):
		if (os.path.isfile(targetfolder + "run" + str(i) + "/fullpixels1.csv")):
			for k in range(1,5):
			
				path = targetfolder + "run" + str(i) + "/fullpixels" + str(k) + ".csv"
				print path
				
				with open(path, 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					for row in reader:
						if (row[11] == str(0)) or (row[11] == str(1)):
							count = row[1]
							QDC = row[7]
							Dd = row[8]
							Dcg = row[9]
							Dline = row[10]
							score = row[11]
							energy = row[12]
							
							entry = [count, QDC, Dd, Dcg, Dline, energy, score]
							
							writer.writerow(entry)
						else:
							pass
		i+=1
