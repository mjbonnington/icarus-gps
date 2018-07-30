#!/usr/bin/python

# [Icarus] env__init__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# Initialises main pipeline environment.


import os
import platform
import sys


def setEnv():
	""" Set some environment variables for basic operation.
	"""
	# Set version string
	os.environ['IC_VERSION'] = "v0.9.13-20180730"

	# Standardise some environment variables across systems.
	# Usernames will always be stored as lowercase for compatibility.
	if platform.system() == "Windows":  # Windows
		os.environ['IC_RUNNING_OS'] = "Windows"
		if not 'IC_USERNAME' in os.environ:
			os.environ['IC_USERNAME'] = os.environ['USERNAME'].lower()
		os.environ['IC_USERHOME'] = os.environ['USERPROFILE']
	elif platform.system() == "Darwin":  # Mac OS
		os.environ['IC_RUNNING_OS'] = "MacOS"
		if not 'IC_USERNAME' in os.environ:
			os.environ['IC_USERNAME'] = os.environ['USER'].lower()
		os.environ['IC_USERHOME'] = os.environ['HOME']
	else:  # Linux
		os.environ['IC_RUNNING_OS'] = "Linux"
		if not 'IC_USERNAME' in os.environ:
			os.environ['IC_USERNAME'] = os.environ['USERNAME'].lower()
		os.environ['IC_USERHOME'] = os.environ['HOME']

	# Check for environment awareness
	try:
		os.environ['IC_ENV']
	except KeyError:
		os.environ['IC_ENV'] = "STANDALONE"

	# Hard-coded relative data directories required by Icarus
	os.environ['IC_SHOTSDIR'] = "vfx"  # Store in global / job settings
	os.environ['IC_METADATA'] = ".icarus"

	# Set up basic paths
	icarusWorkingDir = os.path.dirname(os.path.realpath(__file__))
	icarusRunDir = os.path.join('core', 'run')
	os.environ['IC_WORKINGDIR'] = icarusWorkingDir
	os.environ['IC_BASEDIR'] = icarusWorkingDir.replace(icarusRunDir, '')
	os.environ['IC_FORMSDIR'] = os.path.join(os.environ['IC_BASEDIR'], 'core', 'ui')
	os.environ['IC_CONFIGDIR'] = os.path.join(os.environ['IC_BASEDIR'], 'core', 'config')
	os.environ['IC_USERPREFS'] = os.path.join(os.environ['IC_CONFIGDIR'], 'users', os.environ['IC_USERNAME'])  # User prefs stored on server
	#os.environ['IC_USERPREFS'] = os.path.join(os.environ['IC_USERHOME'], os.environ['IC_METADATA'])  # User prefs stored in user home folder
	os.environ['IC_RECENTFILESDIR'] = os.path.join(os.environ['IC_USERPREFS'], 'recentFiles')

	appendSysPaths()


def appendSysPaths():
	""" Add paths for custom modules.
		Perhaps in the future we should re-structure the modules into
		packages to simplify this?
	"""
	libs = os.path.join(os.environ['IC_BASEDIR'], 'core', 'libs')
	tools = os.path.join(os.environ['IC_BASEDIR'], 'core', 'tools')
	forms = os.path.join(os.environ['IC_BASEDIR'], 'core', 'ui')
	vendor = os.path.join(os.environ['IC_BASEDIR'], 'core', 'vendor')

	pathsToAppend = [forms, vendor]  # Was [os.environ['IC_BASEDIR'], vendor]

	# Add subdirectories in libs and tools directories
	for path in [libs, tools]:
		subdirs = next(os.walk(path))[1]
		if subdirs:
			for subdir in subdirs:
				# Ignore directories that start with a dot
				if not subdir.startswith('.'):
					pathsToAppend.append(os.path.join(path, subdir))

	# Append paths
	for path in pathsToAppend:
		sys.path.append(path)

