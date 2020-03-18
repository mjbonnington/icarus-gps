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

# Import custom modules
from . import appPaths
from . import json_metadata as metadata
from . import os_wrapper
# from . import prompt
from . import verbose


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


def set_env(job, shot, job_path, shot_path):
	""" Set job and shot environment variables.
	"""

	def getInheritedValue(category, setting):
		""" First try to get the value from the shot data, if it returns
			nothing then look in job data instead.
		"""
		value = shot_data.get_attr(category, setting)
		if value is None:
			value = job_data.get_attr(category, setting)

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


	job_path = os_wrapper.absolutePath('%s/$IC_SHOTSDIR' % job_path)  # append 'vfx'
	shot_path = os_wrapper.absolutePath(shot_path)
	job_datafile = os_wrapper.absolutePath('%s/$IC_METADATA/job_data.json' % job_path)
	shot_datafile = os_wrapper.absolutePath('%s/$IC_METADATA/shot_data.json' % shot_path)

	# Create directory for job metadata
	job_data_dir = os.path.dirname(job_datafile)
	shot_data_dir = os.path.dirname(shot_datafile)
	if not os.path.isdir(job_data_dir):
		os_wrapper.createDir(job_data_dir)

	# Set basic environment variables
	os.environ['IC_JOB'] = job
	os.environ['IC_SHOT'] = shot
	os.environ['IC_JOBPATH'] = job_path
	os.environ['IC_SHOTPATH'] = shot_path
	os.environ['IC_JOBDATA'] = job_datafile
	os.environ['IC_SHOTDATA'] = shot_datafile

	# Instantiate job / shot settings classes
	job_data = metadata.Metadata()
	shot_data = metadata.Metadata()
	app_paths = appPaths.AppPaths()

	# Load data
	job_data_loaded = job_data.load(job_datafile)
	shot_data_loaded = shot_data.load(shot_datafile)
	app_paths.loadXML(
		os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), 
		use_template=True)

	# # Load legacy metadata ---------------------------------------------------
	# if not job_data_loaded:
	# 	from . import legacy_metadata
	# 	xml_datafile = os.path.join(job_data_dir, 'jobData.xml')
	# 	py_datafile = os.path.join(job_data_dir, 'jobData.py')
	# 	job_data_loaded, job_data = legacy_metadata.loadLegacyMetadata(xml_datafile, py_datafile, 'IC_JOBDATA')

	# if not shot_data_loaded:
	# 	from . import legacy_metadata
	# 	xml_datafile = os.path.join(shot_data_dir, 'shotData.xml')
	# 	py_datafile = os.path.join(shot_data_dir, 'shotData.py')
	# 	shot_data_loaded, shot_data = legacy_metadata.loadLegacyMetadata(xml_datafile, py_datafile, 'IC_SHOTDATA')
	# # ------------------------------------------------------------------------

	verbose.debug("%s job data loaded: %s, %s shot data loaded: %s" % (job, job_data_loaded, shot, shot_data_loaded))
	# if (not job_data_loaded) or (not shot_data_loaded):
	if job_data_loaded:
		if not shot_data_loaded:
			pass
			# print "Create empty shot data"
	else:  # No job data - open job settings
		return False

	# ------------------------------------------------------------------------

	# # Check if the job is using the correct Icarus version
	# v_current = parseVersion(os.environ['IC_VERSION'])
	# icversion = job_data.get_attr('other', 'icversion')
	# if icversion:
	# 	v_required = parseVersion(icversion)
	# else:
	# 	v_required = (0, 9, 12)  # last incompatible version

	# if v_required[:-1] != v_current[:-1]:  # don't compare point versions
	# 	v_str = "v%d.%d.%d" % v_required
	# 	msg = "This job requires version %s of Icarus. You're currently running %s" % (v_str, os.environ['IC_VERSION'])
	# 	verbose.warning(msg)
	# 	dialog = prompt.Dialog()
	# 	title = "Incompatible Version"

	# 	# The IC_MULTIVERSION env var is set if icarus is running from a
	# 	# multi-version environment. This enables Icarus to spawn itself as a
	# 	# different version for maximum compatibility with lder jobs.
	# 	cwd = os.environ.get('IC_MULTIVERSION', None)
	# 	if cwd:
	# 		msg += "\n\nDo you want to restart with Icarus %s?" % v_str
	# 		if dialog.display(msg, title):
	# 			# TODO: give the option to restart Icarus with the correct version,
	# 			# or attempt to upgrade the project for compatibility.
	# 			# job_data.set_attr('other', 'icversion', os.environ['IC_VERSION'])
	# 			# job_data.save()
	# 			exec_str = os.path.join(cwd, v_str, 'run.py')
	# 			flags = " -j %s -s %s" % (job, shot)
	# 			verbose.print_(exec_str+flags)
	# 			# import subprocess
	# 			# subprocess.call(exec_str+flags, shell=True)
	# 			# sys.exit()
	# 		else:
	# 			return False
	# 	else:
	# 		msg += "\n\nDo you want to upgrade the job for compatibility with the latest version?"
	# 		msg += "\n\nWarning: This might break paths which will need to be relinked manually. This operation cannot be undone."
	# 		if dialog.display(msg, title):
	# 			print "UPGRADE JOB"
	# 		else:
	# 			return False

	# ------------------------------------------------------------------------

	# Terminal / Command Prompt
	if os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['IC_SHELL_RC'] = os_wrapper.absolutePath('$IC_COREDIR/shell_cmd.bat')
	else:
		os.environ['IC_SHELL_RC'] = os_wrapper.absolutePath('$IC_COREDIR/shell_rc')

	# Job / shot env
	# os.environ['IC_ASSETDIR'] = 'assets'
	#os.environ['IC_GLOBALPUBLISHDIR']  = os_wrapper.absolutePath(getInheritedValue('other', 'assetlib'))  # Path needs to be translated for OS portability
	os.environ['IC_JOBPUBLISHDIR'] = os_wrapper.absolutePath('$IC_JOBPATH/$IC_ASSETDIR')
	os.environ['IC_SHOTPUBLISHDIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/$IC_ASSETDIR')
	# os.environ['IC_WIPS_DIR'] = os_wrapper.absolutePath('$IC_JOBPATH/../Deliverables/WIPS')  # Perhaps this shouldn't be hard-coded?
	os.environ['IC_WIPS_DIR'] = os_wrapper.absolutePath(getInheritedValue('other', 'wipsdir'))
	os.environ['IC_ELEMENTS_LIBRARY'] = os_wrapper.absolutePath(getInheritedValue('other', 'elementslib'))  # Path needs to be translated for OS portability
	os.environ['IC_PRODUCTION_BOARD'] = getInheritedValue('other', 'prodboard')
	os.environ['IC_LINEAR_UNIT'] = getInheritedValue('units', 'linear')
	os.environ['IC_ANGULAR_UNIT'] = getInheritedValue('units', 'angle')
	os.environ['IC_TIME_UNIT'] = getInheritedValue('units', 'time')
	os.environ['IC_FPS'] = getInheritedValue('units', 'fps')
	os.environ['IC_STARTFRAME'] = getInheritedValue('time', 'rangestart')
	os.environ['IC_ENDFRAME'] = getInheritedValue('time', 'rangeend')
	os.environ['IC_INFRAME'] = getInheritedValue('time', 'inframe')
	os.environ['IC_OUTFRAME'] = getInheritedValue('time', 'outframe')
	os.environ['IC_POSTER_FRAME'] = getInheritedValue('time', 'posterframe')
	os.environ['IC_RESOLUTION_X'] = getInheritedValue('resolution', 'fullwidth')
	os.environ['IC_RESOLUTION_Y'] = getInheritedValue('resolution', 'fullheight')
	os.environ['IC_PROXY_RESOLUTION_X'] = getInheritedValue('resolution', 'proxywidth')
	os.environ['IC_PROXY_RESOLUTION_Y'] = getInheritedValue('resolution', 'proxyheight')
	os.environ['IC_ASPECT_RATIO'] = str(float(os.environ['IC_RESOLUTION_X']) / float(os.environ['IC_RESOLUTION_Y']))
	# os.environ['IC_EDITOR'] = getAppExecPath('SublimeText')  # Make dynamic 

	return True
