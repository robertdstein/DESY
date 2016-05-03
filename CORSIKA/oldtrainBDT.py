import time, math
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import argparse
import csv
from sklearn.externals import joblib
import random

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="1385224")

cfg = parser.parse_args()

filepath = "/nfs/astrop/d6/rstein/data/"

i = 1

targetfolder = filepath + cfg.jobID +"/"
filename = targetfolder + "BDTpixels.csv"

full = []
fulltest = []

fullscore = []
fulltestscore =[]

sig = []
sigtest = []

sigscore = []
sigtestscore = []

bkg = []
bkgtest = []

bkgscore = []
bkgtestscore = []

with open(filename, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')

	header = next(reader)

	for row in reader:
		count = float(row[0])
		QDC = float(row[1])
		Dd = float(row[2])
		Dcg = float(row[3])
		Dline = float(row[4])
		energy = float(row[5])
		nnmean = float(row[6])
		score = float(row[7])
		channel0 = float(row[8])
		signal = count-nnmean
		entry = [count, QDC, Dd, Dcg, Dline, nnmean, signal]
		
		if random.random() < 0.5:
			full.append(entry)
			fullscore.append(score)

			if score == float(1):
				sig.append(entry)
				sigscore.append(1.)
				
			elif score == float(0):
				bkg.append(entry)
				bkgscore.append(0.)
				
		else :
			fulltest.append(entry)
			fulltestscore.append(score)
			
			if score == float(1):
				sigtest.append(entry)
				sigtestscore.append(1.)
				
			elif score == float(0):
				bkgtest.append(entry)
				bkgtestscore.append(0.)

print time.asctime(time.localtime()), "Datasets produced!"

print time.asctime(time.localtime()), "Training BDT" 

#Train the BDT (Gradient Boosting Classifier)  and save

clf = ensemble.GradientBoostingClassifier(max_depth=8, n_estimators=100, learning_rate=0.008)
clf.fit(full, fullscore)

joblib.dump(clf, '/nfs/astrop/d6/rstein/BDTpickle/DCpixelclassifier.pkl')

print time.asctime(time.localtime()), "BDT Trained"

print "Score on whole training sample is", clf.score(full, fullscore)
print "Score on whole test sample is", clf.score(fulltest, fulltestscore)
print "Score on training signal is ", clf.score(sig, sigscore)
print "Score on test signal is ", clf.score(sigtest, sigtestscore)
print "Score on training background is ", clf.score(bkg, bkgscore)
print "Score on test background is ", clf.score(bkgtest, bkgtestscore)

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

v = ["Channel1", "QDC", "Dd", "Dcg", "Dline", "Nearest Neighbour Mean", "DC Signal"]

print v

print("Feature ranking:")

for i in range(len(v)):
	print("%d. %s (%f) " % (i + 1, v[indices[i]], importances[indices[i]]))

#~ import matplotlib as mpl
#~ mpl.use('Agg')
#~ import matplotlib.pyplot as plt
#~ 
#~ bins = 50
#~ 
#~ sigprobs=[]
#~ sigtestprobs = []
#~ 
#~ probs = clf.predict_proba(sig)
#~ for pair in probs:
	#~ sigprobs.append(pair[1])
#~ 
#~ probs = clf.predict_proba(sigtest)
#~ for pair in probs:
	#~ sigtestprobs.append(pair[1])
#~ 
#~ plt.figure()
#~ 
#~ plotrange=[0,1]
#~ 
#~ sigweights = np.ones(len(sigtestprobs))/float(len(sigtestprobs))
#~ 
#~ plt.hist(sigtestprobs, weights=sigweights,
		 #~ color='r', alpha=0.5, bins=bins, range=plotrange,
		 #~ histtype='stepfilled',
		 #~ label='DC pixel (test)')
		 
#~ bkgprobs=[]
#~ bkgtestprobs = []
#~ 
#~ probs = clf.predict_proba(bkg)
#~ for pair in probs:
	#~ bkgprobs.append(pair[1])
#~ 
#~ probs = clf.predict_proba(bkgtest)
#~ for pair in probs:
	#~ bkgtestprobs.append(pair[1])
	#~ 
#~ bkgweights = np.ones(len(bkgtestprobs))/float(len(bkgtestprobs))
#~ 
#~ 
#~ plt.hist(bkgtestprobs, weights=bkgweights,
		 #~ color='b', alpha=0.5, bins=bins, range=plotrange,
		 #~ histtype='stepfilled',
		 #~ label='Not DC pixel (test)')
#~ 
#~ plt.xlabel("BDT output")
#~ plt.ylabel("Arbitrary units")
#~ plt.legend(loc='best')
#~ 
#~ plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/BDTresponse.pdf")
#~ 
#~ plt.plot()
#~ 
#~ probas_ = clf.fit(full, fullscore).predict_proba(fulltest)
#~ 
#~ fpr, tpr, thresholds = roc_curve(fulltestscore, probas_[:, 1])
#~ roc_auc = auc(fpr, tpr)
#~ print time.asctime(time.localtime()), "Area under the BDT ROC curve : %f" % roc_auc
#~ title = 'BDT ROC curve (area = %0.2f)' % roc_auc

#~ plt.clf()
#~ 
#~ plt.plot(fpr, tpr, label=title)
#~ plt.plot([0, 1], [0, 1], 'k--')
#~ plt.xlim([0.0, 1.0])
#~ plt.ylim([0.0, 1.0])
#~ plt.xlabel('Fraction of Incorrectly Reconstructed Events')
#~ plt.ylabel('Fraction of Correctly Reconstructed Evens')
#~ plt.title('ROC Curve')
#~ plt.legend(loc="lower right")
#~ 
#~ plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/roccurve.pdf")
#~ plt.close()
