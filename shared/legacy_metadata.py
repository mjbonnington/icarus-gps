#!/usr/bin/python

# [Icarus] legacy_metadata.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2019 Gramercy Park Studios
#
# This module contains functions to retain backwards-compatibility with older
# types of Icarus metadata. Converts job/shot/asset metadata from Python
# source and XML files (legacy) to JSON, if JSON files don't exist.
# It's unwieldy and a bit ugly and hopefully will become redundant in the
# future.


import os
import sys

# Import custom modules
from . import jobs
from . import os_wrapper
from . import verbose


j = jobs.Jobs()

# Create mappings for environment variables that may have changed...
# Map the current key name to a list of old equivalents
environ_map = {
	'IC_BASEDIR': ['PIPELINE'], 
	'IC_JOBSROOT': ['JOBSROOT'], 
	'IC_JOBPATH': ['JOBPATH'], 
	'IC_SHOTPATH': ['SHOTPATH'], 
}

# os.environ['PIPELINE'] = os.environ['IC_BASEDIR']
# os.environ['JOBSROOT'] = os.environ['IC_JOBSROOT']
# os.environ['JOBPATH'] = os.environ['IC_JOBPATH']
# os.environ['SHOTPATH'] = os.environ['IC_SHOTPATH']

for key, value in environ_map.items():
	try:
		for oldkey in value:
			os.environ[oldkey] = os.environ[key]
	except AttributeError:
		pass


