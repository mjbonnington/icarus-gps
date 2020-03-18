#!/usr/bin/python

# [renderqueue] rq__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019-2020
#
# Initialise Render Queue environment.


import getpass
import os
#import platform


def set_env():
	""" Set some environment variables for basic operation.
	"""
	os.environ['RQ_USER_PREFS_DIR'] = os.environ.get('IC_USERPREFS', os.path.expanduser('~/.renderqueue'))
	os.environ['RQ_VENDOR'] = os.environ.get('IC_VENDOR', 'MB3D')
	os.environ['RQ_VENDOR_INITIALS'] = os.environ.get('IC_VENDOR_INITIALS', 'MJB')
	os.environ['RQ_USER'] = os.environ.get('IC_USERNAME', getpass.getuser())
	os.environ['RQ_APP'] = os.environ.get('IC_ENV', 'None')

	os.environ['RQ_JOB'] = os.environ.get('IC_JOB', '')
	os.environ['RQ_SHOT'] = os.environ.get('IC_SHOT', '')
	# os.environ['RQ_JOBPATH'] = os.environ['IC_JOBPATH']
	# os.environ['RQ_SHOTPATH'] = os.environ['IC_SHOTPATH']
	os.environ['RQ_STARTFRAME'] = os.environ.get('IC_STARTFRAME', '1001')
	os.environ['RQ_ENDFRAME'] = os.environ.get('IC_ENDFRAME', '1100')

	# Deadline ---------------------------------------------------------------
	os.environ['RQ_DEADLINECOMMAND'] = os.environ.get('IC_DEADLINE_CMD_EXECUTABLE', 'deadlinecommand')
	os.environ['RQ_DEADLINEMONITOR'] = '"%s" -monitor' % os.environ.get('IC_DEADLINE_EXECUTABLE', '')

	# Maya -------------------------------------------------------------------
	v = os.environ.get('IC_MAYA_VERSION', '2018')
	os.environ['RQ_MAYA_VERSION'] = v
	os.environ['RQ_MAYA_SCENES_DIR'] = os.environ.get('IC_MAYA_SCENES_DIR', '.')
	os.environ['RQ_MAYA_PROJECT_DIR'] = os.environ.get('IC_MAYA_PROJECT_DIR', '.')

	os.environ['RQ_MAYA_OUTPUT_FORMAT'] = "<Scene>/<RenderLayer>/<Scene>.<RenderLayer>.<RenderPass>"
	os.environ['RQ_MAYA_OUTPUT_FORMAT_VRAY'] = "<Scene>/<Layer>/<Scene>.<Layer>"

	# Houdini ----------------------------------------------------------------
	v = os.environ.get('IC_HOUDINI_VERSION', '18.0')
	os.environ['RQ_HOUDINI_VERSION'] = '.'.join(v.split('.')[:2])  # Strip revision
	os.environ['RQ_HOUDINI_SCENES_DIR'] = os.environ.get('IC_HOUDINI_SCENES_DIR', '.')

	# Nuke -------------------------------------------------------------------
	v = os.environ.get('IC_NUKE_VERSION', '11.3')
	os.environ['RQ_NUKE_VERSION'] = v.split('v')[0]  # Strip revision
	os.environ['RQ_NUKE_SCRIPTS_DIR'] = os.environ.get('IC_NUKE_SCRIPTS_DIR', '.')


# def setenv():
# 	""" Set some environment variables for basic operation.
# 	"""
# 	# Set version string
# 	os.environ['RQ_VERSION'] = "0.2.0"

# 	# # Set vendor string
# 	# os.environ['RQ_VENDOR'] = "GPS"

# 	# Standardise some environment variables across systems.
# 	# Usernames will always be stored as lowercase for compatibility.
# 	if platform.system() == "Windows":  # Windows
# 		#os.environ['RQ_RUNNING_OS'] = "Windows"
# 		if not 'RQ_USERNAME' in os.environ:
# 			os.environ['RQ_USERNAME'] = os.environ['USERNAME'].lower()
# 		userHome = os.environ['USERPROFILE']
# 	elif platform.system() == "Darwin":  # Mac OS
# 		#os.environ['RQ_RUNNING_OS'] = "MacOS"
# 		if not 'RQ_USERNAME' in os.environ:
# 			os.environ['RQ_USERNAME'] = os.environ['USER'].lower()
# 		userHome = os.environ['HOME']
# 	else:  # Linux
# 		#os.environ['RQ_RUNNING_OS'] = "Linux"
# 		if not 'RQ_USERNAME' in os.environ:
# 			os.environ['RQ_USERNAME'] = os.environ['USER'].lower()
# 		userHome = os.environ['HOME']

# 	# Check for environment awareness
# 	try:
# 		os.environ['RQ_ENV']
# 	except KeyError:
# 		os.environ['RQ_ENV'] = "STANDALONE"

# 	# Set up basic paths
# 	os.environ['RQ_DATABASE'] = 'J:/rq_database'
# 	#os.environ['RQ_BASEDIR'] = os.getcwd()
# 	os.environ['RQ_CONFIGDIR'] = os.path.join(os.environ['RQ_DATABASE'], 'config')
# 	os.environ['RQ_USERPREFS'] = os.path.join(os.environ['RQ_CONFIGDIR'], 'users', os.environ['RQ_USERNAME'])  # User prefs stored on server
# 	#os.environ['RQ_USERPREFS'] = os.path.join(userHome, '.renderqueue')  # User prefs stored in user home folder
# 	os.environ['RQ_HISTORY'] = os.path.join(os.environ['RQ_USERPREFS'], 'history')

# 	appendSysPaths()
