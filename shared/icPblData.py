#!/usr/bin/python

# [Icarus] icPblData.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Saves metadata for a published asset.


import os
import time

# Import custom modules
from . import os_wrapper
from . import json_metadata as metadata


#def writeData(**publish_vars):
def writeData(
	pblDir, 
	assetPblName, 
	assetName, 
	assetType, 
	assetExt, 
	version, 
	notes, 
	assetSrc=None, 
	requires=None, 
	compatible=None):
	""" Store asset metadata in file.
		TODO: pass in dict of args to write out
	"""
	timeFormatStr = "%Y/%m/%d %H:%M:%S"
	#timeFormatStr = "%a, %d %b %Y %H:%M:%S"
	#timeFormatStr = "%a, %d %b %Y %H:%M:%S +0000"  # Format to RFC 2833 standard
	pblTime = time.strftime(timeFormatStr)  # Can be parsed with time.strptime(pblTime, timeFormatStr)
	username = os.environ['IC_USERNAME']

	# Instantiate data classes
	assetData = metadata.Metadata(
		os.path.join(pblDir, 'asset_data.json'))

	# Parse asset file path, make relative
	assetRootDir = os_wrapper.relativePath(os.path.split(pblDir)[0], 'IC_JOBPATH')

	# Parse source scene file path, make relative
	if assetSrc:
		assetSource = os_wrapper.relativePath(assetSrc, 'IC_JOBPATH')
	else:
		assetSource = None

	# Store values - TODO: iterate over list of args to make metadata extensible. N.B. variable names will need to be standardised
	# for key, value in publishVars.iteritems():
	# 	assetData.set_attr('asset', key, value)
	assetData.set_attr('asset', 'assetRootDir', assetRootDir)
	assetData.set_attr('asset', 'assetPblName', assetPblName)
	assetData.set_attr('asset', 'asset', assetName)
	assetData.set_attr('asset', 'assetType', assetType)
	assetData.set_attr('asset', 'assetExt', assetExt)
	assetData.set_attr('asset', 'version', version)
	assetData.set_attr('asset', 'assetSource', assetSource)
	assetData.set_attr('asset', 'requires', requires)
	assetData.set_attr('asset', 'compatible', compatible)
	assetData.set_attr('asset', 'notes', notes)
	assetData.set_attr('asset', 'user', username)
	assetData.set_attr('asset', 'timestamp', pblTime)

	# Save to file
	assetData.save()
