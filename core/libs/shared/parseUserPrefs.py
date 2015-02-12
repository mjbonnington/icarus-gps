#!/usr/bin/python
#support	:Mike Bonnington - mike.bonnington@gps-ldn.com
#title     	:parseUserPrefs
#copyright	:Gramercy Park Studios


from ConfigParser import SafeConfigParser
import os, env__init__

config = SafeConfigParser()
#configFile = '/Users/mikebonnington/Documents/Scripts/icarus/core/config/users/mikebonnington/userPrefs.ini'
configFile = os.path.join(os.environ['ICUSERPREFS'], 'userPrefs.ini')
config.read(configFile)

def create():
	if not os.path.exists(configFile):
		config.add_section('main')
		config.set('main', 'lastjob', '')
		config.set('main', 'minimiseonlaunch', 'True')

		write()


def edit(key, value):
	config.set('main', key, value)

	write()


def write():
	with open(configFile, 'w') as f:
		config.write(f)


def read(key):
	config.read(configFile)

	return config.get('main', key)

