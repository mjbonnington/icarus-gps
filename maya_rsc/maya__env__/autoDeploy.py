#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:autoDeploy
#copyright	:Gramercy Park Studios


import os, sys
import maya.cmds as mc, maya.mel as mel

def deploy():
	#Getting Maya Home
	mayaVersion = mc.about(v=True)
	if mc.about(is64=True):
		#Bypassing a Maya bug 'about -v' not always returning -x64 with 64 bit version
		if '64' not in mayaVersion:
			mayaVersion += '-x64'
		else:
	 		mayaVersion = mayaVersion.replace(' ', '-')
	if sys.platform == 'darwin':
		mayaHome = '/Users/%s/Library/Preferences/Autodesk/maya/%s' % (os.environ['USERNAME'], mayaVersion)
	else:
		mayaHome = '%s/maya/%s' % (mel.eval('getenv HOME'), mayaVersion)
	
	#Pipeline Resources Paths
	#shelves
	shelf_resources = '%s/maya_rsc/shelves' % os.environ['PIPELINE']
	mayaShelvesDir = "%s/prefs/shelves/" % mayaHome
	
	#Copying files
	outputMsg = 'Deploying GPS tools - '
	try:
		os.system('cp %s/* %s/' % (shelf_resources, mayaShelvesDir))
		print '%s Ok' % outputMsg 
	except:
		print '%s Failed' % outputMsg
		
