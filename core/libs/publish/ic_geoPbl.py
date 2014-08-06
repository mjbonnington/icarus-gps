#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:genPbl
#copyright	:Gramercy Park Studios


#generic publish module
import os
import pblChk, pblOptsPrc, vCtrl, pDialog, mkPblDirs, notes, verbose, approvePbl
	
def publish(pathToAsset, assetName, pblTo, slShot, geoType, pblNotes, mail, approved):
	
	jobPath = os.environ["JOBPATH"]
	job = os.environ["JOB"]
	shot_ = os.environ["SHOT"]
	assetType = "geo"
	subsetName = geoType
	prefix = assetName
	convention = "_geo"
	suffix = "_%s" % geoType
	extension = geoType		

	#checking for correct path to Asset
	if not pblChk.chkFile(pathToAsset):
		return

	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#adding shot name to assetPblName if asset is being publish to a shot
	if pblTo != os.environ['JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot
	
	#version control	
	version = vCtrl.version(pblDir)
	#appends approval tag to version if approved
	if approved:
		version += '_apv'

	#confirmation dialog
	dialogTitle = "Publishing"
	dialogMsg = "Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s" % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	#creating publish directories
	pblDir = mkPblDirs.mkDirs(pblDir, version)

	#file operations
	pathToPblAsset = "%s/%s_%s.%s" % (pblDir, assetPblName, version, extension)
	verbose.pblFeed(begin=True)
	verbose.pblFeed(asset = assetPblName)
	os.system("cp %s %s" % (pathToAsset, pathToPblAsset))
	if approved:
		approvePbl.publish(pblDir, assetDir, version)
	verbose.pblFeed(end=True)
	
	#notes file
	pblNotes += '\n\noriginal: %s' % (pathToAsset) 
	pblNotes = notes.notesFile(pblDir, pblNotes)
	
	#publish result dialog
	pblResult = pblChk.sucess(pathToPblAsset)
	dialogTitle = "Publish Report"
	dialogMsg = "Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s" % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)			
	
