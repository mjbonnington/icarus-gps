#!/usr/bin/python
#support	:Mike Bonnington - mike.bonnington@gps-ldn.com
#title     	:userPrefs
#copyright	:Gramercy Park Studios


from ConfigParser import SafeConfigParser
import os, env__init__

config = SafeConfigParser()
configFile = os.path.join(os.environ['ICUSERPREFS'], 'userPrefs.ini')
config.read(configFile)


def create():
	"""Create config file if it doesn't exist and populate with with defaults"""

	if not os.path.exists(configFile):
		config.add_section('main')
		config.set('main', 'lastjob', '')
		config.set('main', 'minimiseonlaunch', 'True')

		config.add_section('gpspreview')
		config.set('gpspreview', 'offscreen', 'True')
		config.set('gpspreview', 'noselection', 'True')
		config.set('gpspreview', 'guides', 'True')
		config.set('gpspreview', 'slate', 'True')
		config.set('gpspreview', 'launchviewer', 'True')
		config.set('gpspreview', 'createqt', 'False')

		write()


def edit(section, key, value):
	config.set(section, key, value)

	write()


def write():
	with open(configFile, 'w') as f:
		config.write(f)


def read():
	config.read(configFile)
