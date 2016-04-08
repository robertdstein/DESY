import ROOT, time
from sklearn import ensemble
import numpy as np
import matplotlib.pyplot as plt
import argparse
import csv
from sklearn.externals import joblib
from sklearn.decomposition import IncrementalPCA, PCA
import array
import itertools
from scipy import linalg
import matplotlib as mpl
from sklearn import mixture 

def run(name, source, quick=False):
    print time.asctime(time.localtime()), "Creating Tree"
    
    #Select tree to be recreated
    
    f = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/MC_Bplus_Kplusmue_qsqminPtBranch.root")
    t = f.Get("DecayTree")
        
    newname = "MC_Bplus_Kplusmue_BDT"
    
    fulldata = joblib.load('pickle/fulldata.pkl')

    clf = joblib.load("pickle/" + name +".pkl")
    
    nFileName = "/net/storage03/data/users/rstein/tuples/qsq/" + newname + ".root"
    print time.asctime(time.localtime()), ('saving File to ' + nFileName)

    nf = ROOT.TFile(nFileName, "RECREATE")
    print time.asctime(time.localtime()), "Cloning Tree"
    nt = t.CloneTree(-1, 'fast')

    nt.SetBranchStatus("*", 0)

    BDT = (array.array('d',[0]))
    BDTBranch = nt.Branch("BDT", BDT, "BDT/D")

    print time.asctime(time.localtime()), "Filling BDT Branch"
    
    print time.asctime(time.localtime()), "Itterating over", nt.GetEntries() , "events"
    
    #Predict probability of signal for every entry, and add to tree
    
    for i in fulldata:
        BDT[0] = clf.predict_proba(i)[0][1]
        BDTBranch.Fill()
    
    print time.asctime(time.localtime()), "Branch Filled!"
    print time.asctime(time.localtime()), "Writing Tree"
    
    nt.SetBranchStatus("*", 1)
    nt.Write("DecayTree")
    nf.Close()
    f.Close()
    
    print time.asctime(time.localtime()), "Tree Written"