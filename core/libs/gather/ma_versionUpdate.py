#!/usr/bin/python

# [Icarus] ma_versionUpdate.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Loads Version Manager and updates asset.


import os


def update(ICSet):
	import mayaOps
	import versionManager
	reload(versionManager)

	ICSetAttrDic = mayaOps.getICSetAttrs(ICSet)
	vManagerDialog = versionManager.dialog()
	updateVersion = vManagerDialog.dialogWindow(ICSetAttrDic['icAssetRootDir'], ICSetAttrDic['icVersion'])
	if not updateVersion:
		return
	else:
		updatePath = os.path.join(ICSetAttrDic['icAssetRootDir'], updateVersion)

		# Update alembic geo caches
		if ICSetAttrDic['icAssetExt'] == 'abc':
			import ma_geoCacheUpdate
			ma_geoCacheUpdate.alembic(ICSet, updatePath)

		# All other geo types
		else:
			import ma_assetUpdate
			ma_assetUpdate.update(ICSet, updatePath)

