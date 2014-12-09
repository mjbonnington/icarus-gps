#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:shotPbl
#copyright	:Gramercy Park Studios


#shot publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, mkPblDirs, icPblData, verbose, approvePbl

def publish(pblTo, pblNotes, mail, approved):
	
	#defining main variables
	shot_ = os.environ['SHOT']
	assetType = 'ma_shot'
	prefix = ''
	convention = shot_
	suffix = '_shot'
	subsetName = ''
	fileType = 'mayaAscii'
	extension = 'ma'


	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#version control	
	version = '%s' % vCtrl.version(pblDir)
	if approved:
		version += '_apv'
	hiddenVersion = '.%s' % version

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
		pblDir = mkPblDirs.mkDirs(pblDir, hiddenVersion, textures=True)
		visiblePblDir = pblDir.replace(hiddenVersion, version)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes)

		#publish operations
		#copying textures to pbl direcotry
		txFullPath = '%s/tx' % pblDir
		txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
		txPaths = (txFullPath, txRelPath)
		mayaOps.relinkTexture(txPaths, updateMaya=False)

		
		#snapshot
		mayaOps.snapShot(pblDir)

		#file operations
		pathToPblAsset = '%s/%s.%s' % (pblDir, assetPblName, extension)
		verbose.pblFeed(msg=assetPblName)
		activeScene = mayaOps.getScene()
		mayaOps.redirectScene(pathToPblAsset)
		mayaOps.saveFile(fileType)
		mayaOps.redirectScene(activeScene)

		#published asset check
		pblResult = pblChk.sucess(pathToPblAsset)

		#making publish visible and updating Maya
		os.system('mv %s %s' % (pblDir, visiblePblDir))
		
		#relinking textures to pbl visible direcotry
		txFullPath = '%s/tx' % visiblePblDir
		txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
		txPaths = (txFullPath, txRelPath)
		mayaOps.relinkTexture(txPaths, copy=False)
		
		verbose.pblFeed(end=True)
	
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		os.system('rm -rf %s' % pblDir)
		pblResult = pblChk.sucess(pathToPblAsset)
		pblResult += verbose.pblRollback()
	
	#publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
