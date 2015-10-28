#!/usr/bin/python

# [Icarus] Set Job
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Functions for job and shot setup.


import os
import defaultDirs, job__env__, jobs, userPrefs, verbose


def setup(job, shot):
	""" Set job.
	"""
	shotPath = getPath(job, shot)
	envVars = job, shot, shotPath
	job__env__.setEnv(envVars)
	defaultDirs.create()
	newEntry = '%s,%s' % (job, shot)
	userPrefs.edit('main', 'lastjob', newEntry)


def getPath(job, shot=False):
	""" Process job and shot names.

		'job' is mandatory
		'shot' is optional, if given return the path to the shot, if not return the path to the job.
	"""
	if shot:
		_path = os.path.join(jobs.dic[job], os.environ['SHOTSROOTRELATIVEDIR'], shot)
	else:
		_path = os.path.join(jobs.dic[job], os.environ['SHOTSROOTRELATIVEDIR'])

	return _path


def listShots(job):
	""" List all available shots in the specified directory.
	"""
	shotsPath = getPath(job)

	# Check shot path exists before proceeding...
	if os.path.exists(shotsPath):
		dirContents = os.listdir(shotsPath)
		shotLs = []

		for item in dirContents:
			# Check for shot naming convention to disregard everything else in directory
			if item.startswith('SH') or item.startswith('PC'):
				shotPath = os.path.join(shotsPath, item)

				# Check that the directory is a valid shot
				if checkShot(shotPath):
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


def checkShot(shotPath):
	""" Check for jobData and shotData modules to ensure the specified shot is valid.
	"""
	valid = True

	jobPath = os.path.split(shotPath)[0]
	jobDataDir = os.path.join(jobPath, os.environ['DATAFILESRELATIVEDIR'])
	shotDataDir = os.path.join(shotPath, os.environ['DATAFILESRELATIVEDIR'])

	if not os.path.isdir(jobDataDir):
		valid = False
		#verbose.settingsData_notFound('Job', jobDataDir)

	if not os.path.isdir(shotDataDir):
		valid = False
		#verbose.settingsData_notFound('Shot', shotDataDir)

	return valid

