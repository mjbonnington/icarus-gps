#!/usr/bin/python

# [Icarus] userPrefs.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Manages user preferences stored in .ini files via Python's ConfigParser
# module.


try:
	from ConfigParser import SafeConfigParser
except ModuleNotFoundError:  # Python 3 compatibility
	from configparser import SafeConfigParser

import os

import osOps
import verbose


config = SafeConfigParser()
configFile = os.path.join(os.environ['ICUSERPREFS'], 'userPrefs.ini')


def read():
	""" Read config file - create it if it doesn't exist.
	"""
	if os.path.exists(configFile):
		config.read(configFile)

	else:
		create()


def write():
	""" Write config file to disk.
	"""
	try:
		with open(configFile, 'w') as f:
			config.write(f)

	except IOError:
		verbose.warning('Unable to write user prefs configuration file.')


def create():
	""" Create config file if it doesn't exist and populate with with
		defaults.
	"""
	userPrefsDir = os.environ['ICUSERPREFS']

	if not os.path.exists(userPrefsDir):
		osOps.createDir(userPrefsDir)

	config.add_section('main')
	config.set('main', 'lastjob', '')
	config.set('main', 'numrecentfiles', '10')
	config.set('main', 'minimiseonlaunch', 'True')
	config.set('main', 'verbosity', '2')

	config.add_section('gpspreview')
	config.set('gpspreview', 'resolutionmode', '0')
	config.set('gpspreview', 'framerangemode', '0')
	config.set('gpspreview', 'offscreen', 'True')
	config.set('gpspreview', 'noselection', 'True')
	config.set('gpspreview', 'guides', 'True')
	config.set('gpspreview', 'slate', 'True')
	config.set('gpspreview', 'launchviewer', 'True')
	config.set('gpspreview', 'createqt', 'False')

	write()


def edit(section, key, value):
	""" Set a value and save config file to disk.
		If the section doesn't exist it will be created.
	"""
	if not config.has_section(section):
		config.add_section(section)

	config.set(section, key, value)

	write()

