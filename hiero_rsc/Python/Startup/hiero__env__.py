#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:hiero__env__
#copyright	:Gramercy Park Studios


#Sets up Hiero environment at startup
import hiero.core as hc
import os


def removeAutoSave():
	#getting project
	hroxAutosave = '%s/%s.hrox.autosave' % (os.environ['HIEROEDITORIALPATH'], os.environ['JOB'])
	if os.path.isfile(hroxAutosave):
		os.system('rm -rf %s' % hroxAutosave)

def loadDailies():
	#getting project
	jobHrox = '%s/%s.hrox' % (os.environ['HIEROEDITORIALPATH'], os.environ['JOB'])
	hieroProj = hc.openProject(jobHrox)

	#getting dailies bin
	dailiesBin = hc.findItemsInProject(hieroProj, hc.Bin, 'Dailies', verbose=0)[0]

	#removing dailies from bin
	dailies = dailiesBin.items()
	for daily in dailies:
	    dailiesBin.removeItem(daily)

	#adding daily folders to dailies bin
	dailiesPath = '%s/dailies' % os.environ['HIEROEDITORIALPATH']
	dailiesFoldersLs = os.listdir(dailiesPath)
	dailiesFoldersLs = sorted(dailiesFoldersLs, reverse=True)
	for folder in dailiesFoldersLs:
	    if os.path.isdir('%s/%s' % (dailiesPath, folder)):
		   dailiesBin.importFolder('%s/%s' % (dailiesPath, folder))
			

removeAutoSave()
loadDailies()