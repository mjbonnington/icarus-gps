#!/usr/bin/python

# [Icarus] ma_assetGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Gather a published asset.


import os
import sys
import traceback

import maya.cmds as mc
import maya.mel as mel

from rsc.maya.scripts import mayaOps
from shared import os_wrapper
from shared import pDialog
from shared import settingsData
from shared import verbose


def gather(gatherPath):

	gatherPath = os.path.expandvars(gatherPath)

	# Instantiate XML data classes
	assetData = settingsData.SettingsData()
	assetData.loadXML(os.path.join(gatherPath, 'assetData.xml'), quiet=True)

	try:
		assetPblName = assetData.getValue('asset', 'assetPblName')
		asset = assetData.getValue('asset', 'asset')
		assetType = assetData.getValue('asset', 'assetType')
		assetExt = assetData.getValue('asset', 'assetExt')

		# Check for preferred .ma or .mb extension
		for item_ in os.listdir(gatherPath):
			if item_.endswith('.ma'):
				assetExt = 'ma'
			elif item_.endswith('.mb'):
				assetExt = 'mb'

		# Get published asset from the gatherPath
		assetPath = os.path.join(gatherPath, '%s.%s' % (assetPblName, assetExt))
		if not os.path.isfile(assetPath):
			verbose.noAsset()
			return

		# Load the appropriate plugin if needed
		if assetExt == 'abc':
			mc.loadPlugin('AbcImport', qt=True)
		elif assetExt == 'fbx':
			mc.loadPlugin('fbxmaya', qt=True)
		elif assetExt == 'obj':
			mc.loadPlugin('objExport', qt=True)

		# Gathering...
		drawOverrides = True
		if assetType == 'ma_shot':
			mayaOps.openScene(assetPath, dialog=False, updateRecentFiles=False)
			mayaOps.redirectScene(os.path.join(os.environ['MAYASCENESDIR'], 'untitled'))
			return
		elif assetExt == 'vrmesh':
			chkNameConflict(asset)
			mel.eval('vrayCreateProxy -node "%s" -dir "%s" -existing -createProxyNode;' % (asset, assetPath))
			vrmeshSG = mc.listSets(ets=True, t=1, object=asset)[0]
			vrmeshShd = mc.listConnections('%s.surfaceShader' % vrmeshSG, s=True, d=False)[0]
			mc.delete(vrmeshSG)
			mc.delete(vrmeshShd)
			newNodeLs=[asset]
		elif assetExt == 'abc':
			chkNameConflict(asset)
			newNodeLs = mc.file(assetPath, i=True, iv=True, rnn=True)
		else:
			chkNameConflict(asset)
			newNodeLs = mc.file(assetPath, i=True, iv=True, rnn=True)

		# Bypasses maya not displaying shading groups in sets. Adds the material node to icSet instead. Sets draw overrides to False.
		if assetType == 'ma_shader':
			drawOverrides = False
			connLs = mc.listConnections(asset, p=True)
			for conn in connLs:
				if '.outColor' in conn:
					icSetAsset = conn.split('.')[0]
		else:
			icSetAsset = asset

		# Sets draw overrides to false if asset is node
		if assetType == 'ma_node' or assetType == 'ic_node':
			drawOverrides = False

		# Generate icSet
		chkNameConflict('ICSet_%s' % assetPblName)

		# Connect original to icSet
		if assetType != 'ma_scene':
			dataSet = mayaOps.icDataSet(icSetAsset, assetData, update=None, drawOverrides=drawOverrides, addElements=True)
			mc.select(asset, r=True, ne=True)
			mc.addAttr(ln = 'icARefTag', dt='string')
			mc.connectAttr('%s.icRefTag' % dataSet,  '%s.icARefTag' % asset, f=True)
			mayaOps.lockAttr([asset], ['.icARefTag'], children=False)
		else:
			drawOverrides = False
			mayaOps.icDataSet(icSetAsset, assetData, update=None, drawOverrides=drawOverrides, addElements=False)


	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for more information.\n\n%s' % traceback.format_exc()
		dialog = pDialog.dialog()
		dialog.display(dialogMsg, dialogTitle, conf=True)


def chkNameConflict(obj):
	""" Check if object(s) with same name exist in scene. Checks for ICSets on
		those objects and renames them accordingly.
	"""
	if mc.objExists(obj):
		verbose.nameConflict(obj)
		objSetLs = mc.listSets(o=obj)
		newObjName = mayaOps.renameObj([obj], '%s_1' %obj, oldName=False)[0]