def loadLegacyMetadata(xml_datafile, py_datafile, env_var=None):
	""" If loading metadata failed, look for legacy metadata and attempt to
		load and/or convert it.
	"""
	# Attempt to load XML datafile
	from shared import xml_metadata
	data_object = xml_metadata.Metadata()
	data_object_loaded = data_object.load(xml_datafile)

	if data_object_loaded:
		if env_var is not None:
			os.environ[env_var] = xml_datafile  # update env var
		return data_object_loaded, data_object

	# If XML file doesn't exist, create defaults, and attempt to convert
	# data from Python data files.
	else:
		# Try to convert from icData.py to XML or JSON (legacy assets)
		data_path = os.path.dirname(xml_datafile)
		if convertAssetData(data_path, data_object):
			data_object_loaded = data_object.reload()
			return data_object_loaded, data_object

		else:
			return False, None


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

	verbose.warning("Could not detect the preferred version of %s.\nPlease set the preferred version in the Job Settings dialog or this app will be unavailable." % app)
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
			jd.set_attr('units', 'linear', jobData.unit)
		except AttributeError:
			pass
		try:
			jd.set_attr('units', 'angle', jobData.angle)
		except AttributeError:
			pass
		try:
			jd.set_attr('units', 'time', jobData.timeFormat)
		except AttributeError:
			pass
		try:
			jd.set_attr('units', 'fps', jobData.fps)
		except AttributeError:
			pass

		# Time settings

		# App versions
		try:
			jd.set_attr('apps', 'Maya', convertAppExecPath('Maya', jobData.mayaVersion, ap))
		except AttributeError:
			pass
		try:
			jd.set_attr('apps', 'Mudbox', convertAppExecPath('Mudbox', jobData.mudboxVersion, ap))
		except AttributeError:
			pass
		try:
			jd.set_attr('apps', 'Mari', convertAppExecPath('Mari', jobData.mariVersion, ap))
		except AttributeError:
			pass
		try:
			jd.set_attr('apps', 'Nuke', convertAppExecPath('Nuke', jobData.nukeVersion, ap))
		except AttributeError:
			pass
		try:
			jd.set_attr('apps', 'RealFlow', convertAppExecPath('RealFlow', jobData.realflowVersion, ap))
		except AttributeError:
			pass
		try:
			jd.set_attr('apps', 'HieroPlayer', convertAppExecPath('HieroPlayer', jobData.hieroPlayerVersion, ap))
		except AttributeError:
			pass

		# Other settings
		try:
			jd.set_attr('other', 'prodboard', jobData.prodBoard)
		except AttributeError:
			pass
		try:
			jd.set_attr('other', 'projtools', jobData.projectTools)
		except AttributeError:
			pass
		try:
			jd.set_attr('other', 'elementslib', jobData.elementsLibrary)
		except AttributeError:
			pass

		# Save XML
		if jd.save():
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
			sd.set_attr('time', 'rangeStart', shotData.frRange[0])
		except AttributeError:
			pass
		try:
			sd.set_attr('time', 'rangeEnd', shotData.frRange[1])
		except AttributeError:
			pass

		# Resolution settings
		try:
			sd.set_attr('resolution', 'fullWidth', shotData.res[0])
		except AttributeError:
			pass
		try:
			sd.set_attr('resolution', 'fullHeight', shotData.res[1])
		except AttributeError:
			pass
		try:
			sd.set_attr('resolution', 'proxyWidth', int(shotData.res[0]) / 2.0)
		except AttributeError:
			pass
		try:
			sd.set_attr('resolution', 'proxyHeight', int(shotData.res[1]) / 2.0)
		except AttributeError:
			pass

		# Save XML
		if sd.save():
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
			data.set_attr('asset', 'assetRootDir', icData.assetRootDir)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'assetPblName', icData.assetPblName)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'asset', icData.asset)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'assetType', icData.assetType)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'assetExt', icData.assetExt)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'version', icData.version)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'requires', icData.requires)
		except AttributeError:
			pass
		try:
			data.set_attr('asset', 'compatible', icData.compatible)
		except AttributeError:
			pass

		# Parse notes field
		try:
			notesLegacy = icData.notes.rsplit('\n\n', 1)
			notes = notesLegacy[0]
			notesFooter = notesLegacy[1].split(' ', 1)
			username = notesFooter[0]
			timestamp = notesFooter[1]

			data.set_attr('asset', 'notes', notes)
			data.set_attr('asset', 'user', username)
			data.set_attr('asset', 'timestamp', timestamp)
		except AttributeError:
			pass

		# Save XML
		if data.save():
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
	paths = [os.environ['IC_JOBPATH'], ]
	shots = _setJob_listShots(os.environ['IC_JOB']) # UPDATE
	for shot in shots:
		paths.append( _setJob_getPath(os.environ['IC_JOB'], shot) ) # UPDATE

	for path in paths:
		assetDir = os.path.join(path, '.publish')
		#print(assetDir)

		if os.path.isdir(assetDir):
			assetTypeDirs = []

			# Get subdirectories
			subdirs = next(os.walk(assetDir))[1]
			if subdirs:
				for subdir in subdirs:
					if not subdir.startswith('.'):  # ignore directories that start with a dot
						assetTypeDirs.append(subdir)

			if assetTypeDirs:
				return True

	return False


def _setJob_getPath(job, shot=False):
	""" Process job and shot names.
		'job' is mandatory.
		'shot' is optional, if given return the path to the shot, if not
		return the path to the job.
		*** DEPRECATED ***
	"""
	jobpath = j.getPath(job, translate=True)

	if shot:
		path = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s" % (jobpath, shot))
	else:
		path = os_wrapper.absolutePath("%s/$IC_SHOTSDIR" % jobpath)

	return path


def _setJob_listShots(job):
	""" List all available shots in the specified directory.
		*** DEPRECATED ***
	"""
	shotsPath = _setJob_getPath(job)

	# Check shot path exists before proceeding...
	if os.path.exists(shotsPath):
		dirContents = os.listdir(shotsPath)
		shotLs = []

		for item in dirContents:
			# Check for shot naming convention to disregard everything else in
			# directory
			if item.startswith('SH') or item.startswith('PC'):
				shotPath = os.path.join(shotsPath, item)

				# Check that the directory is a valid shot
				if _setJob_checkShot(shotPath):
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


def _setJob_checkShot(shotPath):
	""" Check for jobData and shotData modules to ensure the specified shot is
		valid.
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
