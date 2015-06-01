#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :defaultDirs
#copyright  :Gramercy Park Studios

import os
import osOps

def create():
	""" Creates user specific directories for shot work
	"""
	username = os.environ['USERNAME']

	#maya
	for directory in ('scenes', 'playblasts', 'sourceimages', 'renders', 'cache'):
		uDir = os.path.join(os.environ['MAYADIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#mudbox
	for directory in ('scenes', 'models', 'sourceimages'):
		uDir = os.path.join(os.environ['MUDBOXDIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#mari
	for directory in ('scenes', 'geo', 'sourceimages', 'textures', 'renders', 'archives'):
		uDir = os.path.join(os.environ['MARIDIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#photoscan
	#for directory in ('scenes', 'cameras', 'pointClouds', 'geometry', 'sourceImages'):
	#	uDir = os.path.join(os.environ['PHOTOSCANDIR'], directory, username)
	#	if not os.path.isdir(uDir):
	#		osOps.createDir(uDir)

	#nuke
	for directory in ('scripts', 'elements', 'renders'):
		uDir = os.path.join(os.environ['NUKEDIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#realflow
	#for directory in ('.cmdsOrg'): # Something wrong here? Need to figure out what it should be
	#	uDir = '%s/%s' % (os.environ['REALFLOWSCENESDIR'], directory)
	#	if not os.path.isdir(uDir):
	#		osOps.createDir(uDir)

	#env
	for directory in (os.environ['JOBAPPROVEDPUBLISHDIR'], os.environ['SHOTAPPROVEDPUBLISHDIR'], os.environ['JOBPUBLISHDIR'], os.environ['SHOTPUBLISHDIR']):
		if not os.path.isdir(directory):
			#os.system('mkdir -p %s' % dir)
			osOps.createDir(directory)
