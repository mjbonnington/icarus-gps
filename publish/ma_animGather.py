#!/usr/bin/python

# [Icarus] ma_animGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Gather an asset of type 'ma_anim'.


import os
import sys
import traceback

import maya.cmds as mc

from rsc.maya.scripts import mayaOps
from shared import prompt
from shared import json_metadata as metadata
from shared import verbose


def gather(gatherPath):

	gatherPath = os.path.expandvars(gatherPath)

	# Instantiate data classes
	assetData = metadata.Metadata(os.path.join(gatherPath, 'asset_data.json'))

	try:
		assetPblName = assetData.get_attr('asset', 'assetPblName')
		asset = assetData.get_attr('asset', 'asset')
		assetExt = assetData.get_attr('asset', 'assetExt')
		requires = assetData.get_attr('asset', 'requires')

		# Check if ICSet for required asset exists in scene
		if not mc.objExists('ICSet_%s' % requires):
			verbose.animRequires(requires)
			return

		# Check if ICSet with same name exist in scene and delete it
		if mc.objExists('ICSet_%s' % assetPblName):
			mc.delete('ICSet_%s' % assetPblName)

		# Get published asset from the gatherPath
		animFile = os.path.join(gatherPath, '%s.%s' % (assetPblName, assetExt))
		if not os.path.isfile(animFile):
			verbose.noAsset()
			return

		# Load ATOM animation plugin if needed
		mc.loadPlugin('atomImportExport', qt=True)

		# Gathering...
		allObjLs = mc.listRelatives(asset, ad=True, f=True, typ='transform')
		if allObjLs:
			allObjLs.append(asset)
		else:
			allObjLs = [asset]

		# Delete old animation
		mayaOps.deleteChannels(allObjLs, hierarchy=True)
		mc.select(asset, r=True)
		mc.file( animFile, 
				 typ='atomImport', 
				 op=';;targetTime=3; option=replace; match=hierarchy;;selected=childrenToo;;search=;replace=;prefix=;suffix=;mapFile=', 
				 i=True, 
				 ra=True )

		# Generate icSet
		dataSet = mayaOps.icDataSet(asset, assetData)


	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for more information.\n\n%s' % traceback.format_exc()
		dialog = prompt.dialog()
		dialog.display(dialogMsg, dialogTitle, conf=True)

