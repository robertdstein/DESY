import os
import sys


if len(sys.argv) == 3:
	runnumber  = int(sys.argv[1])
	offset = sys.argv[2]
else:
	print "Error: Need runnumber and offset as arguments"
	sys.exit(-1)


base_dir = "/d6/abramow/data/sim_data/dcl"
run_dir = os.path.join(base_dir, "run" + str(runnumber))
base_file_name = os.path.join(run_dir, "run" + str(runnumber) + "_off" + offset)




# open inputcard to extract source theta
f_in = open(os.path.join(run_dir, "run" + str(runnumber) + ".inputcard"))
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

# override for wide field of view background simulations
#telescope_theta = 46.5
#telescope_phi = 180.

#os.chdir("/d6/abramow/software/sim_telarray_cluster/sim_telarray"

os.chdir(os.environ["SIM_TELARRAY_PATH"])

# hess2 configuration



q1 = "zcat " + run_dir + "/run" + str(runnumber) + "_iact.corsika.gz | ./bin/sim_hessarray -c my_hess-phase2.cfg  -DPHASE2B=1 -DHESS2_SECTOR=1 -C SAVE_PHOTONS=2 -C SAMPLED_OUTPUT=0  -C nightsky_background=all:0.100 -C trigger_pixels=1  -C discriminator_threshold=112 -C discriminator_pulse_shape=hess_disc_shape-01-10.dat -C iobuf_maximum=200000000 -C maximum_telescopes=5 -C min_photons=20 -C atmospheric_transmission=atm_trans_1800_1_10_0_0_1800.dat  -C convergent_depth=0 -C telescope_theta=" + str(telescope_theta) + " -C telescope_phi=" + str(telescope_phi) + " -C power_law=2.50 -C histogram_file=" + base_file_name + ".hdata.gz -C output_file=" + base_file_name + ".simhess.gz -C random_state=auto -C show=all - | tee " + base_file_name + ".log > " + run_dir + "/run" + str(runnumber) + "_sim_telarray.log"

print q1

os.system(q1)

os.chdir(run_dir)



#os.system("mv "+ run_dir + "/sim_hessarray/phase2/0.0deg/Log/* ./run"+str(runnumber)+"_off0.log")
#os.system("mv "+ run_dir + "/sim_hessarray/phase2/0.0deg/Histograms/* ./run"+str(runnumber)+"_off0.hdata.gz")
#os.system("mv "+ run_dir + "/sim_hessarray/phase2/0.0deg/Data/* ./run"+str(runnumber)+"_off0.simhess.gz")

# do read_hess

os.system("read_hess -S -r 2 -p  run"+str(runnumber)+".ps run"+str(runnumber)+"_off0.simhess.gz >run"+str(runnumber)+"_read_hess_output.txt")
#os.system("read_hess -S -r 2 run"+str(runnumber)+"_off0.simhess.gz >run"+str(runnumber)+"_read_hess_output.txt")


