#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:init
#copyright	:Gramercy Park Studios

#This file contains Nuke's initializing procedures
import os, sys

#adding to nuke path
nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./scripts')
nuke.pluginAddPath('./plugins')
#thirdparty locations
nuke.pluginAddPath('./gizmos/pxf')

#Nuke seems to ditch the main root environent where it has been called from so the path needs to be appended again
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core', 'ui'))
import env__init__
env__init__.appendSysPaths()
#Nuke opens a entire new Nuke process with 'File>New Script' and doesn't simply create and empty script in the current env.
#The icarus env has to be set temporarily as NUKE_TMP to avoid icarus detecting an existing NUKE env and opening automatically it's UI
os.environ['ICARUSENVAWARE'] = 'NUKE_TMP'
import icarus__main__, gpsNodes
os.environ['ICARUSENVAWARE'] = 'NUKE'

#thirdparty initializations go here


#SHOT DIRECTORIES
nuke.addFavoriteDir('Elements', os.environ['NUKEELEMENTSDIR'])
nuke.addFavoriteDir('Scripts', os.environ['NUKESCRIPTSDIR'])
nuke.addFavoriteDir('Renders', os.environ['NUKERENDERSDIR'])
nuke.addFavoriteDir('Elements Library', os.environ['ELEMENTSLIBRARY'])

#PLATE FORMAT
shotId = '_%s_%s' % (os.environ['JOB'], os.environ['SHOT'])
plateFormat = '%s %s %s' % (os.environ['HRES'], os.environ['VRES'], shotId)
nuke.addFormat( plateFormat)
nuke.knobDefault('Root.format', shotId)
nuke.knobDefault('Root.fps', os.environ['FPS'])
nuke.knobDefault('Root.first_frame', os.environ['STARTFRAME'])
nuke.knobDefault('Root.last_frame', os.environ['ENDFRAME'])