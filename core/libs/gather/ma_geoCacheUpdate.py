#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_geoCacheUpdate
#copyright	:Gramercy Park Studios

import os
import verbose, mayaOps
import maya.cmds as mc

def alembic(ICSet, ICSetAttrDic, updatePath, updateVersion):
		updatePath = '%s.%s' % (os.path.join(updatePath, ICSetAttrDic['icRefTag']), ICSetAttrDic['icAssetExt'])
		assetObj = mc.listConnections('%s.dagSetMembers' % ICSet)[0]
		
		#updating alembic
		#checking if maya object has same name updating asset
		if ICSetAttrDic['icAsset'] != assetObj:
			#Checking for name conflicts with other scene objects
			if mc.objExists(ICSetAttrDic['icAsset']):
				verbose.nameConflict(ICSetAttrDic['icAsset'])
				#storing conflicting object ID
				conflictObj = mc.rename(ICSetAttrDic['icAsset'], '%s_icGeoCache_update_tmp' % ICSetAttrDic['icAsset'])
				#renaming assetObj
				mc.rename(assetObj, ICSetAttrDic['icAsset'])
				#updating asset
				mc.AbcImport(updatePath, ct=ICSetAttrDic['icAsset'])
				#renaming both conflicting obj and assetObj to their original names
				mc.rename(ICSetAttrDic['icAsset'], assetObj)
				mc.rename(conflictObj, ICSetAttrDic['icAsset'])
			else:
				#renmaing maya obj to same name as asset
				mc.rename(assetObj, ICSetAttrDic['icAsset'])
				#updating cache
				mc.AbcImport(updatePath, ct=ICSetAttrDic['icAsset'])
				#renaming maya object back to original name
				mc.rename(ICSetAttrDic['icAsset'], assetObj)
		else:
			#updating asset
			mc.AbcImport(updatePath, ct=ICSetAttrDic['icAsset'])
			
		
		#updating icSet
		mayaOps.versionTag(ICSet, updateVersion)
		return
