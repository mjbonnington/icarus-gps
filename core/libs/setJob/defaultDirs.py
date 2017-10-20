#!/usr/bin/python

# [Icarus] defaultDirs.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Creates user specific directories for shot work.


import os
import osOps


def create(app=None):
	""" Creates user specific directories for shot work.
		TODO: The folder structure should be defined in a preference file and
		generated based on that.
	"""
	username = os.environ['IC_USERNAME']

	###################
	# Generic folders #
	###################

	if app is None:
		# Published assets
		for directory in (os.environ['JOBPUBLISHDIR'], os.environ['SHOTPUBLISHDIR']):
			if not os.path.isdir(directory):
				osOps.createDir(directory)

		# Plate directories
		res_full = "%sx%s" %(os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY'])
		res_proxy = "%sx%s" %(os.environ['PROXY_RESOLUTIONX'], os.environ['PROXY_RESOLUTIONY'])
		plates = (res_full, res_proxy)
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

	################################
	# App-specific project folders #
	################################

	elif app == 'Maya':
		for directory in ('scenes', 'playblasts', 'sourceimages', 'renders', ):
			uDir = os.path.join(os.environ['MAYADIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

		for directory in ('cache', 'data', 'scripts', ):
			nDir = os.path.join(os.environ['MAYADIR'], directory)
			if not os.path.isdir(nDir):
				osOps.createDir(nDir)

		# Copy workspace.mel definition file into Maya project dir
		workspace_def = os.path.join(os.environ['MAYADIR'], 'workspace.mel')
		if not os.path.isfile(workspace_def):
			src = os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'templates', 'workspace.mel')
			osOps.copy(src, workspace_def)

	elif app == 'Mudbox':
		for directory in ('scenes', 'models', 'sourceimages', ):
			uDir = os.path.join(os.environ['MUDBOXDIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'Cinema4D':
		for directory in ('scenes', ):
			uDir = os.path.join(os.environ['C4DDIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'AfterEffects':
		for directory in ('comps', 'elements', 'renders', ):
			uDir = os.path.join(os.environ['AFXDIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'Photoshop':
			uDir = os.path.join(os.environ['PSDIR'], username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'Nuke':
		for directory in ('scripts', 'elements', 'renders', ):
			uDir = os.path.join(os.environ['NUKEDIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'Mari':
		for directory in ('scenes', 'geo', 'sourceimages', 'textures', 'renders', 'archives', ):
			uDir = os.path.join(os.environ['MARIDIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'Photoscan':
		for directory in ('scenes', 'cameras', 'pointClouds', 'geometry', 'sourceimages', ):
			uDir = os.path.join(os.environ['PHOTOSCANDIR'], directory, username)
			if not os.path.isdir(uDir):
				osOps.createDir(uDir)

	elif app == 'RealFlow':
		for directory in ('.cmdsOrg', ):  # Trailing comma required to make iterable, otherwise for loop will iterate over string, i.e. '.', 'c', 'm', 'd', etc.
			nDir = os.path.join(os.environ['REALFLOWSCENESDIR'], directory)
			if not os.path.isdir(nDir):
				osOps.createDir(nDir)

