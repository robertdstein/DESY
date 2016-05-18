import time, math
from sklearn import ensemble
from sklearn import tree
from sklearn.externals.six import StringIO
import numpy as np
from sklearn.metrics import roc_curve, auc
import argparse
import csv
import cPickle as pickle
import random
import os
from telescopeclasses import *
import pydot 

for category in ["hess1", "hess2"]:
	
	clfpicklepath = '/nfs/astrop/d6/rstein/BDTpickle/' + category + 'pixelclassifier.p'
	if os.path.isfile(clfpicklepath):
		print "loading Classifier from", clfpicklepath
		clf = pickle.load(open(clfpicklepath, "rb"))
		dot_data = StringIO() 
		tree.export_graphviz(clf, out_file=dot_data)
		graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
		graph.write_pdf("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/"+category+"tree.pdf") 

