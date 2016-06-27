#!/bin/zsh
# 

#        This is how to submit a job to the cluster:
#          login to a submit node, e.g. astro-wgs01.desy.de
#          Initialize by sourcing init script: . /usr/sge/default/common/settings.sh
#          Start using "qsub empty.sh".
#          Als Arrawy-Job mit "qsub -t 10-100:2 empty.sh" (10 bis 100 mit Schrittweite 2)
#          Mit "qstat" wird der Status der Jobs ausgegeben.
#          Mit "qdel job-id" kann ein Job gekillt werden.

# Name of the job
#$ -N CorsikaSIM

# runtime/ Maximale Laufzeit, hat einfluss auf die Priorität. Die Schwellen sind 2:59:59, 23:59:59, 2:59:59, 167:59:59
#~ #$ -l h_rt=167:59:59
#$ -l h_rt=2:59:59 

# Hosts/  host die benutzt werden sollen
#$ -l hostname="!bird001.desy.de&!bird002.desy.de&!bird003.desy.de&!bird004.desy.de&!bird009.desy.de"

# 32 oder 64 Bit (x86 oder amd6[[:Troubleshooting|Troubleshooting]]4) ? Es gibt mehr Hosts mit 64 Bit.
#$ -l arch="amd64"

# Stacksize/  Größe des Stacks
#$ -l h_stack=15M 

# needed memory/  Benötigter Speicher. Vorsicht: bei mehr als 2G kommt der Job in die long queue.
#$ -l h_vmem=2G

# Disk space/  Benötigter temporärer Festplattenspeicher auf dem Host .
#$ -l h_fsize=20G

# group resource for astroparticle group/ unsere Gruppe, damit haben wir Priorität auf den ASTRO-WGS-Hosts.
#$ -P astrop

# cluster sends email when:/Festlegen, wann eine E-Mail gesendet werden soll:( b bei Beginn, e bei Ende, a bei Abbruch, s bei Suspend)
#$ -m s

# E-Mail
#$ -M robert.stein@desy.de



# Path for/ Pfade für stdout und stderr
#$ -o /nfs/astrop/d6/rstein/cluster_output
#$ -e /nfs/astrop/d6/rstein/cluster_error
#

# Ab hier beginnt das Script

. /nfs/astrop/d1/hhsoft/64bit_crf/ini_python2.7.8_64bit_crf.sh

# This file should be sourced from each example

# The example should work (on Linux) without the following environment variables:
unset HESSROOT
export HESSROOT
unset LD_LIBRARY_PATH
export LD_LIBRARY_PATH

export CTA_PATH=/nfs/astrop/d6/rstein/corsika_simtelarray

# Paths to software, libraries, configuration files (read-only)
export CORSIKA_PATH="$(cd ${CTA_PATH}/corsika-run && pwd -P)"
export SIM_TELARRAY_PATH="$(cd ${CTA_PATH}/sim_telarray && pwd -P)"
export HESSIO_PATH="$(cd ${CTA_PATH}/hessioxxx && pwd -P)"
export LD_LIBRARY_PATH="${HESSIO_PATH}/lib"
export PATH="${HESSIO_PATH}/bin:${SIM_TELARRAY_PATH}/bin:${PATH}"

# Sim_telarray configuration paths are normally compiled-in but you can set
#   SIM_TELARRAY_CONFIG_PATH : replace compiled-in paths with this
#   SIMTEL_CONFIG_PATH : precede compiled-in or replaced paths with this
# while any '-I...' options to sim_telarray precedes any of these paths.
# Recent versions of the generic_run.sh script may also fill in the
# values of environment values SIM_TELARRAY_DEFINES and SIM_TELARRAY_INCLUDES
# early into the sim_telarray command line. 

# Paths where data gets written to. Normally everything goes into
# a sub-directory/symlink 'Data' but you can either set MCDATA_PATH
# or CTA_DATA to direct the output elsewhere.
export CTA_DATA_PATH="${CTA_PATH}/Data"
export MCDATA_PATH="${CTA_DATA_PATH}"

# CORSIKA is run in a 'run......' sub-directory of this path:
export CORSIKA_DATA="${MCDATA_PATH}/corsika"
# Sim_telarray output goes into config dependent sub-directory of this path:
export SIM_TELARRAY_DATA="${CTA_PATH}/sim_telarray/cfg"

printenv | egrep '^(CTA_PATH|CORSIKA_PATH|SIM_TELARRAY_PATH|SIM_TELARRAY_CONFIG_PATH|SIMTEL_CONFIG_PATH|HESSIO_PATH|CTA_DATA|MCDATA_PATH|CORSIKA_DATA|SIM_TELARRAY_DATA|HESSROOT|LD_LIBRARY_PATH|PATH|RUNPATH)=' | sort

export MAX_PRINT_ARRAY=2100
echo "MAX_PRINT_ARRAY set to 2100"

mkdir -p /nfs/astrop/d6/rstein/data/$JOB_ID

for (( i=0; i <= 29; i++ ))
do 
 python /nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/runcorsika.py -rn $((($i*500) + $SGE_TASK_ID)) -td $TMPDIR -jid $JOB_ID

 python /nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/runsimtel.py -rn $((($i*500) + $SGE_TASK_ID)) -jid $JOB_ID -cn DC -td $TMPDIR 

 python /nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/runsimtel.py -rn $((($i*500) + $SGE_TASK_ID)) -jid $JOB_ID -td $TMPDIR

 python /nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/CORSIKA/extractpixels.py -rn $((($i*500) + $SGE_TASK_ID)) -jid $JOB_ID
done




