#!/usr/bin/python

# [Icarus] icPblData.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Manipulates published asset metadata.


import os, time
import jobSettings, verbose


def writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, assetSrc, pblNotes, requires=None, compatible=None):
	""" Store asset metadata in file.
	"""
	timeFormatStr = "%a, %d %b %Y %H:%M:%S"
	#timeFormatStr = "%a, %d %b %Y %H:%M:%S +0000" # Format to RFC 2833 standard
	pblTime = time.strftime(timeFormatStr) # Can be parsed with time.strptime(pblTime, timeFormatStr)
	userName = os.environ['USERNAME']

	# Instantiate XML data classes
	assetData = jobSettings.jobSettings()
	assetData.loadXML(os.path.join(pblDir, 'assetData.xml'))

	# Parse asset file path
	assetRootDir = os.path.split(pblDir)[0]
	assetRootDir = assetRootDir.replace(os.environ['JOBPATH'], '$JOBPATH')
	assetRootDir = assetRootDir.replace('\\', '/') # Ensure backslashes from Windows paths are changed to forward slashes

	# Parse source scene file path
	assetSource = os.path.normpath(assetSrc)
	assetSource = assetSource.replace(os.environ['JOBPATH'], '$JOBPATH')
	assetSource = assetSource.replace('\\', '/') # Ensure backslashes from Windows paths are changed to forward slashes

	# Store values
	assetData.setValue('asset', 'assetRootDir', assetRootDir)
	assetData.setValue('asset', 'assetPblName', assetPblName)
	assetData.setValue('asset', 'asset', assetName)
	assetData.setValue('asset', 'assetType', assetType)
	assetData.setValue('asset', 'assetExt', assetExt)
	assetData.setValue('asset', 'version', version)
	assetData.setValue('asset', 'assetSource', assetSource)
	assetData.setValue('asset', 'requires', requires)
	assetData.setValue('asset', 'compatible', compatible)

	assetData.setValue('asset', 'notes', pblNotes)
	assetData.setValue('asset', 'user', userName)
	assetData.setValue('asset', 'timestamp', pblTime)

	# Save to file
	assetData.saveXML()


	# Legacy code to write out icData.py - remove when XML data is fully working
	pblNotes += '\n\n%s %s' % (userName, pblTime)
	icDataFile = open('%s/icData.py' % pblDir, 'w')
	icDataFile.write("assetRootDir = '%s'\nassetPblName = '%s'\nasset = '%s'\nassetType = '%s'\nassetExt = '%s'\nversion = '%s'\nrequires = '%s'\ncompatible = '%s'\nnotes = '''%s''' " % (assetRootDir, assetPblName, assetName, assetType, assetExt, version, requires, compatible, pblNotes))
	icDataFile.close()

