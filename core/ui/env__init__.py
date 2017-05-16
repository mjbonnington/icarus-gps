#!/usr/bin/python

# [Icarus] env__init__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Initialises main pipeline environment.


import os
import platform
import sys


def setEnv():
	""" Set some environment variables for basic operation.
	"""
	# Set version string
	os.environ['ICARUSVERSION'] = 'v0.9.8-20170516'

	# Standardise some environment variables across systems
	if platform.system() == 'Windows':
		os.environ['ICARUS_RUNNING_OS'] = 'Windows'
		os.environ['HOME'] = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'])
	elif platform.system() == 'Darwin':
		os.environ['ICARUS_RUNNING_OS'] = 'Darwin'
		os.environ['USERNAME'] = os.environ['USER']
	else:
		os.environ['ICARUS_RUNNING_OS'] = 'Linux'

	# Check for environment awareness
	try:
		os.environ['ICARUSENVAWARE']
	except KeyError:
		os.environ['ICARUSENVAWARE'] = 'STANDALONE'

	# Set up basic paths
	icarusWorkingDir = os.path.dirname(os.path.realpath(__file__))
	icarusUIDir = os.path.join('core', 'ui')
	os.environ['ICWORKINGDIR'] = icarusWorkingDir
	os.environ['PIPELINE'] = icarusWorkingDir.replace(icarusUIDir, '')
	os.environ['ICCONFIGDIR'] = os.path.join(os.environ['PIPELINE'], 'core', 'config')
	os.environ['ICUSERPREFS'] = os.path.join(os.environ['ICCONFIGDIR'], 'users', os.environ['USERNAME']) # User prefs stored on server
	#os.environ['ICUSERPREFS'] = os.path.join(os.environ['HOME'], '.icarus') # User prefs stored in user home folder

	# Hard-coded relative data directories required by Icarus
	#os.environ['JOBSROOTRELATIVEDIR'] = 'Project_Media' # Store in global settings? UPDATE: now stored in jobs.xml
	os.environ['SHOTSROOTRELATIVEDIR'] = 'Vfx' # Store in global / job settings?
	os.environ['DATAFILESRELATIVEDIR'] = '.icarus'

	appendSysPaths()


def appendSysPaths():
	""" Add paths for custom modules.
	"""
	libs = os.path.join(os.environ['PIPELINE'], 'core', 'libs')
	tools = os.path.join(os.environ['PIPELINE'], 'core', 'tools')
	vendor = os.path.join(os.environ['PIPELINE'], 'core', 'vendor')

	pathsToAppend = [vendor] # Was [os.environ['PIPELINE'], vendor]

	# Add subdirectories in libs and tools directories
	for path in [libs, tools]:
		subdirs = next(os.walk(path))[1]
		if subdirs:
			for subdir in subdirs:
				if not subdir.startswith('.'): # Ignore directories that start with a dot
					pathsToAppend.append(os.path.join(path, subdir))

	# Append paths
	for path in pathsToAppend:
		# print(path)
		sys.path.append(path)

