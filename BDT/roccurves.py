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
    
    #Load datasets for ROC Curve production
    
    print time.asctime(time.localtime()), "Making ROC Curves"
    
    if quick == True:
        clf = joblib.load("pickle/" + name +"quick.pkl")
        data = joblib.load("pickle/dataq.pkl")
        output = joblib.load("pickle/outputq.pkl")
        datatest = joblib.load("pickle/datatestq.pkl")
        outputtest = joblib.load("pickle/outputtestq.pkl")
    
    else:
        clf = joblib.load("pickle/" + name + ".pkl")
        data = joblib.load("pickle/data.pkl")
        output = joblib.load("pickle/output.pkl")
        datatest = joblib.load("pickle/datatest.pkl")
        outputtest = joblib.load("pickle/outputtest.pkl")
    
    #Plot ROC curves    
    
    probas_ = clf.fit(data, output).predict_proba(datatest)
    fpr, tpr, thresholds = roc_curve(outputtest, probas_[:, 1])
    roc_auc = auc(fpr, tpr)
    print time.asctime(time.localtime()), "Area under the BDT ROC curve : %f" % roc_auc
    title = 'BDT ROC curve (area = %0.2f)' % roc_auc

    pl.clf()

    pl.plot(fpr, tpr, label=title)
    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('ROC Curve')
    pl.legend(loc="lower right")
    if quick == True:
        pl.savefig("output/ROC_" + name +"quick.pdf")
    else:
        pl.savefig("output/ROC_3Pres" + name +".pdf")
    
    print time.asctime(time.localtime()), "ROC Curve Saved as ROC_" + name +".pdf !" 