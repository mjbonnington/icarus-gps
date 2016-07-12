#!/usr/bin/python

# [Icarus] openDirs.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Contains functions to open certain directories in the system's file explorer application.


import os


# Set correct command for operating system's file explorer
if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
	sysCommand = 'explorer'
elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
	sysCommand = 'open'
else:
	sysCommand = 'nautilus'


def open_(path_):
	""" Open the OS native file explorer at the specified directory.
	"""
	path_ = os.path.normpath(path_)
	if os.path.isdir(path_):
		if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
			os.startfile(path_)
		else:
			os.system( '%s %s' % (sysCommand, path_) )
	return


# Preset functions...
def openShot():
	open_( os.environ['SHOTPATH'] )

def openJob():
	open_( os.path.split(os.environ['JOBPATH'])[0] )

def openElementsLib():
	open_( os.environ['ELEMENTSLIBRARY'] )

def openMaya():
	open_( os.environ['MAYADIR'] )

def openMayaScenes():
	open_( os.environ["MAYASCENESDIR"] )

def openMayaSourceimages():
	open_( os.environ["MAYASOURCEIMAGESDIR"] )

def openMayaRenders():
	open_( os.environ["MAYARENDERSDIR"] )

def openMayaPlayblasts():
	open_( os.environ["MAYAPLAYBLASTSDIR"] )

def openNuke():
	open_( os.environ['NUKEDIR'] )

def openNukeScripts():
	open_( os.environ['NUKESCRIPTSDIR'] )

def openNukeElements():
	open_( os.environ['NUKEELEMENTSDIR'] )

def openNukeRenders():
	open_( os.environ['NUKERENDERSDIR'] )

def openRealflowScenes():
	open_( os.environ['REALFLOWSCENESDIR'] )

