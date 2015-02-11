#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_scnPbl
#copyright	:Gramercy Park Studios


#maya scene publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, mkPblDirs, icPblData, verbose, approvePbl, inProgress


def publish(pblTo, slShot, scnName, subsetName, textures, pblNotes, mail, approved):

	
	#defining main variables
	assetType = 'ma_scene'
	prefix = ''
	convention = scnName
	suffix = '_scene'
	fileType = 'mayaAscii'
	extension = 'ma'
	
	#gets all dependants
	allObjLs = mc.ls(tr=True)
	
	#removing maya's default cameras from list 
	defaultCamLs = ['front', 'persp', 'side', 'top']
	for defaultCam in defaultCamLs:
		allObjLs.remove(defaultCam)
		
	#check if asset to publish is referenced
	for allObj in allObjLs: 
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return
			
	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#adding shot name to assetPblName if asset is being publish to a shot
	#determining publish env var for relative directory
	if pblTo == os.environ['SHOTPUBLISHDIR']:
		assetPblName += '_%s' % slShot
	
	#version control	
	version = '%s' % vCtrl.version(pblDir)
	if approved:
		version += '_apv'

	#confirmation dialog
	dialogTitle = 'Publishing'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	#publishing
	try:	
		verbose.pblFeed(begin=True)

		#creating publish directories
		pblDir = mkPblDirs.mkDirs(pblDir, version, textures=True)

		#creating in progress tmp file
		inProgress.start(pblDir)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, scnName, assetType, extension, version, pblNotes)
	
		#publish operations
		try:
			mc.select('ICSet_*', ne=True, r=True)
			icSetLs = mc.ls(sl=True)
			for icSet in icSetLs:
   				mc.delete(icSet)
   		except:
   			pass
		if textures:
			#copying textures to pbl direcotry
			txFullPath = '%s/tx' % pblDir
			txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, updateMaya=True)
			
		#snapshot
		mayaOps.snapShot(pblDir)

		#file operations
		pathToPblAsset = '%s/%s.%s' % (pblDir, assetPblName, extension)
		verbose.pblFeed(msg=assetPblName)
		activeScene = mayaOps.getScene()
		mayaOps.redirectScene(pathToPblAsset)
		mayaOps.saveFile(fileType)
		mayaOps.redirectScene(activeScene)

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
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

