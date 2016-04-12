import argparse, os, math, random, time, sys, csv

offset="0"

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="0")
parser.add_argument("-jid", "--jobID", default="0")

cfg = parser.parse_args()
print int(cfg.runnumber)

data_dir = "/nfs/astrop/d6/rstein/data"

result_dir = data_dir + "/" + str(cfg.jobID)

run_dir = os.path.join(result_dir, "run" + str(cfg.runnumber))
base_file_name = os.path.join(run_dir, "run" + str(cfg.runnumber) + "_off" + offset + "_read_hess_output.txt")

fullldata=[]

with open(base_file_name, 'rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	test=False
	new=False
	current=[]
	for row in reader:
		
		if test:
			new=True
			test=False

		if len(row) > 8:
			if row[8] == "Pixel":
				if str(row[11]) == "1:":
					pixno = row[9]
					channel = row[11]
					count = row[12]
					current.append([pixno[:-1], count, channel[:-1]])
					new=False
					test=True
									
		if new:
			print new, test
			full.append(current)
			current=[]
			new=False
			test=False

for i in range(0, len(full)):
	current=full[i]
	f=open(run_dir + "/pixels" +str(i+1)+".csv", 'w+')
	writer = csv.writer(f, delimiter=',')
	for entry in current:
		writer.writerow(entry)
	f.close()
