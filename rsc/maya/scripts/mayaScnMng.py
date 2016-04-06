#!/usr/bin/python

# [GPS] Maya Scene Management
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Maya scene management module.
# These are wrapper functions for the main code which is in mayaOps.py


import os
import mayaOps


def newMayaScene():
	""" Create a new scene.
	"""
	mayaOps.newScene()


def openMayaScene():
	""" Open a saved scene.
	"""
	mayaOps.openScene(os.environ["MAYASCENESDIR"], "Maya Files (*.ma *.mb)")


def openMayaRecentScene(recentFilePath):
	""" Open a saved scene from the recent files menu.
	"""
	mayaOps.openScene(recentFilePath, dialog=False)


def saveMayaScene():
	""" Save the scene under its current name.
	"""
	sceneName = os.path.split(mayaOps.getScene())[1]
	if sceneName == 'untitled':
		saveMayaSceneAs()
	else:
		ext = os.path.splitext(sceneName)[1][1:] # get the extension without a leading dot
		mayaOps.saveFile(ext)


def saveMayaSceneAs():
	""" Save the scene under a new name.
	"""
	mayaOps.saveFileAs(os.environ["MAYASCENESDIR"], "Maya Files (*.ma *.mb)")


def mayaUpdate():
	""" NOTE - this function doesn't appear to be called from anywhere. Could be redundant?
	"""
	import sys
	shotDataPath = os.environ["SHOTDATA"]
	sys.path.append(shotDataPath)
	import shotData, mayaOps
	reload(shotData)
	os.environ['STARTFRAME'], os.environ['ENDFRAME'] = shotData.frRange
	os.environ['STARTFRAME'], os.environ['ENDFRAME'] = shotData.frRange
	os.environ["FRAMERANGE"] = "%s-%s" % (shotData.frRange[0], shotData.frRange[1])
	os.environ["RESOLUTIONX"] = shotData.res[0]
	os.environ["RESOLUTIONY"] = shotData.res[1]
	os.environ["RESOLUTION"] = "%sx%s" % (shotData.res[0], shotData.res[1])
	mayaOps.update()

