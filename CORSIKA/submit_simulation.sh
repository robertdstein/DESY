#!/bin/zsh
#$ -S /bin/zsh
# script for corsika production, D.Hampf 2011
# 
#$ -l h_vmem=2G
#$ -l h_fsize=20G
#$ -P astrop 
#$ -m aes
#$ -M maike.kunnas@desy.de
#$ -N statistics
#$ -o /nfs/astrop/d5/kunnas/data/sim_data/cluster_msgs
#$ -e /nfs/astrop/d5/kunnas/data/sim_data/error_messages
#$ -l h_rt=23:00:00
#$ -l distro=sld5
#$
#
echo "Shell Script Start"
export SCORE_SOFT='/nfs/astrop/d5/kunnas'
export SCORE_DATA='/nfs/astrop/d5/kunnas/data/sim_data'
#
echo "Cluster Computer Info:"
uname -a
# check if TMPDIR exists as environment var, if not, set to default value:
echo "Temporary directory: " $TMPDIR
#if [ -z "$TMPDIR" ]; then
TMPDIR=$SCORE_SOFT/eppic_score/tmp/
#fi

echo "Starting Python run_simulation script"
echo "Temporary directory: " $TMPDIR
echo "JOB ID:" $JOB_ID
echo "RUNNUMBER:" $1
cd $SCORE_SOFT/eppic_score_64/sim_telarray
python ./run_simulation_64.py $1 $TMPDIR


echo "Shell Script End"

