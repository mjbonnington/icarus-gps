#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:nk_setupPbl
#copyright	:Gramercy Park Studios


#nuke setup publish module
import os, sys, traceback
import nuke
import pblChk, pblOptsPrc, vCtrl, pDialog, mkPblDirs, icPblData, verbose, nukeOps, inProgress

def publish(pblTo, slShot, pblType, pblNotes, mail, approved):
	
	#gets and selects all nodes
	nodeLs = nuke.root().nodes()
		
	#defining main variables
	shot_ = ''
	assetType = 'nk_%s' % pblType
	subsetName = ''
	prefix = ''
	convention = pblType
	suffix = ''
	fileType='nk'
	extension = 'nk'
	

	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#adding shot name to assetPblName if asset is being publish to a shot
	if pblTo == os.environ['SHOTPUBLISHDIR']:
		assetPblName += '_%s' % slShot
		
	
	#version control	
	version = '%s' % vCtrl.version(pblDir)
	if approved:
		version += '_apv'

	#confirmation dialog
	dialogTitle = 'Publishing'
	dialogMsg = 'Asset:  %s\n\nVersion:  %s\n\nSubset:  %s\n\nNotes:  %s' % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	try:	
		verbose.pblFeed(begin=True)

		#creating publish directories
		pblDir = mkPblDirs.mkDirs(pblDir,version)

		#creating in progress tmp file
		inProgress.start(pblDir)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes)

		#Nuke operations
		icSet = nukeOps.createBackdrop(assetPblName, nodeLs)

		#file operations
		pathToPblAsset = '%s/%s.%s' % (pblDir, assetPblName, extension)
		verbose.pblFeed(msg=assetPblName)
		nukeOps.saveAs(pathToPblAsset)
		nuke.delete(icSet)
		
		#viewer snapshot
		nukeOps.viewerSnapshot(pblDir)

		#deleting in progress tmp file
		inProgress.end(pblDir)

		#published asset check
		pblResult = pblChk.success(pathToPblAsset)
		
		verbose.pblFeed(end=True)
	
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		os.system('rm -rf %s' % pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	#publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:  %s\n\nVersion:  %s\n\nSubset: %s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)	
	

