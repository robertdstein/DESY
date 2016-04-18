import argparse, os, math, random, time, sys

offset="0"

parser = argparse.ArgumentParser()
parser.add_argument("-rn", "--runnumber", default="0")
parser.add_argument("-jid", "--jobID", default="0")
parser.add_argument("-cn", "--cardname", default="full")

cfg = parser.parse_args()
print int(cfg.runnumber)

data_dir = "/nfs/astrop/d6/rstein/data"

result_dir = data_dir + "/" + str(cfg.jobID)

run_dir = os.path.join(result_dir, "run" + str(cfg.runnumber))
base_file_name = os.path.join(run_dir, "run" + str(cfg.runnumber) + str(cfg.cardname) + "_off" + offset)

# open inputcard to extract source theta
f_in = open(os.path.join(run_dir, "run" + str(cfg.runnumber) + str(cfg.cardname) + ".inputcard"))
for zeile in f_in:
	if "THETAP" in zeile:
		elements = zeile[:-1].split()
		source_theta = float(elements[1])
	if "PHIP" in zeile:
		elements = zeile[:-1].split()
		source_phi = float(elements[1])
f_in.close()

telescope_theta = source_theta + float(offset)
telescope_phi = 180. - (source_phi + 14.)

os.chdir("/nfs/astrop/d6/rstein/corsika_simtelarray/sim_telarray")

# hess2 configuration


q1 = "zcat " + run_dir + "/run" + str(cfg.runnumber) + str(cfg.cardname) + "-iact.corsika.gz | ./sim_hessarray -c hess-phase2.cfg -DPHASE2B=1 -DHESS2_SECTOR=1 -C IMAGE_FILE=" + base_file_name + ".ps -C PLOT_FILE=" + base_file_name + ".txt -C SAVE_PHOTONS=2 -C SAMPLED_OUTPUT=0  -C nightsky_background=all:0.100 -C trigger_pixels=1  -C discriminator_threshold=112 -C discriminator_pulse_shape=hess_disc_shape-01-10.dat -C iobuf_maximum=200000000 -C maximum_telescopes=5 -C min_photons=20 -C atmospheric_transmission=atm_trans_1800_1_10_0_0_1800.dat  -C convergent_depth=0 -C telescope_theta=" + str(telescope_theta) + " -C telescope_phi=" + str(telescope_phi) + " -C power_law=2.50 -C histogram_file=" + base_file_name + ".hdata.gz -C output_file=" + base_file_name + ".simhess.gz -C random_state=auto -C show=all - | tee " + base_file_name + ".log"

print q1

os.system(q1)

# do read_hess

readhesscmd = "/nfs/astrop/d6/rstein/corsika_simtelarray/hessioxxx/bin/read_hess -S -q -v -r 2 -p " + base_file_name + ".ps " + base_file_name + ".simhess.gz > " + base_file_name + "_read_hess_output.txt"

print readhesscmd

os.system(readhesscmd)


