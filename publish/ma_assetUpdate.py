#!/usr/bin/python

# [Icarus] ma_assetUpdate.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Updates asset.


import os

import maya.cmds as mc

from . import ma_assetGather


def update(ICSet, updatePath):
	updatePath = os.path.expandvars(updatePath)
	version = os.path.split(updatePath)[1]
	assetObj = mc.sets(ICSet, q=True)
	if assetObj:
		assetObj = assetObj[0]

	# Remove old asset from scene
	mc.delete(ICSet)
	mc.delete(assetObj)

	# Gather new asset
	ma_assetGather.gather(updatePath)

