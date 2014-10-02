#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_geoCacheUpdate
#copyright	:Gramercy Park Studios

import os, sys, traceback
import pblChk, verbose, pDialog, mayaOps
import maya.cmds as mc
import maya.mel as mel

def update(gatherPath, icSetSel):
		#retrieves icData from gatherPath
		sys.path.append(gatherPath)
		import icData; reload(icData)
		sys.path.remove(gatherPath)
		
		assetPath = '%s/%s.%s' % (gatherPath, icData.assetPblName, icData.assetExt)
		assetObj = mc.listConnections('%s.dagSetMembers' % icSetSel[0])[0]
		assetObjRefTag = mc.getAttr('%s.icRefTag' % icSetSel[0])
		assetObjVersion = mc.getAttr('%s.icVersion' % icSetSel[0])
		
		#checing asset match
		if icData.assetPblName != assetObjRefTag:
			verbose.assetUpdateMatch()
			return
		
		#confirmation dialog
		dialogTitle = 'Updating'
		dialogMsg = '\n%s\n\nversion:\t%s\n\n will be updated with:\n\nversion:\t%s' % (assetObjRefTag, assetObjVersion, icData.version)
		dialog = pDialog.dialog()
		if not dialog.dialogWindow(dialogMsg, dialogTitle):
			return
		
		#updating alembic
		if icData.assetExt == 'abc':
			#checking if maya object has same name updating asset
			if icData.asset != assetObj:
				#Checking for name conflicts with other scene objects
				if mc.objExists(icData.asset):
					verbose.nameConflict(icData.asset)
					#storing conflicting object ID
					conflictObj = mc.rename(icData.asset, '%s_icGeoCache_update_tmp' % icData.asset)
					#renaming assetObj
					mc.rename(assetObj, icData.asset)
					#updating asset
					mc.AbcImport(assetPath, ct=icData.asset)
					#renaming both conflicting obj and assetObj to their original names
					mc.rename(icData.asset, assetObj)
					mc.rename(conflictObj, icData.asset)
				else:
					#renmaing maya obj to same name as asset
					mc.rename(assetObj, icData.asset)
					#updating cache
					mc.AbcImport(assetPath, ct=icData.asset)
					#renaming maya object back to original name
					mc.rename(icData.asset, assetObj)
			else:
				#updating asset
				mc.AbcImport(assetPath, ct=icData.asset)
			
		
		#updating icSet
		mayaOps.icDataSet(obj=None, icData=icData, update=icSetSel[0])
		return
