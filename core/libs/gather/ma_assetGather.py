#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:assetGather
#copyright	:Gramercy Park Studios

import os, sys, traceback
import pblChk, verbose, pDialog, mayaOps
import maya.cmds as mc
import maya.mel as mel

def gather(gatherPath):

	#retrieves icData from gatherPath
	sys.path.append(gatherPath)
	import icData; reload(icData)
	sys.path.remove(gatherPath)
	
	#check if objects with same name exist in scene
	if mc.objExists(icData.asset):
		verbose.nameConflict(icData.asset)
		mayaOps.renameObj([icData.asset], '%s_' % icData.asset, oldName=False)
	
	try:	
		#checks for prefered .ma or .mb extension
		assetExt = icData.assetExt
		for item_ in os.listdir(gatherPath):
			if item_.endswith('.ma'):
				assetExt = 'ma'
			elif item_.endswith('.mb'):
				assetExt = 'mb'
				
		#gets published asset from the gatherPath
		gatherPath += '/%s.%s' % (icData.assetPblName, assetExt)
		if not os.path.isfile(gatherPath):
			verbose.noAsset()
			return
	
		#loads the appropriate plugin if needed
		mayaAppPath = os.path.split(os.environ['MAYAVERSION'])[0]
		if assetExt == 'abc':
			mc.loadPlugin(os.path.join(mayaAppPath, 'plug-ins/AbcImport.bundle'), qt=True)
		elif assetExt == 'fbx':
			mc.loadPlugin(os.path.join(mayaAppPath, 'plug-ins/fbxmaya.bundle'), qt=True)
		elif assetExt == 'obj':
			mc.loadPlugin(os.path.join(mayaAppPath, 'plug-ins/objExport.bundle'), qt=True)
		
	
		#gathering
		if icData.assetType == 'ma_shot':
			mayaOps.openScene(gatherPath, dialog=False)
			mayaOps.redirectScene('%s/%s' % (os.environ['MAYASCENESDIR'], 'untitled'))
			return
		elif assetExt == 'vrmesh':
			mel.eval('vrayCreateProxy -node "%s" -dir "%s" -existing -createProxyNode;' % (icData.asset, gatherPath))
			vrmeshSG = mc.listSets(ets=True, t=1, object=icData.asset)[0]
			vrmeshShd = mc.listConnections('%s.surfaceShader' % vrmeshSG, s=True, d=False)[0]
			mc.delete(vrmeshSG)
			mc.delete(vrmeshShd)
			newNodeLs=[icData.asset]
		else:
			newNodeLs = mc.file(gatherPath, i=True, iv=True, rnn=True)
	
		#Bypasses maya not displaying shading groups in sets. Adds the material node to icSet instead
		if icData.assetType == 'ma_shader':
			connLs = mc.listConnections(icData.asset, p=True)
			for conn in connLs:
			    if '.outColor' in conn:
				   icSetAsset = conn.split('.')[0]
		else:
			icSetAsset = icData.asset
			
		#generating icSet
		dataSet = mayaOps.icDataSet(icSetAsset, icData)
		
		#connects original to icSet
		if icData.assetType != 'ma_scene':
			mc.select(icData.asset, r=True, ne=True)
			mc.addAttr(ln = 'icARefTag', dt='string')
			mc.connectAttr('%s.icRefTag' % dataSet,  '%s.icARefTag' % icData.asset, f=True)
			mayaOps.lockAttr([icData.asset], ['.icARefTag'], children=False)
			
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for details'
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
