#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :jobChk
#copyright  :Gramercy Park Studios

import os

def chk(shotPath):
	""" Check for jobData and shotData modules to ensure the specified shot is valid
	"""
	valid = True
	jobData = os.path.join(os.path.split(shotPath)[0], os.environ['DATAFILESRELATIVEDIR'], os.environ['JOBDATAFILE'])
	shotData = os.path.join(shotPath, os.environ['DATAFILESRELATIVEDIR'], os.environ['SHOTDATAFILE'])
	if not os.path.isfile(jobData):
		valid = False
		#print "ERROR: Job data not found."
	if not os.path.isfile(shotData):
		valid = False
		#print "ERROR: Shot data not found."
	return valid
