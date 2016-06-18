import os, argparse, subprocess, time
import os.path

def wait():
	proc = subprocess.Popen('qstat', stdout=subprocess.PIPE)
	tmp = str(proc.stdout.read())
	i=31
	j=0
	
	while tmp != "":
		if i > 3:
			print time.asctime(time.localtime()), len(tmp.split('\n'))-3, "entries in queue"
			print time.asctime(time.localtime()), "Waiting for Cluster"
			i=1
			j+=1
		if j > 15:
			print tmp
			j = 0
		time.sleep(10)
		i+=1
		proc = subprocess.Popen('qstat', stdout=subprocess.PIPE)
		tmp = str(proc.stdout.read())
		
delerrors = "rm -rf /d6/rstein/cluster_error/*"
deloutput = "rm -rf /d6/rstein/cluster_output/*"
clear_sims = "rm -rf /d6/rstein/chargereconstructionpickle/fullsims/*"
clear_combined = "rm -rf /d6/rstein/chargereconstructionpickle/combined/*"
for cmd in [delerrors, deloutput, clear_sims, clear_combined]:
	print cmd
	os.system(cmd)

cluster_command = "qsub -t 1-5000:1 submittocluster.sh"
print time.asctime(time.localtime()), cluster_command, "\n"
os.system(cluster_command)

wait()
