#!/usr/bin/python

# [GPS] hiero__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Sets up Hiero environment at startup.


import os
import sys
import hiero.core as hc

# Just like Nuke, Hiero seems to ditch the main root environment where it has
# been called from so the path needs to be appended again.
sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'core', 'run'))
from core import env__init__
env__init__.append_sys_paths()

from shared import os_wrapper
# from shared import verbose


# def removeAutoSave():
# 	""" Remove autosave of project if it exists.
# 	"""
# 	autosave_filename = os_wrapper.absolutePath("$IC_HIERO_EDITORIAL_DIR/$IC_JOB.hrox.autosave")
# 	if os.path.isfile(autosave_filename):
# 		os_wrapper.remove(autosave_filename)


def loadDailies(dailies_categories=['CGI', 'Flame', 'Edit']):
	"""	Load or create project and import dailies.
	"""
	filename = os_wrapper.absolutePath("$IC_HIERO_EDITORIAL_DIR/$IC_JOB.hrox")

	if os.path.isfile(filename):
		hiero_project = hc.openProject(filename)

	else:
		# Create a new project
		hiero_project = hc.newProject()
		clipsBin = hiero_project.clipsBin()

		# Create some bins & attach to the project
		for cat in dailies_categories:
			_bin = hc.Bin(cat)
			clipsBin.addItem(_bin)

		# hiero_project.saveAs(filename)

	for cat in dailies_categories:
		_bin = hc.findItemsInProject(hiero_project, hc.Bin, cat, verbose=0)[0]
		_path = os.path.join(os.environ['IC_WIPS_DIR'], cat)
		loadItems(_path, _bin, emptyBin=True)


def loadItems(path, _bin, emptyBin=True):
	print "Processing bin: %s" %_bin

	# Empty bin
	if emptyBin:
		bin_contents = _bin.items()
		for item in bin_contents:
			_bin.removeItem(item)
			print "Deleted %s" %item

	# Detect if directories exist. Create if not
	if os.path.isdir(path):
		# Add path contents to bin if directory exists
		itemsLs = os.listdir(path)
		itemsLs = sorted(itemsLs, reverse=True)
		for item in itemsLs:
			itemPath = os.path.join(path, item)
			if os.path.isdir(itemPath):
				_bin.importFolder(itemPath)
				print "Imported %s" %itemPath

	else:
		os_wrapper.createDir(path)


# removeAutoSave()
loadDailies()


#------
# import os
# import hiero.core as hc
# wipsProject = hc.newProject()
# clipsBin = wipsProject.clipsBin()
# clipsBin.importFolder(os.environ['IC_WIPS_DIR'])

