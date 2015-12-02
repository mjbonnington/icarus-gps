#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:assetGather
#copyright	:Gramercy Park Studios

import os, sys, traceback
import verbose, pDialog, mayaOps
import maya.cmds as mc

def gather(gatherPath):

	#retrieves icData from gatherPath
	sys.path.append(gatherPath)
	import icData; reload(icData)
	sys.path.remove(gatherPath)
		
	try:	
		#check if ICSet for required asset exists in scene
		if not mc.objExists('ICSet_%s' % icData.requires):
			verbose.animRequires(icData.requires)
			return
		#check if ICSet with same name exist in scene and deletes it
		if mc.objExists('ICSet_%s' % icData.assetPblName):
			mc.delete('ICSet_%s' % icData.assetPblName)
		
		#gets published asset from the gatherPath
		animFile = os.path.join(gatherPath, '%s.%s' (icData.assetPblName, icData.assetExt))
		if not os.path.isfile(animFile):
			verbose.noAsset()
			return

		#loading ATOM animation plugin if needed
		mayaAppPath = os.path.split(os.environ['MAYAVERSION'])[0]
		#mc.loadPlugin(os.path.join(mayaAppPath, 'plug-ins', 'atomImportExport.bundle'), qt=True)
		mc.loadPlugin('atomImportExport', qt=True)

		#gathering
		allObjLs = mc.listRelatives(icData.asset, ad=True, f=True, typ='transform')
		if allObjLs:
			allObjLs.append(icData.asset)
		else:
			allObjLs = [icData.asset]
		#deleting old animation		
		mayaOps.deleteChannels(allObjLs, hierarchy=True)
		mc.select(icData.asset, r=True)
		mc.file(
		animFile,
		typ='atomImport',
		op=';;targetTime=3; option=replace; match=hierarchy;;selected=childrenToo;;search=;replace=;prefix=;suffix=;mapFile=',
		i=True,
		ra=True)
	
		#generating icSet
		dataSet = mayaOps.icDataSet(icData.asset, icData)
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for details'
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
