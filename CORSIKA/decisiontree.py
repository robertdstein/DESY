import time, math
from sklearn import ensemble
from sklearn import tree
import numpy as np
from sklearn.metrics import roc_curve, auc
import argparse
import csv
import cPickle as pickle
import random
import os
from telescopeclasses import *
import pydot
from sklearn.externals.six import StringIO  

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

def isfloat(value):
	try:
		float(value)
		return True
	except ValueError:
		return False
	except TypeError:
		return False

def makeBDTentry(pixelentry):
	bdtentry =[]
	for variable in bdtvariables:
		varsplit = variable.split('.')
		suffix = pixelentry
		if len(varsplit) > 1:
			for name in varsplit[:-1]:
				if hasattr(suffix, name):
					suffix = getattr(suffix, name)
			varname = varsplit[-1]
		else:
			varname = variable
		if hasattr(suffix, varname):
			newval = getattr(suffix, varname)
			if isfloat(newval):
				if float(newval) != float("inf"):
					bdtentry.append(newval)
				else:
					return None, None
			else:
					return None, None
		else:
			return None, None
	return bdtentry, pixelentry.truescore

i = 1
j = 50

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

hess1trainset = []
hess2trainset = []
hess1trainscores = []
hess2trainscores = []

while (i < j):
	targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
	if (os.path.isfile(targetpath)):
		event = pickle.load(open(targetpath, 'rb'))
		hess1pixels, hess2pixels = event.returnforBDT()
		for hess1pixel in hess1pixels:
			bdtentry, truescore = makeBDTentry(hess1pixel)
			if (bdtentry != None) and (truescore != None):
				hess1trainset.append(bdtentry)
				hess1trainscores.append(truescore)
		for hess2pixel in hess2pixels:
			bdtentry, truescore = makeBDTentry(hess2pixel)
			if (bdtentry != None) and (truescore != None):
				hess2trainset.append(bdtentry)
				hess2trainscores.append(truescore)
					
	if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
		print p+1
	i+=1

categories = ["hess2","hess1"]
learningrates = [0.005, 0.008]
trainsets = [hess1trainset, hess2trainset]
scores = [hess1trainscores, hess2trainscores]

for i in range(len(categories)):
	
	category = categories[i]
	learningrate = learningrates[i]
	trainset = trainsets[i]
	trainscoreset = scores[i]
	
	full = []
	fullscore = []
	#~ 
	#~ jobfolder = os.path.join(filepath, cfg.jobID)
	#~ pickledatafolder = os.path.join(jobfolder, "bdtpickle")
	#~ trainfilename = pickledatafolder + "/" + category + "trainbdtdata.p"
	#~ trainscorefilename = pickledatafolder + "/" + category + "trainbdtscores.p"
#~ 
	#~ if os.path.isfile(trainfilename) and os.path.isfile(trainscorefilename):
		#~ print "Loading training dataset from", trainfilename
		#~ print "Loading training scores from", trainscorefilename
	#~ else:
		#~ raise Exception("No BDT data file present at "+ filename)
	#~ 
	#~ full = []
	#~ fullscore = []
	#~ 
	#~ sig = []
	#~ sigscore = []
#~ 
	#~ trainset = pickle.load(open(trainfilename, 'rb'))
	#~ trainscoreset = pickle.load(open(trainscorefilename, 'rb'))
	
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
	
	
	print time.asctime(time.localtime()), "Datasets produced!"
	
	print time.asctime(time.localtime()), "Training BDT" 
	
	#Train the BDT (Gradient Boosting Classifier)  and save
	
	clf = tree.DecisionTreeClassifier()
	clf.fit(full, fullscore)
	
	importances = clf.feature_importances_
	indices = np.argsort(importances)[::-1]
	
	print bdtvariables
	
	print("Feature ranking:")
	
	for i in range(len(bdtvariables)):
		print("%d. %s (%f) " % (i + 1, bdtvariables[indices[i]], importances[indices[i]]))
	
	saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/decisiontree" + category + ".pdf"
	print "Saving to", saveto

	dot_data = StringIO()
	tree.export_graphviz(clf, feature_names=bdtvariables, class_names=["Non-DC", "DC"],  filled=True, rounded=True,out_file=dot_data) 
	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
	graph.write_pdf(saveto)
	graph.write_pdf("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/decisiontree" + category + ".pdf")
	
