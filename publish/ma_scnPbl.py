#!/usr/bin/python

# [Icarus] ma_scnPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# Benjamin Parry <ben.parry@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type ma_scene.


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
from shared import pDialog
from shared import vCtrl
from shared import verbose


def publish(pblTo, slShot, scnName, subtype, textures, pblNotes):

	# Define main variables
	assetType = 'ma_scene'
	subsetName = subtype
	prefix = ''
	convention = scnName
	suffix = '_scene'
	fileType = 'mayaAscii'
	extension = 'ma'

	# Check for illegal characters
	cleanObj = os_wrapper.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Get all dependents
	allObjLs = mc.ls(tr=True)

	# Remove Maya's default cameras from list
	defaultCamLs = ['front', 'persp', 'side', 'top']
	for defaultCam in defaultCamLs:
		allObjLs.remove(defaultCam)

	# Check if asset to publish is referenced
	for allObj in allObjLs:
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)

	# Add shot name to assetPblName if asset is being publish to a shot
	# Determining publish env var for relative directory
	if pblTo != os.environ['IC_JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot

	# Version control
	version = '%s' % vCtrl.version(pblDir)
#	if approved:
#		version += '_apv'

	# Confirmation dialog
	dialogTitle = 'Publishing %s' % convention
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.display(dialogMsg, dialogTitle):
		return

	# Publishing
	try:
		verbose.pblFeed(begin=True)

		# Create publish directories
		pblDir = os_wrapper.createDir(os.path.join(pblDir, version))
		if textures:
			os_wrapper.createDir(os.path.join(pblDir, 'tx'))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = mayaOps.getScene()
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes, src)

		# Publish operations
		try:
			mc.select('ICSet_*', ne=True, r=True)
			icSetLs = mc.ls(sl=True)
			for icSet in icSetLs:
				mc.delete(icSet)
		except:
			pass
		if textures:
			# Copy textures to publish directory (use hardlink instead?)
			txFullPath = os.path.join(pblDir, 'tx')
			# txRelPath = txFullPath.replace(os.path.expandvars('$IC_JOBPATH'), '$IC_JOBPATH')
			# txPaths = (txFullPath, txRelPath)

			# Returns a dict for fileNodes and oldTxPaths if updateMaya = True
			oldTxPaths = mayaOps.updateTextures(txFullPath, updateMaya=True)

		# Take snapshot
		mayaOps.snapShot(pblDir, isolate=False, fit=False)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		activeScene = mayaOps.getScene()
		mayaOps.redirectScene(pathToPblAsset)
		mayaOps.saveFile(fileType, updateRecentFiles=False)

		# Reverts the texture paths
		if textures and oldTxPaths:
				mayaOps.relinkTextures(oldTxPaths)

		mayaOps.redirectScene(activeScene)

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
	dialog = pDialog.dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

