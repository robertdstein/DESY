import sys
import os.path
import argparse, math, random, time
import csv
import numpy as np
import cPickle as pickle
from telescopeclasses import *
from matplotlib import rc
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-jid", "--jobID", default="testdata")

cfg = parser.parse_args()

hess1rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess1signalregressor.p'
hess2rgrpath = '/nfs/astrop/d6/rstein/BDTpickle/hess2signalregressor.p'
if os.path.isfile(hess1rgrpath):
	hess1rgr = pickle.load(open(hess1rgrpath, "r"))
else:
	print "No hess1 pickle!"
if os.path.isfile(hess2rgrpath):
	hess2rgr = pickle.load(open(hess2rgrpath, "r"))
else:
	print "No hess2 pickle!"
	
signalbdtvariables = []
with open('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/signalBDTvariables.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in reader:
		signalbdtvariables.append(row[0])
print signalbdtvariables

minmultiplicity=3

def makeBDTentry(pixelentry):
	bdtentry =[]
	for variable in signalbdtvariables:
		varsplit = variable.split('.')
		suffix = pixelentry
		if len(varsplit) > 1:
			for name in varsplit[:-1]:
				 suffix = getattr(suffix, name)
			varname = varsplit[-1]
		else:
			varname = variable
		if hasattr(suffix, varname):
			newval = getattr(suffix, varname)
			bdtentry.append(newval)
		else:
			return None
	return bdtentry

for sigfit in ["rgr"]:
	filepath = "/nfs/astrop/d6/rstein/data/"
	i = 1
	j = 15000
	totalimages = [0, 0]
	truefour = 0
	truefive=0
	reconfour=0
	reconfive=0
	wronghighmultiplicity = 0
	triggeredimages = [0, 0]
	DCpasstotal = [0, 0]
	correctimages =[0, 0]
	totalcut=[0, 0]
	correctcut = [0, 0]
	
	oldtotalimages =[0, 0]
	oldDCpasstotal = [0, 0]
	oldcorrectimages =[0, 0]
	oldtotalcut=[0, 0]
	oldcorrectcut = [0, 0]
	
	altcorrectimages =[0, 0]
	alttotalcut=[0, 0]
	altcorrectcut = [0, 0]
	
	combinedtotal = [0, 0]
	combinedcorrect = [0, 0]
	
	fulltotal = [0, 0]
	fullcorrect = [0, 0]
	
	finaltotal = [0, 0]
	finalcorrect = [0, 0]
		
	oldcombinedtotal = [0, 0]
	oldcombinedcorrect = [0, 0]
	
	
	cut, ucut, QDCcut, DCcut, signalcut = ic.runforstats()
	arcut = ic.runar()
	
	right = [[], []]
	wrong = [[], []]
	
	oldright=[[], []]
	oldwrong=[[], []]
	
	combinedright = [[], []]
	combinedwrong = [[], []]
	rightDCcounts =[[], []]
	wrongDCcounts=[[],[]]
	rightscores =[[], []]
	wrongscores = [[], []]
	rightsignals =[[], []]
	wrongsignals = [[], []]
	
	passed = [[[], []], [[], []]]
	rejected = [[[], []], [[], []]]
	passeddiff=[[], []]
	rejecteddiff=[[], []]
	
	passedcsignals= [[[], []], [[], []]]
	passedDCsignals = [[[], []], [[], []]]
	rejectedcsignals = [[[], []], [[], []]]
	rejectedDCsignals =[[[], []], [[], []]]
	
	mtotal=0
	
	
	targetfolder = filepath + cfg.jobID +"/"
	
	sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/misc')
	from progressbar import ProgressBar
	custom_options = {
		'end': 100,
		'width': 100,
		'format': '%(progress)s%% [%(fill)s%(blank)s]'
	}
	
	p = ProgressBar(**custom_options)
	print p
	
	hessstatus=[False, False]
	if os.path.isfile(hess1picklepath):
		hessstatus[0] = True
	if os.path.isfile(hess2picklepath):
		hessstatus[1] = True
	if not os.path.isfile(hess1picklepath) and not os.path.isfile(hess2picklepath):
		raise Exception("No BDT saved, so no results to plot!")
	
	while (i < j):
		targetpath = targetfolder +  "run" + str(i) + "/pickle/eventdata.p"
		if (os.path.isfile(targetpath)):
			event = pickle.load(open(targetpath, 'rb'))
			if hasattr(event.simulations, "DC") and hasattr(event.simulations, "full"):
				DCsim =event.simulations.DC
				fullsim = event.simulations.full
				
				k=0
				kar=0
				l=0
				
				for fulltel in fullsim.images:
					if fulltel.BDTID != None:
						fullBDT = fulltel.getBDTpixel()
						candidatesignal = fullBDT.channel1.intensity - fullBDT.nnmean
						if float(ucut) > float(fullBDT.bdtscore) > float(cut):
								if float(candidatesignal) > float(signalcut):
									k+=1
									if float(fulltel.hillas.aspect_ratio_) > arcut:
										kar +=1
					
					if fulltel.QDCID != None:
						l+=1
						
				
				if hasattr(DCsim, "triggerIDs"):		
					truemultiplicity = len(DCsim.triggerIDs)
					
					if int(truemultiplicity) == int(4):
						truefour +=1
					elif int(truemultiplicity) == int(5):
						truefive +=1
						
					if (int(truemultiplicity) < int(4)) and (int(kar) > int(3)):
						wronghighmultiplicity  += 1
						
					
				if int(kar) == int(4):
					reconfour +=1
				elif int(kar) == int(5):
					reconfive +=1
					
										
				mtotal +=1
				totalimages[0] += 4
				totalimages[1] += 1
				
				for index in fullsim.triggerIDs:
					fulltel =  fullsim.images[index]
					trueID=None
					
					if fulltel.size == "HESS1":
						plotindex = 0
						toplot = hessstatus[0]
					elif fulltel.size == "HESS2":
						plotindex = 1
						toplot = hessstatus[1]
					else:
						raise Exception("Telescope.size error, size is " +fulltel.size)
						
						
					DCcount=0
					if index in DCsim.triggerIDs:
						DCtel = DCsim.images[index]
						trueID = DCtel.trueDC
						if hasattr(DCtel.hillas, "image_size_amplitude_"):
							DCcount = DCtel.hillas.image_size_amplitude_
							triggeredimages[plotindex] += 1	
					
					if toplot and (fulltel.BDTID != None):
						fullBDT = fulltel.getBDTpixel()
						
						if (fullBDT.bdtscore != None):
							simplesignal = fullBDT.channel1.intensity - fullBDT.nnmean
							
							if sigfit == None:							
								candidatesignal = simplesignal
							elif sigfit == "rgr":
								bdtentry = makeBDTentry(fullBDT)
								if (fulltel.size=="HESS1") and (bdtentry != None):
									candidatesignal = hess1rgr.predict([bdtentry])[0]
								elif (fulltel.size=="HESS2") and (bdtentry != None):
									candidatesignal = hess2rgr.predict([bdtentry])[0]
								elif bdtentry == None:
									candidatesignal = 0
							else:
								raise Exception("sigfit is "+sigfit)
								
							if DCcount > 0:
								difference = (candidatesignal - DCcount)/DCcount
								absd = math.fabs(difference)
							else:
								difference=None
								absd = None

							if (trueID != None) and (fulltel.BDTID == trueID):
								result = 1
								correctimages[plotindex] += 1
								rightDCcounts[plotindex].append(DCcount)
								rightscores[plotindex].append(fullBDT.bdtscore)
								rightsignals[plotindex].append(candidatesignal)
								right[plotindex].append(fullBDT.bdtscore)
								if float(ucut) > float(fullBDT.bdtscore) > float(cut):
									correctcut[plotindex] += 1
									totalcut[plotindex] += 1
							elif fulltel.BDTID == None:
								print "None!!!"
							else:
								result = 0
								wrongDCcounts[plotindex].append(DCcount)
								wrongscores[plotindex].append(fullBDT.bdtscore)
								wrongsignals[plotindex].append(candidatesignal)
								wrong[plotindex].append(fullBDT.bdtscore)
								if float(ucut) > float(fullBDT.bdtscore) > float(cut):
									totalcut[plotindex] += 1

							passcut = False
							
							if float(result) == float(1):
								if float(ucut) > float(fullBDT.bdtscore) > float(cut):
									if float(simplesignal) > float(signalcut):
										combinedcorrect[plotindex] += 1
										combinedtotal[plotindex] += 1
										combinedright[plotindex].append(fullBDT.bdtscore)
										if (k > minmultiplicity):
											fullcorrect[plotindex] += 1
											fulltotal[plotindex] += 1
										if (kar > minmultiplicity) and (float(fulltel.hillas.aspect_ratio_) > arcut):
											finalcorrect[plotindex] += 1
											finaltotal[plotindex] += 1
											passcut = True
											
							elif float(result) == float(0):
								if float(ucut) > float(fullBDT.bdtscore) > float(cut):
									if float(simplesignal) > float(signalcut):
										combinedtotal[plotindex] += 1
										combinedwrong[plotindex].append(fullBDT.bdtscore)
										if (k > minmultiplicity):
											fulltotal[plotindex] += 1
										if (kar > minmultiplicity) and (float(fulltel.hillas.aspect_ratio_) > arcut):
											finaltotal[plotindex] += 1
											passcut = True
											
							if difference != None:			
								if passcut:
									passed[plotindex][result].append(difference)
									passeddiff[plotindex].append(absd)
									passedcsignals[plotindex][result].append(candidatesignal/DCcount)
									passedDCsignals[plotindex][result].append(DCcount)
								elif (k > minmultiplicity):
									rejected[plotindex][result].append(difference)
									rejecteddiff[plotindex].append(absd)
									rejectedcsignals[plotindex][result].append(candidatesignal/DCcount)
									rejectedDCsignals[plotindex][result].append(DCcount)	
									
					if toplot and (fulltel.QDCID != None):
							
						fullQDC = fulltel.getQDCpixel()
							
						if fulltel.QDCID == trueID:
							oldcorrectimages[plotindex] += 1
							oldright[plotindex].append(fullQDC.rawQDC)
							oldcorrectcut[plotindex] += 1
							oldtotalcut[plotindex] += 1
							if l > minmultiplicity:		
								oldcombinedcorrect[plotindex] += 1
								oldcombinedtotal[plotindex] += 1
						else:
							oldwrong[plotindex].append(fullQDC.QDC)
							oldtotalcut[plotindex] += 1	
							if l > minmultiplicity:
								oldcombinedtotal[plotindex] += 1
	
		if (int(float(i)*100/float(j)) - float(i)*100/float(j)) ==0:
			print p+1
		i+=1
		
	for i in [0, 1]:
		if hessstatus[i]:
			
			message = []
		
			message += "\n \n", 
			message += "We have", str(mtotal), "events. Of these, there are", str(totalimages[i]), "total images, including", str(triggeredimages[i]), "images triggered with DC light."
			message += "In total,", str('{0:.2f}'.format(float(100.*triggeredimages[i]/totalimages[i]))), "% of all images have DC light to reconstruct. \n"
			message += "We have", str(truefour), "true 4-tel events,"
			if truefour > 0:
				message += " giving an expected rate of ", str('{0:.2f}'.format(float(100.*truefour/mtotal))), "%. We reconstruct", str(reconfour), "4-tel events, giving an acceptance rate of", str('{0:.2f}'.format(float(100.*reconfour/truefour))), "%.\n"
			message += "We have", str(truefive), "true 5-tel events, "
			if truefive > 0:
				message += "giving an expected rate of ", str('{0:.2f}'.format(float(100.*truefive/mtotal))), "%. We reconstruct", str(reconfive), "5-tel events, giving an acceptance rate of", str('{0:.2f}'.format(float(100.*reconfive/truefive))), "%.\n"
			message += "There are", str(wronghighmultiplicity), "events which are not really high-multiplicity, a rate of", str('{0:.2f}'.format(float(100.*wronghighmultiplicity/mtotal))), ".\n"
			
			message += "In total,", str(oldcorrectimages[i]), "pixels are correctly identified using QDC method."
			if totalimages[i] > 0:
				message += "Method Identified", str('{0:.2f}'.format(float(100.*oldcorrectimages[i]/totalimages[i]))), "% of all images. \n"
			
			message += "In total,", str(correctimages[i]), "pixels are correctly identified using BDT method."
			if totalimages[i] > 0:
				message += "Method Identified", str('{0:.2f}'.format(float(100.*correctimages[i]/totalimages[i]))), "% of all images. \n \n "
			
			message += "Our QDC cut requires QDC < 0.14 log( Itot / 161 cos(theta)), leaving", str(oldtotalcut[i]), "images. \n "
			message += "Of these,", str(oldcorrectcut[i]), "are correctly identified images. \n "
			if oldtotalcut[i] > 0:
				message += "Successful ID rate after cut is", str('{0:.2f}'.format(float(100.*oldcorrectcut[i]/oldtotalcut[i]))),  "% \n"
				message += "Fraction of pixels correctly identified is", str('{0:.2f}'.format(float(100.*oldcorrectcut[i]/totalimages[i]))), "% \n"
				message += "Fraction of pixels incorrectly identified is", str('{0:.2f}'.format(float(100.*(oldtotalcut[i]-oldcorrectcut[i])/totalimages[i]))), "% \n"
			else:
				message += " \n"
			
			message += "Additionally requiring multiplicity > ", str(minmultiplicity), ", we have", str(oldcombinedtotal[i]), "images . \n "
			message += "Of these,", str(oldcombinedcorrect[i]), "are correctly identified images. \n "
			if oldcombinedtotal[i] > 0:
				message += "Successful ID rate after cut is", str('{0:.2f}'.format(float(100.*oldcombinedcorrect[i]/oldcombinedtotal[i]))),  "% \n"
				message += "Fraction of pixels correctly identified is", str('{0:.2f}'.format(float(100.*(oldcombinedcorrect[i])/totalimages[i]))), "% \n "
				message += "Fraction of pixels incorrectly identified is", str('{0:.2f}'.format(float(100.*(oldcombinedtotal[i]-oldcombinedcorrect[i])/totalimages[i]))), "% \n \n"
			else:
				message += " \n"
				
			message += "Our BDT cut requires Signal Probability >", str(cut), ", we have", str(totalcut[i]), "images. \n"
			message += "Of these,", str(correctcut[i]), "are correctly identified images.\n  "
			if totalcut[i] > 0:
				message += "Successful ID rate after cut is", str('{0:.2f}'.format(float(100.*correctcut[i]/totalcut[i]))), "% \n"
				message += "Fraction of pixels correctly identified is", str('{0:.2f}'.format(float(100.*(correctcut[i])/totalimages[i]))), "% \n"
				message += "Fraction of pixels incorrectly identified is", str('{0:.2f}'.format(float(100.*(totalcut[i]-correctcut[i])/totalimages[i]))), "% \n"
			else:
				message += " \n"
				
			message += "Additionally requiring signal > ", str(signalcut), ", we have", str(combinedtotal[i]), "images. \n"
			message += "Of these,", str(combinedcorrect[i]), "are correctly identified images. \n "
			if combinedtotal[i] > 0:
				message += "Successful ID rate after cut is", str('{0:.2f}'.format(float(100.*combinedcorrect[i]/combinedtotal[i]))), "% \n"
				message += "Fraction of pixels correctly identified is", str('{0:.2f}'.format(float(100.*(combinedcorrect[i])/totalimages[i]))), "% \n"
				message += "Fraction of pixels incorrectly identified is", str('{0:.2f}'.format(float(100.*(combinedtotal[i]-combinedcorrect[i])/totalimages[i]))), "% \n"
				
			message += "Additionally requiring multiplicity > ", str(minmultiplicity), " we have", str(fulltotal[i]), "images . \n "
			message += "Of these,", str(fullcorrect[i]), "are correctly identified images. \n "
			if fulltotal[i] > 0:
				message += "Successful ID rate after cut is", str('{0:.2f}'.format(float(100.*fullcorrect[i]/fulltotal[i]))), "% \n"
				message += "Fraction of pixels correctly identified is", str('{0:.2f}'.format(float(100.*fullcorrect[i]/totalimages[i]))), "% \n"
				message += "Fraction of pixels incorrectly identified is", str('{0:.2f}'.format(float(100.*(fulltotal[i]-fullcorrect[i])/totalimages[i]))), "% \n \n"
				
			message += "Additionally requiring Aspect ratio >", str(arcut)," we have", str(finaltotal[i]), "images . \n "
			message += "Of these,", str(finalcorrect[i]), "are correctly identified images. \n "
			if finaltotal[i] > 0:
				message += "Successful ID rate after cut is", str('{0:.2f}'.format(float(100.*finalcorrect[i]/finaltotal[i]))), "% \n"
				message += "Fraction of pixels correctly identified is", str('{0:.2f}'.format(float(100.*finalcorrect[i]/totalimages[i]))), "% \n"
				message += "Fraction of pixels incorrectly identified is", str('{0:.2f}'.format(float(100.*(finaltotal[i]-finalcorrect[i])/totalimages[i]))), "% \n \n"
				
				 
					
			toprint = ' '.join(message)
			print toprint
			
			def format(val, pos):
			    if val > 0.5:
			        return "DC pixel"
			    else:
			        return "non-DC pixel"

			for rows in [2, 3]:
			
				ax1 = plt.subplot(rows,2,2)
				plt.title("Signal in pure DC pixel without shower", y=1.15)
				plt.hist([rightDCcounts[i],wrongDCcounts[i]], color=['g', 'silver'], label=["Correct", "Incorrect"], stacked=True, bins=50)
				plt.xlabel("DC pixel intensity")
				
				
				ax3 = plt.subplot(rows,2,1)
				plt.title("Distribution of BDT-reconstructed Events", y=1.15)
				plt.hist([right[i], wrong[i]], color=['g', 'silver'], stacked=True, bins=25)
				plt.xlabel("BDT score")
				
				ax3up = ax3.twiny()

				ax3up.xaxis.set_major_locator(plt.MaxNLocator(1))
				
				ax3up.xaxis.set_minor_locator(plt.NullLocator())
				
				ax3up.xaxis.set_major_formatter(plt.FuncFormatter(format))
				ax3up.tick_params(direction='out', pad=5)
				
				ax4 = plt.subplot(rows,2,3)
				plt.title("Distribution of BDT-reconstructed Events, after Score and Signal cuts", y=1.15)
				plt.hist([combinedright[i], combinedwrong[i]], color=['g', 'silver'], stacked=True, bins=25)
				plt.xlabel("BDT score")
				
				ax4up = ax4.twiny()

				ax4up.xaxis.set_major_locator(plt.MaxNLocator(1))
				
				ax4up.xaxis.set_minor_locator(plt.NullLocator()) 
  
				ax4up.xaxis.set_major_formatter(plt.FuncFormatter(format))
				ax4up.tick_params(direction='out', pad=5)
				
				
				ax2 = plt.subplot(rows,2,4)
				
				if len(oldright[i]) > 0:
					plt.title("Distribution of QDC-reconstructed Events", y=1.15)
					plt.hist([oldright[i], oldwrong[i]], color=['g', 'silver'], stacked=True, bins=20)
					plt.xlabel("QDC value")
				
				figure = plt.gcf() # get current figure
				handles, labels = ax1.get_legend_handles_labels()
				figure.legend(handles, labels, loc="upper right")
				
				plt.subplots_adjust(hspace = 0.5)
				if (rows == 2):
					figure.set_size_inches(15, 15)
					plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/hess" + str(i+1) +"stats"+ str(cfg.jobID)+".pdf")
					
				elif rows ==3:

					ax5 = plt.subplot(3,2,5)
					plt.axis('off')
					plt.annotate(toprint, xy=(0.0, 0.0), xycoords="axes fraction",  fontsize=8)
					
					
					ax6 = plt.subplot(3, 2, 6)
					plt.title("Distribution of BDT-reconstructed Events, after cuts", y=1.15)
					plt.scatter(rightscores[i], rightsignals[i], color='g')
					plt.scatter(wrongscores[i], wrongsignals[i], color='silver', edgecolor="k")
					plt.axvline(cut, color='k', ls ="--")
					plt.axhline(signalcut, color='k', ls ="--")
					plt.xlabel("BDT score")
					plt.xlabel("Candidate signal")
								
					figure = plt.gcf() # get current figure
					figure.set_size_inches(20, 15)
					plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/hess" + str(i+1) +"stats"+str(cfg.jobID)+".pdf")
			
				plt.close()
			
			colors =['silver', 'g']
			edgecolors=["k","None"]
			for columns in [1, 2]:
			
				ax1 = plt.subplot(2,columns,1)
				if (len(passed[i][0]) > 0) and (len(passed[i][1]) > 0):
					plt.hist(passed[i], color=colors, stacked=True, bins=20)
				plt.title("DC pixel error for events passing cuts")
				plt.xlabel("Difference from true count")	
				
				linear = np.linspace(1, 3000, 1000)
				plotcut = []
				for entry in linear:
					plotcut.append(signalcut/entry)
				
				if columns == 2:
					ax2 = plt.subplot(2,2,2)
					if (len(rejected[i][0]) > 0) and (len(rejected[i][1]) > 0):
						plt.hist([rejected[i][0], rejected[i][1]], color=colors, stacked=True, bins=20)
					plt.title("DC pixel error for rejected events")
					plt.xlabel("Difference from true count")

					ax4 = plt.subplot(2,2,4)
					for j in range(2):
						plt.scatter( rejectedDCsignals[i][j],rejectedcsignals[i][j], color=colors[j], edgecolor=edgecolors[j], marker="o")
					plt.axhline(1, color='k')
					plt.plot(linear, plotcut, color='k', linestyle='--')
					plt.xlabel("True signal")
					plt.title("True vs. reconstructed signal for rejected events")
					plt.ylabel("Candidate reconstructed signal / True signal")
					
					ax3 = plt.subplot(223, sharex = ax4, sharey=ax4)
					
				elif columns == 1:
					ax3 = plt.subplot(212)
				
				for j in range(2):
					plt.scatter( passedDCsignals[i][j],passedcsignals[i][j], color=colors[j], edgecolor=edgecolors[j], marker="o")
				plt.axhline(1, color='k')
				plt.plot(linear, plotcut, color='k', linestyle='--')
				ax3.fill_between(linear, 0, plotcut, alpha=0.2)
				plt.xlabel("True signal")
				plt.title("True vs. reconstructed signal for accepted events")
				plt.ylabel("Candidate reconstructed signal / True signal")
				ax3.set_ylim([0,5])
				ax3.set_xlim(left=0)
			
			figure = plt.gcf() # get current figure
			figure.set_size_inches(20, 20)
			handles, labels = ax3.get_legend_handles_labels()
			figure.legend(handles, labels, loc="upper right")
			
			plt.savefig("/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/report/graphs/DCcounterrorhess" + str(i+1) + str(sigfit)+str(cfg.jobID)+".pdf")
			
			k=1
			
			for category in ["passed", "rejected"]:
			
				allevents = eval(category +"[i][0]")
				allevents.extend(eval(category +"[i][1]"))
				allevents.sort()
	
				alldiff= eval(category + "diff[i]")
				
				alldiff.sort()
				
				nentries = len(allevents)
				if nentries > 3:
					halfinteger = int(0.5*nentries)
					lowerinteger = int(0.16*nentries)
					upperinteger = int(0.84*nentries)
					integer68 = int(0.68*nentries)
					
					lower = allevents[lowerinteger]
					upper = allevents[upperinteger]
					
					toprint= "Mean = " + str('{0:.2f}'.format(np.mean(allevents)))
					toprint += ". Median = " + str('{0:.2f}'.format(allevents[halfinteger])) + "\n"
					toprint += "Lower = " + str('{0:.2f}'.format(lower))
					toprint += ". Upper = " + str('{0:.2f}'.format(upper)) + "\n"
					toprint += "Sigma = " + str('{0:.2f}'.format(0.5*(upper-lower))) + "\n"
					
					toprint += "Mean absolute difference = "+ str('{0:.2f}'.format(np.mean(alldiff))) + "\n"
					toprint += "Median absolute difference = " + str('{0:.2f}'.format(alldiff[halfinteger])) + "\n"
					toprint += "Sigma = " + str('{0:.2f}'.format(alldiff[integer68])) + "\n"
					
					eval("ax" + str(k) + ".annotate(toprint, xy=(0.6, 0.75), xycoords='axes fraction',  fontsize=10)")
					
					print k, toprint
				
				k+=1
			
			saveto = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/graphs/errorstatshess" + str(i+1) +str(sigfit)+str(cfg.jobID)+".pdf"
			
			print "Saving to", saveto
			
			plt.savefig(saveto)

			plt.close()
	
