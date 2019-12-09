#!/usr/bin/python

# maya__env__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Set Maya-specific environment variables.

import os

from shared import os_wrapper

def set_env():
	# Icarus env vars
	# (N.B. Project path vars are set in templates/projectDir.xml)
	os.environ['IC_MAYA_RENDER_EXECUTABLE'] = os_wrapper.absolutePath('%s/Render' % os.path.dirname(os.environ['IC_MAYA_EXECUTABLE']))
	os.environ['IC_MAYA_SHARED_RESOURCES'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/Maya')  # Store this in app settings / IC global prefs?

	# Maya config vars
	os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = "0"
	os.environ['MAYA_ENABLE_LEGACY_VIEWPORT'] = "1"
	os.environ['MAYA_FORCE_PANEL_FOCUS'] = "0"  # This should prevent panel stealing focus from Qt window on keypress.
	os.environ['MAYA_DISABLE_CLIC_IPM'] = "1"  # Disable the In Product Messaging button (should improve Maya startup & shutdown time).
	os.environ['MAYA_DISABLE_CIP'] = "1"  # Disable the Customer Involvement Program (should improve Maya startup & shutdown time).

	#os.environ['MAYA_MODULE_PATH'] = 
	#os.environ['MAYA_PRESET_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/presets')
	#os.environ['MI_CUSTOM_SHADER_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders/include')
	#os.environ['MI_LIBRARY_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
	#os.environ['VRAY_FOR_MAYA_SHADERS'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
	#os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] += os.pathsep + os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/plugins')

	maya_ver = os.environ['IC_MAYA_VERSION']
	pluginsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/plugins') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/%s/plug-ins' % maya_ver)
	scriptsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/env') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/scripts') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_MAYA_PROJECT_DIR/scripts') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_JOBPUBLISHDIR/scripts') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_SHOTPUBLISHDIR/scripts') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/scripts') + os.pathsep \
	            + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/%s/scripts' % maya_ver)
	iconsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/icons') + os.pathsep \
	          + os_wrapper.absolutePath('$IC_JOBPUBLISHDIR/icons') + os.pathsep \
	          + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/%s/icons' % maya_ver)
	if os.environ['IC_RUNNING_OS'] == "Linux":  # Append the '%B' bitmap placeholder token required for Linux
		iconsPathsModified = []
		for path in iconsPath.split(os.pathsep):
			iconsPathsModified.append(path + r"/%B")
		iconsPath = os.pathsep.join(n for n in iconsPathsModified)

	os.environ['MAYA_SHELF_PATH'] = os_wrapper.absolutePath('$IC_JOBPUBLISHDIR/ma_shelves')  # For custom job shelf
	os.environ['MAYA_PLUG_IN_PATH'] = pluginsPath
	os.environ['MAYA_SCRIPT_PATH'] = scriptsPath
	# os.environ['PYTHONPATH'] = scriptsPath  # this should only happen at Maya launch
	os.environ['XBMLANGPATH'] = iconsPath
