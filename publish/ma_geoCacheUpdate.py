#!/usr/bin/python

# [Icarus] ma_geoCacheUpdate.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Update a published alembit geo cache asset.


import os
import sys

import maya.cmds as mc

from rsc.maya.scripts import mayaOps
from shared import json_metadata as metadata
from shared import verbose


def alembic(ICSet, updatePath):

	updatePath = os.path.expandvars(updatePath)

	# Instantiate data classes
	assetData = metadata.Metadata(os.path.join(updatePath, 'asset_data.json'))

	assetPblName = assetData.get_attr('asset', 'assetPblName')
	asset = assetData.get_attr('asset', 'asset')
	assetExt = assetData.get_attr('asset', 'assetExt')
	version = assetData.get_attr('asset', 'version')
	notes = assetData.get_attr('asset', 'notes')

	updatePath = '%s.%s' % (os.path.join(updatePath, assetPblName), assetExt)
	assetObj = mc.listConnections('%s.dagSetMembers' % ICSet)[0]

	# Check if Maya object has same name updating asset
	if asset != assetObj:
		# Check for name conflicts with other scene objects
		if mc.objExists(asset):
			verbose.nameConflict(asset)
			# Store conflicting object ID
			conflictObj = mc.rename(asset, '%s_icGeoCache_update_tmp' % asset)
			# Rename assetObj
			mc.rename(assetObj, asset)
			# Update asset
			mc.AbcImport(updatePath, ct=asset)
			# Rename both conflicting obj and assetObj to their original names
			mc.rename(asset, assetObj)
			mc.rename(conflictObj, asset)
		else:
			# Rename Maya obj to same name as asset
			mc.rename(assetObj, asset)
			# Update cache
			mc.AbcImport(updatePath, ct=asset)
			# Rename Maya object back to original name
			mc.rename(asset, assetObj)
	else:
		# Update asset
		mc.AbcImport(updatePath, ct=asset)

	# Update icSet
	mayaOps.versionTag(ICSet, version)
	mayaOps.notesTag(ICSet, notes)
	return

