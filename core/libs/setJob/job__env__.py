#!/usr/bin/python

# [Icarus] job__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Sets up job- and shot-related environment variables.


import os, sys
import appPaths, jobs, jobSettings, osOps, verbose


def setEnv(envVars):
	""" Set job and shot environment variables.
	"""

	def getInheritedValue(category, setting):
		""" First try to get the value from the shot data, if it returns nothing then look in job data instead.
		"""
		value = shotData.getValue(category, setting)
		if value == "":
			value = jobData.getValue(category, setting)
			# if value == "":
			# 	value = defaultData.getValue(category, setting)

		return value


	def getAppExecPath(app):
		""" Return the path to the executable for the specified app on the current OS.
		"""
		return ap.getPath(app, getInheritedValue('apps', app), currentOS)


	job, shot, shotPath = envVars
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
	jobData = jobSettings.jobSettings()
	shotData = jobSettings.jobSettings()
#	defaultData = jobSettings.jobSettings()
	ap = appPaths.appPaths()

	jobDataLoaded = jobData.loadXML( os.path.join(jobDataPath, 'jobData.xml') )
	shotDataLoaded = shotData.loadXML( os.path.join(shotDataPath, 'shotData.xml') )
#	defaultData.loadXML( os.path.join(os.environ['ICCONFIGDIR'], 'defaultData.xml') )
	ap.loadXML( os.path.join(os.environ['ICCONFIGDIR'], 'appPaths.xml') )

	# If XML files don't exist, create defaults, and attempt to convert data from Python data files
	if not jobDataLoaded:
		import legacySettings

		# Try to convert from jobData.py to XML (legacy jobs)
		if legacySettings.convertJobData(jobDataPath, jobData, ap):
			jobData.loadXML()
		else:
			return False

	if not shotDataLoaded:
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
			assetDir = 'Assets' # perhaps this shouldn't be hard-coded?

		jobData.setValue('meta', 'assetDir', assetDir)
		jobData.saveXML()
		os.environ['PUBLISHRELATIVEDIR'] = assetDir


	# Set OS identifier strings to get correct app executable paths
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		currentOS = 'win'
	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		currentOS = 'osx'
	elif os.environ['ICARUS_RUNNING_OS'] == 'Linux':
		currentOS = 'linux'


	# Terminal / Command Prompt
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.environ['GPS_RC'] = osOps.absolutePath('$PIPELINE/core/ui/gps_cmd.bat')
	else:
		os.environ['GPS_RC'] = osOps.absolutePath('$PIPELINE/core/ui/.gps_rc')


	# Root paths for cross-platform support
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.environ['FILESYSTEMROOT'] = jobs.win_root
	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		os.environ['FILESYSTEMROOT'] = jobs.osx_root
	else:
		os.environ['FILESYSTEMROOT'] = jobs.linux_root

	os.environ['JOBSROOTWIN'] = jobs.win_root
	os.environ['JOBSROOTOSX'] = jobs.osx_root
#	os.environ['JOBSROOTLINUX'] = jobs.linux_root # not currently required as Linux & OSX mount points should be the same


	# Job / shot env
#	os.environ['GLOBALPUBLISHDIR']  = osOps.absolutePath(getInheritedValue('other', 'assetlib')) # path needs to be translated for OS portability
	os.environ['JOBPUBLISHDIR']     = osOps.absolutePath('$JOBPATH/$PUBLISHRELATIVEDIR')
	os.environ['SHOTPUBLISHDIR']    = osOps.absolutePath('$SHOTPATH/$PUBLISHRELATIVEDIR')
	os.environ['WIPSDIR']           = osOps.absolutePath('$JOBPATH/../Deliverables/WIPS') # perhaps this shouldn't be hard-coded?
	os.environ['RECENTFILESDIR']    = osOps.absolutePath('$ICUSERPREFS/recentFiles')
#	os.environ['ELEMENTSLIBRARY']   = osOps.absolutePath(getInheritedValue('other', 'elementslib')) # path needs to be translated for OS portability
	os.environ['ELEMENTSLIBRARY']   = osOps.absolutePath(getInheritedValue('other', 'elementslib'))
	os.environ['PRODBOARD']         = getInheritedValue('other', 'prodboard')
	os.environ['UNIT']              = getInheritedValue('units', 'linear')
	os.environ['ANGLE']             = getInheritedValue('units', 'angle')
	os.environ['TIMEFORMAT']        = getInheritedValue('units', 'time')
	os.environ['FPS']               = getInheritedValue('units', 'fps')
