#!/usr/bin/python

# [Icarus] recentFiles.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Manage recent file lists for various applications within the pipeline.
# updateLs() and getLs() are the publicly accessible functions.


try:
	from ConfigParser import SafeConfigParser
except ModuleNotFoundError:  # Python 3 compatibility
	from configparser import SafeConfigParser

import os

import osOps
import verbose


config = SafeConfigParser()
configFile = os.path.join(os.environ['RECENTFILESDIR'], '%s.ini' % os.environ['JOB'])


def _read(env):
	""" Read config file - create it if it doesn't exist.
	"""
	if os.path.exists(configFile):
		config.read(configFile)

	else:
		_create(env)


def _write():
	""" Write config file to disk.
	"""
	try:
		with open(configFile, 'w') as f:
			config.write(f)

	except IOError:
		verbose.recentFiles_notWritten()


def _create(env):
	""" Create config file if it doesn't exist and populate with with
		defaults.
	"""
	recentFilesDir = os.environ['RECENTFILESDIR']

	if not os.path.isdir(recentFilesDir):
		osOps.createDir(recentFilesDir)
	if not config.has_section(os.environ['SHOT']): # create shot section if it doesn't exist
		config.add_section(os.environ['SHOT'])
	if not config.has_option(os.environ['SHOT'], env): # create current app option if it doesn't exist
		config.set(os.environ['SHOT'], env, '')

	_write()


def updateLs(newEntry, env=os.environ['IC_ENV']):
	""" Update recent files list and save config file to disk.
	"""
	_read(env)
	_create(env) # create section for the current shot

	fileLs = [] # clear recent file list

	#newEntry = osOps.absolutePath(newEntry) # normalise path for host os
	newEntry = newEntry.replace('\\', '/')
	shotpath = os.environ['SHOTPATH'].replace('\\', '/')

	if newEntry.startswith(shotpath): # only add files in the current shot
		newEntry = newEntry.replace(shotpath, '')

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

		config.set(os.environ['SHOT'], env, '; '.join(n for n in fileLs)) # encode the list into a single line with entries separated by semicolons

		_write()

	else:
		verbose.warning("Entry '%s' could not be added to recent files list. (%s)" %(newEntry, shotpath))


def getLs(env=os.environ['IC_ENV']):
	""" Read recent file list and return list/array to be processed by MEL.
	"""
	_read(env)
	_create(env) # create section for the current shot

	try:
		fileLs = config.get(os.environ['SHOT'], env).split('; ')
	except:
		fileLs = []

	return fileLs

