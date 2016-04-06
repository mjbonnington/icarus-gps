#!/usr/bin/python

# [Icarus] nk_setupPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Publish an asset of the type nk_setup.


import os, sys, traceback
import nuke
import nukeOps, pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, inProgress


def publish(pblTo, slShot, subtype, pblName, pblNotes):

	# Get selection
	nodeLs = nuke.selectedNodes()

	# Check item count
	if subtype == 'node':
		if not pblChk.itemCount(nodeLs):
			return
	else:
		if not pblChk.itemCount(nodeLs, mult=True):
			return

	# Define main variables
	shot_ = ''
	assetType = 'nk_%s' % subtype
	subsetName = ''
	prefix = ''
	convention = pblName
	suffix = '_%s' % subtype
	fileType = 'nk'
	extension = 'nk'

	# Check for illegal characters
	cleanObj = osOps.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)

	# Add shot name to assetPblName if asset is being publish to a shot
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

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = nuke.root().name() #nukeOps.getScriptName()
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes, src)

		# Nuke operations
		icSet = nukeOps.createBackdrop(assetPblName, nodeLs)
		icSet['selected'].setValue(True)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		nukeOps.exportSelection(pathToPblAsset)
		nuke.delete(icSet)

		# Take snapshot
		nukeOps.viewerSnapshot(pblDir)

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

