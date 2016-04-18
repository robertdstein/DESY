import sys
import os
import string
import glob

score_soft = os.path.expandvars("$SCORE_SOFT")
data_dir = os.path.expandvars("$SCORE_DATA")

if len(sys.argv) == 3:
	runnumber  = int(sys.argv[1])
	temp_dir = sys.argv[2]
else:
	print "Error: Need runnumber and output directory as arguments"
	sys.exit(-1)


# default input card
filename_in = score_soft + "/eppic_score_64/eppic_64.inputcard"

#corsika_dir = "/nfs/astrop/d2/corsika64/corsika-6990/run"
corsika_dir = score_soft + "/eppic_score_64/corsika_plotsh/corsika-6990/run"
#corsika_exe = "64corsika6990Linux_QGSJET_gheisha"
corsika_exe = "corsika6990Linux_QGSJET_gheisha"

# directory that contains run directories
result_dir = data_dir

####################################
### create inputcard for corsika ###
####################################

Direc = os.path.join(result_dir, "run" + str(runnumber))
print "Making directory " + Direc
os.mkdir(Direc)

inputcard_name = os.path.join(Direc, "run" + str(runnumber) + ".inputcard")


f_in = open(filename_in)
f_out = open(inputcard_name, "w")

# writing start of new inputcard 
f_out.write("* Used Corsika Version: %s  \n"%corsika_dir)

f_out.write("RUNNR   " + str(runnumber) + "                           number of run     \n")

f_out.write("""
*
* [ Random number generator: 4 sequences used in IACT mode ]
*
""")

f_out.write("SEED    " + str(runnumber*2) + "   0   0                seed for 1st random number sequence\n")
f_out.write("SEED    " + str(runnumber*3) + "   0   0                seed for 2nd random number sequence\n")
f_out.write("SEED    " + str(runnumber*4) + "   0   0                seed for 3rd random number sequence\n")
f_out.write("SEED    " + str(runnumber*5) + "   0   0                seed for 4th random number sequence\n")


f_out.write("DIRECT %s\n"%temp_dir)

iact_name = os.path.join(temp_dir, "run" + str(runnumber) + "_iact.corsika.gz")

f_out.write("TELFIL " + iact_name + ":100:100:1              Telescope photon bunch output (eventio format)  \n")
	
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
print "Now starting CORSIKA run number" + str(runnumber)
print
# during runtime everything is written in temp_dir (on cluster a local disk)
logfile_name = os.path.join(temp_dir, "run" + str(runnumber) + "_simulation.log")
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


print "Output is written to " + temp_dir
q1 = "mv " + os.path.join(temp_dir, "run" + str(runnumber) + "_iact.corsika.gz") + " " + Direc
q2 = "mv " + os.path.join(temp_dir, "run" + str(runnumber) + "_simulation.log") + " " + Direc
#q1 = "mv " + os.path.join(temp_dir, "*") + " " + Direc
print q1
os.system(q1)
os.system(q2)

print "Output is copied into " + Direc


