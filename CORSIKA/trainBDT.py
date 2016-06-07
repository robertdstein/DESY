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
parser.add_argument("-jid", "--jobID", default="traindata")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

bdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/pixelBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		bdtvariables.append(row[0])
print bdtvariables

categories = ["hess2","hess1"]
learningrates = [0.005, 0.008]

for i in range(len(categories)):
	
	category = categories[i]
	learningrate = learningrates[i]

	jobfolder = os.path.join(filepath, cfg.jobID)
	pickledatafolder = os.path.join(jobfolder, "bdtpickle")
	trainfilename = pickledatafolder + "/" + category + "trainbdtdata.p"
	trainscorefilename = pickledatafolder + "/" + category + "trainbdtscores.p"

	if os.path.isfile(trainfilename) and os.path.isfile(trainscorefilename):
		print "Loading training dataset from", trainfilename
		print "Loading training scores from", trainscorefilename
	else:
		raise Exception("No BDT data file present at "+ filename)
	
	full = []
	fullscore = []
	
	sig = []
	sigscore = []

	trainset = pickle.load(open(trainfilename, 'rb'))
	trainscoreset = pickle.load(open(trainscorefilename, 'rb'))
	
	print category, "training dataset contains", len(trainset), "images"
	
	for i in range(len(trainset)):
		bdtentry = trainset[i]
		truescore = trainscoreset[i]
		
		add = True
		for val in bdtentry:
			if float(val) == float("inf"):
				add = False
				
		if add:

			full.append(bdtentry)
			fullscore.append(truescore)
	
			if float(truescore) == float(1):
				sig.append(bdtentry)
				sigscore.append(1.)
	
	print time.asctime(time.localtime()), "Datasets produced!"
	
	print time.asctime(time.localtime()), "Training BDT" 
	
	#Train the BDT (Gradient Boosting Classifier)  and save
	
	clf = ensemble.GradientBoostingClassifier(max_depth=8, n_estimators=100, learning_rate=learningrate)
	clf.fit(full, fullscore)
	
	clfpicklepath = '/nfs/astrop/d6/rstein/BDTpickle/' + category + 'pixelclassifier.p'
	
	pickle.dump(clf, open(clfpicklepath, "wb"))
	
	print time.asctime(time.localtime()), "BDT Trained"
	print time.asctime(time.localtime()), "Saved BDT to", clfpicklepath
	
	importances = clf.feature_importances_
	indices = np.argsort(importances)[::-1]
	
	print bdtvariables
	
	print("Feature ranking:")
	
	for i in range(len(bdtvariables)):
		print("%d. %s (%f) " % (i + 1, bdtvariables[indices[i]], importances[indices[i]]))
	
	testfilename = pickledatafolder + "/" + category + "testbdtdata.p"
	testscorefilename = pickledatafolder + "/" + category + "testbdtscores.p"

	if os.path.isfile(testfilename) and os.path.isfile(testscorefilename):
		print "Loading test dataset from", testfilename
		print "Loading test scores from", testscorefilename
	else:
		print Exception("No BDT data file present at "+ testfilename)
	
	testset = pickle.load(open(testfilename, 'rb'))
	testscoreset = pickle.load(open(testscorefilename, 'rb'))
	
	print category, "training dataset contains", len(testset), "images"
		
	fulltest = []
	fulltestscore =[]
	
	sigtest = []
	sigtestscore = []
	
	for i in range(len(testset)):
		bdtentry = testset[i]
		truescore = testscoreset[i]

		fulltest.append(bdtentry)
		fulltestscore.append(truescore)

		if float(truescore) == float(1):
			sigtest.append(bdtentry)
			sigtestscore.append(1.)
	
	print "Score on whole training sample is", clf.score(full, fullscore)
	if os.path.isfile(testfilename) and os.path.isfile(testscorefilename):
		print "Score on whole test sample is", clf.score(fulltest, fulltestscore)
	print "Score on training signal is ", clf.score(sig, sigscore)
	if os.path.isfile(testfilename) and os.path.isfile(testscorefilename):
		print "Score on test signal is ", clf.score(sigtest, sigtestscore)
