#!/usr/bin/python

# [Icarus] job__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# Sets up job- and shot-related environment variables.
# TODO: This module needs total re-think in light of dynamic app launching.


import os
import sys

from . import appPaths
# from . import jobs
from . import os_wrapper
from . import settingsData
from . import verbose


def setEnv(job, shot, shotPath):
	""" Set job and shot environment variables.
	"""
	def getInheritedValue(category, setting):
		""" First try to get the value from the shot data, if it returns
			nothing then look in job data instead.
		"""
		value = shotData.getValue(category, setting)
		if value == "":
			value = jobData.getValue(category, setting)
			# if value == "":
			# 	value = defaultData.getValue(category, setting)

		return value


	def getAppExecPath(app):
		""" Return the path to the executable for the specified app on the
			current OS.
		"""
		return ap.getPath(app, getInheritedValue('apps', app), currentOS)


	jobPath = os.path.split(shotPath)[0]
	jobDataPath = os.path.join(jobPath, os.environ['IC_METADATA'])
	shotDataPath = os.path.join(shotPath, os.environ['IC_METADATA'])

	# Set basic environment variables
	os.environ['JOB'] = job
	os.environ['SHOT'] = shot
	os.environ['JOBPATH'] = os_wrapper.absolutePath(jobPath)
	os.environ['SHOTPATH'] = os_wrapper.absolutePath(shotPath)
	os.environ['JOBDATA'] = os_wrapper.absolutePath(jobDataPath)
	os.environ['SHOTDATA'] = os_wrapper.absolutePath(shotDataPath)

	os_wrapper.createDir(os.environ['JOBDATA'])

	# Instantiate job / shot settings classes
	jobData = settingsData.SettingsData()
	shotData = settingsData.SettingsData()
	#defaultData = settingsData.SettingsData()
	ap = appPaths.AppPaths()

	jobDataLoaded = jobData.loadXML(os.path.join(jobDataPath, 'jobData.xml'), use_template=False)
	shotDataLoaded = shotData.loadXML(os.path.join(shotDataPath, 'shotData.xml'), use_template=False)
	#defaultData.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'defaultData.xml'))
	ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), use_template=True)

	# ------------------------------------------------------------------------
	# If XML files don't exist, create defaults, and attempt to convert data
	# from Python data files
	jobDataLegacy = False
	if not jobDataLoaded:
		from . import legacySettings

		# Try to convert from jobData.py to XML (legacy jobs)
		if legacySettings.convertJobData(jobDataPath, jobData, ap):
			jobDataLegacy = True
			jobData.loadXML()
		else:
			return False

	if jobDataLegacy and not shotDataLoaded:
		from . import legacySettings

		# Try to convert from shotData.py to XML (legacy jobs)
		if legacySettings.convertShotData(shotDataPath, shotData):
			shotData.loadXML()


	# Check if the job is using the old hidden asset publish directory
	assetDir = jobData.getValue('meta', 'assetDir')
	if assetDir:
		os.environ['IC_ASSETDIR'] = assetDir
	else:
		from . import legacySettings

		# Check for existing legacy published assets in the job and shot(s)
		if legacySettings.checkAssetPath():
			assetDir = '.publish'
		else:
			assetDir = 'Assets'  # Perhaps this shouldn't be hard-coded?

		jobData.setValue('meta', 'assetDir', assetDir)
		jobData.saveXML()
		os.environ['IC_ASSETDIR'] = assetDir
	# ------------------------------------------------------------------------


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
	#os.environ['GLOBALPUBLISHDIR']  = os_wrapper.absolutePath(getInheritedValue('other', 'assetlib'))  # Path needs to be translated for OS portability
	os.environ['JOBPUBLISHDIR']     = os_wrapper.absolutePath('$JOBPATH/$IC_ASSETDIR')
	os.environ['SHOTPUBLISHDIR']    = os_wrapper.absolutePath('$SHOTPATH/$IC_ASSETDIR')
	os.environ['WIPSDIR']           = os_wrapper.absolutePath('$JOBPATH/../Deliverables/WIPS')  # Perhaps this shouldn't be hard-coded?
	os.environ['ELEMENTSLIBRARY']   = os_wrapper.absolutePath(getInheritedValue('other', 'elementslib'))  # Path needs to be translated for OS portability
	os.environ['PRODBOARD']         = getInheritedValue('other', 'prodboard')
	os.environ['UNIT']              = getInheritedValue('units', 'linear')
	os.environ['ANGLE']             = getInheritedValue('units', 'angle')
	os.environ['TIMEFORMAT']        = getInheritedValue('units', 'time')
	os.environ['FPS']               = getInheritedValue('units', 'fps')
	os.environ['STARTFRAME']        = getInheritedValue('time', 'rangeStart')
	os.environ['ENDFRAME']          = getInheritedValue('time', 'rangeEnd')
	os.environ['INFRAME']           = getInheritedValue('time', 'inFrame')
	os.environ['OUTFRAME']          = getInheritedValue('time', 'outFrame')
	os.environ['POSTERFRAME']       = getInheritedValue('time', 'posterFrame')
	os.environ['RESOLUTIONX']       = getInheritedValue('resolution', 'fullWidth')
	os.environ['RESOLUTIONY']       = getInheritedValue('resolution', 'fullHeight')
	os.environ['PROXY_RESOLUTIONX'] = getInheritedValue('resolution', 'proxyWidth')
	os.environ['PROXY_RESOLUTIONY'] = getInheritedValue('resolution', 'proxyHeight')
	os.environ['ASPECTRATIO']       = str(float(os.environ['RESOLUTIONX']) / float(os.environ['RESOLUTIONY']))
	os.environ['EDITOR']            = getAppExecPath('SublimeText')  # Make dynamic 


	# Application specific environment variables...
	# TODO: move out to individual modules

	# Redshift centralised deployment
	if getAppExecPath('Redshift') is not "":
		# os.environ['redshift_LICENSE'] = "port@hostname"
		os.environ['REDSHIFT_COREDATAPATH'] = getAppExecPath('Redshift')
	elif os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['REDSHIFT_COREDATAPATH'] = "C:/ProgramData/Redshift"
	elif os.environ['IC_RUNNING_OS'] == "MacOS":
		os.environ['REDSHIFT_COREDATAPATH'] = "/usr/redshift"
	elif os.environ['IC_RUNNING_OS'] == "Linux":
		os.environ['REDSHIFT_COREDATAPATH'] = "/Applications/redshift"


	# Maya
	os.environ['MAYAVERSION']         = getAppExecPath('Maya')
	os.environ['MAYARENDERVERSION']   = os_wrapper.absolutePath('%s/Render' %os.path.dirname(os.environ['MAYAVERSION']))
	os.environ['MAYADIR']             = os_wrapper.absolutePath('$SHOTPATH/3D/maya')  # Currently needed by render submitter
	os.environ['MAYASCENESDIR']       = os_wrapper.absolutePath('$MAYADIR/scenes/$IC_USERNAME')  # Currently needed by render submitter
	os.environ['MAYASOURCEIMAGESDIR'] = os_wrapper.absolutePath('$MAYADIR/sourceimages/$IC_USERNAME')  # Currently needed by openDirs
	os.environ['MAYARENDERSDIR']      = os_wrapper.absolutePath('$MAYADIR/renders/$IC_USERNAME')  # Currently needed by daily publish
	os.environ['MAYAPLAYBLASTSDIR']   = os_wrapper.absolutePath('$MAYADIR/playblasts/$IC_USERNAME')  # Currently needed by daily publish
	os.environ['MAYASHAREDRESOURCES'] = os_wrapper.absolutePath('$FILESYSTEMROOT/_Library/3D/Maya')  # Store this in app settings / ic global prefs?

	try:
		maya_ver = str(jobData.getAppVersion('Maya'))
		os.environ['MAYA_VER'] = maya_ver

		os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = "0"
		os.environ['MAYA_ENABLE_LEGACY_VIEWPORT'] = "1"
		os.environ['MAYA_FORCE_PANEL_FOCUS'] = "0"  # This should prevent panel stealing focus from Qt window on keypress.
		os.environ['MAYA_DISABLE_CLIC_IPM'] = "1"  # Disable the In Product Messaging button (should improve Maya startup & shutdown time).
		os.environ['MAYA_DISABLE_CIP'] = "1"  # Disable the Customer Involvement Program (should improve Maya startup & shutdown time).

		pluginsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/plugins') + os.pathsep \
					+ os_wrapper.absolutePath('$MAYASHAREDRESOURCES/%s/plug-ins' %maya_ver)
		scriptsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/maya__env__') + os.pathsep \
					+ os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/scripts') + os.pathsep \
					+ os_wrapper.absolutePath('$MAYADIR/scripts') + os.pathsep \
					+ os_wrapper.absolutePath('$JOBPUBLISHDIR/scripts') + os.pathsep \
					+ os_wrapper.absolutePath('$SHOTPUBLISHDIR/scripts') + os.pathsep \
					+ os_wrapper.absolutePath('$MAYASHAREDRESOURCES/scripts') + os.pathsep \
					+ os_wrapper.absolutePath('$MAYASHAREDRESOURCES/%s/scripts' %maya_ver)
		iconsPath = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/icons') + os.pathsep \
				  + os_wrapper.absolutePath('$JOBPUBLISHDIR/icons') + os.pathsep \
				  + os_wrapper.absolutePath('$MAYASHAREDRESOURCES/%s/icons' %maya_ver)
		if os.environ['IC_RUNNING_OS'] == "Linux":  # Append the '%B' bitmap placeholder token required for Linux
			iconsPathsModified = []
			for path in iconsPath.split(os.pathsep):
				iconsPathsModified.append(path + r"/%B")
			iconsPath = os.pathsep.join(n for n in iconsPathsModified)

		#os.environ['MAYA_MODULE_PATH'] = 
		#os.environ['MAYA_PRESET_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/presets')
		#os.environ['MI_CUSTOM_SHADER_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders/include')
		#os.environ['MI_LIBRARY_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
		#os.environ['VRAY_FOR_MAYA_SHADERS'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
		#os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] += os.pathsep + os_wrapper.absolutePath('$IC_BASEDIR/rsc/maya/plugins')

		os.environ['MAYA_SHELF_PATH'] = os_wrapper.absolutePath('$JOBPUBLISHDIR/ma_shelves')
		os.environ['MAYA_PLUG_IN_PATH'] = pluginsPath
		os.environ['MAYA_SCRIPT_PATH'] = scriptsPath
		os.environ['PYTHONPATH'] = scriptsPath
		os.environ['XBMLANGPATH'] = iconsPath

	except (AttributeError, KeyError, TypeError):
		verbose.warning("Unable to set Maya environment variables - please check job settings to ensure Maya version is set.")


	# Nuke
	os.environ['NUKEVERSION']     = getAppExecPath('Nuke')
	os.environ['NUKE_VER']        = str(jobData.getAppVersion('Nuke'))  # Temporary for Deadline submit
	os.environ['NUKEDIR']         = os_wrapper.absolutePath('$SHOTPATH/2D/nuke')  # Currently needed by render submitter
	os.environ['NUKEELEMENTSDIR'] = os_wrapper.absolutePath('$NUKEDIR/elements/$IC_USERNAME')  # Currently needed by openDirs
	os.environ['NUKESCRIPTSDIR']  = os_wrapper.absolutePath('$NUKEDIR/scripts/$IC_USERNAME')  # Currently needed by render submitter
	os.environ['NUKERENDERSDIR']  = os_wrapper.absolutePath('$NUKEDIR/renders/$IC_USERNAME')  # Currently needed by daily publish
	os.environ['NUKE_PATH']       = os_wrapper.absolutePath('$IC_BASEDIR/rsc/nuke')


	# Hiero / HieroPlayer
	os.environ['HIEROPLAYERVERSION'] = getAppExecPath('HieroPlayer')
	os.environ['HIEROEDITORIALPATH'] = os_wrapper.absolutePath('$JOBPATH/../Editorial/Hiero')
	os.environ['HIERO_PLUGIN_PATH']  = os_wrapper.absolutePath('$IC_BASEDIR/rsc/hiero')


	# After Effects
	os.environ['AFXVERSION']     = getAppExecPath('AfterEffects')
	# os.environ['AFXDIR']         = os_wrapper.absolutePath('$SHOTPATH/2D/aftereffects')
	# os.environ['AFXELEMENTSDIR'] = os_wrapper.absolutePath('$AFXDIR/elements/$IC_USERNAME')
	# os.environ['AFXCOMPSDIR']    = os_wrapper.absolutePath('$AFXDIR/comps/$IC_USERNAME')
	# os.environ['AFXRENDERSDIR']  = os_wrapper.absolutePath('$AFXDIR/renders/$IC_USERNAME')


	# Photoshop
	os.environ['PSVERSION'] = getAppExecPath('Photoshop')
	# os.environ['PSDIR']     = os_wrapper.absolutePath('$SHOTPATH/2D/photoshop')


	# Bridge
	os.environ['BRIDGEVERSION'] = getAppExecPath('Bridge')


	# Mudbox
	os.environ['MUDBOXVERSION']            = getAppExecPath('Mudbox')
	# os.environ['MUDBOXDIR']                = os_wrapper.absolutePath('$SHOTPATH/3D/mudbox')
	# os.environ['MUDBOXSCENESDIR']          = os_wrapper.absolutePath('$MUDBOXDIR/scenes/$IC_USERNAME')
	os.environ['MUDBOX_PLUG_IN_PATH']      = os_wrapper.absolutePath('$IC_BASEDIR/rsc/mudbox/plugins') 
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'


	# Mari
	os.environ['MARIVERSION']                = getAppExecPath('Mari')
	os.environ['MARI_NUKEWORKFLOW_PATH']     = getAppExecPath('Nuke')
	os.environ['MARIDIR']                    = os_wrapper.absolutePath('$SHOTPATH/3D/mari')
	os.environ['MARISCENESDIR']              = os_wrapper.absolutePath('$MARIDIR/scenes/$IC_USERNAME')
	os.environ['MARIGEODIR']                 = os_wrapper.absolutePath('$MARIDIR/geo/$IC_USERNAME')
	os.environ['MARITEXTURESDIR']            = os_wrapper.absolutePath('$MARIDIR/textures/$IC_USERNAME')
	os.environ['MARIRENDERSDIR']             = os_wrapper.absolutePath('$MARIDIR/renders/$IC_USERNAME')
	os.environ['MARI_DEFAULT_IMAGEPATH']     = os_wrapper.absolutePath('$MARIDIR/sourceimages/$IC_USERNAME')
	os.environ['MARI_SCRIPT_PATH']           = os_wrapper.absolutePath('$IC_BASEDIR/rsc/mari/scripts')
	os.environ['MARI_CACHE']                 = os.environ['MARISCENESDIR']
	os.environ['MARI_WORKING_DIR']           = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['SHOTPUBLISHDIR']
	os.environ['MARI_DEFAULT_ARCHIVE_PATH']  = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_EXPORT_PATH']   = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_IMPORT_PATH']   = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_RENDER_PATH']   = os.environ['MARIRENDERSDIR']
	os.environ['MARI_DEFAULT_CAMERA_PATH']   = os.environ['SHOTPUBLISHDIR']


	# RealFlow (2013)
	os.environ['REALFLOWVERSION']                    = getAppExecPath('RealFlow')
	# os.environ['REALFLOWDIR']                        = os_wrapper.absolutePath('$SHOTPATH/3D/realflow')
	# os.environ['REALFLOWSCENESDIR']                  = os_wrapper.absolutePath('$REALFLOWDIR/$IC_USERNAME')  # Currently needed by openDirs
	# os.environ['RFDEFAULTPROJECT']                   = os_wrapper.absolutePath('$REALFLOWSCENESDIR/${JOB}_${SHOT}')  # Curly brackets required for correct variable expansion
	# os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH']    = os_wrapper.absolutePath('$REALFLOWSCENESDIR/.cmdsOrg/commandsOrganizer.dat')
	os.environ['RF_RSC']                             = os_wrapper.absolutePath('$IC_BASEDIR/rsc/realflow')
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = os_wrapper.absolutePath('$IC_BASEDIR/rsc/realflow/scripts/startup.rfs')
	os.environ['RFOBJECTSPATH']                      = os_wrapper.absolutePath('$SHOTPUBLISHDIR/ma_geoCache/realflow')


	# Cinema 4D
	c4d_ver = str(jobData.getAppVersion('Cinema4D'))
	os.environ['C4DVERSION']      = getAppExecPath('Cinema4D')
	os.environ['C4DDIR']          = os_wrapper.absolutePath('$SHOTPATH/3D/c4d') #temp
	os.environ['C4DSCENESDIR']    = os_wrapper.absolutePath('$C4DDIR/scenes/$IC_USERNAME') #temp
	os.environ['C4D_PLUGINS_DIR'] = os_wrapper.absolutePath('$FILESYSTEMROOT/_Library/3D/C4D/%s/plugins' %c4d_ver)
	os.environ['C4D_SCRIPTS_DIR'] = os_wrapper.absolutePath('$FILESYSTEMROOT/_Library/3D/C4D/%s/scripts' %c4d_ver)


	# Clarisse
	# sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'clarisse'))


	# djv_view
	os.environ['DJVVERSION'] = getAppExecPath('djv_view')
	# djv_ver = str(jobData.getAppVersion('djv_view'))
	# djv_embedded_ver = '1.1.0'
	# if os.environ['IC_RUNNING_OS'] == "Windows":
	# 	# os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_convert.exe')  # Latest 32-bit version
	# 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Windows-64/bin/djv_convert.exe' %djv_embedded_ver)
	# 	os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Windows-64/bin/djv_view.exe' %djv_embedded_ver)

	# elif os.environ['IC_RUNNING_OS'] == "MacOS":
	# 	os.environ['DJV_LIB']     = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/lib' %djv_embedded_ver)
	# 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/bin/djv_convert' %djv_embedded_ver)
	# 	os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/bin/djv_view.sh' %djv_embedded_ver)
	# 	# os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/MacOS/djv-1.0.5-OSX-64' %djv_embedded_ver)

	# else:
	# 	os.environ['DJV_LIB']     = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/lib' %djv_embedded_ver)
	# 	os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/bin/djv_convert' %djv_embedded_ver)
	# 	os.environ['DJV_PLAY']    = os_wrapper.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/bin/djv_view' %djv_embedded_ver)

	os.environ['DJV_PLAY'] = os.environ['DJVVERSION']
	os.environ['DJV_LIB']  = os_wrapper.absolutePath('%s/../lib' %os.path.dirname(os.environ['DJVVERSION']))
	if os.environ['IC_RUNNING_OS'] == "Windows":
		os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('%s/djv_convert.exe' %os.path.dirname(os.environ['DJVVERSION']))
	else:  # Mac OS X and Linux
		os.environ['DJV_CONVERT'] = os_wrapper.absolutePath('%s/djv_convert' %os.path.dirname(os.environ['DJVVERSION']))


	# Deadline Monitor / Slave
	os.environ['DEADLINEVERSION'] = getAppExecPath('Deadline')
	if os.environ['IC_RUNNING_OS'] == "MacOS":
		os.environ['DEADLINECMDVERSION']   = os_wrapper.absolutePath('%s/../../../Resources/deadlinecommand' %os.path.dirname(os.environ['DEADLINEVERSION']))
	else:  # Windows or Linux
		os.environ['DEADLINECMDVERSION']   = os_wrapper.absolutePath('%s/deadlinecommand' %os.path.dirname(os.environ['DEADLINEVERSION']))
	# os.environ['DEADLINEMONITORVERSION'] = getAppExecPath('DeadlineMonitor')
	# os.environ['DEADLINESLAVEVERSION']   = getAppExecPath('DeadlineSlave')


	return True

