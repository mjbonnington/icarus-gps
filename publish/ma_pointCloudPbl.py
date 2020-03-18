#!/usr/bin/python

# [Icarus] ma_pointCloudPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# Benjamin Parry <ben.parry@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Publish an asset of the type ic_pointCloud.


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


def publish(pblTo, slShot, subtype, textures, pblNotes):

	# Get selection
	objLs = mc.ls(sl=True)

	# Check item count
	if not pblChk.itemCount(objLs):
		return

	# Define main variables
	geoType = 'abc'
	subsetName = subtype
	assetType = 'ic_pointCloud'
	prefix = ''
	convention = objLs[0]
	suffix = '_pointCloud'
	ma_fileType = 'mayaBinary'
	extension = geoType

	# Check for illegal characters
	cleanObj = os_wrapper.sanitize(convention)
	if cleanObj != convention:
		verbose.illegalCharacters(convention)
		return

	# Check if item is particle
	objSh = mc.listRelatives(objLs[0])[0]
	objType = mayaOps.nodetypeCheck(objSh)
	if objType not in ('particle', 'nParticle'):
		verbose.pointCloudParticle()
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
	if pblTo != os.environ['IC_JOBPUBLISHDIR']:
		assetPblName += '_%s' % slShot
		pblRelDir = '$IC_SHOTPUBLISHDIR'
	else:
		pblRelDir = '$IC_JOBPUBLISHDIR'

	# Version control
	version = '%s' % vCtrl.version(pblDir)
#	if approved:
#		version += '_apv'

	# Confirmation dialog
	dialogTitle = 'Publishing %s' % convention
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\nNotes:\t%s' % (assetPblName, version, subsetName, pblNotes)
	dialog = prompt.Dialog()
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
		if textures:
			# Copy textures to publish directory (use hardlink instead?)
			txFullPath = os.path.join(pblDir, 'tx')
			# txRelPath = txFullPath.replace(pblTo, pblRelDir)
			# txPaths = (txFullPath, txRelPath)

			# Returns a dict for fileNodes and oldTxPaths if updateMaya = True
			oldTxPaths = mayaOps.updateTextures(txFullPath, txObjLs=allObjLs, updateMaya=True)

		# Get transform data, write to file and zero obj out
		objTrs = mayaOps.getTransforms(convention)
		if objTrs:
			objT, objR, objS = objTrs
		else:
			raise RuntimeError(verbose.noGetTranforms())

		trsDataFile = open('%s/trsData.py' % (pblDir), 'w')
		trsDataFile.write('t=%s\nr=%s\ns=%s' % (objT, objR, objS))
		trsDataFile.close()
		mayaOps.applyTransforms(convention, [0,0,0], [0,0,0], [1,1,1])

		# Take snapshot
		mayaOps.snapShot(pblDir, isolate=True, fit=True)

		# File operations
		pathToPblAsset = os.path.join(pblDir, '%s.%s' % (assetPblName, extension))
		verbose.pblFeed(msg=assetPblName)
		mayaOps.exportSelection(pathToPblAsset, ma_fileType)
		mayaOps.exportGeo(objLs, geoType, pathToPblAsset)

		# Re-apply original transforms to object
		mayaOps.applyTransforms(convention, objT, objR, objS)

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
		os_wrapper.remove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = 'Publish Report'
	dialogMsg = 'Asset:\t%s\n\nVersion:\t%s\n\nSubset:\t%s\n\n\n%s' % (assetPblName, version, subsetName, pblResult)
	dialog = prompt.Dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

