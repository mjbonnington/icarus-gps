#!/usr/bin/python

# Legacy Settings
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Fallback functions to convert data from python files to XML, if XML files don't exist.


import re, sys
import verbose


def convertAppExecPath(app, path, ap):
	""" Given an executable path for an app, determine the version
	"""
	vers = ap.getVersions(app)
	for ver in vers:
		if ver in path:
			return ver

	return ""


def parseJobPath(path, element):
	""" Find the element (project number, job number) in the job path
	"""
	if element == 'projnum':
		pattern = re.compile(r'\d{6}')
	elif element == 'jobnum':
		pattern = re.compile(r'\d{7}')
	match = pattern.search(path)
	if match is not None:
		return match.group()

	return ""


def convertJobData(jobDataPath, jd, ap):
	""" Read job data from python source and save out an XML file
	"""
	sys.path.append(jobDataPath)
	import jobData
	reload(jobData)
	sys.path.remove(jobDataPath)

	# Job settings
	jd.setValue('job', 'projnum', parseJobPath(jobDataPath, 'projnum'))
	jd.setValue('job', 'jobnum', parseJobPath(jobDataPath, 'jobnum'))

	# Units settings
	jd.setValue('units', 'time', jobData.timeFormat)
	jd.setValue('units', 'linear', jobData.unit)
	jd.setValue('units', 'angle', jobData.angle)

	# Time settings
	jd.setValue('time', 'fps', jobData.fps)

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


def convertShotData(shotDataPath, sd):
	""" Read job data from python source and save out an XML file
	"""
	sys.path.append(shotDataPath)
	import shotData
	reload(shotData)
	sys.path.remove(shotDataPath)

	# General settings
	sd.setValue('resolution', 'fullWidth', shotData.res[0])
	sd.setValue('resolution', 'fullHeight', shotData.res[1])
	sd.setValue('time', 'rangeStart', shotData.frRange[0])
	sd.setValue('time', 'rangeEnd', shotData.frRange[1])

	# Save XML
	if sd.saveXML():
		verbose.settingsData_written('Shot')
		#print "Shot settings data file saved."
		return True
	else:
		verbose.settingsData_notWritten('Shot')
		#print "Warning: Shot settings data file could not be saved."
		return False

