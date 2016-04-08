import ROOT, time
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
import csv
from sklearn.externals import joblib

def run(name, quick = False):
    
    #Producing a ranked list of variables
    
    print time.asctime(time.localtime()), "Ranking Features"
    
    if quick == True:
        clf = joblib.load("pickle/" + name +"quick.pkl")
    else:
        clf = joblib.load("pickle/" + name + ".pkl")

    v = joblib.load("pickle/variables.pkl")

    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]

    print("Feature ranking:")

    for f in range(len(v)):
        print("%d. %s (%f) " % (f + 1, v[indices[f]], importances[indices[f]]))