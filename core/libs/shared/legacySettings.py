#!/usr/bin/python

# [Icarus] legacySettings.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# This module contains functions to retain backwards-compatibility with older
# types of Icarus metadata. Converts job/shot/asset metadata from Python files
# (legacy) to XML, if XML files don't exist.
# It's unwieldy and a bit ugly and hopefully will become redundant in the
# future.


import os
import sys

import jobs
import osOps
import verbose

j = jobs.Jobs()

try:
	os.environ['PIPELINE'] = os.environ['IC_BASEDIR']
except AttributeError:
	pass



def reloadModule(module):
	""" Reload module, compatible with Python 2 & 3.
	"""
	try:
		reload  # Python 2.7
	except NameError:
		try:
			from importlib import reload  # Python 3.4+
		except ImportError:
			from imp import reload  # Python 3.0 - 3.3

	reload(module)


def convertAppExecPath(app, path, ap):
	""" Given an executable path for an app, determine the version.
	"""
	vers = ap.getVersions(app)
	for ver in vers:
		if ver in path:
			return ver

	verbose.warning("Could not detect the preferred version of %s.\nPlease set the preferred version in the Job Settings dialog or this app will be unavailable." %app)
	return ""


def convertJobData(dataPath, jd, ap):
	""" Read job data from python source and save out an XML file.
		'jd' is jobData object.
		'ap' is appPaths object.
	"""
	if os.path.isfile(os.path.join(dataPath, 'jobData.py')):
		sys.path.append(dataPath)
		import jobData
		reloadModule(jobData)
		sys.path.remove(dataPath)

		# Units settings
		try:
			jd.setValue('units', 'linear', jobData.unit)
		except AttributeError:
			pass
		try:
			jd.setValue('units', 'angle', jobData.angle)
		except AttributeError:
			pass
		try:
			jd.setValue('units', 'time', jobData.timeFormat)
		except AttributeError:
			pass
		try:
			jd.setValue('units', 'fps', jobData.fps)
		except AttributeError:
			pass

		# Time settings

		# App versions
		try:
			jd.setValue('apps', 'Maya', convertAppExecPath('Maya', jobData.mayaVersion, ap))
		except AttributeError:
			pass
		try:
			jd.setValue('apps', 'Mudbox', convertAppExecPath('Mudbox', jobData.mudboxVersion, ap))
		except AttributeError:
			pass
		try:
			jd.setValue('apps', 'Mari', convertAppExecPath('Mari', jobData.mariVersion, ap))
		except AttributeError:
			pass
		try:
			jd.setValue('apps', 'Nuke', convertAppExecPath('Nuke', jobData.nukeVersion, ap))
		except AttributeError:
			pass
		try:
			jd.setValue('apps', 'RealFlow', convertAppExecPath('RealFlow', jobData.realflowVersion, ap))
		except AttributeError:
			pass
		try:
			jd.setValue('apps', 'HieroPlayer', convertAppExecPath('HieroPlayer', jobData.hieroPlayerVersion, ap))
		except AttributeError:
			pass

		# Other settings
		try:
			jd.setValue('other', 'prodboard', jobData.prodBoard)
		except AttributeError:
			pass
		try:
			jd.setValue('other', 'projtools', jobData.projectTools)
		except AttributeError:
			pass
		try:
			jd.setValue('other', 'elementslib', jobData.elementsLibrary)
		except AttributeError:
			pass

		# Save XML
		if jd.saveXML():
			verbose.message("Successfully converted legacy job data to XML.")
			return True
		else:
			return False

	else:
		verbose.print_("Cannot convert settings: job data not found.", 4)
		return False


def convertShotData(dataPath, sd):
	""" Read shot data from python source and save out an XML file.
		'sd' is shotData object.
	"""
	if os.path.isfile(os.path.join(dataPath, 'shotData.py')):
		sys.path.append(dataPath)
		import shotData
		reloadModule(shotData)
		sys.path.remove(dataPath)

		# Time settings
		try:
			sd.setValue('time', 'rangeStart', shotData.frRange[0])
		except AttributeError:
			pass
		try:
			sd.setValue('time', 'rangeEnd', shotData.frRange[1])
		except AttributeError:
			pass

		# Resolution settings
		try:
			sd.setValue('resolution', 'fullWidth', shotData.res[0])
		except AttributeError:
			pass
		try:
			sd.setValue('resolution', 'fullHeight', shotData.res[1])
		except AttributeError:
			pass
		try:
			sd.setValue('resolution', 'proxyWidth', int(shotData.res[0]) / 2.0)
		except AttributeError:
			pass
		try:
			sd.setValue('resolution', 'proxyHeight', int(shotData.res[1]) / 2.0)
		except AttributeError:
			pass

		# Save XML
		if sd.saveXML():
			verbose.message("Successfully converted legacy shot data to XML.")
			return True
		else:
			return False

	else:
		verbose.print_("Cannot convert settings: shot data not found.", 4)
		return False


