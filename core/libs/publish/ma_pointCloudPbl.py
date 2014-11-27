#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ic_pointCloudPbl
#copyright	:Gramercy Park Studios


#pointCloud publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, mkPblDirs, icPblData, verbose, approvePbl

def publish(pblTo, slShot, subsetName, textures, pblNotes, mail, approved):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return
	
	#checks if item is particle
	objSh = mc.listRelatives(objLs[0])[0]
	objType = mayaOps.nodetypeCheck(objSh)
	if objType not in ('particle', 'nParticle'):
		verbose.pointCloudParticle()
		return
		
	#defining main variables
	geoType = 'abc'
	assetType = 'ic_pointCloud'
	prefix = objLs[0]
	convention = '_pointCloud'
	suffix = ''
	ma_fileType = 'mayaBinary'
	extension = geoType
		
	#gets all dependants	
	allObjLs = mc.listRelatives(objLs[0], ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(objLs[0])
	else:
		allObjLs = [objLs[0]]
		
	#check if asset to publish is a set
	if mc.nodeType(objLs[0]) == 'objectSet':
		verbose.noSetsPbl()
		return
		
	#check if asset to publish is an icSet
	if mayaOps.chkIcDataSet(objLs[0]):
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
		pblDir = mkPblDirs.mkDirs(pblDir, hiddenVersion, textures)

		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, objLs[0], assetType, extension, version, pblNotes)
	
		#maya operations
		if textures:
			txFullPath = '%s/tx' % pblDir
			txRelPath = txFullPath.replace(pblTo, pblRelDir)
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, txObjLs=allObjLs)
		#getting tranforms, writting to file and zeroing obj out
		objTrs = mayaOps.getTransforms(objLs[0])
		if objTrs:
			objT, objR, objS = objTrs
		else:
			raise RunitmeError(verbose.noGetTranforms())
		
		trsDataFile = open('%s/trsData.py' % (pblDir), 'w')
		trsDataFile.write('t=%s\nr=%s\ns=%s' % (objT, objR, objS))
		trsDataFile.close()
		mayaOps.applyTransforms(objLs[0], [0,0,0], [0,0,0], [1,1,1])
		mayaOps.snapShot(pblDir)

		#file operations
		pathToPblAsset = '%s/%s.%s' % (pblDir, assetPblName, extension)
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, ma_fileType)
		mayaOps.exportGeo(objLs, geoType, pathToPblAsset)
		#reapplying original tranforms to object
		mayaOps.applyTransforms(objLs[0], objT, objR, objS)

		#published asset check
		pblResult = pblChk.sucess(pathToPblAsset)
		
		#making publish visible
		visiblePblDir = pblDir.replace(hiddenVersion, version)
		os.system('mv %s %s' % (pblDir, visiblePblDir))
		
		#approving publish
		if approved:
			approvePbl.publish(apvDir, visiblePblDir, assetDir, assetType, version)
		
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

