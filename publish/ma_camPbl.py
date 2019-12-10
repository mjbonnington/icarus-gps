#!/usr/bin/python

# [Icarus] ma_camPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type ic_camera.


import os
import sys
import traceback

import maya.cmds as mc

from . import pblChk
from . import pblOptsPrc
from . import inProgress
from rsc.maya.scripts import mayaOps
from shared import icPblData
from shared import os_wrapper
from shared import prompt
from shared import vCtrl
from shared import verbose


def publish(pblTo, slShot, subtype, pblNotes):

	# Get selection
	objLs = mc.ls(sl=True)

	# Check item count
	if not pblChk.itemCount(objLs):
		return

	# Define main variables
	shot_ = os.environ['IC_SHOT']
	assetType = 'ic_camera'
	subsetName = ''
	prefix = ''
	convention = subtype
	suffix = '_camera'
	fileType='mayaAscii'
	extension = 'ma'

	# Get all dependents
	allObjLs = mc.listRelatives(objLs[0], ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(objLs[0])
	else:
		allObjLs = [objLs[0]]

	# Check if selection is a camera
	if not mayaOps.cameraNodeCheck(objLs[0]):
		verbose.notCamera()
		return

	# Check if asset to publish is referenced
	for allObj in allObjLs: 
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	assetPblName += '_%s' % slShot

	# Version control
	version = '%s' % vCtrl.version(pblDir)
#	if approved:
#		version += '_apv'

	# Confirmation dialog
	dialogTitle = 'Publishing %s' % assetPblName # convention
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = prompt.dialog()
	if not dialog.display(dialogMsg, dialogTitle):
		return

	# Publishing
	try:
		verbose.pblFeed(begin=True)

		# Create publish directories
		pblDir = os_wrapper.createDir(os.path.join(pblDir, version))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = mayaOps.getScene()
		# icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes, src)
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes, src)

		# Maya operations
		mayaOps.deleteICDataSet(allObjLs)
		newcamLs = mayaOps.cameraBake(objLs, assetPblName)
		objLs = [newcamLs[0]]
		attrLs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
		mayaOps.lockAttr(objLs, attrLs)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, fileType)
		mayaOps.nkCameraExport(objLs, pblDir, assetPblName, version)
		mayaOps.exportGeo(objLs, 'fbx', pathToPblAsset)
	#	os_wrapper.setPermissions(os.path.join(pblDir, '*'))

		# Delete in-progress tmp file
		inProgress.end(pblDir)

		# Published asset check
		pblResult = pblChk.success(pathToPblAsset)

		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		os_wrapper.remove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = prompt.dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

