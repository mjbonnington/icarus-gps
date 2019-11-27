#!/usr/bin/python

# [Icarus] icDeployTools.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019 Gramercy Park Studios
#
# Copy Maya tools (shelves, modules, etc.) from pipeline into Maya prefs dir
# at startup. This ensures the correct items are loaded and prevents possible
# user modification if redirecting the env vars to look in the shared
# location.


import os
import sys
import maya.cmds as mc

# Import custom modules
from shared import os_wrapper
from shared import verbose


# Deploy custom tool shelves
def deploy():
	mayaShelvesDir = os.path.join(mc.about(preferences=True), 'prefs', 'shelves')
	# mayaModulesDir = os.path.join(mc.about(preferences=True), 'modules')

	try:
		os_wrapper.copyDirContents(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'shelves'), mayaShelvesDir)
		# os_wrapper.copyDirContents(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'modules'), mayaModulesDir)
		# os_wrapper.copyDirContents(os.path.join(os.environ['IC_JOBPUBLISHDIR'], 'ma_shelves'), mayaShelvesDir)
		verbose.message("Successfully deployed %s tools." % os.environ['IC_VENDOR_INITIALS'])
		return True

	except:
		verbose.warning("Failed to deploy %s tools." % os.environ['IC_VENDOR_INITIALS'])
		return False
