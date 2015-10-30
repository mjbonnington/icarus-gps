#!/usr/bin/python

# [GPS] userSetup.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Commands to execute at Maya startup.


import os, sys
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core', 'ui'))
import env__init__
env__init__.appendSysPaths()
import maya.cmds as mc
os.environ['ICARUSENVAWARE'] = 'MAYA'
import mayaOps, osOps, verbose


# Deploy custom tool shelves
shelfResources = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'shelves')
mayaShelvesDir = os.path.join(mc.about(preferences=True), 'prefs', 'shelves')

try:
	osOps.copyDirContents(shelfResources, mayaShelvesDir)
	verbose.gpsToolDeploy('OK')
except:
	verbose.gpsToolDeploy('Failed')


# List of plugins to load by default
ma_pluginLs = ['AbcExport', 
               'AbcImport', 
               'fbxmaya', 
               'objExport', 
               'OpenEXRLoader', 
               'tiffFloatReader']

for ma_plugin in ma_pluginLs:
	mc.loadPlugin(ma_plugin, qt=True)
