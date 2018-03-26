#!/usr/bin/python

# [Icarus] icPblData.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Saves metadata for a published asset.


import os
import time

import settingsData
import osOps
import verbose


def writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, notes, assetSrc=None, requires=None, compatible=None):
#def writeData(publishVars):
	""" Store asset metadata in file.
		TODO: pass in list of args to write out, iterate over list
	"""
	timeFormatStr = "%a, %d %b %Y %H:%M:%S"
	#timeFormatStr = "%a, %d %b %Y %H:%M:%S +0000" # Format to RFC 2833 standard
	pblTime = time.strftime(timeFormatStr) # Can be parsed with time.strptime(pblTime, timeFormatStr)
	username = os.environ['IC_USERNAME']

	# Instantiate XML data classes
	assetData = settingsData.SettingsData()
	assetData.loadXML(os.path.join(pblDir, 'assetData.xml'), quiet=True)

	# Parse asset file path, make relative
	assetRootDir = osOps.relativePath(os.path.split(pblDir)[0], 'JOBPATH')

	# Parse source scene file path, make relative
	if assetSrc:
		assetSource = osOps.relativePath(assetSrc, 'JOBPATH')
	else:
		assetSource = None

	# Store values - TODO: iterate over list of args to make metadata extensible. N.B. variable names will need to be standardised
#	for key, value in publishVars.iteritems():
#		assetData.setValue('asset', key, value)
	assetData.setValue('asset', 'assetRootDir', assetRootDir)
	assetData.setValue('asset', 'assetPblName', assetPblName)
	assetData.setValue('asset', 'asset', assetName)
	assetData.setValue('asset', 'assetType', assetType)
	assetData.setValue('asset', 'assetExt', assetExt)
	assetData.setValue('asset', 'version', version)
	assetData.setValue('asset', 'assetSource', assetSource)
	assetData.setValue('asset', 'requires', requires)
	assetData.setValue('asset', 'compatible', compatible)
	assetData.setValue('asset', 'notes', notes)
	assetData.setValue('asset', 'user', username)
	assetData.setValue('asset', 'timestamp', pblTime)

	# Save to file
	assetData.saveXML()


	# Legacy code to write out icData.py - remove when XML data is fully working
	# notes += '\n\n%s %s' % (username, pblTime)
	# icDataFile = open('%s/icData.py' % pblDir, 'w')
	# icDataFile.write("assetRootDir = '%s'\nassetPblName = '%s'\nasset = '%s'\nassetType = '%s'\nassetExt = '%s'\nversion = '%s'\nrequires = '%s'\ncompatible = '%s'\nnotes = '''%s''' " % (assetRootDir, assetPblName, assetName, assetType, assetExt, version, requires, compatible, notes))
	# icDataFile.close()

