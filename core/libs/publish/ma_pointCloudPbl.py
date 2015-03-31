#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_pointCloudPbl
#copyright	:Gramercy Park Studios


#pointCloud publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, approvePbl, inProgress

def publish(pblTo, slShot, subsetName, textures, pblNotes, mail, approved):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return
		
	#defining main variables
	geoType = 'abc'
	assetType = 'ic_pointCloud'
	prefix = ''
	convention = objLs[0]
	suffix = '_pointCloud'
	ma_fileType = 'mayaBinary'
	extension = geoType

	#sanitizes selection charatcers
	cleanObj = osOps.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	#checks if item is particle
	objSh = mc.listRelatives(objLs[0])[0]
	objType = mayaOps.nodetypeCheck(objSh)
	if objType not in ('particle', 'nParticle'):
		verbose.pointCloudParticle()
		return
		
	#gets all dependants	
	allObjLs = mc.listRelatives(convention, ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(convention)
	else:
		allObjLs = [convention]
		
	#check if asset to publish is a set
	if mc.nodeType(convention) == 'objectSet':
		verbose.noSetsPbl()
		return
		
	#check if asset to publish is an icSet
	if mayaOps.chkIcDataSet(convention):
		verbose.noICSetsPbl()
		return

	#check if asset to publish is referenced
	for allObj in allObjLs:
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()

	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#determining approved publish directory
	#determining publish env var for relative directory
	if pblTo != os.environ['JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot
		pblRelDir = '$SHOTPUBLISHDIR'
		apvDir = os.environ['SHOTAPPROVEDPUBLISHDIR']
	else:
		pblRelDir = '$JOBPUBLISHDIR'
		apvDir = os.environ['JOBAPPROVEDPUBLISHDIR']
	
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
		pblDir = osOps.createDir(os.path.join(pblDir, version))
		if textures:
			osOps.createDir(os.path.join(pblDir, 'tx'))

		#creating in progress tmp file
		inProgress.start(pblDir)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes)
	
		#maya operations
		if textures:
			txFullPath = os.path.join(pblDir, 'tx')
			txRelPath = txFullPath.replace(pblTo, pblRelDir)
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, txObjLs=allObjLs, updateMaya=True)

		#getting tranform data, writting to file and zeroing obj out
		objTrs = mayaOps.getTransforms(convention)
		if objTrs:
			objT, objR, objS = objTrs
		else:
			raise RunitmeError(verbose.noGetTranforms())
		
		trsDataFile = open('%s/trsData.py' % (pblDir), 'w')
		trsDataFile.write('t=%s\nr=%s\ns=%s' % (objT, objR, objS))
		trsDataFile.close()
		mayaOps.applyTransforms(convention, [0,0,0], [0,0,0], [1,1,1])
		mayaOps.snapShot(pblDir)

		#file operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, ma_fileType)
		mayaOps.exportGeo(objLs, geoType, pathToPblAsset)
		#reapplying original tranforms to object
		mayaOps.applyTransforms(convention, objT, objR, objS)
		
		#approving publish
		if approved:
			approvePbl.publish(apvDir, pblDir, assetDir, assetType, version)

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
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

