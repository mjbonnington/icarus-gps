#!/usr/bin/python

# [Icarus] ma_fxPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Publish an asset of the type ma_fx.


import os, sys, traceback
import maya.cmds as mc
import mayaOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, inProgress


def publish(pblTo, slShot, subtype, textures, pblNotes):

	# Get selection
	objLs = mc.ls(sl=True)

	# Check item count
	if not pblChk.itemCount(objLs):
		return

	# Define main variables
	assetType = 'ma_fx'
	subsetName = subtype
	prefix = ''
	convention = objLs[0]
	suffix = '_fx'
	fileType = 'mayaBinary'
	extension = 'mb'

	# Check for illegal characters
	cleanObj = osOps.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Get all dependents
	allObjLs = mc.listRelatives(convention, ad=True, f=True, typ='transform')
	if allObjLs:
		allObjLs.append(convention)
	else:
		allObjLs = [convention]

	# Check if asset to publish is a set
	if mc.nodeType(convention) == 'objectSet':
		verbose.noSetsPbl()
		return

	# Check if asset to publish is an icSet
	if mayaOps.chkIcDataSet(convention):
		verbose.noICSetsPbl()
		return

	# Check if asset to publish is referenced
	for allObj in allObjLs:
		if mc.referenceQuery(allObj, inr=True):
			verbose.noRefPbl()
			return

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)

	# Add shot name to assetPblName if asset is being publish to a shot
	# Determining publish env var for relative directory
	if pblTo != os.environ['JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot

	# Version control
	version = '%s' % vCtrl.version(pblDir)
#	if approved:
#		version += '_apv'

	# Confirmation dialog
	dialogTitle = 'Publishing %s' % convention
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	# Publishing
	try:
		verbose.pblFeed(begin=True)

		# Create publish directories
		pblDir = osOps.createDir(os.path.join(pblDir, version))
		if textures:
			osOps.createDir(os.path.join(pblDir, 'tx'))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = mayaOps.getScene()
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes, src)

		# Maya operations
		mayaOps.deleteICDataSet(allObjLs)
		if textures:
			# Copy textures to publish directory (use hardlink instead?)
			txFullPath = os.path.join(pblDir, 'tx')
			txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
			txPaths = (txFullPath, txRelPath)
			mayaOps.relinkTexture(txPaths, txObjLs=allObjLs, updateMaya=True)

		# Take snapshot
		mayaOps.snapShot(pblDir, isolate=True, fit=True)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, fileType)
	#	osOps.setPermissions(os.path.join(pblDir, '*'))

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
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

