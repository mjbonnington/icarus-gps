#!/usr/bin/python

# [Icarus] ma_animPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type ma_anim.


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


def publish(pblTo, slShot, pblNotes):

	# Get selection
	objLs = mc.ls(sl=True)

	# Check item count
	if not pblChk.itemCount(objLs):
		return

	# Define main variables
	shot_ = os.environ['IC_SHOT']
	assetType = 'ma_anim'
	subsetName = ''
	prefix = ''
	convention = objLs[0]
	suffix = '_anim'
	fileType = 'atomExport'
	extension = 'atom'

	# Check for illegal characters
	cleanObj = os_wrapper.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Get all dependents
	allObjLs = mc.listRelatives(convention, ad=True, f=True)
	# Add original selection to allObj if no dependents are found
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

	# Check if selected asset is a published asset and matches the asset name
	try:
		ICSetConn = mc.listConnections('%s.icARefTag' % convention)
		if not ICSetConn[0].startswith('ICSet'):
			raise RuntimeError('ICSet')
	except:
		verbose.pblAssetReq()
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
		requires = mc.getAttr('%s.icRefTag' % ICSetConn[0])
		compatible = '%s_%s' % (requires, mc.getAttr('ICSet_%s.icVersion' % requires))
		icPblData.writeData(pblDir, assetPblName, convention, assetType, extension, version, pblNotes, src, requires, compatible)

		# Maya operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportAnimation(pathToPblAsset, pblDir, objLs)
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

