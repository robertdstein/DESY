import ROOT, time
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import argparse
import csv
from sklearn.externals import joblib

def run(name, bins = 30, quick = False):
    
    #Plot TMVA-style response curves
    
    print time.asctime(time.localtime()), "Plotting Response Curves"
    
    v = joblib.load("pickle/variables.pkl")
    
    if quick == True:
        clf = joblib.load("pickle/" + name +"quick.pkl")
        signal = joblib.load('pickle/signalq.pkl')
        signaltest = joblib.load('pickle/signaltestq.pkl')
        signaloutput = joblib.load('pickle/signaloutputq.pkl')
        signaloutputtest = joblib.load('pickle/signaloutputtestq.pkl')
        background = joblib.load('pickle/backgroundq.pkl')
        backgroundtest = joblib.load('pickle/backgroundtestq.pkl')
        backgroundoutput= joblib.load('pickle/backgroundoutputq.pkl')
        backgroundoutputtest = joblib.load('pickle/backgroundoutputtestq.pkl')
    
    else:
        clf = joblib.load("pickle/" + name + ".pkl")
        signal = joblib.load('pickle/signal.pkl')
        signaltest = joblib.load('pickle/signaltest.pkl')
        signaloutput = joblib.load('pickle/signaloutputtest.pkl')
        signaloutputtest = joblib.load('pickle/signaloutputtest.pkl')
        background = joblib.load('pickle/background.pkl')
        backgroundtest = joblib.load('pickle/backgroundtest.pkl')
        backgroundoutput= joblib.load('pickle/backgroundoutput.pkl')
        backgroundoutputtest = joblib.load('pickle/backgroundoutputtest.pkl')   
    
    #Produce seperate signal and background curves
    
    decisions1 = []
    for X,y in ((signal, signaloutput), (signaltest, signaloutputtest)):
        d = clf.decision_function(X[y>0.5]).ravel()
        decisions1 += [d]
    
    decisions2 = []
    for X,y in ((background, backgroundoutput), (backgroundtest, backgroundoutputtest)):
        d = clf.decision_function(X[y<0.5]).ravel()
        decisions2 += [d]
        
    low = min(np.min(d) for d in decisions1)
    high = max(np.max(d) for d in decisions1)
    low_high = (low,high)
    
    plt.figure()
    
    plt.hist(decisions1[0],
             color='r', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='S (train)')

    hist, bins = np.histogram(decisions1[1],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions1[1]) / sum(hist)
    err = np.sqrt(hist * scale) / scale
    
    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='S (test)')
    
    plt.hist(decisions2[0],
             color='b', alpha=0.5, range=low_high, bins=bins,
             histtype='stepfilled', normed=True,
             label='B (train)')
    hist, bins = np.histogram(decisions2[1],
                              bins=bins, range=low_high, normed=True)
    scale = len(decisions2[0]) / sum(hist)
    err = np.sqrt(hist * scale) / scale

    plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='B (test)')

    plt.xlabel("BDT output")
    plt.ylabel("Arbitrary units")
    plt.legend(loc='best')
    
    if quick == True:
        plt.savefig("output/Response" + name + "quick.pdf")
    else:
        plt.savefig("output/Response" + name + ".pdf")