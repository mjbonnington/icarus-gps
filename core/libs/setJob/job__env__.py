#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:job__env__
#copyright	:Gramercy Park Studios


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
	os.environ['SHOTPATH'] = shotPath
	os.environ['JOBPATH'] = os.path.split(shotPath)[0]
	os.environ['JOBDATA'] = jobDataPath
	os.environ['SHOTDATA'] = shotDataPath
	os.environ['JOB'] = job
	os.environ['SHOT'] = shot
	os.environ['PRODBOARD'] = jobData.prodBoard
	os.environ['PROJECTTOOLS'] = jobData.projectTools
	os.environ['FRAMEVIEWER'] = jobData.frameViewer
	os.environ['JOBAPPROVEDPUBLISHDIR'] = os.path.join(os.environ['JOBPATH'], 'Assets', '3D')
	os.environ['SHOTAPPROVEDPUBLISHDIR'] = os.path.join(os.environ['SHOTPATH'], 'Publish')
	os.environ['PUBLISHRELATIVEDIR'] = '.publish'
	os.environ['JOBPUBLISHDIR'] = os.path.join(os.environ['JOBPATH'] , os.environ['PUBLISHRELATIVEDIR'])
	os.environ['SHOTPUBLISHDIR'] = os.path.join(os.environ['SHOTPATH'], os.environ['PUBLISHRELATIVEDIR'])
	os.environ['WIPSDIR'] = os.path.join(os.path.split(os.environ['JOBPATH'])[0], 'Deliverables', 'WIPS')
	os.environ['ELEMENTSLIBRARY'] = jobData.elementsLibrary
	os.environ['TIMEFORMAT'] = jobData.timeFormat	
	os.environ['ANGLE'] = jobData.angle	
	os.environ['UNIT'] = jobData.unit
	os.environ['FPS'] = jobData.fps
	os.environ['FRAMERANGE'] = '%s-%s' % (shotData.frRange[0], shotData.frRange[1])
	os.environ['STARTFRAME'] = shotData.frRange[0]
	os.environ['ENDFRAME'] = shotData.frRange[1]
	os.environ['RESOLUTION'] = '%sx%s' % (shotData.res[0], shotData.res[1])
	os.environ['RESOLUTIONX'] = shotData.res[0]
	os.environ['RESOLUTIONY'] = shotData.res[1]
	os.environ['ASPECTRATIO'] = '%s' % float(float(shotData.res[0]) / float(shotData.res[1]))
	os.environ['HRES'] = shotData.res[0]
	os.environ['VRES'] = shotData.res[1]
	os.environ['RECENTFILESDIR'] = '/Users/%s/.icRecentFiles' % os.environ['USERNAME']
	#MARI
	os.environ['MARIDIR'] = '%s/3D/mari' % shotPath
	os.environ['MARISCENESDIR'] = '%s/scenes/%s' % (os.environ['MARIDIR'], os.environ['USERNAME'])
	os.environ['MARIGEODIR'] = '%s/geo/%s' % (os.environ['MARIDIR'], os.environ['USERNAME'])
	os.environ['MARITEXTURESDIR'] = '%s/textures/%s' % (os.environ['MARIDIR'], os.environ['USERNAME'])
	os.environ['MARIRENDERSDIR'] = '%s/renders/%s' % (os.environ['MARIDIR'], os.environ['USERNAME'])
	os.environ['MARI_CACHE'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_IMAGEPATH'] = '%s/sourceimages' % (os.environ['MARIDIR'])
	os.environ['MARI_WORKING_DIR'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_GEOMETRY_PATH'] = os.environ['SHOTAPPROVEDPUBLISHDIR']
	os.environ['MARI_DEFAULT_ARCHIVE_PATH'] = os.environ['MARISCENESDIR']
	os.environ['MARI_DEFAULT_EXPORT_PATH'] = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_IMPORT_PATH'] = os.environ['MARITEXTURESDIR']
	os.environ['MARI_DEFAULT_RENDER_PATH'] = os.environ['MARIRENDERSDIR']
	os.environ['MARI_DEFAULT_CAMERA_PATH'] = os.environ['SHOTAPPROVEDPUBLISHDIR']
	os.environ['MARI_SCRIPT_PATH'] = '%s/mari_rsc/scripts' % os.environ['PIPELINE']
	os.environ['MARI_NUKEWORKFLOW_PATH'] = jobData.nukeVersion
	os.environ['MARIVERSION'] = jobData.mariVersion
	#MAYA ENV
	os.environ['PATH'] = '%s:%s/maya_rsc/dlls' % (os.environ['PATH'], os.environ['PIPELINE'])
	os.environ['PYTHONPATH'] = '%s/maya_rsc/maya__env__:%s/maya_rsc/scripts:%s/maya_rsc' % (os.environ['PIPELINE'], os.environ['PIPELINE'], os.environ['JOBDATA'])
	os.environ['MAYA_DEBUG_ENABLE_CRASH_REPORTING'] = '0'
	os.environ['MAYA_PLUG_IN_PATH'] = '%s/maya_rsc/plugins' % os.environ['PIPELINE']
	os.environ['MAYA_SCRIPT_PATH'] = '%s/maya_rsc/maya__env__:%s/maya_rsc/scripts:%s/maya_rsc' % (os.environ['PIPELINE'], os.environ['PIPELINE'], os.environ['JOBDATA'])
	os.environ['MI_CUSTOM_SHADER_PATH'] = '%s/maya_rsc/shaders/include' % os.environ['PIPELINE']
	os.environ['MI_LIBRARY_PATH'] = '%s/maya_rsc/shaders:' % os.environ['PIPELINE']
	os.environ['VRAY_FOR_MAYA_SHADERS'] = '%s/maya_rsc/shaders/' % os.environ['PIPELINE']
	os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'] = '%s:%s/maya_rsc/plugins' % (os.environ['VRAY_FOR_MAYA2014_PLUGINS_x64'], os.environ['PIPELINE'])
	os.environ['XBMLANGPATH'] = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'icons')
	os.environ['MAYA_PRESET_PATH'] = '%s/maya_rsc/presets' % os.environ['PIPELINE']
	os.environ['MAYADIR'] = '%s/3D/maya' % shotPath
	os.environ['MAYASCENESDIR'] = '%s/scenes/%s' % (os.environ['MAYADIR'], os.environ['USERNAME'])
	os.environ['MAYAPLAYBLASTSDIR'] = '%s/playblasts/%s' % (os.environ['MAYADIR'], os.environ['USERNAME'])
	os.environ['MAYACACHEDIR'] = '%s/cache/%s' % (os.environ['MAYADIR'], os.environ['USERNAME'])
	os.environ['MAYASOURCEIMAGESDIR'] = '%s/sourceimages' % (os.environ['MAYADIR'])
	os.environ['MAYARENDERSDIR'] = '%s/renders/%s' % (os.environ['MAYADIR'], os.environ['USERNAME'])
	os.environ['MAYAVERSION'] = jobData.mayaVersion
	#MUDBOXENV
	os.environ['MUDBOXDIR'] = '%s/3D/mudbox' % shotPath
	os.environ['MUDBOXSCENESDIR'] = '%s/scenes/%s' % (os.environ['MUDBOXDIR'], os.environ['USERNAME'])
	os.environ['MUDBOX_IDLE_LICENSE_TIME'] = '60'
	os.environ['MUDBOX_PLUG_IN_PATH'] = '%s/mudbox_rsc/plugins' % os.environ['PIPELINE']
	os.environ['MUDBOXVERSION'] = jobData.mudboxVersion
	#NUKE ENV
	os.environ['NUKE_PATH'] = os.path.join(os.environ['PIPELINE'], 'nuke_rsc')
	os.environ['NUKEDIR'] = '%s/2D/nuke' % shotPath
	os.environ['NUKEELEMENTSDIR'] = os.path.join(os.environ['NUKEDIR'], 'elements', os.environ['USERNAME'])
	os.environ['NUKESCRIPTSDIR'] = os.path.join(os.environ['NUKEDIR'], 'scripts', os.environ['USERNAME'])
	os.environ['NUKERENDERSDIR'] = os.path.join(os.environ['NUKEDIR'], 'renders', os.environ['USERNAME'])
	os.environ['NUKEVERSION'] = jobData.nukeVersion
	#HIERO ENV
	os.environ['HIEROEDITORIALPATH'] = '%s/Editorial/Hiero/' % os.path.split(os.environ['JOBPATH'])[0]
	os.environ['HIEROPLAYERVERSION'] = jobData.hieroPlayerVersion
	os.environ['HIERO_PLUGIN_PATH'] = '%s/hiero_rsc' % os.environ['PIPELINE']
	#CLARISSE ENV
	#sys.path.append(os.path.join(os.environ['PIPELINE'], 'clarisse_rsc'))
	#REALFLOW
	os.environ['REALFLOWDIR'] = '%s/3D/realflow' % shotPath
	os.environ['REALFLOWVERSION'] = jobData.realflowVersion
	os.environ['REALFLOWSCENESDIR'] = '%s/%s' % (os.environ['REALFLOWDIR'], os.environ['USERNAME'])
	os.environ['RF_STARTUP_PYTHON_SCRIPT_FILE_PATH'] = os.path.join(os.environ['PIPELINE'], 'realflow_rsc', 'scripts/startup.rfs')
	os.environ['RFDEFAULTPROJECT'] = os.path.join(os.environ['REALFLOWSCENESDIR'], '%s_%s' % (os.environ['JOB'], os.environ['SHOT']))
	os.environ['RFOBJECTSPATH'] = '%s/ma_geoCache/realflow' % os.environ['SHOTPUBLISHDIR']
	os.environ['RF_RSC'] = os.path.join(os.environ['PIPELINE'], 'realflow_rsc')
	os.environ['RF_COMMANDS_ORGANIZER_FILE_PATH'] = os.path.join(os.environ['REALFLOWSCENESDIR'] , '.cmdsOrg/commandsOrganizer.dat')
	#DJV
	os.environ['DJVCONVERTPATH'] = '%s/external_apps/djv/djv-1.0.3-OSX-64.app/Contents/Resources/bin' % os.environ['PIPELINE']