#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:nk_setupPbl
#copyright	:Gramercy Park Studios


#nuke setup publish module
import os, sys, traceback
import nuke
import pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, nukeOps, inProgress


def publish(pblTo, slShot, pblType, pblName, pblNotes, mail, approved):
	
	#gets selection
	nodeLs = nuke.selectedNodes()
	
	#checks item count
	if pblType == 'node':
		if not pblChk.itemCount(nodeLs):
			return
	else:
		if not pblChk.itemCount(nodeLs, mult=True):
			return
		
	#defining main variables
	shot_ = ''
	assetType = 'nk_%s' % pblType
	subsetName = ''
	prefix = ''
	convention = pblName
	suffix = '_%s' % pblType
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
		pblDir = osOps.createDir(os.path.join(pblDir, version))

		#creating in progress tmp file
		inProgress.start(pblDir)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes)

		#Nuke operations
		icSet = nukeOps.createBackdrop(assetPblName, nodeLs)
		icSet['selected'].setValue(True)

		#file operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		nukeOps.exportSelection(pathToPblAsset)
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
		osOps.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	#publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:  %s\n\nVersion:  %s\n\nSubset: %s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)	
	

