import time, math
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import matplotlib.pyplot as plt
import argparse
import csv
from sklearn.externals import joblib

def run(source, detectorcount, mindetections, allcounts):
	
	alldata = []
	
	for k in range (detectorcount, mindetections -1, -1):
		
		count = allcounts[detectorcount-k]
		
		testcount = int(float(count)/4.) 
		print k, count, testcount
		
		if int(testcount) > int(1):

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
			
			with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='|')
				
				j = 0
		
				for row in reader:
					if j == 0:
						j = 1
					else:
						detections = row[0]
						reconx = row[1]
						recony = row[2]
						reconEPN = row[3]
						reconZ = row[4]
						reconHeight = row[5]
						truex = row[6]
						truey = row[7]
						trueEPN = row[8]
						trueZ = row[9]
						trueHeight = row[10]
						likelihood = row[13]
						
						if int(detections) == int(k):
							
							deltaz = math.fabs(float(trueZ)-float(reconZ))
							entry = [reconEPN, likelihood]
							
							if int(j) < int(testcount):
								full.append(entry)
								
								if float(deltaz) == float(0):
									fullscore.append(1)
									sig.append(entry)
									sigscore.append(1)
									
								elif float(deltaz) > float(0):
									fullscore.append(0)
									bkg.append(entry)
									bkgscore.append(0)
									
							else :
								fulltest.append(entry)
								
								if float(deltaz) == float(0):
									fulltestscore.append(1)
									sigtest.append(entry)
									sigtestscore.append(1)
									
								elif float(deltaz) > float(0):
									fulltestscore.append(0)
									bkgtest.append(entry)
									bkgtestscore.append(0)
								
							j += 1
			
			print time.asctime(time.localtime()), "Datasets produced!"
			
			print time.asctime(time.localtime()), "Training BDT" 
			
			#Train the BDT (Gradient Boosting Classifier)  and save
		
			clf = ensemble.GradientBoostingClassifier(max_depth = 3, n_estimators = 100)
			clf.fit(full, fullscore)
			
			joblib.dump(clf, '/afs/desy.de/user/s/steinrob/Documents/DESY/BDT/pickle/' + str(source) + str(k) + '.pkl')
			
			print time.asctime(time.localtime()), "BDT Trained"
			
			print clf.feature_importances_
			
			print "Score on whole training sample is", clf.score(full, fullscore)
			print "Score on whole test sample is", clf.score(fulltest, fulltestscore)
			print "Score on training signal is ", clf.score(sig, sigscore)
			print "Score on test signal is ", clf.score(sigtest, sigtestscore)
			print "Score on training background is ", clf.score(bkg, bkgscore)
			print "Score on test background is ", clf.score(bkgtest, bkgtestscore)
			
			bins = 20
			
			sigprobs=[]
			sigtestprobs = []
			
			probs = clf.predict_proba(sig)
			for pair in probs:
				sigprobs.append(pair[1])
			
			probs = clf.predict_proba(sigtest)
			for pair in probs:
				sigtestprobs.append(pair[1])
		
			plt.figure()
			
			plotrange=[0,1]
			
			plt.hist(sigtestprobs,
					 color='r', alpha=0.5, bins=bins, range=plotrange,
					 histtype='stepfilled', normed=True,
					 label='DeltaZ = 0 (test)')
		
			hist, bins = np.histogram(sigprobs,
									  bins=bins,range=plotrange, normed=True)
			scale = len(sigtestprobs) / sum(hist)
			err = np.sqrt(hist * scale) / scale
			
			width = (bins[1] - bins[0])
			center = (bins[:-1] + bins[1:]) / 2
			plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label='DeltaZ = 0  (train)')
			
			bkgprobs=[]
			bkgtestprobs = []
			
			probs = clf.predict_proba(bkg)
			for pair in probs:
				bkgprobs.append(pair[1])
			
			probs = clf.predict_proba(bkgtest)
			for pair in probs:
				bkgtestprobs.append(pair[1])
		
			
			plt.hist(bkgtestprobs,
					 color='b', alpha=0.5, bins=bins, range=plotrange,
					 histtype='stepfilled', normed=True,
					 label='DeltaZ > 0 (test)')
		
			hist, bins = np.histogram(bkgprobs,
									  bins=bins,range=plotrange, normed=True)
			scale = len(bkgtestprobs) / sum(hist)
			err = np.sqrt(hist * scale) / scale
			
			width = (bins[1] - bins[0])
			center = (bins[:-1] + bins[1:]) / 2
			plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label='DeltaZ > 0 (train)')
		
			plt.xlabel("BDT output")
			plt.ylabel("Arbitrary units")
			plt.legend(loc='best')
			
			plt.savefig("BDTresponse" + str(k) + ".pdf")
			
			plt.subplot(2,1,2)
			
			probas_ = clf.fit(full, fullscore).predict_proba(fulltest)
			fpr, tpr, thresholds = roc_curve(fulltestscore, probas_[:, 1])
			roc_auc = auc(fpr, tpr)
			print time.asctime(time.localtime()), "Area under the BDT ROC curve : %f" % roc_auc
			title = 'BDT ROC curve (area = %0.2f)' % roc_auc
		
			plt.clf()
		
			plt.plot(fpr, tpr, label=title)
			plt.plot([0, 1], [0, 1], 'k--')
			plt.xlim([0.0, 1.0])
			plt.ylim([0.0, 1.0])
			plt.xlabel('False Positive Rate')
			plt.ylabel('True Positive Rate')
			plt.title('ROC Curve')
			plt.legend(loc="lower right")
			
			plt.savefig("roccurve" + str(k) + ".pdf")
			plt.close()
			
			fullset = full
			fullset.extend(fulltest)
			alldata.append(fullset)
			
		else:
			alldata.append([])
	
		
	with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/" + str(source) + "_BDT.csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Detections","X","Y","Energy Per Nucleon","Z","Height","True X","True Y","True Energy per nucleon","True Z","True Height", "Phi", "Epsilon", "Theta", "Guess Log Likelihood", "BDT"])
	
		for k in range (detectorcount, mindetections -1, -1):
			
			count = allcounts[detectorcount-k]
		
			testcount = int(float(count)/4.) 
		
			if int(testcount) > int(1):
	
				subset = alldata[detectorcount-k]
			
				clf = joblib.load('/afs/desy.de/user/s/steinrob/Documents/DESY/BDT/pickle/' + str(source) + str(k) + '.pkl')
								
				probs = clf.predict_proba(subset)
		
				with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/"+ str(source) +".csv", 'rb') as csvfile:
					reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					
					j = -1
				
					for row in reader:
						if j < 0:
							j = 0
							
						else:
							detections = row[0]
							reconx = row[1]
							recony = row[2]
							reconEPN = row[3]
							reconZ = row[4]
							reconHeight = row[5]
							truex = row[6]
							truey = row[7]
							trueEPN = row[8]
							trueZ = row[9]
							trueHeight = row[10]
							likelihood = row[13]
							
							if int(detections) == int(k):
								
								entry = [reconEPN, likelihood]
								
								BDT = probs[j][1]
							
								row.append(BDT)
								writer.writerow(row)
							
								j+=1
								
	

	
