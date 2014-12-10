#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:assetUpdate
#copyright	:Gramercy Park Studios

import os
import ma_assetGather
import maya.cmds as mc

def update(ICSet, updatePath):
	version = os.path.split(updatePath)[1]
	assetObj = mc.sets(ICSet, q=True)
	if assetObj:
		assetObj = assetObj[0]
	#removing old asset from scene
	mc.delete(ICSet)
	mc.delete(assetObj)
	#gathering new asset
	ma_assetGather.gather(updatePath)
