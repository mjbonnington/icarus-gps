#!/usr/bin/python

# [GPS] userSetup.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Commands to execute at Maya startup.


import os
import sys

sys.path.append(os.environ['IC_BASEDIR'])
from core import env__init__
env__init__.appendSysPaths()

import maya.cmds as mc
os.environ['IC_ENV'] = 'MAYA'

from rsc.maya.scripts import mayaOps
from shared import osOps
from shared import verbose


batchMode = mc.about(batch=True)

# Deploy custom tool shelves
if not batchMode:
	mayaShelvesDir = os.path.join(mc.about(preferences=True), 'prefs', 'shelves')
	# mayaModulesDir = os.path.join(mc.about(preferences=True), 'modules')
	try:
		osOps.copyDirContents(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'shelves'), mayaShelvesDir)
		# osOps.copyDirContents(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'modules'), mayaModulesDir)
		# osOps.copyDirContents(os.path.join(os.environ['JOBPUBLISHDIR'], 'ma_shelves'), mayaShelvesDir)
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
	mc.loadPlugin(ma_plugin, quiet=True)