#	os.environ['HANDLES']           = getInheritedValue('time', 'handles') # need to split this into in and out points
	os.environ['STARTFRAME']        = getInheritedValue('time', 'rangeStart')
	os.environ['ENDFRAME']          = getInheritedValue('time', 'rangeEnd')
	os.environ['INFRAME']           = getInheritedValue('time', 'inFrame')
	os.environ['OUTFRAME']          = getInheritedValue('time', 'outFrame')
	os.environ['FRAMERANGE']        = '%s-%s' % (os.environ['STARTFRAME'], os.environ['ENDFRAME']) # is this necessary?
	os.environ['POSTERFRAME']       = getInheritedValue('time', 'posterFrame')
	os.environ['RESOLUTIONX']       = getInheritedValue('resolution', 'fullWidth')
	os.environ['RESOLUTIONY']       = getInheritedValue('resolution', 'fullHeight')
	os.environ['RESOLUTION']        = '%sx%s' % (os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY']) # is this necessary?
	os.environ['PROXY_RESOLUTIONX'] = getInheritedValue('resolution', 'proxyWidth')
	os.environ['PROXY_RESOLUTIONY'] = getInheritedValue('resolution', 'proxyHeight')
	os.environ['PROXY_RESOLUTION']  = '%sx%s' % (os.environ['PROXY_RESOLUTIONX'], os.environ['PROXY_RESOLUTIONY']) # is this necessary?
	os.environ['ASPECTRATIO']       = str( float(os.environ['RESOLUTIONX']) / float(os.environ['RESOLUTIONY']) )


	# Application specific environment variables...

	# Maya
	os.environ['MAYAVERSION']         = getAppExecPath('Maya')
	os.environ['MAYARENDERVERSION']   = osOps.absolutePath('%s/Render' % os.path.dirname( os.environ['MAYAVERSION'] ))
	os.environ['MAYADIR']             = osOps.absolutePath('$SHOTPATH/3D/maya')
	os.environ['MAYASCENESDIR']       = osOps.absolutePath('$MAYADIR/scenes/$USERNAME')
	os.environ['MAYAPLAYBLASTSDIR']   = osOps.absolutePath('$MAYADIR/playblasts/$USERNAME')
	os.environ['MAYACACHEDIR']        = osOps.absolutePath('$MAYADIR/cache/$USERNAME')
	os.environ['MAYASOURCEIMAGESDIR'] = osOps.absolutePath('$MAYADIR/sourceimages/$USERNAME')
	os.environ['MAYARENDERSDIR']      = osOps.absolutePath('$MAYADIR/renders/$USERNAME')

	#os.environ['PATH'] = os.path.join('%s;%s' % (os.environ['PATH'], os.environ['PIPELINE']), 'rsc', 'maya', 'dlls')
	#os.environ['PATH'] += os.pathsep + os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'dlls') # - this DLLs folder doesn't actually exist?
	#os.environ['PYTHONPATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'maya__env__;%s' % os.environ['PIPELINE'], 'rsc', 'maya', 'scripts')
	os.environ['PYTHONPATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'maya__env__') + os.pathsep + os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'scripts')
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.environ['PYTHONPATH'] = "C:\ProgramData\Redshift\Plugins\Maya\Common\scripts" + os.pathsep + os.environ['PYTHONPATH'] # hack for Redshift/XGen
		os.environ['redshift_LICENSE'] = "62843@10.105.11.11" # temporary fix for Redshift license - this should be set via a system environment variable
	os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = '0'
	os.environ['MAYA_PLUG_IN_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'plugins')
	#os.environ['MAYA_SHELF_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'shelves')
	os.environ['MAYA_SCRIPT_PATH'] = os.path.join(os.environ['PIPELINE'],'rsc', 'maya', 'maya__env__') + os.pathsep + os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'scripts')
	#os.environ['MI_CUSTOM_SHADER_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'shaders', 'include')
	#os.environ['MI_LIBRARY_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'shaders')
	os.environ['VRAY_FOR_MAYA_SHADERS'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'shaders')
	try:
		os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] += os.pathsep + os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'plugins')
	except (AttributeError, KeyError):
		pass
	if os.environ['ICARUS_RUNNING_OS'] == 'Linux':
		os.environ['XBMLANGPATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'icons', '%B')
	else:
		os.environ['XBMLANGPATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'icons')
	os.environ['MAYA_PRESET_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'presets')


	# Nuke
	os.environ['NUKEVERSION']     = getAppExecPath('Nuke')
	os.environ['NUKEDIR']         = osOps.absolutePath('$SHOTPATH/2D/nuke')
	os.environ['NUKEELEMENTSDIR'] = osOps.absolutePath('$NUKEDIR/elements/$USERNAME')
	os.environ['NUKESCRIPTSDIR']  = osOps.absolutePath('$NUKEDIR/scripts/$USERNAME')
	os.environ['NUKERENDERSDIR']  = osOps.absolutePath('$NUKEDIR/renders/$USERNAME')
	os.environ['NUKE_PATH']       = osOps.absolutePath('$PIPELINE/rsc/nuke')


	# Mudbox
	os.environ['MUDBOXVERSION']            = getAppExecPath('Mudbox')
	os.environ['MUDBOXDIR']                = osOps.absolutePath('$SHOTPATH/3D/mudbox')
	os.environ['MUDBOXSCENESDIR']          = osOps.absolutePath('$MUDBOXDIR/scenes/$USERNAME')
	os.environ['MUDBOX_PLUG_IN_PATH']      = osOps.absolutePath('$PIPELINE/rsc/mudbox/plugins') 
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'


	# Mari
	os.environ['MARIVERSION']                = getAppExecPath('Mari')
	os.environ['MARI_NUKEWORKFLOW_PATH']     = getAppExecPath('Nuke')
	os.environ['MARIDIR']                    = osOps.absolutePath('$SHOTPATH/3D/mari')
	os.environ['MARISCENESDIR']              = osOps.absolutePath('$MARIDIR/scenes/$USERNAME')
	os.environ['MARIGEODIR']                 = osOps.absolutePath('$MARIDIR/geo/$USERNAME')
	os.environ['MARITEXTURESDIR']            = osOps.absolutePath('$MARIDIR/textures/$USERNAME')
	os.environ['MARIRENDERSDIR']             = osOps.absolutePath('$MARIDIR/renders/$USERNAME')
	os.environ['MARI_DEFAULT_IMAGEPATH']     = osOps.absolutePath('$MARIDIR/sourceimages/$USERNAME')
	os.environ['MARI_SCRIPT_PATH']           = osOps.absolutePath('$PIPELINE/rsc/mari/scripts')
	os.environ['MARI_CACHE']                 = os.environ['MARISCENESDIR']
	os.environ['MARI_WORKING_DIR']           = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['SHOTPUBLISHDIR']
	os.environ['MARI_DEFAULT_ARCHIVE_PATH']  = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_EXPORT_PATH']   = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_IMPORT_PATH']   = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_RENDER_PATH']   = os.environ['MARIRENDERSDIR']
	os.environ['MARI_DEFAULT_CAMERA_PATH']   = os.environ['SHOTPUBLISHDIR']


	# Hiero
	os.environ['HIEROPLAYERVERSION'] = getAppExecPath('HieroPlayer')
	os.environ['HIEROEDITORIALPATH'] = osOps.absolutePath('$JOBPATH/../Editorial/Hiero')
	os.environ['HIERO_PLUGIN_PATH']  = osOps.absolutePath('$PIPELINE/rsc/hiero')


	# RealFlow (2013)
	os.environ['REALFLOWVERSION']                    = getAppExecPath('RealFlow')
	os.environ['REALFLOWDIR']                        = osOps.absolutePath('$SHOTPATH/3D/realflow')
	os.environ['REALFLOWSCENESDIR']                  = osOps.absolutePath('$REALFLOWDIR/$USERNAME')
	os.environ['RFDEFAULTPROJECT']                   = osOps.absolutePath('$REALFLOWSCENESDIR/$JOB_$SHOT')
	os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH']    = osOps.absolutePath('$REALFLOWSCENESDIR/.cmdsOrg/commandsOrganizer.dat')
	os.environ['RF_RSC']                             = osOps.absolutePath('$PIPELINE/rsc/realflow')
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = osOps.absolutePath('$PIPELINE/rsc/realflow/scripts/startup.rfs')
	os.environ['RFOBJECTSPATH']                      = osOps.absolutePath('$SHOTPUBLISHDIR/ma_geoCache/realflow')


	# Clarisse
	#sys.path.append(os.path.join(os.environ['PIPELINE'], 'rsc', 'clarisse'))


	# djv_view
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		# Note: using 32-bit version of djv_view for QuickTime compatibility on Windows
		os.environ['DJV_LIB']     = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-Windows-32/lib')
		os.environ['DJV_CONVERT'] = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_convert.exe')
		os.environ['DJV_PLAY']    = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_view.exe')

	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		os.environ['DJV_LIB']     = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/lib')
		os.environ['DJV_CONVERT'] = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/bin/djv_convert')
		os.environ['DJV_PLAY']    = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/bin/djv_view.sh')
	#	os.environ['DJV_PLAY']    = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/MacOS/djv-1.0.5-OSX-64')

	else:
		os.environ['DJV_LIB']     = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-Linux-64/lib')
		os.environ['DJV_CONVERT'] = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-Linux-64/bin/djv_convert')
		os.environ['DJV_PLAY']    = osOps.absolutePath('$PIPELINE/external_apps/djv/djv-1.0.5-Linux-64/bin/djv_view')


	# Deadline Monitor / Slave
	os.environ['DEADLINEMONITORVERSION'] = getAppExecPath('DeadlineMonitor')
	os.environ['DEADLINESLAVEVERSION']   = getAppExecPath('DeadlineSlave')


	return True

