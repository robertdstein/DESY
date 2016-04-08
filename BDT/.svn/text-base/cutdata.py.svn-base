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

def run():
    print time.asctime(time.localtime()), "Creating Tree"
    
    #The percentage x for the selection requirement BDT > x%
    percentage = 90
    
    selection = "(BDT > 0." + str(percentage) +")"     
        
    name = "DATA_Bplus_Kplusmue_BDT"

    print time.asctime(time.localtime()), "Creating Second Tree"

    h = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + name + ".root", "READ")
    v = h.Get("DecayTree")
    g = ROOT.TFile("/net/storage03/data/users/rstein/tuples/qsq/" + name+ "_cut" + str(percentage) + ".root", "recreate") 
    
    #Producing a new tree    
    
    vcount = v.GetEntriesFast()
    print time.asctime(time.localtime()), "Contains", vcount, "entries"
    print time.asctime(time.localtime()), "Contains", v.GetEntries(selection), "entries to be copied"

    print time.asctime(time.localtime()), "Cloning Tree..."
    nt=v.CopyTree(selection)

    print time.asctime(time.localtime()), "Tree Cloned!"
    nt.Write()
    g.Close()

    print time.asctime(time.localtime()), "Branch Filled!"