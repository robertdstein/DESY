import time, math
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import argparse
import csv
import cPickle as pickle
import random
import os
from telescopeclasses import *
import lpdfit as lf

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="regressorset")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

signalbdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/signalBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		signalbdtvariables.append(row[0])
print signalbdtvariables

def makeBDTentry(pixelentry):
	bdtentry =[]
	for variable in signalbdtvariables:
		varsplit = variable.split('.')
		suffix = pixelentry
		if len(varsplit) > 1:
			for name in varsplit[:-1]:
				if hasattr(suffix, name):
					suffix = getattr(suffix, name)
				else:
					return None
			varname = varsplit[-1]
		else:
			varname = variable
		if hasattr(suffix, varname):
			newval = getattr(suffix, varname)
			bdtentry.append(newval)
		else:
			return None
	return bdtentry

categories = ["hess2","hess1"]
learningrates = [0.2, 0.6]

for i in range(len(categories)):
	
	category = categories[i]
	learningrate = learningrates[i]

	jobfolder = os.path.join(filepath, cfg.jobID)
	pickledatafolder = os.path.join(jobfolder, "bdtpickle")
	filename = pickledatafolder + "/" + category + "candidatepixels.p"
	signalfilename = pickledatafolder + "/" + category + "DCsignals.p"
	trueZfilename = pickledatafolder + "/" + category + "trueZ.p"

	if os.path.isfile(filename) and os.path.isfile(signalfilename) and os.path.isfile(trueZfilename):
		print "Loading training dataset from", filename
		print "Loading training scores from", signalfilename
	else:
		raise Exception("No BDT data file present at "+ filename)
	
	full = []
	scores = []

	trainset = pickle.load(open(filename, 'rb'))
	signals= pickle.load(open(signalfilename, 'rb'))
	trueZ = pickle.load(open(trueZfilename, 'rb'))
	
	print category, "training dataset contains", len(trainset), "images"
	
	for i in range(len(trainset)):
		pix = trainset[i]
		truesignal = signals[i]
		Z = float(trueZ[i])
		#~ print i, "Z is", Z
		fitsignal = lf.run(pix, Z)
		
		bdtentry = makeBDTentry(pix)
		
		if (bdtentry != None) and (fitsignal != None):
			full.append(bdtentry)
			scores.append(fitsignal)

	
	print time.asctime(time.localtime()), "Datasets produced!"
	
	print time.asctime(time.localtime()), "Training BDT" 
	
	#Train the BDT (Gradient Boosting Classifier)  and save
	
	rgr = ensemble.GradientBoostingRegressor(n_estimators=1000, max_depth=8, learning_rate=learningrate)
	rgr.fit(np.array(full), np.array(scores))
	
	rgrpicklepath = '/nfs/astrop/d6/rstein/BDTpickle/' + category + 'signalregressor.p'
	
	pickle.dump(rgr, open(rgrpicklepath, "wb"))
	
	print time.asctime(time.localtime()), "BDT Trained"
	print time.asctime(time.localtime()), "Saved BDT to", rgrpicklepath
	
	importances = rgr.feature_importances_
	indices = np.argsort(importances)[::-1]
	
	print signalbdtvariables
	
	print("Feature ranking:")
	
	for i in range(len(signalbdtvariables)):
		print("%d. %s (%f) " % (i + 1, signalbdtvariables[indices[i]], importances[indices[i]]))
	

	
