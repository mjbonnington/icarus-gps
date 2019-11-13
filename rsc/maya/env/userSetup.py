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

# Set environment (should be done first)
os.environ['IC_ENV'] = 'MAYA'

# Append pipeline base dir to Python path
sys.path.append(os.environ['IC_BASEDIR'])
from core import env__init__
env__init__.appendSysPaths()

import maya.cmds as mc

# from rsc.maya.scripts import mayaOps
# from shared import os_wrapper
# from shared import verbose

# Set up path remapping for cross-platform support
if os.environ['FILESYSTEMROOT'] != "None":
	mc.dirmap(enable=True)
	if os.environ['FILESYSTEMROOTWIN'] != "None":
		mc.dirmap(
			mapDirectory=(
				os.environ['FILESYSTEMROOTWIN'], 
				os.environ['FILESYSTEMROOT']))
	if os.environ['FILESYSTEMROOTOSX'] != "None":
		mc.dirmap(
			mapDirectory=(
				os.environ['FILESYSTEMROOTOSX'], 
				os.environ['FILESYSTEMROOT']))
	if os.environ['FILESYSTEMROOTLINUX'] != "None":
		mc.dirmap(
			mapDirectory=(
				os.environ['FILESYSTEMROOTLINUX'], 
				os.environ['FILESYSTEMROOT']))

batchMode = mc.about(batch=True)

# Deploy custom tool shelves
if not batchMode:
	from shared import os_wrapper
	from shared import verbose

	mayaShelvesDir = os.path.join(mc.about(preferences=True), 'prefs', 'shelves')
	# mayaModulesDir = os.path.join(mc.about(preferences=True), 'modules')
	try:
		os_wrapper.copyDirContents(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'shelves'), mayaShelvesDir)
		# os_wrapper.copyDirContents(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'modules'), mayaModulesDir)
		# os_wrapper.copyDirContents(os.path.join(os.environ['IC_JOBPUBLISHDIR'], 'ma_shelves'), mayaShelvesDir)
		verbose.gpsToolDeploy('OK')
	except:
		verbose.gpsToolDeploy('Failed')

	# # Instance the Icarus UI
	# from core.app_session import *
	# from core import icarus
	# session.icarus = icarus.app(app='maya')

	# Update Maya scene defaults at startup
	from rsc.maya.scripts import mayaOps
	mayaOps.update()
	#source gpsRenderSetup.mel; gpsRenderSetup.setCommonOptions()

# Load plugins ---------------------------------------------------------------
# List of plugins to load by default
ma_pluginLs = ['AbcExport', 
               'AbcImport', 
               'fbxmaya', 
               'objExport', 
               'OpenEXRLoader', 
               'tiffFloatReader']

for ma_plugin in ma_pluginLs:
	mc.loadPlugin(ma_plugin, quiet=True)
