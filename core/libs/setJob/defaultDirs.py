#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:defaultDirs
#copyright	:Gramercy Park Studios

import os
import osOps

#creates user specific directories for shot work
def create():
	userName = os.environ['USERNAME']
	#jobPath = os.environ['SHOTPATH']

	#maya
	for dir in ('scenes', 'playblasts', 'sourceimages', 'renders', 'cache'):
		uDir = os.path.join(os.environ['MAYADIR'], dir, userName)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#mudbox
	for dir in ('scenes', 'models', 'sourceimages'):
		uDir = os.path.join(os.environ['MUDBOXDIR'], dir, userName)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#mari
	for dir in ('scenes', 'geo', 'sourceimages', 'textures', 'renders', 'archives'):
		uDir = os.path.join(os.environ['MARIDIR'], dir, userName)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#photoscan
	#for dir in ('scenes', 'cameras', 'pointClouds', 'geometry', 'sourceImages'):
	#	uDir = os.path.join(jobPath, '3D', 'photoscan', dir, userName)
	#	if not os.path.isdir(uDir):
	#		osOps.createDir(uDir)

	#nuke
	for dir in ('scripts', 'elements', 'renders'):
		uDir = os.path.join(os.environ['NUKEDIR'], dir, userName)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#realflow
	for dir in ('.cmdsOrg'):
		uDir = '%s/%s' % (os.environ['REALFLOWSCENESDIR'], dir)
		if not os.path.isdir(uDir):
			osOps.createDir(uDir)

	#env
	for dir in (os.environ['JOBAPPROVEDPUBLISHDIR'], os.environ['SHOTAPPROVEDPUBLISHDIR'], os.environ['JOBPUBLISHDIR'], os.environ['SHOTPUBLISHDIR']):
		if not os.path.isdir(dir):
			os.system('mkdir -p %s' % dir)
			osOps.createDir(uDir)
