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

import appPaths
# import jobs
import osOps
import settingsData
import verbose


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
	jobDataPath = os.path.join(jobPath, os.environ['DATAFILESRELATIVEDIR'])
	shotDataPath = os.path.join(shotPath, os.environ['DATAFILESRELATIVEDIR'])

	# Set basic environment variables
	os.environ['JOB'] = job
	os.environ['SHOT'] = shot
	os.environ['JOBPATH'] = osOps.absolutePath(jobPath)
	os.environ['SHOTPATH'] = osOps.absolutePath(shotPath)
	os.environ['JOBDATA'] = osOps.absolutePath(jobDataPath)
	os.environ['SHOTDATA'] = osOps.absolutePath(shotDataPath)

	osOps.createDir(os.environ['JOBDATA'])

	# Instantiate job / shot settings classes
	jobData = settingsData.settingsData()
	shotData = settingsData.settingsData()
#	defaultData = settingsData.settingsData()
	ap = appPaths.AppPaths()

	jobDataLoaded = jobData.loadXML(os.path.join(jobDataPath, 'jobData.xml'), use_template=False)
	shotDataLoaded = shotData.loadXML(os.path.join(shotDataPath, 'shotData.xml'), use_template=False)
#	defaultData.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'defaultData.xml'))
	ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), use_template=True)

	# ------------------------------------------------------------------------
	# If XML files don't exist, create defaults, and attempt to convert data
	# from Python data files
	jobDataLegacy = False
	if not jobDataLoaded:
		import legacySettings

		# Try to convert from jobData.py to XML (legacy jobs)
		if legacySettings.convertJobData(jobDataPath, jobData, ap):
			jobDataLegacy = True
			jobData.loadXML()
		else:
			return False

	if jobDataLegacy and not shotDataLoaded:
		import legacySettings

		# Try to convert from shotData.py to XML (legacy jobs)
		if legacySettings.convertShotData(shotDataPath, shotData):
			shotData.loadXML()


	# Check if the job is using the old hidden asset publish directory
	assetDir = jobData.getValue('meta', 'assetDir')
	if assetDir:
		os.environ['PUBLISHRELATIVEDIR'] = assetDir
	else:
		import legacySettings

		# Check for existing legacy published assets in the job and shot(s)
		if legacySettings.checkAssetPath():
			assetDir = '.publish'
		else:
			assetDir = 'Assets'  # Perhaps this shouldn't be hard-coded?

		jobData.setValue('meta', 'assetDir', assetDir)
		jobData.saveXML()
		os.environ['PUBLISHRELATIVEDIR'] = assetDir
	# ------------------------------------------------------------------------


	# Set OS identifier strings to get correct app executable paths
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		currentOS = 'win'
	elif os.environ['IC_RUNNING_OS'] == 'Darwin':
		currentOS = 'osx'
	elif os.environ['IC_RUNNING_OS'] == 'Linux':
		currentOS = 'linux'


	# Terminal / Command Prompt
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		os.environ['IC_SHELL_RC'] = osOps.absolutePath('$IC_WORKINGDIR/shell_cmd.bat')
	else:
		os.environ['IC_SHELL_RC'] = osOps.absolutePath('$IC_WORKINGDIR/shell_rc')


	# Job / shot env
#	os.environ['GLOBALPUBLISHDIR']  = osOps.absolutePath(getInheritedValue('other', 'assetlib'))  # Path needs to be translated for OS portability
	os.environ['JOBPUBLISHDIR']     = osOps.absolutePath('$JOBPATH/$PUBLISHRELATIVEDIR')
	os.environ['SHOTPUBLISHDIR']    = osOps.absolutePath('$SHOTPATH/$PUBLISHRELATIVEDIR')
	os.environ['WIPSDIR']           = osOps.absolutePath('$JOBPATH/../Deliverables/WIPS')  # Perhaps this shouldn't be hard-coded?
	os.environ['ELEMENTSLIBRARY']   = osOps.absolutePath(getInheritedValue('other', 'elementslib'))  # Path needs to be translated for OS portability
	os.environ['PRODBOARD']         = getInheritedValue('other', 'prodboard')
	os.environ['UNIT']              = getInheritedValue('units', 'linear')
	os.environ['ANGLE']             = getInheritedValue('units', 'angle')
	os.environ['TIMEFORMAT']        = getInheritedValue('units', 'time')
	os.environ['FPS']               = getInheritedValue('units', 'fps')
