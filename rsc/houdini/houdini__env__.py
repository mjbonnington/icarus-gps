#!/usr/bin/python

# houdini__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Houdini-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	os.environ['HOUDINI_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini') + os.pathsep \
	                           + os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini/env') + os.pathsep + "&" + os.pathsep
	# os.environ['HOUDINI_SCRIPT_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini/scripts') + os.pathsep + "&" + os.pathsep
	os.environ['HOUDINI_UI_ICON_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini/icons') + os.pathsep \
	                                   + os_wrapper.absolutePath('$IC_FORMSDIR/icons') + os.pathsep + "&" + os.pathsep
	os.environ['HOUDINI_TOOLBAR_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini/shelves') + os.pathsep + "&" + os.pathsep
	# os.environ['JOB'] = os.environ['IC_HOUDINI_PROJECT_DIR']
	# os.environ['HIP'] = os_wrapper.absolutePath('$IC_HOUDINI_PROJECT_DIR/scenes')

	if os.environ['IC_RUNNING_OS'] == "Windows":
		# os.environ['HOUDINI_TEXT_CONSOLE'] = "1"  # Use a normal shell window for console output
		os.environ['HOUDINI_DISABLE_CONSOLE'] = "1"  # Disable text console completely

	# os.environ['HOUDINI_NO_ENV_FILE'] = "1"  # Don't load the user's houdini.env
	# os.environ['HOUDINI_NO_ENV_FILE_OVERRIDES'] = "1"  # Don't allow overrides to existing vars from the user's houdini.env
	# os.environ['HSITE'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/Houdini')  # Store this in app settings / IC global prefs?