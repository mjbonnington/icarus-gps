#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:assetGather
#copyright	:Gramercy Park Studios

import os, sys, traceback
import verbose, pDialog, mayaOps
import maya.cmds as mc
import maya.mel as mel

def gather(gatherPath):

	#retrieves icData from gatherPath
	#removes specific icData attributes that do not consistently exist in all icData modules and
	#are kept in memory even after a reload() or a del. Feels quite hacky and horrible but I've not found a way around this
	#This is only needed temporarily though as older assets do not have this icData attr
	sys.path.append(gatherPath)
	import icData
	try:
		del icData.assetRootDir
	except AttributeError:
		pass
	reload(icData)
	sys.path.remove(gatherPath)
	
	try:	
		#checks for prefered .ma or .mb extension
		assetExt = icData.assetExt
		for item_ in os.listdir(gatherPath):
			if item_.endswith('.ma'):
				assetExt = 'ma'
			elif item_.endswith('.mb'):
				assetExt = 'mb'
				
		#gets published asset from the gatherPath
		assetPath = '%s/%s.%s' % (gatherPath, icData.assetPblName, assetExt)
		if not os.path.isfile(assetPath):
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
		drawOverrides = True
		if icData.assetType == 'ma_shot':
			mayaOps.openScene(assetPath, dialog=False)
			mayaOps.redirectScene('%s/%s' % (os.environ['MAYASCENESDIR'], 'untitled'))
			return
		elif assetExt == 'vrmesh':
			chkNameConflict(icData.asset)
			mel.eval('vrayCreateProxy -node "%s" -dir "%s" -existing -createProxyNode;' % (icData.asset, assetPath))
			vrmeshSG = mc.listSets(ets=True, t=1, object=icData.asset)[0]
			vrmeshShd = mc.listConnections('%s.surfaceShader' % vrmeshSG, s=True, d=False)[0]
			mc.delete(vrmeshSG)
			mc.delete(vrmeshShd)
			newNodeLs=[icData.asset]
		elif assetExt == 'abc':
			chkNameConflict(icData.asset)
			newNodeLs = mc.file(assetPath, i=True, iv=True, rnn=True)
		else:
			chkNameConflict(icData.asset)
			newNodeLs = mc.file(assetPath, i=True, iv=True, rnn=True)
	
		#Bypasses maya not displaying shading groups in sets. Adds the material node to icSet instead. Sets draw overrides to False
		if icData.assetType == 'ma_shader':
			drawOverrides = False
			connLs = mc.listConnections(icData.asset, p=True)
			for conn in connLs:
			    if '.outColor' in conn:
				   icSetAsset = conn.split('.')[0]
		else:
			icSetAsset = icData.asset
			
		#Sets draw overrides to false if asset is node
		if icData.assetType == 'ma_node' or icData.assetType == 'ic_node':
			drawOverrides = False
			
		#generating icSet
		chkNameConflict('ICSet_%s' % icData.assetPblName)
		
		#connects original to icSet
		if icData.assetType != 'ma_scene':
			dataSet = mayaOps.icDataSet(icSetAsset, icData, update=None, drawOverrides=drawOverrides, addElements=True)
			mc.select(icData.asset, r=True, ne=True)
			mc.addAttr(ln = 'icARefTag', dt='string')
			mc.connectAttr('%s.icRefTag' % dataSet,  '%s.icARefTag' % icData.asset, f=True)
			mayaOps.lockAttr([icData.asset], ['.icARefTag'], children=False)
		else:
			drawOverrides = False
			mayaOps.icDataSet(icSetAsset, icData, update=None, drawOverrides=drawOverrides, addElements=False)
			
			
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for details'
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

#check if objects with same name exist in scene. Checks for ICSets on those objects and renames it accordingly
def chkNameConflict(obj):
	if mc.objExists(obj):
		verbose.nameConflict(obj)
		objSetLs = mc.listSets(o=obj)
		newObjName = mayaOps.renameObj([obj], '%s_' % obj, oldName=False)[0]
		
		
		
		
		
		