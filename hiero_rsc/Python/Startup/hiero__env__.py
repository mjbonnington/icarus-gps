#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:hiero__env__
#copyright	:Gramercy Park Studios


#Sets up Hiero environment at startup
import hiero.core as hc
import os, sys
#just like nuke hiero seems to ditch the main root environent where it has been called from so the path needs to be appended again
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core/ui'))
import env__init__
env__init__.appendSysPaths()

import verbose

def removeAutoSave():
	#getting project
	hroxAutosave = '%s/%s.hrox.autosave' % (os.environ['HIEROEDITORIALPATH'], os.environ['JOB'])
	if os.path.isfile(hroxAutosave):
		os.system('rm -rf %s' % hroxAutosave)

def loadDailies():
	#getting project
	jobHrox = '%s/%s.hrox' % (os.environ['HIEROEDITORIALPATH'], os.environ['JOB'])
	#opening jobHrox if exists
	if os.path.isfile(jobHrox):
		hieroProj = hc.openProject(jobHrox)	
		
		#getting dailies bin
		dailiesBin = hc.findItemsInProject(hieroProj, hc.Bin, 'Dailies', verbose=0)[0]

		#removing dailies from bin
		dailies = dailiesBin.items()
		for daily in dailies:
		    dailiesBin.removeItem(daily)

		#detecting if dailies folder exsits. if not creates one
		dailiesPath = '%s/dailies' % os.environ['HIEROEDITORIALPATH']
		if os.path.isdir(dailiesPath):
			#adding daily folders to dailies bin if dailies folder exists
			dailiesFoldersLs = os.listdir(dailiesPath)
			dailiesFoldersLs = sorted(dailiesFoldersLs, reverse=True)
			for folder in dailiesFoldersLs:
			    if os.path.isdir('%s/%s' % (dailiesPath, folder)):
				   dailiesBin.importFolder('%s/%s' % (dailiesPath, folder))
		else:
			os.system('mkdir -p %s' % dailiesPath)
	else:
		verbose.noHrox(jobHrox)
			

removeAutoSave()
loadDailies()