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

def loadDailies(cg=True, flame=True, edit=True):
	#getting project
	jobHrox = '%s/%s.hrox' % (os.environ['HIEROEDITORIALPATH'], os.environ['JOB'])
	#opening jobHrox if exists
	if os.path.isfile(jobHrox):
		hieroProj = hc.openProject(jobHrox)	

		#CG
		if cg:
			cgBin = hc.findItemsInProject(hieroProj, hc.Bin, 'CG', verbose=0)[0]
			cgPath = os.path.join(os.environ['WIPSDIR'], 'CGI')
			loadItems(cgPath, cgBin, emptyBin=True)
			
			
		#Flame
		if flame:
			flameBin = hc.findItemsInProject(hieroProj, hc.Bin, 'Flame', verbose=0)[0]
			flamePath = os.path.join(os.environ['WIPSDIR'], 'Flame')
			loadItems(flamePath, flameBin, emptyBin=True)
				
		
		#Edit
		if edit:
			editBin = hc.findItemsInProject(hieroProj, hc.Bin, 'Edit', verbose=0)[0]
			editPath = os.path.join(os.environ['WIPSDIR'], 'Edit')
			loadItems(editPath, editBin, emptyBin=True)
							
	else:
		verbose.noHrox(jobHrox)
		
def loadItems(path, bin, emptyBin=True):
	#emptying bin
	if emptyBin:
		binContents = bin.items()
		for content in binContents:
		    bin.removeItem(content)
	#detecting if directories exsit. if not creates one
	if os.path.isdir(path):
		#adding path contents to bin if directory exists
		itemsLs = os.listdir(path)
		itemsLs = sorted(itemsLs, reverse=True)
		for item in itemsLs:
			itemPath = os.path.join(path, item)
			if os.path.isdir(itemPath):
			   bin.importFolder(itemPath)
	else:
		os.system('mkdir -p %s' % path)

removeAutoSave()
loadDailies()