#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_animPbl
#copyright	:Gramercy Park Studios


#animation curve publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose

def publish(pblTo, slShot, pblNotes, mail, approved):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return
		
	#defining main variables
	shot_ = os.environ['SHOT']
	assetType = 'ma_anim'
	subsetName = ''
	prefix = ''
	convention = objLs[0]
	suffix = '_anim'
	fileType = 'atomExport'
	extension = 'atom'
		
	#gets all dependants
	allObjLs = mc.listRelatives(objLs[0], ad=True, f=True)
	
	##adds original selection to allObj if no dependants are found
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
			return
		
	#check if selected asset is a published asset and matches the asset name
	try:
		ICSetConn = mc.listConnections('%s.icARefTag' % objLs[0])
		if not ICSetConn[0].startswith('ICSet'):
			raise RuntimeError('ICSet')
	except:
		verbose.pblAssetReq()
		return
						
	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	
	#adding shot name to assetPblName if asset is being publish to a shot
	if pblTo != os.environ['JOBPUBLISHDIR']:
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
		pblDir = osOps.createDir(os.path.join(pblDir, version))

		#creating in progress tmp file
		inProgress.start(pblDir)

		#ic publish data file
		requires = mc.getAttr('%s.icRefTag' % ICSetConn[0])
		compatible = '%s_%s' % (requires, mc.getAttr('ICSet_%s.icVersion' % requires))
		icPblData.writeData(pblDir, assetPblName, objLs[0], assetType, extension, version, pblNotes, requires, compatible)
		
		#file operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportAnimation(pathToPblAsset, pblDir, objLs)

		#published asset check
		pblResult = pblChk.sucess(pathToPblAsset)

		#deleting in progress tmp file
		inProgress.end(pblDir)

		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		osOps.recurseRemove(pblDir)
		pblResult = pblChk.sucess(pathToPblAsset)
		pblResult += verbose.pblRollback()
	
	#publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)