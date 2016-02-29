#!/usr/bin/python

# [Icarus] job__env__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Sets up job- and shot-related environment variables.


import os, sys
import jobs, jobSettings, osOps, appPaths, verbose


def setEnv(envVars):
	""" Set job and shot environment variables.
	"""

	def getInheritedValue(category, setting):
		""" First try to get the value from the shot data, if it returns nothing then look in job data instead.
		"""
		value = shotData.getValue(category, setting)
		if value == "":
			value = jobData.getValue(category, setting)
#			if value == "":
#				value = defaultData.getValue(category, setting)

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
	os.environ['JOBPATH'] = os.path.normpath(jobPath)
	os.environ['SHOTPATH'] = os.path.normpath(shotPath)
	os.environ['JOBDATA'] = os.path.normpath(jobDataPath)
	os.environ['SHOTDATA'] = os.path.normpath(shotDataPath)

	osOps.createDir(os.environ['JOBDATA'])

	# Instantiate job / shot settings classes
	jobData = jobSettings.jobSettings()
	shotData = jobSettings.jobSettings()
#	defaultData = jobSettings.jobSettings()
	ap = appPaths.appPaths()

	jobDataLoaded = jobData.loadXML(os.path.join(jobDataPath, 'jobData.xml'))
	shotDataLoaded = shotData.loadXML(os.path.join(shotDataPath, 'shotData.xml'))
