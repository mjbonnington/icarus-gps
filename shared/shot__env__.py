#!/usr/bin/python

# [Icarus] shot__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Sets up shot-related environment variables.
# TODO: This module needs total re-think in light of dynamic app launching.


import os
import sys

from . import appPaths
# from . import jobs
from . import os_wrapper
from . import settings_data_xml
from . import verbose


def set_env(job, shot, shot_path):
	""" Set job and shot environment variables.
	"""

	def getInheritedValue(category, setting):
		""" First try to get the value from the shot data, if it returns
			nothing then look in job data instead.
		"""
		value = shot_data.getValue(category, setting)
		if value is None:
			value = job_data.getValue(category, setting)
			# if value is None:
			# 	value = default_data.getValue(category, setting)

		#return value

		# Return an empty string, not None, so value can be stored in an
		# environment variable without raising an error
		if value is None:
			return ""
		else:
			return str(value)


	def getAppExecPath(app):
		""" Return the path to the executable for the specified app on the
			current OS.
		"""
		return app_paths.getPath(app, getInheritedValue('apps', app), currentOS)


	job_path = os.path.split(shot_path)[0]
	job_data_path = os.path.join(job_path, os.environ['IC_METADATA'])
	shot_data_path = os.path.join(shot_path, os.environ['IC_METADATA'])

	# Set basic environment variables
	os.environ['IC_JOB'] = job
	os.environ['IC_SHOT'] = shot
	os.environ['IC_JOBPATH'] = os_wrapper.absolutePath(job_path)
	os.environ['IC_SHOTPATH'] = os_wrapper.absolutePath(shot_path)
	os.environ['IC_JOBDATA'] = os_wrapper.absolutePath(job_data_path)
	os.environ['IC_SHOTDATA'] = os_wrapper.absolutePath(shot_data_path)

	os_wrapper.createDir(os.environ['IC_JOBDATA'])

	# Instantiate job / shot settings classes
	job_data = settings_data_xml.SettingsData()
	shot_data = settings_data_xml.SettingsData()
	#default_data = settings_data_xml.SettingsData()
	app_paths = appPaths.AppPaths()

	# Load data
	job_data.loadXML(os.path.join(job_data_path, 'jobData.xml'), use_template=False)
	shot_data.loadXML(os.path.join(shot_data_path, 'shotData.xml'), use_template=False)
	#default_data.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'defaultData.xml'))
	app_paths.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), use_template=True)

	os.environ['IC_ASSETDIR'] = 'assets'

	# Check if the job is using the correct Icarus version
	icVersion = job_data.getValue('meta', 'icVersion')
	if icVersion:
		if icVersion != os.environ['IC_VERSION']:
			verbose.warning("This job requires version %s of Icarus. You're currently running %s" % (icVersion, os.environ['IC_VERSION']))
	else:
		job_data.setValue('meta', 'icVersion', os.environ['IC_VERSION'])
		job_data.saveXML()

	# Set OS identifier strings to get correct app executable paths
	if os.environ['IC_RUNNING_OS'] == "Windows":
		currentOS = "win"
	elif os.environ['IC_RUNNING_OS'] == "MacOS":
		currentOS = "osx"
	elif os.environ['IC_RUNNING_OS'] == "Linux":
		currentOS = "linux"

	# Terminal / Command Prompt
	if os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['IC_SHELL_RC'] = os_wrapper.absolutePath('$IC_WORKINGDIR/shell_cmd.bat')
	else:
		os.environ['IC_SHELL_RC'] = os_wrapper.absolutePath('$IC_WORKINGDIR/shell_rc')

	# Job / shot env
	#os.environ['IC_GLOBALPUBLISHDIR']  = os_wrapper.absolutePath(getInheritedValue('other', 'assetlib'))  # Path needs to be translated for OS portability
	os.environ['IC_JOBPUBLISHDIR'] = os_wrapper.absolutePath('$IC_JOBPATH/$IC_ASSETDIR')
	os.environ['IC_SHOTPUBLISHDIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/$IC_ASSETDIR')
	os.environ['IC_WIPS_DIR'] = os_wrapper.absolutePath('$IC_JOBPATH/../Deliverables/WIPS')  # Perhaps this shouldn't be hard-coded?
	os.environ['IC_ELEMENTS_LIBRARY'] = os_wrapper.absolutePath(getInheritedValue('other', 'elementslib'))  # Path needs to be translated for OS portability
	os.environ['IC_PRODUCTION_BOARD'] = getInheritedValue('other', 'prodboard')
	os.environ['IC_LINEAR_UNIT'] = getInheritedValue('units', 'linear')
	os.environ['IC_ANGULAR_UNIT'] = getInheritedValue('units', 'angle')
	os.environ['IC_TIME_UNIT'] = getInheritedValue('units', 'time')
	os.environ['IC_FPS'] = getInheritedValue('units', 'fps')
	os.environ['IC_STARTFRAME'] = getInheritedValue('time', 'rangeStart')
	os.environ['IC_ENDFRAME'] = getInheritedValue('time', 'rangeEnd')
	os.environ['IC_INFRAME'] = getInheritedValue('time', 'inFrame')
	os.environ['IC_OUTFRAME'] = getInheritedValue('time', 'outFrame')
	os.environ['IC_POSTER_FRAME'] = getInheritedValue('time', 'posterFrame')
	os.environ['IC_RESOLUTION_X'] = getInheritedValue('resolution', 'fullWidth')
	os.environ['IC_RESOLUTION_Y'] = getInheritedValue('resolution', 'fullHeight')
	os.environ['IC_PROXY_RESOLUTION_X'] = getInheritedValue('resolution', 'proxyWidth')
	os.environ['IC_PROXY_RESOLUTION_Y'] = getInheritedValue('resolution', 'proxyHeight')
	os.environ['IC_ASPECT_RATIO'] = str(float(os.environ['IC_RESOLUTION_X']) / float(os.environ['IC_RESOLUTION_Y']))
	os.environ['IC_EDITOR'] = getAppExecPath('SublimeText')  # Make dynamic 

	# ------------------------------------------------------------------------

	# # Application specific environment variables...
	# # TODO: move out to individual modules and evaluate on seting shot

	# # Redshift centralised deployment
	# # os.environ['IC_REDSHIFT_EXECUTABLE'] = getAppExecPath('Redshift')
	# if os.environ['IC_REDSHIFT_EXECUTABLE'] != "":
	# 	# os.environ['redshift_LICENSE'] = "port@hostname"
	# 	os.environ['REDSHIFT_COREDATAPATH'] = os.environ['IC_REDSHIFT_EXECUTABLE']
	# elif os.environ['IC_RUNNING_OS'] == "Windows":
	# 	os.environ['REDSHIFT_COREDATAPATH'] = "C:/ProgramData/Redshift"
	# elif os.environ['IC_RUNNING_OS'] == "MacOS":
	# 	os.environ['REDSHIFT_COREDATAPATH'] = "/usr/redshift"
	# elif os.environ['IC_RUNNING_OS'] == "Linux":
	# 	os.environ['REDSHIFT_COREDATAPATH'] = "/Applications/redshift"


	# # Maya
	# # os.environ['IC_MAYA_EXECUTABLE'] = getAppExecPath('Maya')
	# os.environ['IC_MAYA_RENDER_EXECUTABLE'] = os_wrapper.absolutePath('%s/Render' % os.path.dirname(os.environ['IC_MAYA_EXECUTABLE']))
	# os.environ['IC_MAYA_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/maya')  # Currently needed by render submitter
	# os.environ['IC_MAYA_SCENES_DIR'] = os_wrapper.absolutePath('$IC_MAYA_PROJECT_DIR/scenes')  # Currently needed by render submitter
	# os.environ['IC_MAYA_SOURCEIMAGES_DIR'] = os_wrapper.absolutePath('$IC_MAYA_PROJECT_DIR/sourceimages')  # Currently needed by openDirs
	# os.environ['IC_MAYA_RENDERS_DIR'] = os_wrapper.absolutePath('$IC_MAYA_PROJECT_DIR/renders')  # Currently needed by daily publish
	# os.environ['IC_MAYA_PLAYBLASTS_DIR'] = os_wrapper.absolutePath('$IC_MAYA_PROJECT_DIR/playblasts')  # Currently needed by daily publish
	# os.environ['IC_MAYA_SHARED_RESOURCES'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/Maya')  # Store this in app settings / ic global prefs?

	# try:
	# 	# maya_ver = str(job_data.getAppVersion('Maya'))
	# 	# os.environ['IC_MAYA_VERSION'] = maya_ver
	# 	maya_ver = os.environ['IC_MAYA_VERSION']

	# 	os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = "0"
	# 	os.environ['MAYA_ENABLE_LEGACY_VIEWPORT'] = "1"
	# 	os.environ['MAYA_FORCE_PANEL_FOCUS'] = "0"  # This should prevent panel stealing focus from Qt window on keypress.
	# 	os.environ['MAYA_DISABLE_CLIC_IPM'] = "1"  # Disable the In Product Messaging button (should improve Maya startup & shutdown time).
	# 	os.environ['MAYA_DISABLE_CIP'] = "1"  # Disable the Customer Involvement Program (should improve Maya startup & shutdown time).

	# 	pluginsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/plugins') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/%s/plug-ins' % maya_ver)
	# 	scriptsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/env') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/scripts') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_MAYA_PROJECT_DIR/scripts') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_JOBPUBLISHDIR/scripts') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_SHOTPUBLISHDIR/scripts') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/scripts') + os.pathsep \
	# 	            + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/%s/scripts' % maya_ver)
	# 	iconsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/icons') + os.pathsep \
	# 	          + os_wrapper.absolutePath('$IC_JOBPUBLISHDIR/icons') + os.pathsep \
	# 	          + os_wrapper.absolutePath('$IC_MAYA_SHARED_RESOURCES/%s/icons' % maya_ver)
	# 	if os.environ['IC_RUNNING_OS'] == "Linux":  # Append the '%B' bitmap placeholder token required for Linux
	# 		iconsPathsModified = []
	# 		for path in iconsPath.split(os.pathsep):
	# 			iconsPathsModified.append(path + r"/%B")
	# 		iconsPath = os.pathsep.join(n for n in iconsPathsModified)

	# 	#os.environ['MAYA_MODULE_PATH'] = 
	# 	#os.environ['MAYA_PRESET_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/presets')
	# 	#os.environ['MI_CUSTOM_SHADER_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders/include')
	# 	#os.environ['MI_LIBRARY_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
	# 	#os.environ['VRAY_FOR_MAYA_SHADERS'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
	# 	#os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] += os.pathsep + os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/plugins')

	# 	os.environ['MAYA_SHELF_PATH'] = os_wrapper.absolutePath('$IC_JOBPUBLISHDIR/ma_shelves')
	# 	os.environ['MAYA_PLUG_IN_PATH'] = pluginsPath
	# 	os.environ['MAYA_SCRIPT_PATH'] = scriptsPath
	# 	# os.environ['PYTHONPATH'] = scriptsPath  # this should only happen at Maya launch
	# 	os.environ['XBMLANGPATH'] = iconsPath

	# except (AttributeError, KeyError, TypeError):
	# 	verbose.warning("Unable to set Maya environment variables - please check job settings to ensure Maya version is set.")


	# # Houdini
	# # os.environ['IC_HOUDINI_EXECUTABLE'] = getAppExecPath('Houdini')
	# # os.environ['IC_HOUDINI_VERSION'] = str(job_data.getAppVersion('Houdini'))  # Temporary for Deadline submit
	# os.environ['IC_HOUDINI_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/houdini')  # Currently needed by render submitter
	# os.environ['IC_HOUDINI_SCENES_DIR'] = os_wrapper.absolutePath('$IC_HOUDINI_PROJECT_DIR/scenes')  # Currently needed by render submitter

	# os.environ['HOUDINI_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini') + os.pathsep \
	#                            + os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini/env') + os.pathsep + "&" + os.pathsep
	# os.environ['HOUDINI_UI_ICON_PATH'] = os_wrapper.absolutePath('$IC_FORMSDIR/icons') + os.pathsep + "&" + os.pathsep
	# os.environ['HOUDINI_TOOLBAR_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/houdini/shelves') + os.pathsep + "&" + os.pathsep
	# # os.environ['JOB'] = os.environ['IC_HOUDINI_PROJECT_DIR']
	# # os.environ['HIP'] = os_wrapper.absolutePath('$IC_HOUDINI_PROJECT_DIR/scenes')


	# # Nuke
	# # os.environ['IC_NUKE_EXECUTABLE'] = getAppExecPath('Nuke')
	# # os.environ['IC_NUKE_VERSION'] = str(job_data.getAppVersion('Nuke'))  # Temporary for Deadline submit
	# os.environ['IC_NUKE_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/nuke')  # Currently needed by render submitter
	# os.environ['IC_NUKE_ELEMENTS_DIR'] = os_wrapper.absolutePath('$IC_NUKE_PROJECT_DIR/elements')  # Currently needed by openDirs
	# os.environ['IC_NUKE_SCRIPTS_DIR'] = os_wrapper.absolutePath('$IC_NUKE_PROJECT_DIR/scripts')  # Currently needed by render submitter
	# os.environ['IC_NUKE_RENDERS_DIR'] = os_wrapper.absolutePath('$IC_NUKE_PROJECT_DIR/renders')  # Currently needed by daily publish

	# os.environ['NUKE_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/nuke') + os.pathsep \
	#                         + os_wrapper.absolutePath('$IC_BASEDIR/rsc/nuke/env')


	# # Hiero / HieroPlayer
	# # os.environ['IC_HIEROPLAYER_EXECUTABLE'] = getAppExecPath('HieroPlayer')
	# os.environ['IC_HIERO_EDITORIAL_DIR'] = os_wrapper.absolutePath('$IC_JOBPATH/../Editorial/Hiero')

	# os.environ['HIERO_PLUGIN_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/hiero')


	# # After Effects
	# # os.environ['IC_AE_EXECUTABLE'] = getAppExecPath('AfterEffects')
	# # os.environ['IC_AE_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/aftereffects')
	# # os.environ['IC_AE_ELEMENTS_DIR'] = os_wrapper.absolutePath('$IC_AE_PROJECT_DIR/elements')
	# # os.environ['IC_AE_COMPS_DIR'] = os_wrapper.absolutePath('$IC_AE_PROJECT_DIR/comps')
	# # os.environ['IC_AE_RENDERS_DIR'] = os_wrapper.absolutePath('$IC_AE_PROJECT_DIR/renders')


	# # Photoshop
	# # os.environ['IC_PS_EXECUTABLE'] = getAppExecPath('Photoshop')
	# # os.environ['IC_PS_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/photoshop')


	# # Bridge
	# # os.environ['IC_BRIDGE_EXECUTABLE'] = getAppExecPath('Bridge')


	# # Mudbox
	# # os.environ['IC_MUDBOX_EXECUTABLE'] = getAppExecPath('Mudbox')
	# # os.environ['IC_MUDBOX_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/mudbox')
	# # os.environ['IC_MUDBOX_SCENES_DIR'] = os_wrapper.absolutePath('$IC_MUDBOX_PROJECT_DIR/scenes')

	# os.environ['MUDBOX_PLUG_IN_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/mudbox/plugins') 
	# os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'


	# # Mari
	# # os.environ['IC_MARI_EXECUTABLE'] = getAppExecPath('Mari')
	# os.environ['IC_MARI_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/mari')
	# os.environ['IC_MARI_SCENES_DIR'] = os_wrapper.absolutePath('$IC_MARI_PROJECT_DIR/scenes')
	# os.environ['IC_MARI_GEO_DIR'] = os_wrapper.absolutePath('$IC_MARI_PROJECT_DIR/geo')
	# os.environ['IC_MARI_TEXTURES_DIR'] = os_wrapper.absolutePath('$IC_MARI_PROJECT_DIR/textures')
	# os.environ['IC_MARI_RENDERS_DIR'] = os_wrapper.absolutePath('$IC_MARI_PROJECT_DIR/renders')

	# # os.environ['MARI_NUKEWORKFLOW_PATH'] = getAppExecPath('Nuke')
	# os.environ['MARI_NUKEWORKFLOW_PATH'] = os.environ['IC_NUKE_EXECUTABLE']
	# os.environ['MARI_DEFAULT_IMAGEPATH'] = os_wrapper.absolutePath('$IC_MARI_PROJECT_DIR/sourceimages')
	# os.environ['MARI_SCRIPT_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/mari/scripts')
	# os.environ['MARI_CACHE'] = os.environ['IC_MARI_SCENES_DIR']
	# os.environ['MARI_WORKING_DIR'] = os.environ['IC_MARI_SCENES_DIR']
	# os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['IC_SHOTPUBLISHDIR']
	# os.environ['MARI_DEFAULT_ARCHIVE_PATH'] = os.environ['IC_MARI_SCENES_DIR']
	# os.environ['MARI_DEFAULT_EXPORT_PATH'] = os.environ['IC_MARI_TEXTURES_DIR']
	# os.environ['MARI_DEFAULT_IMPORT_PATH'] = os.environ['IC_MARI_TEXTURES_DIR']
	# os.environ['MARI_DEFAULT_RENDER_PATH'] = os.environ['IC_MARI_RENDERS_DIR']
	# os.environ['MARI_DEFAULT_CAMERA_PATH'] = os.environ['IC_SHOTPUBLISHDIR']


	# # RealFlow (2013)
	# # os.environ['IC_REALFLOW_EXECUTABLE'] = getAppExecPath('RealFlow')
	# # os.environ['IC_REALFLOW_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/realflow')
	# # os.environ['IC_REALFLOW_SCENES_DIR'] = os_wrapper.absolutePath('$IC_REALFLOW_PROJECT_DIR/$IC_USERNAME')  # Currently needed by openDirs

	# # os.environ['RFDEFAULTPROJECT'] = os_wrapper.absolutePath('$IC_REALFLOW_SCENES_DIR/${IC_JOB}_${IC_SHOT}')  # Curly brackets required for correct variable expansion
	# # os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH'] = os_wrapper.absolutePath('$IC_REALFLOW_SCENES_DIR/.cmdsOrg/commandsOrganizer.dat')
	# os.environ['RF_RSC'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/realflow')
	# os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/realflow/scripts/startup.rfs')
	# os.environ['RFOBJECTSPATH'] = os_wrapper.absolutePath('$IC_SHOTPUBLISHDIR/ma_geoCache/realflow')


	# # Cinema 4D
	# # os.environ['IC_C4D_EXECUTABLE'] = getAppExecPath('Cinema4D')
	# # os.environ['IC_C4D_VERSION'] = str(job_data.getAppVersion('Cinema4D'))
	# os.environ['IC_C4D_PROJECT_DIR'] = os_wrapper.absolutePath('$IC_SHOTPATH/c4d') #temp
	# os.environ['IC_C4D_SCENES_DIR'] = os_wrapper.absolutePath('$IC_C4D_PROJECT_DIR/scenes') #temp

	# os.environ['C4D_PLUGINS_DIR'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/C4D/$IC_C4D_VERSION/plugins')
	# os.environ['C4D_SCRIPTS_DIR'] = os_wrapper.absolutePath('$IC_FILESYSTEM_ROOT/_Library/3D/C4D/$IC_C4D_VERSION/scripts')


	# # Clarisse
	# # sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'clarisse'))


	# # djv_view
	# # os.environ['IC_DJV_EXECUTABLE'] = getAppExecPath('djv_view')
	# # djv_ver = str(job_data.getAppVersion('djv_view'))
	# # djv_embedded_ver = '1.1.0'
	# # if os.environ['IC_RUNNING_OS'] == "Windows":
	# # 	# os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_convert.exe')  # Latest 32-bit version
	# # 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Windows-64/bin/djv_convert.exe' %djv_embedded_ver)
	# # 	os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Windows-64/bin/djv_view.exe' %djv_embedded_ver)

	# # elif os.environ['IC_RUNNING_OS'] == "MacOS":
	# # 	os.environ['DJV_LIB']     = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/lib' %djv_embedded_ver)
	# # 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/bin/djv_convert' %djv_embedded_ver)
	# # 	os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/bin/djv_view.sh' %djv_embedded_ver)
	# # 	# os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/MacOS/djv-1.0.5-OSX-64' %djv_embedded_ver)

	# # else:
	# # 	os.environ['DJV_LIB']     = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/lib' %djv_embedded_ver)
	# # 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/bin/djv_convert' %djv_embedded_ver)
	# # 	os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/bin/djv_view' %djv_embedded_ver)

	# os.environ['DJV_PLAY'] = os.environ['IC_DJV_EXECUTABLE']
	# os.environ['DJV_LIB']  = os_wrapper.absolutePath('%s/../lib' % os.path.dirname(os.environ['IC_DJV_EXECUTABLE']))
	# if os.environ['IC_RUNNING_OS'] == "Windows":
	# 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('%s/djv_convert.exe' % os.path.dirname(os.environ['IC_DJV_EXECUTABLE']))
	# else:  # Mac OS X and Linux
	# 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('%s/djv_convert' % os.path.dirname(os.environ['IC_DJV_EXECUTABLE']))


	# # Deadline Monitor / Slave
	# # os.environ['IC_DEADINE_EXECUTABLE'] = getAppExecPath('Deadline')
	# if os.environ['IC_RUNNING_OS'] == "MacOS":
	# 	os.environ['IC_DEADINE_CMD_EXECUTABLE']   = os_wrapper.absolutePath('%s/../../../Resources/deadlinecommand' % os.path.dirname(os.environ['IC_DEADINE_EXECUTABLE']))
	# else:  # Windows or Linux
	# 	os.environ['IC_DEADINE_CMD_EXECUTABLE']   = os_wrapper.absolutePath('%s/deadlinecommand' % os.path.dirname(os.environ['IC_DEADINE_EXECUTABLE']))


	return True
