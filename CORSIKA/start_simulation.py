#
#  Corsika simulation for HESS
#
#  Daniel Hampf 2011
#
# chain goes as follows:
#
#  1) start_simulation.py
#  2) submit_simulation.sh
#  3) run_simulation.py    <-- does the work



import os
import sys

data_dir = os.path.expandvars("$SCORE_DATA")

# reading and incrementing runnumber
f_runnumber = open(data_dir+"/runnumber.dat")
runnumber = int(f_runnumber.readline())
f_runnumber.close()

runnumber += 1

f_runnumber = open(data_dir+"/runnumber.dat","w")
f_runnumber.write(str(runnumber) + "\n")
f_runnumber.close()

cluster = False
if cluster == False:
	os.system("./submit_simulation.sh " + str(runnumber))
if cluster == True:
	os.system("qsub submit_simulation.sh " + str(runnumber))	
	sys.exit()