#	defaultData.loadXML(os.path.join(os.environ['ICCONFIGDIR'], 'defaultData.xml'))
	ap.loadXML(os.path.join(os.environ['ICCONFIGDIR'], 'appPaths.xml'))

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
	#assetDir = getInheritedValue('meta', 'assetDir')
	assetDir = jobData.getValue('meta', 'assetDir')
	if assetDir:
		os.environ['PUBLISHRELATIVEDIR'] = assetDir
	else:
		import legacySettings

		# Check for existing legacy published assets in the job and shot(s)
		if legacySettings.checkAssetPath():
			assetDir = '.publish'
		else:
			assetDir = 'Assets' # Perhaps this shouldn't be hard-coded?

		jobData.setValue('meta', 'assetDir', assetDir)
		jobData.saveXML()
		os.environ['PUBLISHRELATIVEDIR'] = assetDir


	# Set OS identifier strings to get correct app executable paths
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		currentOS = 'osx'
	elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		currentOS = 'win'
	elif os.environ['ICARUS_RUNNING_OS'] == 'Linux':
		currentOS = 'linux'


	# Terminal / Command Prompt
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.environ['GPS_RC'] = os.path.join(os.environ['PIPELINE'], 'core', 'ui', 'gps_cmd.bat')
	else:
		os.environ['GPS_RC'] = os.path.join(os.environ['PIPELINE'], 'core', 'ui', '.gps_rc')

	# Jobs root paths for cross-platform support
	os.environ['JOBSROOTWIN'] = jobs.win_root
	os.environ['JOBSROOTOSX'] = jobs.osx_root
	#os.environ['JOBSROOTLINUX'] = jobs.linux_root # Not currently required as Linux & OSX mount points should be the same

	# Job / shot env
	#os.environ['GLOBALPUBLISHDIR'] = os.path.normpath( getInheritedValue('other', 'assetlib') ) # Path needs to be translated for OS portability
	os.environ['JOBPUBLISHDIR'] = os.path.normpath( os.path.join(os.environ['JOBPATH'], os.environ['PUBLISHRELATIVEDIR']) )
	os.environ['SHOTPUBLISHDIR'] = os.path.normpath( os.path.join(os.environ['SHOTPATH'], os.environ['PUBLISHRELATIVEDIR']) )
	os.environ['WIPSDIR'] = os.path.normpath( os.path.join(os.path.split(os.environ['JOBPATH'])[0], 'Deliverables', 'WIPS') ) # Perhaps this shouldn't be hard-coded?
	os.environ['RECENTFILESDIR'] = os.path.normpath( os.path.join(os.environ['ICUSERPREFS'], 'recentFiles') )
	os.environ['ELEMENTSLIBRARY'] = os.path.normpath( getInheritedValue('other', 'elementslib') ) # Path needs to be translated for OS portability
	os.environ['PRODBOARD'] = getInheritedValue('other', 'prodboard')
	#os.environ['PROJECTTOOLS'] = getInheritedValue('other', 'projtools') # Is this necessary?
	os.environ['UNIT'] = getInheritedValue('units', 'linear')
	os.environ['ANGLE'] = getInheritedValue('units', 'angle')
	os.environ['TIMEFORMAT'] = getInheritedValue('units', 'time')
	os.environ['FPS'] = getInheritedValue('units', 'fps')
	os.environ['HANDLES'] = getInheritedValue('time', 'handles')
	os.environ['STARTFRAME'] = getInheritedValue('time', 'rangeStart')
	os.environ['ENDFRAME'] = getInheritedValue('time', 'rangeEnd')
	os.environ['FRAMERANGE'] = '%s-%s' % (os.environ['STARTFRAME'], os.environ['ENDFRAME']) # Is this necessary?
	os.environ['RESOLUTIONX'] = getInheritedValue('resolution', 'fullWidth')
	os.environ['RESOLUTIONY'] = getInheritedValue('resolution', 'fullHeight')
	os.environ['RESOLUTION'] = '%sx%s' % (os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY']) # Is this necessary?
	os.environ['PROXY_RESOLUTIONX'] = getInheritedValue('resolution', 'proxyWidth')
	os.environ['PROXY_RESOLUTIONY'] = getInheritedValue('resolution', 'proxyHeight')
	os.environ['PROXY_RESOLUTION'] = '%sx%s' % (os.environ['PROXY_RESOLUTIONX'], os.environ['PROXY_RESOLUTIONY']) # Is this necessary?
	os.environ['ASPECTRATIO'] = str( float(os.environ['RESOLUTIONX']) / float(os.environ['RESOLUTIONY']) )

	# Mari
	os.environ['MARIDIR'] = os.path.join(os.environ['SHOTPATH'] , '3D', 'mari')
	os.environ['MARISCENESDIR'] = os.path.join(os.environ['MARIDIR'], 'scenes', os.environ['USERNAME'])
	os.environ['MARIGEODIR'] = os.path.join(os.environ['MARIDIR'], 'geo', os.environ['USERNAME'])
	os.environ['MARITEXTURESDIR'] = os.path.join(os.environ['MARIDIR'], 'textures', os.environ['USERNAME'])
	os.environ['MARIRENDERSDIR'] = os.path.join(os.environ['MARIDIR'], 'renders', os.environ['USERNAME'])
	os.environ['MARI_CACHE'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_IMAGEPATH'] = os.path.join(os.environ['MARIDIR'], 'sourceimages', os.environ['USERNAME'])
	os.environ['MARI_WORKING_DIR'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['SHOTPUBLISHDIR']
	os.environ['MARI_DEFAULT_ARCHIVE_PATH'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_EXPORT_PATH'] = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_IMPORT_PATH'] = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_RENDER_PATH'] = os.environ['MARIRENDERSDIR']
	os.environ['MARI_DEFAULT_CAMERA_PATH'] = os.environ['SHOTPUBLISHDIR']
	os.environ['MARI_SCRIPT_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'mari', 'scripts')
	os.environ['MARI_NUKEWORKFLOW_PATH'] = getAppExecPath('Nuke') #jobData.nukeVersion
	os.environ['MARIVERSION'] = getAppExecPath('Mari') #jobData.mariVersion

	# Maya
	#os.environ['PATH'] = os.path.join('%s;%s' % (os.environ['PATH'], os.environ['PIPELINE']), 'rsc', 'maya', 'dlls')
	#os.environ['PATH'] += os.pathsep + os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'dlls') # - this DLLs folder doesn't actually exist?
	#os.environ['PYTHONPATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'maya__env__;%s' % os.environ['PIPELINE'], 'rsc', 'maya', 'scripts')
	os.environ['PYTHONPATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'maya__env__') + os.pathsep + os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'scripts')
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.environ['PYTHONPATH'] = "C:\ProgramData\Redshift\Plugins\Maya\Common\scripts" + os.pathsep + os.environ['PYTHONPATH'] # Hack for Redshift/XGen
		os.environ['redshift_LICENSE'] = "62843@10.105.11.11" # Temporary fix for Redshift license - this should be set via a system environment variable
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
	os.environ['MAYADIR'] = os.path.join(os.environ['SHOTPATH'], '3D', 'maya')
	os.environ['MAYASCENESDIR'] = os.path.join(os.environ['MAYADIR'], 'scenes', os.environ['USERNAME'])
	os.environ['MAYAPLAYBLASTSDIR'] = os.path.join(os.environ['MAYADIR'], 'playblasts', os.environ['USERNAME'])
	os.environ['MAYACACHEDIR'] = os.path.join(os.environ['MAYADIR'], 'cache', os.environ['USERNAME'])
	os.environ['MAYASOURCEIMAGESDIR'] = os.path.join(os.environ['MAYADIR'], 'sourceimages', os.environ['USERNAME'])
	os.environ['MAYARENDERSDIR'] = os.path.join(os.environ['MAYADIR'], 'renders', os.environ['USERNAME'])
	os.environ['MAYAVERSION'] = getAppExecPath('Maya') #os.path.normpath(jobData.mayaVersion)
	os.environ['MAYARENDERVERSION'] = os.path.join( os.path.dirname( os.environ['MAYAVERSION'] ), 'Render' )

	# Mudbox
	os.environ['MUDBOXDIR'] = os.path.join(os.environ['SHOTPATH'], '3D', 'mudbox')
	os.environ['MUDBOXSCENESDIR'] = os.path.join(os.environ['MUDBOXDIR'], 'scenes', os.environ['USERNAME'])
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'
	os.environ['MUDBOX_PLUG_IN_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'mudbox', 'plugins') 
	os.environ['MUDBOXVERSION'] = getAppExecPath('Mudbox') #jobData.mudboxVersion

	# Nuke
	os.environ['NUKE_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'nuke')
	os.environ['NUKEDIR'] = os.path.join(os.environ['SHOTPATH'], '2D', 'nuke')
	os.environ['NUKEELEMENTSDIR'] = os.path.join(os.environ['NUKEDIR'], 'elements', os.environ['USERNAME'])
	os.environ['NUKESCRIPTSDIR'] = os.path.join(os.environ['NUKEDIR'], 'scripts', os.environ['USERNAME'])
	os.environ['NUKERENDERSDIR'] = os.path.join(os.environ['NUKEDIR'], 'renders', os.environ['USERNAME'])
	os.environ['NUKEVERSION'] = getAppExecPath('Nuke') #jobData.nukeVersion
	#os.environ['NUKEXVERSION'] = '%s --nukex' % jobData.nukeVersion # now being set in launchApps.py

	# Hiero
	os.environ['HIEROEDITORIALPATH'] = os.path.join(os.path.split(os.environ['JOBPATH'])[0], 'Editorial', 'Hiero') 
	os.environ['HIEROPLAYERVERSION'] = getAppExecPath('HieroPlayer') #jobData.hieroPlayerVersion
	os.environ['HIERO_PLUGIN_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'hiero')

	# Clarisse
	#sys.path.append(os.path.join(os.environ['PIPELINE'], 'rsc', 'clarisse'))

	# RealFlow
	os.environ['REALFLOWDIR'] = os.path.join(os.environ['SHOTPATH'], '3D', 'realflow')
	os.environ['REALFLOWVERSION'] = getAppExecPath('RealFlow') #jobData.realflowVersion
	os.environ['REALFLOWSCENESDIR'] = os.path.join(os.environ['REALFLOWDIR'], os.environ['USERNAME'])
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'realflow', 'scripts', 'startup.rfs')
	os.environ['RFDEFAULTPROJECT'] = os.path.join(os.environ['REALFLOWSCENESDIR'], '%s_%s' % (os.environ['JOB'], os.environ['SHOT']))
	os.environ['RFOBJECTSPATH'] = os.path.join(os.environ['SHOTPUBLISHDIR'], 'ma_geoCache', 'realflow')
	os.environ['RF_RSC'] = os.path.join(os.environ['PIPELINE'], 'rsc', 'realflow')
	os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH'] = os.path.join(os.environ['REALFLOWSCENESDIR'] , '.cmdsOrg', 'commandsOrganizer.dat')

	# djv_view
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		# Note: using 32-bit version of djv_view for QuickTime compatibility on Windows
		os.environ['DJV_LIB'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-Windows-32/lib' % os.environ['PIPELINE'])
		os.environ['DJV_CONVERT'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_convert.exe' % os.environ['PIPELINE'])
		os.environ['DJV_PLAY'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-Windows-32/bin/djv_view.exe' % os.environ['PIPELINE'])

	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		os.environ['DJV_LIB'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/lib' % os.environ['PIPELINE'])
		os.environ['DJV_CONVERT'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/bin/djv_convert' % os.environ['PIPELINE'])
		os.environ['DJV_PLAY'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/bin/djv_view.sh' % os.environ['PIPELINE'])
		#os.environ['DJV_PLAY'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/MacOS/djv-1.0.5-OSX-64' % os.environ['PIPELINE'])

	else:
		os.environ['DJV_LIB'] = '%s/external_apps/djv/djv-1.0.5-Linux-64/lib' % os.environ['PIPELINE']
		os.environ['DJV_CONVERT'] = '%s/external_apps/djv/djv-1.0.5-Linux-64/bin/djv_convert' % os.environ['PIPELINE']
		os.environ['DJV_PLAY'] = '%s/external_apps/djv/djv-1.0.5-Linux-64/bin/djv_view' % os.environ['PIPELINE']

	# Deadline Monitor / Slave
	os.environ['DEADLINEMONITORVERSION'] = getAppExecPath('DeadlineMonitor')
	os.environ['DEADLINESLAVEVERSION'] = getAppExecPath('DeadlineSlave')

	return True

