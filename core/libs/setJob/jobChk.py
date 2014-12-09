#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:jobChk
#copyright	:Gramercy Park Studios

import os

#checks for jobData and shotData modules to ensure the specified shot is valid
def chk(shotPath):	
	jobData = os.path.join(os.path.split(shotPath)[0], os.environ['DATAFILESRELATIVEDIR'], os.environ['JOBDATAFILE'])
	shotData = os.path.join(shotPath, os.environ['DATAFILESRELATIVEDIR'], os.environ['SHOTDATAFILE'])
	if not os.path.isfile(jobData) or not os.path.isfile(shotData):
		return
	return -1





	
	
