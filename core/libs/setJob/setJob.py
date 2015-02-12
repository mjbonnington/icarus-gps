#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:setJob
#copyright	:Gramercy Park Studios


import setDirs, userPrefs, job__env__, pathPrc

def setup(job, shot):
	shotPath = pathPrc.process(job, shot)
	envVars = job, shot, shotPath
	job__env__.setEnv(envVars)
	setDirs.mkDirs()
	newEntry = '%s,%s' % (job, shot)
	userPrefs.edit('main', 'lastjob', newEntry)
