import os, argparse, subprocess, time
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("-bid", "--BDTID", default="2842781")
parser.add_argument("-tid", "--testID", default="2567181")
parser.add_argument("-t", "--train", action="store_true")
parser.add_argument("-re", "--reextract", action="store_true")

cfg = parser.parse_args()

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

filepath = "/nfs/astrop/d6/rstein/data/"
targetfolder = filepath + cfg.BDTID +"/"
filename = targetfolder + "BDTpixels.csv"

if cfg.reextract:
	picklepath = '/nfs/astrop/d6/rstein/BDTpickle/DCpixelclassifier.pkl'
	if os.path.isfile(picklepath):
		remove_old_BDT = "rm " + picklepath 
		os.system(remove_old_BDT)
	rextract_for_BDT = "qsub -t 1-2000:1 extractpixelsoncluster.sh " + cfg.BDTID
	print time.asctime(time.localtime()), rextract_for_BDT, "\n"
	os.system(rextract_for_BDT)
	wait()

if os.path.isfile(filename) and not cfg.reextract:
	pass
else:
	BDT_combine_command = "python combineforBDT.py -jid " + cfg.BDTID
	print time.asctime(time.localtime()), BDT_combine_command, "\n"
	os.system(BDT_combine_command)
	
if cfg.train:
	traincommand = "python trainBDT.py -jid " + cfg.BDTID
	print time.asctime(time.localtime()), traincommand, "\n"
	os.system(traincommand)

execute = "qsub -t 1-2000:1 extractpixelsoncluster.sh " + cfg.testID
print time.asctime(time.localtime()), execute, "\n"
os.system(execute)

wait()

combinecommand = "python combinestatistics.py -jid " + cfg.testID
print time.asctime(time.localtime()), combinecommand
os.system(combinecommand)

errorcommand = "python counterrorstats.py -jid " + cfg.testID
print time.asctime(time.localtime()),errorcommand
os.system(errorcommand)	
	
