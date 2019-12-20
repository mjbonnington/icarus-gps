#!/usr/bin/python

# [Icarus] icarus__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Initialise main pipeline environment and set global configuration.


import json
import os
import platform
import sys


def set_env():
	""" Set some environment variables for basic operation.
	"""
	# Set version string
	os.environ['IC_VERSION'] = "v0.10.0-20191220"

	# Set vendor strings
	os.environ['IC_VENDOR'] = "Gramercy Park Studios"
	os.environ['IC_VENDOR_INITIALS'] = "GPS"

	# Standardise some environment variables across systems.
	# Usernames will always be stored as lowercase for compatibility.
	if platform.system() == "Windows":  # Windows
		os.environ['IC_RUNNING_OS'] = "Windows"
		os.environ['IC_USERHOME'] = os.environ['USERPROFILE']
		username = os.environ['USERNAME']
	elif platform.system() == "Darwin":  # Mac OS
		os.environ['IC_RUNNING_OS'] = "MacOS"
		os.environ['IC_USERHOME'] = os.environ['HOME']
		username = os.environ['USER']
	else:  # Linux
		os.environ['IC_RUNNING_OS'] = "Linux"
		os.environ['IC_USERHOME'] = os.environ['HOME']
		username = os.environ['USER']

	if 'IC_USERNAME' not in os.environ:
		os.environ['IC_USERNAME'] = username.lower()

	# Check for environment awareness
	try:
		os.environ['IC_ENV']
	except KeyError:
		os.environ['IC_ENV'] = "STANDALONE"

	# Set up basic paths
	core_working_dir = os.path.dirname(os.path.realpath(__file__))
	os.environ['IC_COREDIR'] = core_working_dir
	os.environ['IC_BASEDIR'] = os.path.dirname(core_working_dir)
	os.environ['IC_FORMSDIR'] = os.path.join(os.environ['IC_BASEDIR'], 'ui')
	if 'IC_CONFIGDIR' not in os.environ:
		os.environ['IC_CONFIGDIR'] = os.path.join(os.environ['IC_BASEDIR'], 'config')

	# Attempt to load global prefs
	prefsfile = os.path.join(os.environ['IC_CONFIGDIR'], 'icarus_globals.json')
	if os.path.isfile(prefsfile):
		# Load prefs and set defaults
		with open(prefsfile, 'r') as f:
			prefs = json.load(f)

	else:
		# Create empty prefs dir, display global settings settings dialog
		prefs = {}
		os.environ['IC_FIRSTRUN'] = "True"
		if not os.path.isdir(os.environ['IC_CONFIGDIR']):
			os.makedirs(os.environ['IC_CONFIGDIR'])

	os.environ['IC_METADATA'] = prefs.get('global.metadata', ".icarus")
	os.environ['IC_SHOTSDIR'] = prefs.get('global.shotsdir', "vfx")
	os.environ['IC_ASSETDIR'] = prefs.get('global.assetsdir', "assets")
	os.environ['IC_ASSETLIBRARY'] = prefs.get('global.assetlibrary', "")

	userprefs = prefs.get('global.userprefs')
	if userprefs == "Home folder":  # User prefs stored in user home folder
		os.environ['IC_USERPREFS'] = os.path.join(os.environ['IC_USERHOME'], os.environ['IC_METADATA'])
	else:  # User prefs stored on server
		os.environ['IC_USERPREFS'] = os.path.join(os.environ['IC_CONFIGDIR'], 'users', os.environ['IC_USERNAME'])
	if not os.path.isdir(os.environ['IC_USERPREFS']):
		os.makedirs(os.environ['IC_USERPREFS'])

	os.environ['IC_RECENTFILESDIR'] = os.path.join(os.environ['IC_USERPREFS'], 'recent')
	if not os.path.isdir(os.environ['IC_RECENTFILESDIR']):
		os.makedirs(os.environ['IC_RECENTFILESDIR'])

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
