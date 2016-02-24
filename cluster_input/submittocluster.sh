#        This is how to submit a job to the cluster:
#          login to a submit node, e.g. astro-wgs01.desy.de
#          Initialize by sourcing init script: . /usr/sge/default/common/settings.sh
#          Start using "qsub empty.sh".
#          Als Arrawy-Job mit "qsub -t 10-100:2 empty.sh" (10 bis 100 mit Schrittweite 2)
#          Mit "qstat" wird der Status der Jobs ausgegeben.
#          Mit "qdel job-id" kann ein Job gekillt werden.

# Name of the job
#$ -N ChargeReconstruction

# runtime/ Maximale Laufzeit, hat einfluss auf die Priorität. Die Schwellen sind 2:59:59, 23:59:59, 2:59:59, 167:59:59
#$ -l h_rt=2:59:59 

# Hosts/  host die benutzt werden sollen
#$ -l hostname="!bird001.desy.de&!bird002.desy.de&!bird003.desy.de&!bird004.desy.de&!bird009.desy.de"

# 32 oder 64 Bit (x86 oder amd6[[:Troubleshooting|Troubleshooting]]4) ? Es gibt mehr Hosts mit 64 Bit.
#$ -l arch="amd64"

# Stacksize/  Größe des Stacks
#$ -l h_stack=10M 

# needed memory/  Benötigter Speicher. Vorsicht: bei mehr als 2G kommt der Job in die long queue.
#$ -l h_vmem=512M

# Disk space/  Benötigter temporärer Festplattenspeicher auf dem Host .
#$ -l h_fsize=2G

# group resource for astroparticle group/ unsere Gruppe, damit haben wir Priorität auf den ASTRO-WGS-Hosts.
#$ -P astrop

# cluster sends email when:/Festlegen, wann eine E-Mail gesendet werden soll:( b bei Beginn, e bei Ende, a bei Abbruch, s bei Suspend)
#$ -m as

# E-Mail
#$ -M robert.stein@desy.de

# Path for/ Pfade für   stdout und stderr
#$ -o /afs/desy.de/user/s/steinrob/Documents/DESY/cluster_output
#$ -e /afs/desy.de/user/s/steinrob/Documents/DESY/cluster_output
#
#

# Ab hier beginnt das Script

ls
pwd

. /nfs/astrop/d1/hhsoft/ini_python2.7.8.sh

python /afs/desy.de/user/s/steinrob/Documents/DESY/cluster_input/execute$SGE_TASK_ID.py
#cp $TMPDIR/* /afs/desy.de/user/s/steinrob/Documents/DESY/cluster_output
