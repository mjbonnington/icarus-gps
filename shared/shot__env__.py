#!/usr/bin/python

# [Icarus] shot__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Set up shot-related environment variables.

import os
import sys

from . import appPaths
from . import os_wrapper
from . import pDialog
from . import settings_data_xml
from . import verbose


def set_env(job, shot, shot_path):
	""" Set job and shot environment variables.
	"""

	def getInheritedValue(category, setting):
		""" First try to get the value from the shot data, if it returns
			nothing then look in job data instead.
		"""
		value = shot_data.getValue(category, setting)
		if value is None:
			value = job_data.getValue(category, setting)
			# if value is None:
			# 	value = default_data.getValue(category, setting)

		#return value

		# Return an empty string, not None, so value can be stored in an
		# environment variable without raising an error
		if value is None:
			return ""
		else:
			return str(value)


	# def getAppExecPath(app):
	# 	""" Return the path to the executable for the specified app on the
	# 		current OS.
	# 	"""
	# 	# Set OS identifier strings to get correct app executable paths
	# 	if os.environ['IC_RUNNING_OS'] == "Windows":
	# 		currentOS = "win"
	# 	elif os.environ['IC_RUNNING_OS'] == "MacOS":
	# 		currentOS = "osx"
	# 	elif os.environ['IC_RUNNING_OS'] == "Linux":
	# 		currentOS = "linux"

	# 	return app_paths.getPath(app, getInheritedValue('apps', app), currentOS)


	def parseVersion(v_str):
		""" Parse version string and return a 3-tuple containing the major,
			minor and point version as integers.
		"""
		try:
			version = v_str.rsplit('-')[0]  # Strip date from version number
			v_split = version.lstrip('v').split('.')
			v_major = int(v_split[0])
			v_minor = int(v_split[1])
			v_point = int(v_split[2])
			return v_major, v_minor, v_point

		except (ValueError, KeyError):
			verbose.warning("Could not parse version string.")
			return None


	job_path = os.path.split(shot_path)[0]
	job_data_path = os.path.join(job_path, os.environ['IC_METADATA'])
	shot_data_path = os.path.join(shot_path, os.environ['IC_METADATA'])

	# Set basic environment variables
	os.environ['IC_JOB'] = job
	os.environ['IC_SHOT'] = shot
	os.environ['IC_JOBPATH'] = os_wrapper.absolutePath(job_path)
	os.environ['IC_SHOTPATH'] = os_wrapper.absolutePath(shot_path)
	os.environ['IC_JOBDATA'] = os_wrapper.absolutePath(job_data_path)
	os.environ['IC_SHOTDATA'] = os_wrapper.absolutePath(shot_data_path)

	os_wrapper.createDir(os.environ['IC_JOBDATA'])

	# Instantiate job / shot settings classes
	job_data = settings_data_xml.SettingsData()
	shot_data = settings_data_xml.SettingsData()
	#default_data = settings_data_xml.SettingsData()
	app_paths = appPaths.AppPaths()

	# Load data
	job_data.loadXML(os.path.join(job_data_path, 'jobData.xml'), use_template=False)
	shot_data.loadXML(os.path.join(shot_data_path, 'shotData.xml'), use_template=False)
	#default_data.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'defaultData.xml'))
	app_paths.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), use_template=True)

	os.environ['IC_ASSETDIR'] = 'assets'

	# Check if the job is using the correct Icarus version
	v_current = parseVersion(os.environ['IC_VERSION'])
	icVersion = job_data.getValue('meta', 'icVersion')
	if icVersion:
		v_required = parseVersion(icVersion)
	else:
		v_required = (0, 9, 12)  # last incompatible version

	if v_required[:-1] != v_current[:-1]:  # don't compare point version
		v_str = "v%d.%d.%d" % v_required
		msg = "This job requires version %s of Icarus. You're currently running %s" % (v_str, os.environ['IC_VERSION'])
		verbose.warning(msg)
		dialog = pDialog.dialog()
		title = "Incompatible Version"
		# msg += "\n\nDo you want to continue?"
		# msg += "\n\nYou have two options:"
		# msg += "\n\nRestart with Icarus %s" % v_str
		# msg += "\n\nUpgrade the job for compatibility with the latest version"

		cwd = os.environ.get('IC_MULTIVERSION', None)
		if cwd:
			msg += "\n\nDo you want to restart with Icarus %s?" % v_str
			if dialog.display(msg, title):
				# TODO: give the option to restart Icarus with the correct version,
				# or attempt to upgrade the project for compatibility.
				# job_data.setValue('meta', 'icVersion', os.environ['IC_VERSION'])
				# job_data.saveXML()
				exec_str = os.path.join(cwd, v_str, 'run.py')
				flags = " -j %s -s %s" % (job, shot)
				verbose.print_(exec_str+flags)
				subprocess.call(exec_str+flags, shell=True)
				sys.exit()
			else:
				return False


	# Terminal / Command Prompt
	if os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['IC_SHELL_RC'] = os_wrapper.absolutePath('$IC_WORKINGDIR/shell_cmd.bat')
	else:
		os.environ['IC_SHELL_RC'] = os_wrapper.absolutePath('$IC_WORKINGDIR/shell_rc')

	# Job / shot env
	#os.environ['IC_GLOBALPUBLISHDIR']  = os_wrapper.absolutePath(getInheritedValue('other', 'assetlib'))  # Path needs to be translated for OS portability
	os.environ['IC_JOBPUBLISHDIR'] = os_wrapper.absolutePath('$IC_JOBPATH/$IC_ASSETDIR')
	os.environ['IC_SHOTPUBLISHDIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/$IC_ASSETDIR')
	os.environ['IC_WIPS_DIR'] = os_wrapper.absolutePath('$IC_JOBPATH/../Deliverables/WIPS')  # Perhaps this shouldn't be hard-coded?
	os.environ['IC_ELEMENTS_LIBRARY'] = os_wrapper.absolutePath(getInheritedValue('other', 'elementslib'))  # Path needs to be translated for OS portability
	os.environ['IC_PRODUCTION_BOARD'] = getInheritedValue('other', 'prodboard')
	os.environ['IC_LINEAR_UNIT'] = getInheritedValue('units', 'linear')
	os.environ['IC_ANGULAR_UNIT'] = getInheritedValue('units', 'angle')
	os.environ['IC_TIME_UNIT'] = getInheritedValue('units', 'time')
	os.environ['IC_FPS'] = getInheritedValue('units', 'fps')
	os.environ['IC_STARTFRAME'] = getInheritedValue('time', 'rangeStart')
	os.environ['IC_ENDFRAME'] = getInheritedValue('time', 'rangeEnd')
	os.environ['IC_INFRAME'] = getInheritedValue('time', 'inFrame')
	os.environ['IC_OUTFRAME'] = getInheritedValue('time', 'outFrame')
	os.environ['IC_POSTER_FRAME'] = getInheritedValue('time', 'posterFrame')
	os.environ['IC_RESOLUTION_X'] = getInheritedValue('resolution', 'fullWidth')
	os.environ['IC_RESOLUTION_Y'] = getInheritedValue('resolution', 'fullHeight')
	os.environ['IC_PROXY_RESOLUTION_X'] = getInheritedValue('resolution', 'proxyWidth')
	os.environ['IC_PROXY_RESOLUTION_Y'] = getInheritedValue('resolution', 'proxyHeight')
	os.environ['IC_ASPECT_RATIO'] = str(float(os.environ['IC_RESOLUTION_X']) / float(os.environ['IC_RESOLUTION_Y']))
	# os.environ['IC_EDITOR'] = getAppExecPath('SublimeText')  # Make dynamic 

	return True
