#!/usr/bin/python

# [Icarus] icarus__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Initialise main pipeline environment.


import os
import platform
import sys


def set_env():
	""" Set some environment variables for basic operation.
	"""
	# Set version string
	os.environ['IC_VERSION'] = "v0.10.0-20191213"

	# Set vendor strings
	os.environ['IC_VENDOR'] = "Gramercy Park Studios"
	os.environ['IC_VENDOR_INITIALS'] = "GPS"

	# Standardise some environment variables across systems.
	# Usernames will always be stored as lowercase for compatibility.
	if platform.system() == "Windows":  # Windows
		os.environ['IC_RUNNING_OS'] = "Windows"
		if 'IC_USERNAME' not in os.environ:
			os.environ['IC_USERNAME'] = os.environ['USERNAME'].lower()
		os.environ['IC_USERHOME'] = os.environ['USERPROFILE']
	elif platform.system() == "Darwin":  # Mac OS
		os.environ['IC_RUNNING_OS'] = "MacOS"
		if 'IC_USERNAME' not in os.environ:
			os.environ['IC_USERNAME'] = os.environ['USER'].lower()
		os.environ['IC_USERHOME'] = os.environ['HOME']
	else:  # Linux
		os.environ['IC_RUNNING_OS'] = "Linux"
		if 'IC_USERNAME' not in os.environ:
			os.environ['IC_USERNAME'] = os.environ['USER'].lower()
		os.environ['IC_USERHOME'] = os.environ['HOME']

	# Check for environment awareness
	try:
		os.environ['IC_ENV']
	except KeyError:
		os.environ['IC_ENV'] = "STANDALONE"

	# Hard-coded relative data directories required by Icarus
	os.environ['IC_SHOTSDIR'] = "Vfx"  # Store in global / job settings
	os.environ['IC_METADATA'] = ".icarus"  # Where Icarus stores its metadata
	os.environ['IC_ASSETDIR'] = "assets"  # Where published assets are stored

	# Set up basic paths
	icarusWorkingDir = os.path.dirname(os.path.realpath(__file__))
	os.environ['IC_WORKINGDIR'] = icarusWorkingDir
	os.environ['IC_BASEDIR'] = os.path.dirname(icarusWorkingDir)
	os.environ['IC_FORMSDIR'] = os.path.join(os.environ['IC_BASEDIR'], 'ui')
	os.environ['IC_CONFIGDIR'] = os.path.join(os.environ['IC_BASEDIR'], 'config')

	userprefs = 'server'
	if userprefs == 'server':  # User prefs stored on server
		os.environ['IC_USERPREFS'] = os.path.join(os.environ['IC_CONFIGDIR'], 'users', os.environ['IC_USERNAME'])
	elif userprefs == 'home':  # User prefs stored in user home folder
		os.environ['IC_USERPREFS'] = os.path.join(os.environ['IC_USERHOME'], os.environ['IC_METADATA'])

	os.environ['IC_RECENTFILESDIR'] = os.path.join(os.environ['IC_USERPREFS'], 'recentfiles')

	append_sys_paths()


def append_sys_paths():
	""" Add paths for custom modules.
		Only add the UI/forms dir so that Qt.py, ui_template.py, compiled UI
		files and resources can be loaded without using relative imports.
	"""
	pathsToAppend = [
		os.environ['IC_FORMSDIR'], 
	]

	# Append paths
	for path in pathsToAppend:
		sys.path.append(path)