def convertAssetData(dataPath, data):
	""" Read asset data from python source and save out an XML file.
	"""
	if os.path.isfile(os.path.join(dataPath, 'icData.py')):
		sys.path.append(dataPath)
		import icData
		reloadModule(icData)
		sys.path.remove(dataPath)

		# Store values
		try:
			data.setValue('asset', 'assetRootDir', icData.assetRootDir)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'assetPblName', icData.assetPblName)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'asset', icData.asset)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'assetType', icData.assetType)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'assetExt', icData.assetExt)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'version', icData.version)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'requires', icData.requires)
		except AttributeError:
			pass
		try:
			data.setValue('asset', 'compatible', icData.compatible)
		except AttributeError:
			pass

		# Parse notes field
		try:
			notesLegacy = icData.notes.rsplit('\n\n', 1)
			notes = notesLegacy[0]
			notesFooter = notesLegacy[1].split(' ', 1)
			username = notesFooter[0]
			timestamp = notesFooter[1]

			data.setValue('asset', 'notes', notes)
			data.setValue('asset', 'user', username)
			data.setValue('asset', 'timestamp', timestamp)
		except AttributeError:
			pass

		# Save XML
		if data.saveXML():
			verbose.message("Successfully converted legacy asset data to XML.")
			return True
		else:
			return False

	else:
		verbose.print_("Cannot convert settings: asset data not found.", 4)
		return False


def checkAssetPath():
	""" Check for existence of published assets within job's '.publish'
		directory.
		Return True as soon as any assets are found in any of the job or
		shot(s).
		This function should only run if the value 'meta/assetDir' is not set
		in the job settings data.
	"""
	verbose.print_("Checking for published assets...", 4)

	# import setJob

	# Get the paths of the job and all shots within the job
	paths = [os.environ['JOBPATH'], ]
	shots = setJob_listShots(os.environ['SHOW']) # UPDATE
	for shot in shots:
		paths.append( setJob_getPath(os.environ['SHOW'], shot) ) # UPDATE

	for path in paths:
		assetDir = os.path.join(path, '.publish')
		#print(assetDir)

		if os.path.isdir(assetDir):
			assetTypeDirs = []

			# Get subdirectories
			subdirs = next(os.walk(assetDir))[1]
			if subdirs:
				for subdir in subdirs:
					if not subdir.startswith('.'): # ignore directories that start with a dot
						assetTypeDirs.append(subdir)

			if assetTypeDirs:
				return True

	return False


def setJob_getPath(job, shot=False):
	""" Process job and shot names.
		'job' is mandatory.
		'shot' is optional, if given return the path to the shot, if not return the path to the job.
		*** DEPRECATED ***
	"""
	jobpath = j.getPath(job, translate=True)

	if shot:
		path = osOps.absolutePath("%s/$IC_SHOTSDIR/%s" %(jobpath, shot))
	else:
		path = osOps.absolutePath("%s/$IC_SHOTSDIR" %jobpath)

	return path


def setJob_listShots(job):
	""" List all available shots in the specified directory.
		*** DEPRECATED ***
	"""
	shotsPath = setJob_getPath(job)

	# Check shot path exists before proceeding...
	if os.path.exists(shotsPath):
		dirContents = os.listdir(shotsPath)
		shotLs = []

		for item in dirContents:
			# Check for shot naming convention to disregard everything else in directory
			if item.startswith('SH') or item.startswith('PC'):
				shotPath = os.path.join(shotsPath, item)

				# Check that the directory is a valid shot
				if setJob_checkShot(shotPath):
					shotLs.append(item)

		if len(shotLs):
			shotLs.sort()
			shotLs.reverse()
			return shotLs

		else:
			verbose.noShot(shotsPath)
			return False

	else:
		verbose.noJob(shotsPath)
		return False


def setJob_checkShot(shotPath):
	""" Check for jobData and shotData modules to ensure the specified shot is valid.
		*** DEPRECATED ***
	"""
	valid = True

	jobPath = os.path.split(shotPath)[0]
	#jobDataDir = os.path.join(jobPath, os.environ['IC_METADATA'])
	shotDataDir = os.path.join(shotPath, os.environ['IC_METADATA'])

	# if not os.path.isdir(jobDataDir):
	# 	valid = False

	if not os.path.isdir(shotDataDir):
		valid = False

	return valid

