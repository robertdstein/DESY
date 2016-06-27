import argparse, os, math, random, time, sys, csv, cmath
import os.path
import numpy as np
import cPickle as pickle
from sklearn import ensemble
import initialisecuts as ic
import re
import cmath
from telescopeclasses import *

sys.path.append('/nfs/astrop/d6/rstein/Hamburg-Cosmic-Rays/positioning/')

import lightdensity as ld
import cherenkovradius as cr

def run(pixel, Z):
	if hasattr(pixel, "hillasparams") and hasattr(pixel, "dchillasparams"):
		if hasattr(pixel.hillasparams, "core_distance_to_telescope") and hasattr(pixel.hillasparams, "energy") and hasattr(pixel.dchillasparams, "Hmax_"):
			coredistance = getattr(pixel.hillasparams, "core_distance_to_telescope")
			energy = getattr(pixel.hillasparams, "energy")
			height = getattr(pixel.dchillasparams, "Hmax_")
		else:
			#~ print "Doesn't have variables"
			#~ raw_input("prompt")
			return None
		
		epn = energy/56
		rmax , theta = cr.run(epn, height, 1, fit="exp")
		if coredistance > rmax:
			return ld.f1(coredistance, Z=Z)
		else:
			return ld.f2(coredistance, Z=Z, rmax=rmax)
	else:
		#~ print "Doesn't have containers"
		#~ raw_input("prompt")
		return None
