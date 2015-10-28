#!/usr/bin/python

# [GPS] Maya Scene Management
# v0.1
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Maya scene management module.


import os

def newMayaScene():
	import mayaOps
	mayaOps.newScene()

def openMayaScene():
	import mayaOps
	mayaOps.openScene(os.environ["MAYASCENESDIR"], "Maya Files (*.ma *.mb)")

def openMayaRecentScene(recentFilePath):
	import mayaOps
	mayaOps.openScene(recentFilePath, dialog=False)

def saveMayaSceneAs():
	import mayaOps
	mayaOps.saveFileAs(os.environ["MAYASCENESDIR"], "Maya Files (*.ma *.mb)")

def saveMayaScene():
	import mayaOps
	sceneName = os.path.split(mayaOps.getScene())[1]
	if sceneName == 'untitled':
		saveMayaSceneAs()
	else:
		sceneName, sceneExt = sceneName.split('.')
		mayaOps.saveFile(sceneExt)

def mayaUpdate():
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

