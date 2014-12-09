#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ma_versionUpdate
#copyright	:Gramercy Park Studios

import os
import versionManager


#loads version manager and updates asset

def update(ICSet):
	import mayaOps
	ICSetAttrDic = mayaOps.getICSetAttrs(ICSet)
	vManagerDialog = versionManager.dialog()
	updateVersion = vManagerDialog.dialogWindow(ICSetAttrDic['icAssetRootDir'], ICSetAttrDic['icVersion'])
	if not updateVersion:
		return
	else:
		updatePath = os.path.join(ICSetAttrDic['icAssetRootDir'], updateVersion)
		#updating alembic geocaches
		if ICSetAttrDic['icAssetExt'] == 'abc':
			import ma_geoCacheUpdate
			ma_geoCacheUpdate.alembic(ICSet, ICSetAttrDic, updatePath, updateVersion)
		#all other geo types
		else:
			import ma_assetUpdate
			ma_assetUpdate.update(ICSet, updatePath)
	