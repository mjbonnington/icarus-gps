#!/usr/bin/python

# [Icarus] ma_nodePbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# Benjamin Parry <ben.parry@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type ma_node.


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


def publish(pblTo, slShot, nodeType, textures, pblNotes):

	# Get selection
	objLs = mc.ls(sl=True)
	
	# Check item count
	if not pblChk.itemCount(objLs):
		return

	# Define main variables
	assetType = '%s_node' % nodeType
	subsetName = mc.nodeType(objLs[0])
	prefix = ''
	convention = objLs[0]
	suffix = '_node'
	fileType = 'mayaAscii'
	extension = 'ma'

	# Check for illegal characters
	cleanObj = os_wrapper.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Check if asset to publish is a set
	if mc.nodeType(convention) == 'objectSet':
		verbose.noSetsPbl()
		return

	# Check if asset to publish is an icSet
	if mayaOps.chkIcDataSet(convention):
		verbose.noICSetsPbl()
		return

	# Check if asset to publish is referenced
	if mc.referenceQuery(convention, inr=True):
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

		# Maya operations
		mayaOps.deleteICDataSet(objLs)
		if textures:
			# Copy textures to publish directory (use hardlink instead?)
			txFullPath = os.path.join(pblDir, 'tx')
			# txRelPath = txFullPath.replace(os.path.expandvars('$JOBPATH'), '$JOBPATH')
			# txPaths = (txFullPath, txRelPath)

			# Returns a dict for fileNodes and oldTxPaths if updateMaya = True
			oldTxPaths = mayaOps.updateTextures(txFullPath, txObjLs=objLs, updateMaya=True)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, fileType)
		# Write Nuke file if ic and file node type
		if nodeType == 'ic':
			if subsetName == 'file':
				fileTypeLs = ('.jpg', '.jpeg', '.hdr', '.exr', '.tif', '.tiff', '.tga', '.png')
				fileLs = os.listdir(os.path.join(pblDir, 'tx'))
				for file_ in fileLs:
					if file_.endswith(fileTypeLs, -4):
						fileName = file_
						mayaOps.nkFileNodeExport(objLs, nodeType, fileName, pblDir, pblDir, assetPblName, version)

		# Reverts the texture paths
		if textures and oldTxPaths:
				mayaOps.relinkTextures(oldTxPaths)

		# Delete in-progress tmp file
		inProgress.end(pblDir)

		# Published asset check
		pblResult = pblChk.success(pathToPblAsset)

		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		os_wrapper.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = pDialog.dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

