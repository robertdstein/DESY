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

for category in ["hess1", "hess2"]:
	
	clfpicklepath = '/nfs/astrop/d6/rstein/BDTpickle/' + category + 'pixelclassifier.p'
	if os.path.isfile(clfpicklepath):
		clf = pickle.load(open(clfpicklepath, "rb"))
		
		print "loading Classifier from", clfpicklepath
		
		importances = clf.feature_importances_
		indices = np.argsort(importances)[::-1]
		
		print bdtvariables
		
		print("Feature ranking:")
		
		for i in range(len(bdtvariables)):
			print("%d. %s (%f) " % (i + 1, bdtvariables[indices[i]], importances[indices[i]]))
	
