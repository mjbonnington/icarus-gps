#!/usr/bin/python

# [Icarus] ma_versionUpdate.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Loads Version Manager and updates asset.


import os


def update(ICSet):
	from rsc.maya.scripts import mayaOps
	from tools.versionManager import versionManager
	reload(versionManager)

	ICSetAttrDic = mayaOps.getICSetAttrs(ICSet)
	vManagerDialog = versionManager.dialog()
	updateVersion = vManagerDialog.display(ICSetAttrDic['icAssetRootDir'], ICSetAttrDic['icVersion'])
	if not updateVersion:
		return
	else:
		updatePath = os.path.join(ICSetAttrDic['icAssetRootDir'], updateVersion)

		# Update alembic geo caches
		if ICSetAttrDic['icAssetExt'] == 'abc':
			from . import ma_geoCacheUpdate
			ma_geoCacheUpdate.alembic(ICSet, updatePath)

		# All other geo types
		else:
			from . import ma_assetUpdate
			ma_assetUpdate.update(ICSet, updatePath)

