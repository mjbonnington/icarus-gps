#!/usr/bin/python

# [Icarus] defaultDirs.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Creates user specific directories for shot work.


import os
import osOps


def create():
	""" Creates user specific directories for shot work.
	"""
	username = os.environ['USERNAME']

	# Maya
	for directory in ('scenes', 'playblasts', 'sourceimages', 'renders', 'cache'):
		uDir = os.path.join(os.environ['MAYADIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

		# Copy workspace.mel definition file into Maya project dir
		workspace_def = os.path.join(os.environ['MAYADIR'], 'workspace.mel')
		if not os.path.isfile(workspace_def):
			src = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'templates', 'workspace.mel')
			osOps.copy(src, workspace_def)

	# Mudbox
	for directory in ('scenes', 'models', 'sourceimages'):
		uDir = os.path.join(os.environ['MUDBOXDIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	# Mari
	for directory in ('scenes', 'geo', 'sourceimages', 'textures', 'renders', 'archives'):
		uDir = os.path.join(os.environ['MARIDIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	# Photoscan
	#for directory in ('scenes', 'cameras', 'pointClouds', 'geometry', 'sourceImages'):
	#	uDir = os.path.join(os.environ['PHOTOSCANDIR'], directory, username)
	#	if not os.path.isdir(uDir):
	#		osOps.createDir(uDir)

	# Nuke
	for directory in ('scripts', 'elements', 'renders'):
		uDir = os.path.join(os.environ['NUKEDIR'], directory, username)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	# RealFlow
	for directory in ('.cmdsOrg', ): # Trailing comma required to make iterable, otherwise for loop will iterate over string, i.e. '.', 'c', 'm', 'd', etc.
		uDir = os.path.join(os.environ['REALFLOWSCENESDIR'], directory)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	# Plate directories
	plates = (os.environ['RESOLUTION'], os.environ['PROXY_RESOLUTION'])
	platesDir = os.path.join(os.environ['SHOTPATH'], 'Plate')
	if not os.path.isdir(platesDir):
		osOps.createDir(platesDir)
	# Delete any pre-existing redundant plate directories that are empty
	for directory in os.listdir(platesDir):
		existingDir = os.path.join(platesDir, directory)
		if os.path.isdir(existingDir) and not os.listdir(existingDir):
			if directory not in plates:
				osOps.recurseRemove(existingDir)
	# Create plate directory named with resolution
	for directory in plates:
		plateDir = os.path.join(platesDir, directory)
		if not os.path.isdir(plateDir):
			osOps.createDir(plateDir)

	# Published assets
	for directory in (os.environ['JOBAPPROVEDPUBLISHDIR'], os.environ['SHOTAPPROVEDPUBLISHDIR'], os.environ['JOBPUBLISHDIR'], os.environ['SHOTPUBLISHDIR']):
		if not os.path.isdir(directory):
			osOps.createDir(directory)

