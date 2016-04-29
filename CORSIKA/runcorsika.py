import argparse, os, math, random, time, sys

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="0")
parser.add_argument("-td", "--tempdir", default="/nfs/astrop/d6/rstein/tmp/")
parser.add_argument("-jid", "--jobID", default="0")

cfg = parser.parse_args()
print int(cfg.runnumber), cfg.tempdir

data_dir = "/nfs/astrop/d6/rstein/data"

# default input card
filename_in = "/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/run.inputcard"

corsika_dir = "/nfs/astrop/d6/rstein/corsika_simtelarray/corsika-run"
corsika_exe = "corsika74000Linux_QGSJET_urqmd"

# directory that contains run directories
result_dir = data_dir + "/" + str(cfg.jobID)

####################################
### create inputcard for corsika ###
####################################

Direc = os.path.join(result_dir, "run" + str(cfg.runnumber))
print "Making directory " + Direc
if not os.path.exists(Direc):
	os.mkdir(Direc)

cards = ["full", "DC"]

for cardname in cards:
	
	Direc = os.path.join(cfg.tempdir, cardname)
	print "Making directory " + Direc
	if not os.path.exists(Direc):
		os.mkdir(Direc)

	inputcard_name = os.path.join(Direc, "run" + str(cfg.runnumber) + str(cardname) + ".inputcard")
	
	f_in = open(filename_in)
	f_out = open(inputcard_name, "w")
	
	# writing start of new inputcard 
	f_out.write("* Used Corsika Version: %s  \n"%corsika_dir)
	
	f_out.write("RUNNR   " + str(cfg.runnumber) + "                           number of run     \n")
	
	f_out.write(" \n")
	f_out.write("* \n")
	f_out.write("* [ Random number generator: 4 sequences used in IACT mode ] \n")
	f_out.write("* \n")
	f_out.write(" \n")
	
	f_out.write("SEED    " + str((int(cfg.runnumber)*4) + 0 + int(cfg.jobID)) + "   0   0                seed for 1st random number sequence\n")
	f_out.write("SEED    " + str((int(cfg.runnumber)*4) + 1 + int(cfg.jobID)) + "   0   0                seed for 2nd random number sequence\n")
	f_out.write("SEED    " + str((int(cfg.runnumber)*4) + 2 + int(cfg.jobID)) + "   0   0                seed for 3rd random number sequence\n")
	f_out.write("SEED    " + str((int(cfg.runnumber)*4) + 3 + int(cfg.jobID)) + "   0   0                seed for 4th random number sequence\n")
	
	
	f_out.write("DIRECT %s\n"%(Direc +"/"))
	
	iact_name = os.path.join(Direc, "run" + str(cfg.runnumber) + str(cardname) + "-iact.corsika.gz")
	
	f_out.write("TELFIL " + iact_name + ":100:100:1              Telescope photon bunch output (eventio format)  \n")

	if cardname == "DC":
		f_out.write("ECUTS 0.3 1E7 1E7 0.003 \n")
		
	elif cardname == "full":
		f_out.write("ECUTS 0.3 0.3 0.003 0.003 \n")
	
	# read input card with default values
	for zeile in f_in:
		f_out.write(zeile)
		

		
	f_in.close()
	f_out.close()
	
	####################################
	
	####################################
	####################################
	####################################
	
	print
	print "Now starting CORSIKA run number" + str(cfg.runnumber)
	print
	# during runtime everything is written in temp_dir (on cluster a local disk)
	logfile_name = os.path.join(Direc, "run" + str(cfg.runnumber) + str(cardname) + "-simulation.log")
	#if os.path.exists(logfile_name):
	#	os.system("rm " + logfile_name)
	
	
	print "Corsika Directory: " + corsika_dir
	os.chdir(corsika_dir)
	print "Changed into Corsika Directory: "+ os.getcwd()
	os.system("cat %s"%inputcard_name)
	#Starting Corsika
	q1 = "./" + corsika_exe + " < " + inputcard_name + " > " + logfile_name
	#q1 = "./" + corsika_exe + " < " + inputcard_name
	print q1
	os.system(q1)
	
	print "Output is written to " + Direc
	
	#~ filetypes = ["-iact.corsika.gz", "-simulation.log"]
	#~ 
	#~ for suffix in filetypes:
		#~ filename = os.path.join(cfg.tempdir, "run" + str(cfg.runnumber) + str(cardname)+ suffix)
		#~ if os.path.isfile(filename):
			#~ q = "mv " + filename + " " + Direc
			#~ os.system(q)
			#~ print q
			#~ 
	#~ width = 6-len(str(cfg.runnumber))
	#~ IDno = (width*str(0)) + str(cfg.runnumber)
	#~ print IDno
			#~ 
	#~ filename = os.path.join(cfg.tempdir, "CER" + IDno)
	#~ if os.path.isfile(filename):
		#~ q = "mv " + filename + " " + Direc
		#~ os.system(q)
		#~ print q
		#~ 
	#~ filecore = "DAT" + IDno
	#~ filetypes = ["", ".long", ".dbase"]
	#~ for suffix in filetypes:
		#~ filename = os.path.join(cfg.tempdir, filecore + suffix )
		#~ if os.path.isfile(filename):
			#~ q = "mv " + filename + " " + Direc
			#~ os.system(q)
			#~ print q
	#~ 
	#~ print "Output is copied into " + Direc


