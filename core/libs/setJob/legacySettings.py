#!/usr/bin/python

# [Icarus] legacySettings.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Fallback functions to convert job/shot/asset metadata from python files (legacy) to XML, if XML files don't exist.


import os, sys
import verbose


def convertAppExecPath(app, path, ap):
	""" Given an executable path for an app, determine the version.
	"""
	vers = ap.getVersions(app)
	for ver in vers:
		if ver in path:
			return ver

	print "Warning: could not detect the preferred version of %s.\nPlease set the preferred version in the Job Settings dialog or this app will be unavailable." %app
	return ""


def convertJobData(dataPath, jd, ap):
	""" Read job data from python source and save out an XML file.
	"""
	if os.path.isfile(os.path.join(dataPath, 'jobData.py')):
		verbose.settingsData_convert('jobData')

		sys.path.append(dataPath)
		import jobData
		reload(jobData)
		sys.path.remove(dataPath)

		# Job settings
		#jd.setValue('job', 'projnum', parseJobPath(dataPath, 'projnum'))
		#jd.setValue('job', 'jobnum', parseJobPath(dataPath, 'jobnum'))

		# Units settings
		jd.setValue('units', 'linear', jobData.unit)
		jd.setValue('units', 'angle', jobData.angle)
		jd.setValue('units', 'time', jobData.timeFormat)
		jd.setValue('units', 'fps', jobData.fps)

		# Time settings

		# App versions
		jd.setValue('apps', 'Maya', convertAppExecPath('Maya', jobData.mayaVersion, ap))
		jd.setValue('apps', 'Mudbox', convertAppExecPath('Mudbox', jobData.mudboxVersion, ap))
		jd.setValue('apps', 'Mari', convertAppExecPath('Mari', jobData.mariVersion, ap))
		jd.setValue('apps', 'Nuke', convertAppExecPath('Nuke', jobData.nukeVersion, ap))
		jd.setValue('apps', 'RealFlow', convertAppExecPath('RealFlow', jobData.realflowVersion, ap))
		jd.setValue('apps', 'HieroPlayer', convertAppExecPath('HieroPlayer', jobData.hieroPlayerVersion, ap))

		# Other settings
		jd.setValue('other', 'prodboard', jobData.prodBoard)
		jd.setValue('other', 'projtools', jobData.projectTools)
		jd.setValue('other', 'elementslib', jobData.elementsLibrary)

		# Save XML
		if jd.saveXML():
			verbose.settingsData_written('Job')
			#print "Job settings data file saved."
			return True
		else:
			verbose.settingsData_notWritten('Job')
			#print "Warning: Job settings data file could not be saved."
			return False

	else:
		#print "Cannot convert settings: jobData.py not found."
		return False


def convertShotData(dataPath, sd):
	""" Read shot data from python source and save out an XML file.
	"""
	if os.path.isfile(os.path.join(dataPath, 'shotData.py')):
		verbose.settingsData_convert('shotData')

		sys.path.append(dataPath)
		import shotData
		reload(shotData)
		sys.path.remove(dataPath)

		# Time settings
		sd.setValue('time', 'rangeStart', shotData.frRange[0])
		sd.setValue('time', 'rangeEnd', shotData.frRange[1])

		# Resolution settings
		sd.setValue('resolution', 'fullWidth', shotData.res[0])
		sd.setValue('resolution', 'fullHeight', shotData.res[1])
		sd.setValue('resolution', 'proxyWidth', int(shotData.res[0]) / 2)
		sd.setValue('resolution', 'proxyHeight', int(shotData.res[1]) / 2)

		# Save XML
		if sd.saveXML():
			verbose.settingsData_written('Shot')
			#print "Shot settings data file saved."
			return True
		else:
			verbose.settingsData_notWritten('Shot')
			#print "Warning: Shot settings data file could not be saved."
			return False

	else:
		#print "Cannot convert settings: shotData.py not found."
		return False


def convertAssetData(dataPath, ad):
	""" Read asset data from python source and save out an XML file.
	"""
	if os.path.isfile(os.path.join(dataPath, 'icData.py')):
		verbose.settingsData_convert('icData', 'assetData')

		sys.path.append(dataPath)
		import icData
		reload(icData)
		sys.path.remove(dataPath)

		# Store values
		ad.setValue('asset', 'assetRootDir', icData.assetRootDir)
		ad.setValue('asset', 'assetPblName', icData.assetPblName)
		ad.setValue('asset', 'asset', icData.asset)
		ad.setValue('asset', 'assetType', icData.assetType)
		ad.setValue('asset', 'assetExt', icData.assetExt)
		ad.setValue('asset', 'version', icData.version)
		ad.setValue('asset', 'requires', icData.requires)
		ad.setValue('asset', 'compatible', icData.compatible)

		# Parse notes field
		notesLegacy = icData.notes.rsplit('\n\n', 1)
		notes = notesLegacy[0]
		notesFooter = notesLegacy[1].split(' ', 1)
		username = notesFooter[0]
		timestamp = notesFooter[1]

		ad.setValue('asset', 'notes', notes)
		ad.setValue('asset', 'user', username)
		ad.setValue('asset', 'timestamp', timestamp)

		# Save XML
		if ad.saveXML():
			verbose.settingsData_written('Asset')
			#print "Asset settings data file saved."
			return True
		else:
			verbose.settingsData_notWritten('Asset')
			#print "Warning: Asset settings data file could not be saved."
			return False

	else:
		#print "Cannot convert settings: icData.py not found."
		return False

