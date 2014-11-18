#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:nodePbl
#copyright	:Gramercy Park Studios


#generic publish module
import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, mkPblDirs, icPblData, verbose, approvePbl

	
def publish(pblTo, slShot, nodeType, subsetName, textures, pblNotes, mail, approved):
	
	#gets selection
	objLs = mc.ls(sl=True)
	
	#checks item count
	if not pblChk.itemCount(objLs):
		return
		
	#defining main variables
	assetType = '%s_node' % nodeType
	prefix = ''
	convention = objLs[0]
	suffix = '_node'
	fileType = 'mayaAscii'
	extension = 'ma'
	subsetName = mc.nodeType(objLs[0])
		

	#check if asset to publish is referenced
	if mc.referenceQuery(objLs[0], inr=True):
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
		visiblePblDir = pblDir.replace(hiddenVersion, version)
		
		#ic publish data file
		icPblData.writeData(pblDir, assetPblName, objLs[0], assetType, extension, version, pblNotes)
	
		#maya operations
		mayaOps.deleteICDataSet(objLs)
		if textures:
			#copying textures to pbl direcotry
			txFullPath = '%s/tx' % pblDir
			txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, txObjLs=objLs, updateMaya=False)

		#file operations
		pathToPblAsset = '%s/%s.%s' % (pblDir, assetPblName, extension)
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, fileType)
		#writing nuke file if ic and file node type
		if nodeType == 'ic':
			if subsetName == 'file':
				fileTypeLs = ('.jpg', '.jpeg', '.hdr', '.exr', '.tif', '.tiff', '.tga', '.png')
				fileLs = os.listdir('%s/tx' % pblDir)
				for file_ in fileLs:
					if file_.endswith(fileTypeLs, -4):
						fileName = file_
				mayaOps.nkFileNodeExport(objLs, nodeType, fileName, pblDir, visiblePblDir, assetPblName, version)
		
		#published asset check
		pblResult = pblChk.sucess(pathToPblAsset)
		
		#making publish visible
		os.system('mv %s %s' % (pblDir, visiblePblDir))
		
		#relinking textures to pbl visible direcotry
		if textures:
			txFullPath = '%s/tx' % visiblePblDir
			txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, txObjLs=objLs, copy=False)
			
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
	
	
