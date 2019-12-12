#!/usr/bin/python

# [GPS] userSetup.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Commands to execute at Maya startup.
# This module has been deprecated: all operations moved to userSetup.mel


import os
import sys

# Set environment (should be done first)
os.environ['IC_ENV'] = 'MAYA'

# Append pipeline base dir to Python path
sys.path.append(os.environ['IC_BASEDIR'])
# from core.app_session import *
from core import icarus__env__
icarus__env__.append_sys_paths()

import maya.cmds as mc

# from rsc.maya.scripts import mayaOps
# from shared import os_wrapper
# from shared import verbose

# Set up path remapping for cross-platform support
if os.environ['IC_FILESYSTEM_ROOT'] != "None":
	mc.dirmap(enable=True)
	if os.environ['IC_FILESYSTEM_ROOT_WIN'] != "None":
		mc.dirmap(
			mapDirectory=(
				os.environ['IC_FILESYSTEM_ROOT_WIN'], 
				os.environ['IC_FILESYSTEM_ROOT']))
	if os.environ['IC_FILESYSTEM_ROOT_OSX'] != "None":
		mc.dirmap(
			mapDirectory=(
				os.environ['IC_FILESYSTEM_ROOT_OSX'], 
				os.environ['IC_FILESYSTEM_ROOT']))
	if os.environ['IC_FILESYSTEM_ROOT_LINUX'] != "None":
		mc.dirmap(
			mapDirectory=(
				os.environ['IC_FILESYSTEM_ROOT_LINUX'], 
				os.environ['IC_FILESYSTEM_ROOT']))

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

	# Initialise Scene Manager
	# from tools.scenemanager import scenemanager
	# session.scnmgr = scenemanager.create(app='maya')
	# session.scnmgr.set_defaults()

	# Update Maya scene defaults at startup
	# from rsc.maya.scripts import mayaOps
	# mayaOps.update()
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
