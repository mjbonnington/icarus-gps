#!/usr/bin/python

# Recent Files
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Manage recent file lists for various applications within the pipeline.
# updateLs() and getLs() are the publicly accessible functions.


from ConfigParser import SafeConfigParser
import os
import osOps, verbose


config = SafeConfigParser()
configFile = os.path.join(os.environ['RECENTFILESDIR'], '%s.ini' % os.environ['JOB'])


def _read(env):
	""" Read config file - create it if it doesn't exist
	"""
	if os.path.exists(configFile):
		config.read(configFile)

	else:
		_create(env)


def _write():
	""" Write config file to disk
	"""
	try:
		with open(configFile, 'w') as f:
			config.write(f)

	except IOError:
		verbose.recentFiles_notWritten()


def _create(env):
	""" Create config file if it doesn't exist and populate with with defaults
	"""
	recentFilesDir = os.environ['RECENTFILESDIR']

	if not os.path.isdir(recentFilesDir):
		osOps.createDir(recentFilesDir)
	if not config.has_section(os.environ['SHOT']): # create shot section if it doesn't exist
		config.add_section(os.environ['SHOT'])
	if not config.has_option(os.environ['SHOT'], env): # create current app option if it doesn't exist
		config.set(os.environ['SHOT'], env, '')

	_write()


def updateLs(newEntry, env=os.environ['ICARUSENVAWARE']):
	""" Update recent files list and save config file to disk
	"""
	_read(env)
	_create(env) # create section for the current shot

	fileLs = [] # clear recent file list

	if newEntry.startswith(os.environ['SHOTPATH']): # only add files in the current shot
		newEntry = newEntry.replace(os.environ['SHOTPATH'], '')

		fileStr = config.get(os.environ['SHOT'], env)

		if not fileStr=='':
			fileLs = fileStr.split('; ')
		else:
			fileLs = []

		if newEntry in fileLs: # if the entry already exists in the list, delete it
			fileLs.remove(newEntry)

		fileLs.insert(0, newEntry) # prepend entry to the list

		while len(fileLs) > 10: # limit list to ten entries - currently hard-coded, but could be saved in user prefs?
			fileLs.pop()

		config.set(os.environ['SHOT'], env, '; '.join(n for n in fileLs))

		_write()


def getLs(env=os.environ['ICARUSENVAWARE']):
	""" Read recent file list and return list/array to be processed by MEL
	"""
	_read(env)
	_create(env) # create section for the current shot

	try:
		fileLs = config.get(os.environ['SHOT'], env).split('; ')
	except:
		fileLs = []

	return fileLs
