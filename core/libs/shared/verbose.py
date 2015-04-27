#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:verbose
#copyright	:Gramercy Park Studios

#this module processes verbosity printing

def approval(start=False, end=False):
	if start:
		print 'Processing approval...'
		return
	if end:
		print 'Approved.'
		return
	
def approvalOSError():
	print 'Some assets may not have gone trough the approval process. Some file links may be missing.'

def animRequires(asset):
	print 'Requires %s' % asset

def assetConflict():
	print 'Asset already exists in scene'
	
def assetUpdateMatch():
	print 'Assets do not match. Update canceled.'
	
def chkDirSize():
	print 'Comparing directory sizes...'
	
def chooseCameraPreview():
	print 'Please choose a camera view to preview from'
	
def concurrentPublish():
	return 'Another publish for the same asset is currently under progress. Please check your settings or try again later.'

def dailyFail():
	return 'Could not verify daily files.'

def gpsPreview_uiValues():
	print 'Not all GPS Preview UI values could be read'

def gpsToolDeploy(status):
	print 'Deploying GPS tools - %s' % status

def icarusLaunch(icarusVersion, icarusLocation):
	print 'GRAMERCY PARK STUDIOS - ICARUS %s\n' % icarusVersion
	
def ignored(asset):
	print '%s ignored' % asset

def illegalCharacters(string=''):
	print '"%s" contains illegal characters.' % string
	
def integersInput(input):
	print '%s input must be integers' % input

def itemSel():
	print 'Please select one item'
		
def launchApp(application):
	print 'Launching %s...' % application

def jobSet(job, shot):
	print 'Job set. Working on %s - %s' % (job, shot)

def lightLinkError(lightRelinkResult):
	print 'Light link error: The following objects could not be relinked.\n%s' % lightRelinkResult

def locatorsOnly():
	print 'Only locators can be published as nulls.'

def lodARequired():
	raise('lodA level required')

def nameConflict(assetName):
	print 'Asset with name "%s" already exists in scene. Existing asset has been renamed' % assetName

def noAsset():
	print 'Could not find any compatible assets'
	
def noDir():
	print 'Could not find the specified directory'
	
def noDirContents():
	print 'The specified directory is empty'
	
def noEnv():
	print 'Could not lanuch Icarus - No environment could be found'

def noFile():
	print 'Could not find the specified file'

def noGetTranforms():
	print 'Could not get object transforms'
	
def noHrox(hroxFile):
	print '%s - File could not be found.' % hroxFile
	
def noICSetsPbl():
	print 'ICSets cannot be selected for publishing'

def noJob(job):
	print 'ERROR: The job path "%s" does not exist. The job may have been archived, moved or deleted.' % job
	
def noMainLayer():
	print 'Please set a main layer'
	
def noNotes():
	print 'No notes found'

def noPermissionsSet():
	print 'Warning: Permissions could not be set'
	
def noReference():
	print 'The specified node is not a reference'

def noRefPbl():
	print 'Cannot publish referenced assets'
	
def noRefTag():
	print 'No reference tag found'
	
def noRendersPbl():
	print 'No renders have been published'

def noSel():
	print 'Nothing selected'
	
def noSeq(dir):
	print '\nNo sequence or bad sequence format found in\n\n%s\n\nSequences must have the format [<file_name>.<padding>.<extension>]' % dir
	
def noSetsPbl():
	print 'Sets cannot be selected for publishing'

def noShot(shot):
	print 'ERROR: No valid shots found in job path "%s".' % shot

def notCamera():
	print 'The current selection is not a camera'
	
def noVersion():
	print 'No versioning detected'
	
def notVersionManagerCompatible(icSet):
	print 'The selected ICSet is not compatible with Version Manager'

def pblFeed(msg=None, begin=None, end=None):
	if msg:
		print msg
		return
	if begin:
		print 'Publishing...'
		return
	if end:
		print 'Done.'
		return
		
def pblRollback():
	msg =  'Current publish has been rolled back. No changes made.\nCheck console output for details'
	print msg	
	return msg

def pblAssetReq():
	print 'Animation can only be published from published assets'
	
def pointCloudParticle():
	print 'pointCloud publishing requires a particle or nParticle object'
	
def processing(asset=None):
	print 'processing: %s...' % asset
	
def recentFiles_notWritten():
	print '[Icarus] Warning: unable to write recent files configuration file.'
	
def redFields():
	print 'All fields in red are mandatory'
	
def renderElements(layer=None, pass_=None, versionHeader=False):
	if versionHeader:
		print '\n\nRENDER PUBLISH INFO: %s\n--\n[<layer>_<pass>]\n--' % versionHeader
		return
	else:
		print '[%s_%s]' % (layer, pass_)
		
def shaderLinkError(shaderRelinkResult):
	print 'Shader link error: The following objects could not be relinked.\n%s' % shaderRelinkResult

def shaderSupport():
	print 'The specified node is not a shading group'

def userPrefs_notWritten():
	print '[Icarus] Warning: unable to write user prefs configuration file.'
	
