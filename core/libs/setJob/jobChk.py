#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :jobChk
#copyright  :Gramercy Park Studios

import os, verbose

def chk(shotPath):
	""" Check for jobData and shotData modules to ensure the specified shot is valid
	"""
	valid = True
	jobPath = os.path.split(shotPath)[0]
	jobDataDir = os.path.join(jobPath, os.environ['DATAFILESRELATIVEDIR'])
	shotDataDir = os.path.join(shotPath, os.environ['DATAFILESRELATIVEDIR'])
	if not os.path.isdir(jobDataDir):
		valid = False
		#verbose.settingsData_notFound('Job', jobDataDir)
	if not os.path.isdir(shotDataDir):
		valid = False
		#verbose.settingsData_notFound('Shot', shotDataDir)
	return valid
