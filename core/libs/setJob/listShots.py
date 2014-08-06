#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:listShots
#copyright	:Gramercy Park Studios


import os
import pathPrc, jobChk

def list_(job):
	shotsPath = pathPrc.process(job)
	dirContents = os.listdir(shotsPath)
	shotLs = []
	for item in dirContents:
		#Checks for shot naming convention to discard everything else in directory
		if item.startswith('SH') or item.startswith('PC'):
			shotPath = os.path.join(shotsPath, item)
			#performs jobChk to ensure that directories are valid shots
			if jobChk.chk(shotPath):
				shotLs.append(item)
	
	shotLs.sort(); shotLs.reverse()
	return shotLs
		
	
	