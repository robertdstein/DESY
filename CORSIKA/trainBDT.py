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

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="2842781")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

bdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/pixelBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		bdtvariables.append(row[0])
print bdtvariables

i = 1

for category in ["hess1"]:

	jobfolder = os.path.join(filepath, cfg.jobID)
	pickledatafolder = os.path.join(jobfolder, "bdtpickle")
	filename = pickledatafolder + "/" + category + "bdtdata.p"
	scorefilename = pickledatafolder + "/" + category + "bdtscores.p"

	if os.path.isfile(filename) and os.path.isfile(scorefilename):
		print "Loading dataset from", filename
		print "Loading scores from", scorefilename
	else:
		raise Exception("No BDT data file present at "+ filename)
	
	full = []
	fulltest = []
	
	fullscore = []
	fulltestscore =[]
	
	sig = []
	sigtest = []
	
	sigscore = []
	sigtestscore = []
	
	pixelset = pickle.load(open(filename, 'rb'))
	scoreset = pickle.load(open(scorefilename, 'rb'))
	
	print category, "dataset contains", len(pixelset), "images"
	
	for i in range(len(pixelset)):
		bdtentry = pixelset[i]
		truescore = scoreset[i]

		if random.random() < 0.5:
			full.append(bdtentry)
			fullscore.append(truescore)
	
			if float(truescore) == float(1):
				sig.append(bdtentry)
				sigscore.append(1.)
				
		else :
			fulltest.append(bdtentry)
			fulltestscore.append(truescore)
			
			if float(truescore) == float(1):
				sigtest.append(bdtentry)
				sigtestscore.append(1.)
	
	print time.asctime(time.localtime()), "Datasets produced!"
	
	print time.asctime(time.localtime()), "Training BDT" 
	
	#Train the BDT (Gradient Boosting Classifier)  and save
	
	clf = ensemble.GradientBoostingClassifier(max_depth=8, n_estimators=100, learning_rate=0.008)
	clf.fit(full, fullscore)
	
	clfpicklepath = '/nfs/astrop/d6/rstein/BDTpickle/' + category + 'pixelclassifier.p'
	
	pickle.dump(clf, open(clfpicklepath, "wb"))
	
	print time.asctime(time.localtime()), "BDT Trained"
	print time.asctime(time.localtime()), "Saved BDT to", clfpicklepath
	
	print "Score on whole training sample is", clf.score(full, fullscore)
	print "Score on whole test sample is", clf.score(fulltest, fulltestscore)
	print "Score on training signal is ", clf.score(sig, sigscore)
	print "Score on test signal is ", clf.score(sigtest, sigtestscore)
	
	importances = clf.feature_importances_
	indices = np.argsort(importances)[::-1]
	
	print bdtvariables
	
	print("Feature ranking:")
	
	for i in range(len(bdtvariables)):
		print("%d. %s (%f) " % (i + 1, bdtvariables[indices[i]], importances[indices[i]]))
	
