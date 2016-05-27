import os, argparse, subprocess, time
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("-bid", "--BDTID", default="2842781")
parser.add_argument("-tid", "--testID", default="2567181")
parser.add_argument("-t", "--train", action="store_true")
parser.add_argument("-tr", "--trainregressor", action="store_true")
parser.add_argument("-re", "--reextract", action="store_true")
parser.add_argument("-rc", "--recombine", action="store_true")

cfg = parser.parse_args()

telnames = ["hess1", "hess2"]

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

print delerrors
os.system(delerrors)
print deloutput
os.system(deloutput)

bdttargetfolder = "/nfs/astrop/d6/rstein/data/" + cfg.BDTID + "/bdtpickle/"
bdtfilename = bdttargetfolder + "hess2bdtdata.p"

if not cfg.reextract:
	pass
else:
	rextract_for_BDT = "qsub -t 1-200:1 extractpixelsoncluster.sh " + cfg.BDTID + " False"
	print time.asctime(time.localtime()), rextract_for_BDT, "\n"
	os.system(rextract_for_BDT)
	wait()
	BDT_combine_command = "python combineforBDT.py -jid " + cfg.BDTID
	print time.asctime(time.localtime()), BDT_combine_command, "\n"
	os.system(BDT_combine_command)
	
if cfg.train:
	traincommand = "python trainBDT.py -jid " + cfg.BDTID
	print time.asctime(time.localtime()), traincommand, "\n"
	os.system(traincommand)
	
statstargetfolder = "/nfs/astrop/d6/rstein/data" + cfg.testID + "statspickle/"
statsfilename = statstargetfolder + "datastats.pkl"
	
if not cfg.train and not cfg.recombine:
	pass
else:
	execute = "qsub -t 1-200:1 extractpixelsoncluster.sh " + cfg.testID + " True"
	print time.asctime(time.localtime()), execute, "\n"
	os.system(execute)
	
	wait()
	
if not cfg.train and not cfg.recombine and not cfg.trainregressor:
	pass
else:
	rgrcommand = "python trainextrapolation.py -jid " + cfg.BDTID
	print time.asctime(time.localtime()), rgrcommand, "\n"
	os.system(rgrcommand)
	lpdcommand = "python lpdforfixedenergy.py"
	os.system(lpdcommand)
	
stats_combine_command = "python combineforstatistics.py -jid " + cfg.testID
print time.asctime(time.localtime()), stats_combine_command, "\n"
os.system(stats_combine_command)
