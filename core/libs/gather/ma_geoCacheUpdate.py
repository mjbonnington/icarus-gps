#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_geoCacheUpdate
#copyright	:Gramercy Park Studios

import os, sys
import verbose, mayaOps
import maya.cmds as mc

def alembic(ICSet, updatePath):
		sys.path.append(updatePath)
		import icData; reload(icData)
		sys.path.remove(updatePath)
		
		updatePath = '%s.%s' % (os.path.join(updatePath, icData.assetPblName), icData.assetExt)
		assetObj = mc.listConnections('%s.dagSetMembers' % ICSet)[0]
		
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
				mc.AbcImport(updatePath, ct=icData.asset)
				#renaming both conflicting obj and assetObj to their original names
				mc.rename(icData.asset, assetObj)
				mc.rename(conflictObj, icData.asset)
			else:
				#renmaing maya obj to same name as asset
				mc.rename(assetObj, icData.asset)
				#updating cache
				mc.AbcImport(updatePath, ct=icData.asset)
				#renaming maya object back to original name
				mc.rename(icData.asset, assetObj)
		else:
			#updating asset
			mc.AbcImport(updatePath, ct=icData.asset)
			
		#updating icSet
		mayaOps.versionTag(ICSet, icData.version)
		mayaOps.notesTag(ICSet, icData.notes)
		return
