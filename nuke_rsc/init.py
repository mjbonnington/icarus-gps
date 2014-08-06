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
nuke.pluginAddPath('./plugins/J_Ops')

#Nuke seems to ditch the main root environent where it has been called from so the path needs to be appended again
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core/ui'))
import env__init__
env__init__.appendSysPaths()
import icarus__main__, setLog, gpsNodes

#thirdparty initializations
import J_Ops_init; import J_Ops

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