import time, math
from sklearn.tree import DecisionTreeRegressor
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
			
			fullclassifier=[]
			fulltestclassifier=[]
			
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
							entry = [reconx, recony, reconHeight, reconEPN, likelihood]
							
							if int(j) < int(testcount):
								full.append(entry)
								
								if float(deltaz) == float(0):
									fullscore.append(0.)
									fullclassifier.append(1)
									sig.append(entry)
									sigscore.append(0.)
									
								elif float(deltaz) > float(0):
									fullscore.append(deltaz)
									fullclassifier.append(0)
									bkg.append(entry)
									bkgscore.append(deltaz)
									
							else :
								fulltest.append(entry)
								
								if float(deltaz) == float(0):
									fulltestscore.append(0.)
									fulltestclassifier.append(1)
									sigtest.append(entry)
									sigtestscore.append(0.)
									
								elif float(deltaz) > float(0):
									fulltestscore.append(deltaz)
									fulltestclassifier.append(0)
									bkgtest.append(entry)
									bkgtestscore.append(deltaz)
								
							j += 1
			
			print time.asctime(time.localtime()), "Datasets produced!"
			
			print time.asctime(time.localtime()), "Training BDT" 
			
			#Train the BDT (Gradient Boosting Classifier)  and save
			
			lr = (0.25/math.sqrt(math.log(count)))
			md = int(math.log(count))
		
			rgr = DecisionTreeRegressor()
			rgr.fit(full, fullscore)
			
			joblib.dump(rgr, '/afs/desy.de/user/s/steinrob/Documents/DESY/BDT/pickle/' + str(source) + str(k) + 'regressor.pkl')
			
			clf = ensemble.GradientBoostingClassifier(max_depth=1, n_estimators=100, learning_rate=0.05)
			clf.fit(full, fullclassifier)
			
			joblib.dump(clf, '/afs/desy.de/user/s/steinrob/Documents/DESY/BDT/pickle/' + str(source) + str(k) + 'classifier.pkl')
			
			print time.asctime(time.localtime()), "BDT Trained"
			
			print "Score on whole training sample is", clf.score(full, fullclassifier)
			print "Score on whole test sample is", clf.score(fulltest, fulltestclassifier)
			#~ print "Score on training signal is ", clf.score(sig, sigscore)
			#~ print "Score on test signal is ", clf.score(sigtest, sigtestscore)
			#~ print "Score on training background is ", clf.score(bkg, bkgscore)
			#~ print "Score on test background is ", clf.score(bkgtest, bkgtestscore)
			
			bins = 50
			
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
			
			sigweights = np.ones(len(sigtestprobs))/float(len(sigtestprobs))
			
			plt.hist(sigtestprobs, weights=sigweights,
					 color='r', alpha=0.5, bins=bins, range=plotrange,
					 histtype='stepfilled',
					 label='DeltaZ = 0 (test)')
					 
			bkgprobs=[]
			bkgtestprobs = []
			
			probs = clf.predict_proba(bkg)
			for pair in probs:
				bkgprobs.append(pair[1])
			
			probs = clf.predict_proba(bkgtest)
			for pair in probs:
				bkgtestprobs.append(pair[1])
				
			bkgweights = np.ones(len(bkgtestprobs))/float(len(bkgtestprobs))
		
			
			plt.hist(bkgtestprobs, weights=bkgweights,
					 color='b', alpha=0.5, bins=bins, range=plotrange,
					 histtype='stepfilled',
					 label='DeltaZ > 0 (test)')
		
			plt.xlabel("BDT output")
			plt.ylabel("Arbitrary units")
			plt.legend(loc='best')
			
			plt.savefig("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/BDTresponse" + str(k) + ".pdf")
			
			plt.subplot(2,1,2)
			
			probas_ = clf.fit(full, fullclassifier).predict_proba(fulltest)
			
			fpr, tpr, thresholds = roc_curve(fulltestclassifier, probas_[:, 1])
			roc_auc = auc(fpr, tpr)
			print time.asctime(time.localtime()), "Area under the BDT ROC curve : %f" % roc_auc
			title = 'BDT ROC curve (area = %0.2f)' % roc_auc
		
			plt.clf()
		
			plt.plot(fpr, tpr, label=title)
			plt.plot([0, 1], [0, 1], 'k--')
			plt.xlim([0.0, 1.0])
			plt.ylim([0.0, 1.0])
			plt.xlabel('Fraction of Incorrectly Reconstructed Events')
			plt.ylabel('Fraction of Correctly Reconstructed Evens')
			plt.title('ROC Curve')
			plt.legend(loc="lower right")
			
			plt.savefig("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/graphs/roccurve" + str(k) + ".pdf")
			plt.close()
			
			fullset = full
			fullset.extend(fulltest)
			alldata.append(fullset)
			
		else:
			alldata.append([])
	
		
	with open("/afs/desy.de/user/s/steinrob/Documents/DESY/positioning/reconstructeddata/" + str(source) + "_BDT.csv", 'wb') as csvout:
		writer = csv.writer(csvout, delimiter=',', quotechar='|')
		writer.writerow(["Detections","X","Y","Energy Per Nucleon","Z","Height","True X","True Y","True Energy per nucleon","True Z","True Height", "Phi", "Epsilon", "Theta", "Guess Log Likelihood", "Classifier", "BDT"])
	
		for k in range (detectorcount, mindetections -1, -1):
			
			count = allcounts[detectorcount-k]
		
			testcount = int(float(count)/4.) 
		
			if int(testcount) > int(1):
	
				subset = alldata[detectorcount-k]
				
				clf=joblib.load('/afs/desy.de/user/s/steinrob/Documents/DESY/BDT/pickle/' + str(source) + str(k) + 'classifier.pkl')
				
				probs=clf.predict_proba(subset)
			
				rgr= joblib.load('/afs/desy.de/user/s/steinrob/Documents/DESY/BDT/pickle/' + str(source) + str(k) + 'regressor.pkl')
								
				classes = rgr.predict(subset)
		
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
								classifier = classes[j]
							
								row.append(classifier)
								row.append(BDT)
								writer.writerow(row)
							
								j+=1
