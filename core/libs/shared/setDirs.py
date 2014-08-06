#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:setDirs

import os, time

def mkDirs():
	userName = os.environ['USERNAME']
	jobPath = os.environ['SHOTPATH']
	
	#maya
	mayaDirLs = ['scenes', 'playblasts', 'renders', 'cache']
	for mayaDir in mayaDirLs:
		uDir = '%s/3D/maya/%s/%s' % (jobPath, mayaDir, userName)
		if not os.path.isdir(uDir):
			os.system('mkdir -p %s'  % uDir)
			os.system('chmod -R 775 %s' % uDir)
			
	#recent working files
	uDir = os.environ['RECENTFILESDIR']
	filePrefix = '%s_%s' % (os.environ['JOB'], os.environ['SHOT'])
	mayaFile = '%s_mayaScnLs.ic' % filePrefix
	nukeFile = '%s_nukeScrLs.ic' % filePrefix
	uFiles = [mayaFile, nukeFile]
	if not os.path.isdir(uDir):
			os.system('mkdir -p %s'  % uDir)
			os.system('chmod -R 775 %s' % uDir)
	for uFile in uFiles:
		uFilePath = '%s/%s' % (uDir, uFile)
		if not os.path.isfile(uFilePath):
			fileHandle = open(uFilePath, "w")
			fileHandle.close()
			os.system('chmod -R 775 %s' % uFilePath)
			
	#mudbox
	mudboxDirLs = ['scenes', 'models', 'sourceimages']
	for mudboxDir in mudboxDirLs:
		uDir = '%s/3D/mudbox/%s/%s' % (jobPath, mudboxDir, userName)
		if not os.path.isdir(uDir):
			os.system('mkdir -p %s'  % uDir)
			os.system('chmod -R 775 %s' % uDir)
			
	#mari
	mariDirLs = ['scenes', 'geo', 'sourceimages', 'textures', 'renders', 'archives']
	for mariDir in mariDirLs:
		uDir = '%s/3D/mari/%s/%s' % (jobPath, mariDir, userName)
		if not os.path.isdir(uDir):
			os.system('mkdir -p %s'  % uDir)
			os.system('chmod -R 775 %s' % uDir)

	#photoscan
	photoScanDirLs = ['scenes', 'cameras', 'pointClouds', 'geometry', 'sourceImages']
	for photoScanDir in photoScanDirLs:
		uDir = '%s/3D/photoscan/%s/%s' % (jobPath, photoScanDir, userName)
		if not os.path.isdir(uDir):
			os.system('mkdir -p %s'  % uDir)
			os.system('chmod -R 775 %s' % uDir)
	
	#nuke
	nukeDirLs = ['scripts', 'elements', 'renders']
	for nukeDir in nukeDirLs:
		uDir = '%s/%s/%s' % (os.environ['NUKEDIR'], nukeDir, userName)
		if not os.path.isdir(uDir):
			os.system('mkdir -p %s' % uDir)
			os.system('chmod -R 775 %s' % uDir)
	
	#realflow
	realflowDirLs = ['.cmdsOrg']
	for realflowDir in realflowDirLs:
		uDir = '%s/%s' % (os.environ['REALFLOWSCENESDIR'], realflowDir)
		if not os.path.isdir(uDir):
			os.system('mkdir -p %s' % uDir)
			os.system('chmod -R 775 %s' % uDir)
			
	#env
	envDirLs = [os.environ['JOBAPPROVEDPUBLISHDIR'], os.environ['SHOTAPPROVEDPUBLISHDIR'], os.environ['JOBPUBLISHDIR'], os.environ['SHOTPUBLISHDIR']]
	for envDir in envDirLs:
		if not os.path.isdir(envDir):
			os.system('mkdir -p %s' % envDir)
			os.system('chmod -R 777 %s' % envDir)
