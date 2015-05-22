#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :autoDeploy
#copyright  :Gramercy Park Studios


import os, sys
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core', 'ui'))
import env__init__
env__init__.appendSysPaths()
import maya.cmds as mc, maya.mel as mel
import verbose, osOps

def deploy():
	#Getting Maya Home
	mayaVersion = mc.about(v=True)
	#if mc.about(is64=True):
	#	#Bypassing a Maya bug 'about -v' not always returning -x64 with 64 bit version
	#	if '64' not in mayaVersion:
	#		mayaVersion += '-x64'
	#	else:
	#		mayaVersion = mayaVersion.replace(' ', '-')
	mayaVersion = mayaVersion.replace(' ', '-')

	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		mayaHome = os.path.join(mel.eval('getenv HOME'), 'Library', 'Preferences', 'Autodesk', 'maya', mayaVersion)
	elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		mayaHome = os.path.join(os.environ['HOMEPATH'], 'Documents', 'maya', mayaVersion)
	else:
		mayaHome = os.path.join(mel.eval('getenv HOME'), 'maya', mayaVersion)

	#Pipeline Resources Paths
	#shelves
	shelf_resources = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'shelves')
	mayaShelvesDir = os.path.join(mayaHome, 'prefs', 'shelves')

	#Copying files
	try:
		osOps.copyDirContents(shelf_resources, mayaShelvesDir)
		verbose.gpsToolDeploy('Ok')
	except:
		verbose.gpsToolDeploy('Failed')
