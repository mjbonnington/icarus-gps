#!/usr/bin/python

# [Icarus] Legacy Settings
# v0.2
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Fallback functions to convert job and shot data from python files (legacy) to XML, if XML files don't exist.


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


def convertJobData(jobDataPath, jd, ap):
	""" Read job data from python source and save out an XML file.
	"""
	if os.path.isfile(os.path.join(jobDataPath, 'jobData.py')):
		verbose.settingsData_convert('jobData')

		sys.path.append(jobDataPath)
		import jobData
		reload(jobData)
		sys.path.remove(jobDataPath)

		# Job settings
		#jd.setValue('job', 'projnum', parseJobPath(jobDataPath, 'projnum'))
		#jd.setValue('job', 'jobnum', parseJobPath(jobDataPath, 'jobnum'))

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


def convertShotData(shotDataPath, sd):
	""" Read shot data from python source and save out an XML file.
	"""
	if os.path.isfile(os.path.join(shotDataPath, 'shotData.py')):
		verbose.settingsData_convert('shotData')

		sys.path.append(shotDataPath)
		import shotData
		reload(shotData)
		sys.path.remove(shotDataPath)

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

