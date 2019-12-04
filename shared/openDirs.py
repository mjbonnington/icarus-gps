#!/usr/bin/python

# [Icarus] openDirs.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# Contains functions to open certain directories in the system's file explorer
# application.


import os


# Set correct command for operating system's file explorer
if os.environ['IC_RUNNING_OS'] == "Windows":
	sysCommand = "explorer"  # "start"
elif os.environ['IC_RUNNING_OS'] == "MacOS":
	sysCommand = "open"
else:  # Linux
	sysCommand = "nautilus"


def open_(path_):
	""" Open the OS native file explorer at the specified directory.
	"""
	path_ = os.path.normpath(path_)
	if os.path.isdir(path_):
		if os.environ['IC_RUNNING_OS'] == "Windows":
			os.startfile(path_)
		else:
			os.system('%s %s' %(sysCommand, path_))
	return


# Preset functions...
def openShot():
	open_(os.environ['IC_SHOTPATH'])

def openJob():
	open_(os.path.split(os.environ['IC_JOBPATH'])[0])

def openElementsLib():
	open_(os.environ['IC_ELEMENTS_LIBRARY'])

def openMaya():
	open_(os.environ['IC_MAYA_PROJECT_DIR'])

def openMayaScenes():
	open_(os.environ['IC_MAYA_SCENES_DIR'])

def openMayaSourceimages():
	open_(os.environ['IC_MAYA_SOURCEIMAGES_DIR'])

def openMayaRenders():
	open_(os.environ['IC_MAYA_RENDERS_DIR'])

def openMayaPlayblasts():
	open_(os.environ['IC_MAYA_PLAYBLASTS_DIR'])

def openNuke():
	open_(os.environ['IC_NUKE_PROJECT_DIR'])

def openNukeScripts():
	open_(os.environ['IC_NUKE_SCRIPTS_DIR'])

def openNukeElements():
	open_(os.environ['IC_NUKE_ELEMENTS_DIR'])

def openNukeRenders():
	open_(os.environ['IC_NUKE_RENDERS_DIR'])

def openRealflowScenes():
	open_(os.environ['IC_REALFLOW_SCENES_DIR'])

