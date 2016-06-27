import os

filepath = "/nfs/astrop/d6/rstein/data/"
i = 1
j = 5001
offset = 10000 

sourcejob = "1271826"
destinationjob ="regressorset"

sourcefolder = filepath + sourcejob + "/"
targetfolder = filepath + destinationjob + "/"

while (i < j):
	sourcepath = sourcefolder +  "run" + str(i) + "/"
	if os.path.isdir(sourcepath):
		targetpath = targetfolder + "run" + str (i + offset) + "/"
		move_command = "mv "+ sourcepath + " " +targetpath 
		print move_command
		os.system(move_command)
	i+=1
