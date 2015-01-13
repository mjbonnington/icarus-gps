#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:listShots
#copyright	:Gramercy Park Studios


#lists all available shots in the specified directory

import os
import pathPrc, jobChk

def list_(job):
	shotsPath = pathPrc.process(job)

	# Check shot path exists before proceeding...
	if os.path.exists(shotsPath):
		dirContents = os.listdir(shotsPath)
		shotLs = []
		for item in dirContents:
			#Checks for shot naming convention to discard everything else in directory
			if item.startswith('SH') or item.startswith('PC'):
				shotPath = os.path.join(shotsPath, item)
				#performs jobChk to ensure that directories are valid shots
				if jobChk.chk(shotPath):
					shotLs.append(item)

		if len(shotLs):
			shotLs.sort(); shotLs.reverse()
			return shotLs
		else:
			print "ERROR: No valid shots found in job path '%s'." %shotsPath
			return False

	else:
		print "ERROR: The job path '%s' does not exist. The job may have been archived, moved or deleted." %shotsPath
		return False
