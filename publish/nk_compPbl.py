#!/usr/bin/python

# [Icarus] nk_compPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type nk_comp.


import os
import sys
import traceback

import nuke

from . import pblChk
from . import pblOptsPrc
from . import inProgress
from rsc.nuke.scripts import nukeOps
from shared import icPblData
from shared import os_wrapper
from shared import pDialog
from shared import vCtrl
from shared import verbose


def publish(pblTo, slShot, subtype, pblNotes):

	# Get selection
	nodeLs = nuke.root().nodes()

	# Define main variables
	shot_ = ''
	assetType = 'nk_%s' % subtype
	subsetName = ''
	prefix = ''
	convention = subtype
	suffix = ''
	fileType='nk'
	extension = 'nk'

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)

	# Add shot name to assetPblName if asset is being publish to a shot
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

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# Store asset metadata in file
		src = nuke.root().name() #nukeOps.getScriptName()
		icPblData.writeData(pblDir, assetPblName, assetPblName, assetType, extension, version, pblNotes, src)

		# Nuke operations
		icSet = nukeOps.createBackdrop(assetPblName, nodeLs)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		# nukeOps.saveAs(pathToPblAsset)
		nuke.scriptSaveAs(pathToPblAsset)
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
		os_wrapper.remove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