#	os.environ['HANDLES']           = getInheritedValue('time', 'handles')  # Using INFRAME & OUTFRAME instead - although not implemented
	os.environ['STARTFRAME']        = getInheritedValue('time', 'rangeStart')
	os.environ['ENDFRAME']          = getInheritedValue('time', 'rangeEnd')
	os.environ['INFRAME']           = getInheritedValue('time', 'inFrame')
	os.environ['OUTFRAME']          = getInheritedValue('time', 'outFrame')
	os.environ['FRAMERANGE']        = '%s-%s' % (os.environ['STARTFRAME'], os.environ['ENDFRAME'])
	os.environ['POSTERFRAME']       = getInheritedValue('time', 'posterFrame')
	os.environ['RESOLUTIONX']       = getInheritedValue('resolution', 'fullWidth')
	os.environ['RESOLUTIONY']       = getInheritedValue('resolution', 'fullHeight')
	os.environ['PROXY_RESOLUTIONX'] = getInheritedValue('resolution', 'proxyWidth')
	os.environ['PROXY_RESOLUTIONY'] = getInheritedValue('resolution', 'proxyHeight')
	os.environ['ASPECTRATIO']       = str(float(os.environ['RESOLUTIONX']) / float(os.environ['RESOLUTIONY']))


	# Application specific environment variables...

	# Maya
	os.environ['MAYAVERSION']         = getAppExecPath('Maya')
	os.environ['MAYARENDERVERSION']   = osOps.absolutePath('%s/Render' %os.path.dirname(os.environ['MAYAVERSION']))
	os.environ['MAYADIR']             = osOps.absolutePath('$SHOTPATH/3D/maya')  # Currently needed by render submitter
	os.environ['MAYASCENESDIR']       = osOps.absolutePath('$MAYADIR/scenes/$IC_USERNAME')  # Currently needed by render submitter
	# os.environ['MAYASOURCEIMAGESDIR'] = osOps.absolutePath('$MAYADIR/sourceimages/$IC_USERNAME')
	os.environ['MAYARENDERSDIR']      = osOps.absolutePath('$MAYADIR/renders/$IC_USERNAME')  # Currently needed by daily publish
	os.environ['MAYAPLAYBLASTSDIR']   = osOps.absolutePath('$MAYADIR/playblasts/$IC_USERNAME')  # Currently needed by daily publish
	os.environ['MAYASHAREDRESOURCES'] = osOps.absolutePath('$FILESYSTEMROOT/_Library/3D/Maya')  # Store this in app settings / ic global prefs?

	try:
		maya_ver = jobData.getAppVersion('Maya')
		os.environ['MAYA_VER'] = maya_ver

		os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = '0'
		os.environ['MAYA_FORCE_PANEL_FOCUS'] = '0'  # This should prevent panel stealing focus from Qt window on keypress.
		os.environ['MAYA_DISABLE_CLIC_IPM'] = '1'  # Disable the In Product Messaging button (should improve Maya startup & shutdown time).
		os.environ['MAYA_DISABLE_CIP'] = '1'  # Disable the Customer Involvement Program (should improve Maya startup & shutdown time).

		pluginsPath = osOps.absolutePath('$IC_BASEDIR/rsc/maya/plugins') + os.pathsep \
					+ osOps.absolutePath('$MAYASHAREDRESOURCES/%s/plug-ins' %maya_ver)
		scriptsPath = osOps.absolutePath('$IC_BASEDIR/rsc/maya/maya__env__') + os.pathsep \
					+ osOps.absolutePath('$IC_BASEDIR/rsc/maya/scripts') + os.pathsep \
					+ osOps.absolutePath('$MAYADIR/scripts') + os.pathsep \
					+ osOps.absolutePath('$JOBPUBLISHDIR/scripts') + os.pathsep \
					+ osOps.absolutePath('$SHOTPUBLISHDIR/scripts') + os.pathsep \
					+ osOps.absolutePath('$MAYASHAREDRESOURCES/scripts') + os.pathsep \
					+ osOps.absolutePath('$MAYASHAREDRESOURCES/%s/scripts' %maya_ver)
		if os.environ['IC_RUNNING_OS'] == 'Linux':  # Append the '%B' bitmap placeholder token required for Linux
			iconsPath = osOps.absolutePath('$IC_BASEDIR/rsc/maya/icons/%B') + os.pathsep \
					  + osOps.absolutePath('$JOBPUBLISHDIR/icons/%B') + os.pathsep \
					  + osOps.absolutePath('$MAYASHAREDRESOURCES/%s/icons/%B' %maya_ver)
		else:
			iconsPath = osOps.absolutePath('$IC_BASEDIR/rsc/maya/icons') + os.pathsep \
					  + osOps.absolutePath('$JOBPUBLISHDIR/icons') + os.pathsep \
					  + osOps.absolutePath('$MAYASHAREDRESOURCES/%s/icons' %maya_ver)

		#os.environ['MAYA_MODULE_PATH'] = 
		#os.environ['MAYA_PRESET_PATH'] = osOps.absolutePath('$IC_BASEDIR/rsc/maya/presets')
		#os.environ['MI_CUSTOM_SHADER_PATH'] = osOps.absolutePath('$IC_BASEDIR/rsc/maya/shaders/include')
		#os.environ['MI_LIBRARY_PATH'] = osOps.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
		#os.environ['VRAY_FOR_MAYA_SHADERS'] = osOps.absolutePath('$IC_BASEDIR/rsc/maya/shaders')
		#os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] += os.pathsep + osOps.absolutePath('$IC_BASEDIR/rsc/maya/plugins')

		if os.environ['IC_RUNNING_OS'] == 'Windows':  # Set up centralised deployment of Redshift plugin for Maya
			# if getAppExecPath('Redshift') is not "":
			if getAppExecPath('rs') is not "":
				os.environ['REDSHIFT_COREDATAPATH']         = getAppExecPath('Redshift')
				os.environ['REDSHIFT_COMMON_ROOT']          = osOps.absolutePath('$REDSHIFT_COREDATAPATH/Plugins/Maya/Common')
				os.environ['REDSHIFT_PLUG_IN_PATH']         = osOps.absolutePath('$REDSHIFT_COREDATAPATH/Plugins/Maya/%s/nt-x86-64' %maya_ver)
				os.environ['REDSHIFT_SCRIPT_PATH']          = osOps.absolutePath('$REDSHIFT_COMMON_ROOT/scripts')
				os.environ['REDSHIFT_XBMLANGPATH']          = osOps.absolutePath('$REDSHIFT_COMMON_ROOT/icons')
				os.environ['REDSHIFT_RENDER_DESC_PATH']     = osOps.absolutePath('$REDSHIFT_COMMON_ROOT/rendererDesc')
				os.environ['REDSHIFT_CUSTOM_TEMPLATE_PATH'] = osOps.absolutePath('$REDSHIFT_COMMON_ROOT/scripts/NETemplates')
				os.environ['REDSHIFT_MAYAEXTENSIONSPATH']   = osOps.absolutePath('$REDSHIFT_PLUG_IN_PATH/extensions')
				os.environ['REDSHIFT_PROCEDURALSPATH']      = osOps.absolutePath('$REDSHIFT_COREDATAPATH/Procedurals')
				pluginsPath += os.pathsep + os.environ['REDSHIFT_PLUG_IN_PATH']
				scriptsPath += os.pathsep + os.environ['REDSHIFT_SCRIPT_PATH']
				iconsPath   += os.pathsep + os.environ['REDSHIFT_XBMLANGPATH']
				os.environ['MAYA_RENDER_DESC_PATH'] = os.environ['REDSHIFT_RENDER_DESC_PATH']
				# os.environ['PATH'] += os.pathsep + os.environ['REDSHIFT_PLUG_IN_PATH']
				os.environ['PATH'] += os.pathsep + os.environ['REDSHIFT_PLUG_IN_PATH'] + os.pathsep + osOps.absolutePath('$REDSHIFT_COREDATAPATH/bin')
				os.environ['MAYA_CUSTOM_TEMPLATE_PATH'] = os.environ['REDSHIFT_CUSTOM_TEMPLATE_PATH']
			os.environ['redshift_LICENSE'] = "62843@10.105.11.11"

		os.environ['MAYA_SHELF_PATH'] = osOps.absolutePath('$JOBPUBLISHDIR/ma_shelves')
		os.environ['MAYA_PLUG_IN_PATH'] = pluginsPath
		os.environ['MAYA_SCRIPT_PATH'] = scriptsPath
		os.environ['PYTHONPATH'] = scriptsPath
		os.environ['XBMLANGPATH'] = iconsPath

	except (AttributeError, KeyError, TypeError):
		verbose.warning("Unable to set Maya environment variables - please check job settings to ensure Maya version is set.")


	# Nuke
	os.environ['NUKEVERSION']     = getAppExecPath('Nuke')
	os.environ['NUKE_VER']        = jobData.getAppVersion('Nuke')  # Temporary for Deadline submit
	os.environ['NUKEDIR']         = osOps.absolutePath('$SHOTPATH/2D/nuke')  # Currently needed by render submitter
	# os.environ['NUKEELEMENTSDIR'] = osOps.absolutePath('$NUKEDIR/elements/$IC_USERNAME')
	os.environ['NUKESCRIPTSDIR']  = osOps.absolutePath('$NUKEDIR/scripts/$IC_USERNAME')  # Currently needed by render submitter
	os.environ['NUKERENDERSDIR']  = osOps.absolutePath('$NUKEDIR/renders/$IC_USERNAME')  # Currently needed by daily publish
	os.environ['NUKE_PATH']       = osOps.absolutePath('$IC_BASEDIR/rsc/nuke')


	# Hiero / HieroPlayer
	os.environ['HIEROPLAYERVERSION'] = getAppExecPath('HieroPlayer')
	os.environ['HIEROEDITORIALPATH'] = osOps.absolutePath('$JOBPATH/../Editorial/Hiero')
	os.environ['HIERO_PLUGIN_PATH']  = osOps.absolutePath('$IC_BASEDIR/rsc/hiero')


	# After Effects
	os.environ['AFXVERSION']     = getAppExecPath('AfterEffects')
	# os.environ['AFXDIR']         = osOps.absolutePath('$SHOTPATH/2D/aftereffects')
	# os.environ['AFXELEMENTSDIR'] = osOps.absolutePath('$AFXDIR/elements/$IC_USERNAME')
	# os.environ['AFXCOMPSDIR']    = osOps.absolutePath('$AFXDIR/comps/$IC_USERNAME')
	# os.environ['AFXRENDERSDIR']  = osOps.absolutePath('$AFXDIR/renders/$IC_USERNAME')


	# Photoshop
	os.environ['PSVERSION'] = getAppExecPath('Photoshop')
	# os.environ['PSDIR']     = osOps.absolutePath('$SHOTPATH/2D/photoshop')


	# Bridge
	os.environ['BRIDGEVERSION'] = getAppExecPath('Bridge')


	# Mudbox
	os.environ['MUDBOXVERSION']            = getAppExecPath('Mudbox')
	# os.environ['MUDBOXDIR']                = osOps.absolutePath('$SHOTPATH/3D/mudbox')
	# os.environ['MUDBOXSCENESDIR']          = osOps.absolutePath('$MUDBOXDIR/scenes/$IC_USERNAME')
	os.environ['MUDBOX_PLUG_IN_PATH']      = osOps.absolutePath('$IC_BASEDIR/rsc/mudbox/plugins') 
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'


	# Mari
	os.environ['MARIVERSION']                = getAppExecPath('Mari')
	os.environ['MARI_NUKEWORKFLOW_PATH']     = getAppExecPath('Nuke')
	os.environ['MARIDIR']                    = osOps.absolutePath('$SHOTPATH/3D/mari')
	os.environ['MARISCENESDIR']              = osOps.absolutePath('$MARIDIR/scenes/$IC_USERNAME')
	os.environ['MARIGEODIR']                 = osOps.absolutePath('$MARIDIR/geo/$IC_USERNAME')
	os.environ['MARITEXTURESDIR']            = osOps.absolutePath('$MARIDIR/textures/$IC_USERNAME')
	os.environ['MARIRENDERSDIR']             = osOps.absolutePath('$MARIDIR/renders/$IC_USERNAME')
	os.environ['MARI_DEFAULT_IMAGEPATH']     = osOps.absolutePath('$MARIDIR/sourceimages/$IC_USERNAME')
	os.environ['MARI_SCRIPT_PATH']           = osOps.absolutePath('$IC_BASEDIR/rsc/mari/scripts')
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
	# os.environ['REALFLOWDIR']                        = osOps.absolutePath('$SHOTPATH/3D/realflow')
	# os.environ['REALFLOWSCENESDIR']                  = osOps.absolutePath('$REALFLOWDIR/$IC_USERNAME')
	# os.environ['RFDEFAULTPROJECT']                   = osOps.absolutePath('$REALFLOWSCENESDIR/${JOB}_${SHOT}')  # Curly brackets required for correct variable expansion
	# os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH']    = osOps.absolutePath('$REALFLOWSCENESDIR/.cmdsOrg/commandsOrganizer.dat')
	os.environ['RF_RSC']                             = osOps.absolutePath('$IC_BASEDIR/rsc/realflow')
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = osOps.absolutePath('$IC_BASEDIR/rsc/realflow/scripts/startup.rfs')
	os.environ['RFOBJECTSPATH']                      = osOps.absolutePath('$SHOTPUBLISHDIR/ma_geoCache/realflow')


	# Cinema 4D
	os.environ['C4DVERSION']   = getAppExecPath('Cinema4D')
	# os.environ['C4DDIR']       = osOps.absolutePath('$SHOTPATH/3D/c4d')
	# os.environ['C4DSCENESDIR'] = osOps.absolutePath('$C4DDIR/scenes/$IC_USERNAME')


	# Clarisse
	# sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'clarisse'))


	# djv_view
	os.environ['DJVVERSION'] = getAppExecPath('djv_view')
	# djv_ver = jobData.getAppVersion('djv_view')
	# djv_embedded_ver = '1.1.0'
	# if os.environ['IC_RUNNING_OS'] == 'Windows':
	# 	#os.environ['DJV_CONVERT'] = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_convert.exe')  # Latest 32-bit version
	# 	os.environ['DJV_CONVERT'] = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Windows-64/bin/djv_convert.exe' %djv_embedded_ver)
	# 	os.environ['DJV_PLAY']    = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Windows-64/bin/djv_view.exe' %djv_embedded_ver)

	# elif os.environ['IC_RUNNING_OS'] == 'Darwin':
	# 	os.environ['DJV_LIB']     = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/lib' %djv_embedded_ver)
	# 	os.environ['DJV_CONVERT'] = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/bin/djv_convert' %djv_embedded_ver)
	# 	os.environ['DJV_PLAY']    = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/Resources/bin/djv_view.sh' %djv_embedded_ver)
	# 	# os.environ['DJV_PLAY']    = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-OSX-64.app/Contents/MacOS/djv-1.0.5-OSX-64' %djv_embedded_ver)

	# else:
	# 	os.environ['DJV_LIB']     = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/lib' %djv_embedded_ver)
	# 	os.environ['DJV_CONVERT'] = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/bin/djv_convert' %djv_embedded_ver)
	# 	os.environ['DJV_PLAY']    = osOps.absolutePath('$IC_BASEDIR/external_apps/djv/djv-%s-Linux-64/bin/djv_view' %djv_embedded_ver)

	os.environ['DJV_PLAY'] = os.environ['DJVVERSION']
	os.environ['DJV_LIB']  = osOps.absolutePath('%s/../lib' %os.path.dirname(os.environ['DJVVERSION']))
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		os.environ['DJV_CONVERT'] = osOps.absolutePath('%s/djv_convert.exe' %os.path.dirname(os.environ['DJVVERSION']))
	else:  # Mac OS X and Linux
		os.environ['DJV_CONVERT'] = osOps.absolutePath('%s/djv_convert' %os.path.dirname(os.environ['DJVVERSION']))


	# Deadline Monitor / Slave
	os.environ['DEADLINEVERSION'] = getAppExecPath('Deadline')
	if os.environ['IC_RUNNING_OS'] == 'Darwin':
		os.environ['DEADLINECMDVERSION']   = osOps.absolutePath('%s/../../../Resources/deadlinecommand' %os.path.dirname(os.environ['DEADLINEVERSION']))
	else:  # Windows or Linux
		os.environ['DEADLINECMDVERSION']   = osOps.absolutePath('%s/deadlinecommand' %os.path.dirname(os.environ['DEADLINEVERSION']))
	# os.environ['DEADLINEMONITORVERSION'] = getAppExecPath('DeadlineMonitor')
	# os.environ['DEADLINESLAVEVERSION']   = getAppExecPath('DeadlineSlave')


	return True

