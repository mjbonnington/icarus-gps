#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_camPbl
#copyright	:Gramercy Park Studios


#camera publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, inProgress

def publish(pblTo, slShot, cameraType, pblNotes):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return
		
	#defining main variables
	shot_ = os.environ['SHOT']
	assetType = 'ic_camera'
	subsetName = ''
	prefix = ''
	convention = cameraType
	suffix = '_camera'
	fileType='mayaAscii'
	extension = 'ma'
		
	#gets all dependants	
	allObjLs = mc.listRelatives(objLs[0], ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(objLs[0])
	else:
		allObjLs = [objLs[0]]
		
	#checks if selection is a camera
	if not mayaOps.cameraNodeCheck(objLs[0]):
		verbose.notCamera()
		return

	#check if asset to publish is referenced
	for allObj in allObjLs: 
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return

	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	assetPblName += '_%s' % slShot

	#version control	
	version = '%s' % vCtrl.version(pblDir)
	#if approved:
	#	version += '_apv'

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

		#maya operations
		mayaOps.deleteICDataSet(allObjLs)
		newcamLs = mayaOps.cameraBake(objLs, assetPblName)
		objLs = [newcamLs[0]]
		attrLs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
		mayaOps.lockAttr(objLs, attrLs)

		#file operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, fileType)
		mayaOps.nkCameraExport(objLs, pblDir, assetPblName, version)
		mayaOps.exportGeo(objLs, 'fbx', pathToPblAsset)
		osOps.setPermissions(os.path.join(pblDir, '*'))

		#deleting in progress tmp file
		inProgress.end(pblDir)

		#published asset check
		pblResult = pblChk.success(pathToPblAsset)

		#deleting in progress tmp file
		inProgress.end(pblDir)

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
	
