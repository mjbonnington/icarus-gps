#!/usr/bin/python

# [Icarus] ma_shotPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Publish an asset of the type ma_shot.


import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, inProgress


def publish(pblTo, pblNotes):

	# Define main variables
	assetType = 'ma_shot'
	subsetName = ''
	prefix = ''
	convention = os.environ['SHOT']
	suffix = '_shot'
	fileType = 'mayaAscii'
	extension = 'ma'

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)

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
		pblDir = osOps.createDir(os.path.join(pblDir, version))
		osOps.createDir(os.path.join(pblDir, 'tx'))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = mayaOps.getScene()
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes, src)

		# Publish operations
		# Copy textures to publish directory (use hardlink instead?)
		txFullPath = os.path.join(pblDir, 'tx')
		txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
		txPaths = (txFullPath, txRelPath)
		mayaOps.relinkTexture(txPaths, updateMaya=True)

		# Take snapshot
		mayaOps.snapShot(pblDir, isolate=False, fit=False)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		activeScene = mayaOps.getScene()
		mayaOps.redirectScene(pathToPblAsset)
		mayaOps.saveFile(fileType, updateRecentFiles=False)
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
		osOps.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

