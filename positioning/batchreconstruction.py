import argparse, math, random
import csv
import numpy as np
import minimise as m

def run(source, outputfile, rgw):
	with open("data/"+ str(source) +".csv", 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		i = 0
		for row in reader:
			if i == 0:
				i = 1
			else:
				m.min(row, rgw)
