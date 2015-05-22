#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :job__env__
#copyright  :Gramercy Park Studios


import os, sys

#sets job and shot environment variables
def setEnv(envVars):
	job, shot, shotPath = envVars
	jobDataPath = os.path.join(os.path.split(shotPath)[0], os.environ['DATAFILESRELATIVEDIR'])
	shotDataPath = os.path.join(shotPath, os.environ['DATAFILESRELATIVEDIR'])
	sys.path.append(jobDataPath); sys.path.append(shotDataPath)
	import jobData, shotData
	reload(jobData); reload(shotData)
	sys.path.remove(jobDataPath); sys.path.remove(shotDataPath)
	#TERMINAL
	os.environ['GPS_RC'] = os.path.join(os.environ['PIPELINE'], 'core', 'ui', '.gps_rc')

	#job env
	os.environ['SHOTPATH'] = os.path.normpath(shotPath)
	os.environ['JOBPATH'] = os.path.normpath( os.path.split(os.environ['SHOTPATH'])[0] )
	os.environ['JOBDATA'] = os.path.normpath( os.path.join(os.environ['JOBPATH'], os.environ['DATAFILESRELATIVEDIR']) )
	os.environ['SHOTDATA'] = os.path.normpath(shotDataPath)
	os.environ['JOB'] = job
	os.environ['SHOT'] = shot
	os.environ['PRODBOARD'] = jobData.prodBoard
	os.environ['PROJECTTOOLS'] = jobData.projectTools
	os.environ['FRAMEVIEWER'] = os.path.normpath(jobData.frameViewer)
	os.environ['JOBAPPROVEDPUBLISHDIR'] = os.path.normpath( os.path.join(os.environ['JOBPATH'], 'Assets', '3D') )
	os.environ['SHOTAPPROVEDPUBLISHDIR'] = os.path.normpath( os.path.join(os.environ['SHOTPATH'], 'Publish') )
	os.environ['PUBLISHRELATIVEDIR'] = '.publish'
	os.environ['JOBPUBLISHDIR'] = os.path.normpath( os.path.join(os.environ['JOBPATH'] , os.environ['PUBLISHRELATIVEDIR']) )
	os.environ['SHOTPUBLISHDIR'] = os.path.normpath( os.path.join(os.environ['SHOTPATH'], os.environ['PUBLISHRELATIVEDIR']) )
	os.environ['WIPSDIR'] = os.path.normpath( os.path.join(os.path.split(os.environ['JOBPATH'])[0], 'Deliverables', 'WIPS') )
	os.environ['ELEMENTSLIBRARY'] = os.path.normpath(jobData.elementsLibrary)
	os.environ['TIMEFORMAT'] = jobData.timeFormat
	os.environ['ANGLE'] = jobData.angle
	os.environ['UNIT'] = jobData.unit
	os.environ['FPS'] = jobData.fps
	os.environ['STARTFRAME'] = shotData.frRange[0]
	os.environ['ENDFRAME'] = shotData.frRange[1]
	os.environ['FRAMERANGE'] = '%s-%s' % (os.environ['STARTFRAME'], os.environ['ENDFRAME'])
	os.environ['RESOLUTIONX'] = shotData.res[0]
	os.environ['RESOLUTIONY'] = shotData.res[1]
	os.environ['RESOLUTION'] = '%sx%s' % (os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY'])
	os.environ['PROXY_RESOLUTIONX'] = str(int(os.environ['RESOLUTIONX'])/2)
	os.environ['PROXY_RESOLUTIONY'] = str(int(os.environ['RESOLUTIONY'])/2)
	os.environ['PROXY_RESOLUTION'] = '%sx%s' % (os.environ['PROXY_RESOLUTIONX'], os.environ['PROXY_RESOLUTIONY'])
	os.environ['ASPECTRATIO'] = '%s' % float(float(os.environ['RESOLUTIONX']) / float(os.environ['RESOLUTIONY']))
	os.environ['RECENTFILESDIR'] = os.path.normpath( os.path.join(os.environ['ICUSERPREFS'], 'recentFiles') )

	#MARI
	os.environ['MARIDIR'] = os.path.join(os.environ['SHOTPATH'] , '3D', 'mari')
	os.environ['MARISCENESDIR'] = os.path.join(os.environ['MARIDIR'], 'scenes', os.environ['USERNAME'])
	os.environ['MARIGEODIR'] = os.path.join(os.environ['MARIDIR'], 'geo', os.environ['USERNAME'])
	os.environ['MARITEXTURESDIR'] = os.path.join(os.environ['MARIDIR'], 'textures', os.environ['USERNAME'])
	os.environ['MARIRENDERSDIR'] = os.path.join(os.environ['MARIDIR'], 'renders', os.environ['USERNAME'])
	os.environ['MARI_CACHE'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_IMAGEPATH'] = os.path.join(os.environ['MARIDIR'], 'sourceimages', os.environ['USERNAME'])
	os.environ['MARI_WORKING_DIR'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['SHOTAPPROVEDPUBLISHDIR']
	os.environ['MARI_DEFAULT_ARCHIVE_PATH'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_EXPORT_PATH'] = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_IMPORT_PATH'] = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_RENDER_PATH'] = os.environ['MARIRENDERSDIR']
	os.environ['MARI_DEFAULT_CAMERA_PATH'] = os.environ['SHOTAPPROVEDPUBLISHDIR']
	os.environ['MARI_SCRIPT_PATH'] = os.path.join(os.environ['PIPELINE'], 'mari_rsc', 'scripts')
	os.environ['MARI_NUKEWORKFLOW_PATH'] = jobData.nukeVersion
	os.environ['MARIVERSION'] = jobData.mariVersion

	#MAYA ENV
	#os.environ['PATH'] = os.path.join('%s;%s' % (os.environ['PATH'], os.environ['PIPELINE']), 'maya_rsc', 'dlls')
	os.environ['PATH'] += os.pathsep + os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'dlls') # - this DLLs folder doesn't actually exist?
	#os.environ['PYTHONPATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'maya__env__;%s' % os.environ['PIPELINE'], 'maya_rsc', 'scripts')
	os.environ['PYTHONPATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'maya__env__') + os.pathsep + os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'scripts')
	os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = '0'
	os.environ['MAYA_PLUG_IN_PATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'plugins')
	#os.environ['MAYA_SHELF_PATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'shelves')
	os.environ['MAYA_SCRIPT_PATH'] = os.path.join(os.environ['PIPELINE'],'maya_rsc', 'maya__env__') + os.pathsep + os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'scripts')
	os.environ['MI_CUSTOM_SHADER_PATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'shaders', 'include')
	os.environ['MI_LIBRARY_PATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'shaders')
	os.environ['VRAY_FOR_MAYA_SHADERS'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'shaders')
	try:
		os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] += os.pathsep + os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'plugins')
	except (AttributeError, KeyError):
		pass
	if os.environ['ICARUS_RUNNING_OS'] == 'Linux':
		os.environ['XBMLANGPATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'icons', '%B')
	else:
		os.environ['XBMLANGPATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'icons')
	os.environ['MAYA_PRESET_PATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'presets')
	os.environ['MAYADIR'] = os.path.join(os.environ['SHOTPATH'], '3D', 'maya')
	os.environ['MAYASCENESDIR'] = os.path.join(os.environ['MAYADIR'], 'scenes', os.environ['USERNAME'])
	os.environ['MAYAPLAYBLASTSDIR'] = os.path.join(os.environ['MAYADIR'], 'playblasts', os.environ['USERNAME'])
	os.environ['MAYACACHEDIR'] = os.path.join(os.environ['MAYADIR'], 'cache', os.environ['USERNAME'])
	os.environ['MAYASOURCEIMAGESDIR'] = os.path.join(os.environ['MAYADIR'], 'sourceimages', os.environ['USERNAME'])
	os.environ['MAYARENDERSDIR'] = os.path.join(os.environ['MAYADIR'], 'renders', os.environ['USERNAME'])
	os.environ['MAYAVERSION'] = os.path.normpath(jobData.mayaVersion)
	os.environ['MAYARENDERVERSION'] = os.path.join( os.path.dirname( os.path.normpath(jobData.mayaVersion) ), 'Render' )
	#os.environ['MAYARENDERVERSION'] = os.path.join(os.path.dirname(jobData.mayaVersion), 'Render')

	#MUDBOXENV
	os.environ['MUDBOXDIR'] = os.path.join(os.environ['SHOTPATH'], '3D', 'mudbox')
	os.environ['MUDBOXSCENESDIR'] = os.path.join(os.environ['MUDBOXDIR'], 'scenes', os.environ['USERNAME'])
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'
	os.environ['MUDBOX_PLUG_IN_PATH'] = os.path.join(os.environ['PIPELINE'], 'mudbox_rsc', 'plugins') 
	os.environ['MUDBOXVERSION'] = jobData.mudboxVersion

	#NUKE ENV
	os.environ['NUKE_PATH'] = os.path.join(os.environ['PIPELINE'], 'nuke_rsc')
	os.environ['NUKEDIR'] = os.path.join(os.environ['SHOTPATH'], '2D', 'nuke')
	os.environ['NUKEELEMENTSDIR'] = os.path.join(os.environ['NUKEDIR'], 'elements', os.environ['USERNAME'])
	os.environ['NUKESCRIPTSDIR'] = os.path.join(os.environ['NUKEDIR'], 'scripts', os.environ['USERNAME'])
	os.environ['NUKERENDERSDIR'] = os.path.join(os.environ['NUKEDIR'], 'renders', os.environ['USERNAME'])
	os.environ['NUKEVERSION'] = jobData.nukeVersion
	#os.environ['NUKEXVERSION'] = '%s --nukex' % jobData.nukeVersion # now being set in launchApps.py

	#HIERO ENV
	os.environ['HIEROEDITORIALPATH'] = os.path.join(os.path.split(os.environ['JOBPATH'])[0], 'Editorial', 'Hiero') 
	os.environ['HIEROPLAYERVERSION'] = jobData.hieroPlayerVersion
	os.environ['HIERO_PLUGIN_PATH'] = os.path.join(os.environ['PIPELINE'], 'hiero_rsc')

	#CLARISSE ENV
	#sys.path.append(os.path.join(os.environ['PIPELINE'], 'clarisse_rsc'))

	#REALFLOW
	os.environ['REALFLOWDIR'] = os.path.join(os.environ['SHOTPATH'], '3D', 'realflow')
	os.environ['REALFLOWVERSION'] = jobData.realflowVersion
	os.environ['REALFLOWSCENESDIR'] = os.path.join(os.environ['REALFLOWDIR'], os.environ['USERNAME'])
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = os.path.join(os.environ['PIPELINE'], 'realflow_rsc', 'scripts', 'startup.rfs')
	os.environ['RFDEFAULTPROJECT'] = os.path.join(os.environ['REALFLOWSCENESDIR'], '%s_%s' % (os.environ['JOB'], os.environ['SHOT']))
	os.environ['RFOBJECTSPATH'] = os.path.join(os.environ['SHOTPUBLISHDIR'], 'ma_geoCache', 'realflow')
	os.environ['RF_RSC'] = os.path.join(os.environ['PIPELINE'], 'realflow_rsc')
	os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH'] = os.path.join(os.environ['REALFLOWSCENESDIR'] , '.cmdsOrg', 'commandsOrganizer.dat')

	#DJV
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		os.environ['DJV_LIB'] = '%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/lib' % os.environ['PIPELINE']
		os.environ['DJV_CONVERT'] = '%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/bin/djv_convert' % os.environ['PIPELINE']
		os.environ['DJV_PLAY'] = '%s/external_apps/djv/djv-1.0.5-OSX-64.app/Contents/Resources/bin/djv_view.sh' % os.environ['PIPELINE']
	elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.environ['DJV_LIB'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-Windows-64/lib' % os.environ['PIPELINE'])
		os.environ['DJV_CONVERT'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-Windows-64/bin/djv_convert.exe' % os.environ['PIPELINE'])
		os.environ['DJV_PLAY'] = os.path.normpath('%s/external_apps/djv/djv-1.0.5-Windows-64/bin/djv_view.exe' % os.environ['PIPELINE'])
	else:
		os.environ['DJV_LIB'] = '%s/external_apps/djv/djv-1.0.5-Linux-64/lib' % os.environ['PIPELINE']
		os.environ['DJV_CONVERT'] = '%s/external_apps/djv/djv-1.0.5-Linux-64/bin/djv_convert' % os.environ['PIPELINE']
		os.environ['DJV_PLAY'] = '%s/external_apps/djv/djv-1.0.5-Linux-64/bin/djv_view' % os.environ['PIPELINE']

	# Temp declaration until appPaths.xml, and jobData / shotData implementation changed
	os.environ['DEADLINEMONITORVERSION'] = '/Applications/Thinkbox/Deadline7/DeadlineMonitor7.app/Contents/MacOS/DeadlineMonitor7'
	os.environ['DEADLINESLAVEVERSION'] = '/Applications/Thinkbox/Deadline7/DeadlineSlave7.app/Contents/MacOS/DeadlineSlave7'
