import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
import time, math
from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
import numpy as np
from sklearn.metrics import roc_curve, auc
import pylab as pl
import argparse
import csv
import random
from classes import *
import cPickle as pickle

def run(trainingset, statsset, mindetections):
	
	alldata = []
	
	trainsimset = pickle.load(open(trainingset, 'rb'))
	detectorcount = trainsimset[0].ndetectors
	j=0
	
	for k in range (detectorcount, mindetections -1, -1):
		
		full = []
		fulltest = []
		
		fullscore = []
		fulltestscore =[]
		
		fullclassifier=[]
		fulltestclassifier=[]
					
		
		for simset in trainsimset:
			for sim in simset.simulations:	
				recon = sim.reconstructed
				observed = sim.detected
				true = sim.true
				
				if int(observed.DCmultiplicity) == int(k):
					
					deltaz = int(math.fabs(float(true.Z)-float(recon.Z)))
					entry = makeBDTentry(recon)
					
					if entry != None:			
						full.append(entry)
						if float(deltaz) == float(0):
							fullscore.append(0.)
							fullclassifier.append(1)
							
						elif float(deltaz) > float(0):
							fullscore.append(deltaz)
							fullclassifier.append(0)
		
		print time.asctime(time.localtime()), "Datasets produced!"
		
		print time.asctime(time.localtime()), "Training BDT" 
		
		#Train the BDT (Gradient Boosting Classifier)  and save
			
		#~ rgr = DecisionTreeRegressor()
		#~ rgr.fit(full, fullscore)
		#~ 
		#~ pickle.dump(rgr, open('/d6/rstein/BDTpickle/regressor'+str(k) +'.p', "wb"))
		learningrate = [0.2, 0.2][j]
		
		clf = ensemble.GradientBoostingClassifier(max_depth=15, n_estimators=100, learning_rate=learningrate)
		clf.fit(full, fullclassifier)
		
		pickle.dump(clf, open('/d6/rstein/BDTpickle/classifier'+str(k) +'.p', 'wb'))
		
		print time.asctime(time.localtime()), "BDT Trained"
		
		print "Score on whole training sample is", clf.score(full, fullclassifier)
		#~ print "Score on whole test sample is", clf.score(fulltest, fulltestclassifier)
		
		importances = clf.feature_importances_
		indices = np.argsort(importances)[::-1]
		
		print("Feature ranking:")
	
		for f in range(len(bdtvariables)):
			print("%d. %s (%f) " % (f + 1, bdtvariables[indices[f]], importances[indices[f]]))
		
		plt.subplot(2,1,2)
		
		#~ probas_ = clf.fit(full, fullclassifier).predict_proba(fulltest)
		#~ 
		#~ fpr, tpr, thresholds = roc_curve(fulltestclassifier, probas_[:, 1])
		#~ roc_auc = auc(fpr, tpr)
		#~ print time.asctime(time.localtime()), "Area under the BDT ROC curve : %f" % roc_auc
		#~ title = 'BDT ROC curve (area = %0.2f)' % roc_auc
	#~ 
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
		#~ plt.savefig("/d6/rstein/Hamburg-Cosmic-Rays/positioning/graphs/roccurve" + str(k) + ".pdf")
		#~ plt.close()
		
		fullset = full
		#~ fullset.extend(fulltest)
		alldata.append(fullset)
		
		j+=1

	
	datasimset = pickle.load(open(statsset, 'rb'))
	
	for k in range (detectorcount, mindetections -1, -1):
		
		print "Loading Classifier", k	
		
		clf=pickle.load(open('/d6/rstein/BDTpickle/classifier'+str(k) +'.p','rb'))

		for simset in datasimset:
			for sim in simset.simulations:	
				recon = sim.reconstructed
				observed = sim.detected
				true = sim.true
						
				if int(observed.DCmultiplicity) == int(k):
					
					deltaz = math.fabs(float(true.Z)-float(recon.Z))
					entry = makeBDTentry(recon)
					BDT = clf.predict_proba([entry])[0][1]
					recon.BDTscore = BDT
	
	pickle.dump(datasimset, open(statsset, 'wb'))
	
	
				
