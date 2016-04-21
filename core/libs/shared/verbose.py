#!/usr/bin/python

# [Icarus] verbose.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# This module processes verbosity printing.


import userPrefs
userPrefs.read()
if not userPrefs.config.has_option('main', 'verbosity'):
	userPrefs.config.set('main', 'verbosity', '3')


statusBar = None


def print_(message, verbosityLevel=3, status=True, log=False):
	""" Print the message to the console.
		If 'status' is True, the message will be shown on the main UI status bar.
		If 'log' is True, the message will be written to a logfile (not yet implemented).

		Verbosity Levels:
		0 - Nothing is output
		1 - Errors and messages requiring user action
		2 - Errors and warning messages
		3 - Info message (default)
		4 - Detailed info messages
	"""
	global statusBar

	userPrefs.read()

	if verbosityLevel <= userPrefs.config.getint('main', 'verbosity'):
		print message

	if verbosityLevel <= 3 and status and statusBar is not None:
		statusBar.showMessage(message, 10000)


def registerStatusBar(statusBarObj):
	""" Register a QStatusBar object with this module so that messages can be printed to the appropriate UI status bar.
	"""
	global statusBar
	statusBar = statusBarObj


# Messages follow in alphabetical order...
def appPaths_noApp(app):
	print_( "Warning: Application '%s' does not exist." % app, 2 )

def appPaths_noVersion(app, ver):
	print_( "Warning: Application '%s' has no '%s' version." % (app, ver), 2 )

def appPaths_enterVersion():
	print_( "Please enter a version.", 1 )

def appPaths_guessPathFailed(os):
	print_( "Warning: Failed to guess %s path." % os, 2 )

#def approval(start=False, end=False):
#	if start:
#		print_( 'Processing approval...', 3 )
#		return
#	if end:
#		print_( 'Approved.', 3 )
#		return
#
#def approvalOSError():
#	print_( 'Warning: Some assets may not have gone through the approval process. Some file links may be missing.', 2 )

def animRequires(asset):
	print_( 'Requires %s' % asset, 1 )

def assetConflict():
	print_( 'Asset already exists in scene', 2 )

def assetUpdateMatch():
	print_( 'Assets do not match. Update cancelled.', 2 )

def chkDirSize():
	print_( 'Comparing directory sizes...', 3 )

def concurrentPublish():
	return 'Another publish for the same asset is currently under progress. Please check your settings or try again later.'

def dailyFail():
	return 'Could not verify daily files.'

def defaultJobSettings():
	print_( "Unable to load job settings. Default values have been applied.\nPlease review the settings in the editor and click Save when done.", 1 )

def gpsPreview_uiValues():
	print_( 'Not all GPS Preview UI values could be read', 2 )

def gpsToolDeploy(status):
	print_( 'Deploying GPS tools... %s' % status, 3 )

def icarusLaunch(icarusVersion, icarusLocation=""):
	print_( 'GRAMERCY PARK STUDIOS - ICARUS %s\n' % icarusVersion, 0 )

def ignored(asset):
	print_( '%s ignored' % asset, 2 )

def illegalCharacters(string=''):
	print_( '"%s" contains illegal characters.' % string, 1 )

def integersInput(input):
	print_( '%s input must be integers' % input, 1 )

def itemSel():
	print_( 'Please select one item', 1 )

def launchApp(application):
	print_( 'Launching %s...' % application, 3 )

def launchAppNotFound(application):
	print_( 'ERROR: Unable to launch %s - the executable could not be found.' % application, 2 )

def launchAppNotSet(application):
	print_( 'ERROR: Unable to launch %s - executable path not set. Please set the correct location from the job settings window.' % application, 2 )

def jobSet(job, shot):
	print_( 'Shot set: Now working on %s - %s' % (job, shot), 3 )

def lightLinkError(lightRelinkResult):
	print_( 'Light link error: The following objects could not be relinked.\n%s' % lightRelinkResult, 1 )

def locatorsOnly():
	print_( 'Only locators can be published as nulls.', 2 )

def lodARequired():
	raise('lodA level required')

def nameConflict(assetName):
	print_( 'Asset with name "%s" already exists in scene. Existing asset has been renamed' % assetName, 2 )

def noAsset():
	print_( 'Could not find any compatible assets', 1 )

def noDir():
	print_( 'Could not find the specified directory', 1 )

def noDirContents():
	print_( 'The specified directory is empty', 2 )

def noEnv():
	print_( 'Could not launch Icarus - No environment could be found', 1 )

def noFile():
	print_( 'Could not find the specified file', 1 )

def noGetTranforms():
	print_( 'Could not get object transforms', 1 )

def noHrox(hroxFile):
	print_( '%s - File could not be found.' % hroxFile, 1 )

def noICSetsPbl():
	print_( 'ICSets cannot be selected for publishing', 1 )

def noJob(job):
	print_( 'ERROR: The job path "%s" does not exist. The job may have been archived, moved or deleted.' % job, 1 )

def noJobs():
	print_( 'ERROR: No active jobs found.', 2 )

def noMainLayer():
	print_( 'Please set a main layer', 1 )

def noNotes():
	print_( 'No notes found', 2 )

def noPermissionsSet():
	print_( 'Warning: Permissions could not be set', 2 )

def noReference():
	print_( 'The specified node is not a reference', 1 )

def noRefPbl():
	print_( 'Cannot publish referenced assets', 1 )

def noRefTag():
	print_( 'No reference tag found', 1 )

def noRendersPbl():
	print_( 'No renders have been published', 1 )

def noSel():
	print_( 'Nothing selected', 2 )

def noSeq(dir):
	print_( "'%s': No sequence or bad sequence format.\nSequences must be in the format [<filename>.<padding>.<extension>]" % dir, 2 )

def noSetsPbl():
	print_( 'Sets cannot be selected for publishing', 1 )

def noShot(shot):
	print_( 'Warning: No valid shots found in job path "%s".' % shot, 2 )

def notCamera():
	print_( 'The current selection is not a camera', 2 )

def noVersion():
	print_( 'No versioning detected', 1 )

def notVersionManagerCompatible(icSet):
	print_( 'The selected ICSet is not compatible with Version Manager', 1 )

def pblFeed(msg=None, begin=None, end=None):
	if msg:
		print_( msg, 3 )
		return
	if begin:
		print_( 'Publishing...', 3 )
		return
	if end:
		print_( 'Done.', 3 )
		return

def pblRollback():
	msg = 'Current publish has been rolled back. No changes made.\nCheck console output for details'
	print_( msg, 1 )
	return msg

def pblAssetReq():
	print_( 'Animation can only be published from published assets', 1 )

def pblSaveSnapshot():
	print_( 'Saving snapshot...', 3 )

def pointCloudParticle():
	print_( 'pointCloud publishing requires a particle or nParticle object', 1 )

def processing(asset=None):
	print_( 'processing: %s...' % asset, 3 )

def recentFiles_notWritten():
	print_( 'Warning: unable to write recent files configuration file.', 2 )

def redFields():
	print_( 'All fields in red are mandatory', 1 )

def renderElements(layer=None, pass_=None, versionHeader=False):
	if versionHeader:
		print_( '\n\nRENDER PUBLISH INFO: %s\n--\n[<layer>_<pass>]\n--' % versionHeader, 3 )
		return
	else:
		print_( '[%s_%s]' % (layer, pass_), 3 )

def settingsData_written(settingsType):
	print_( "%s settings data file saved." % settingsType, 3 )

def settingsData_notWritten(settingsType):
	print_( "Error: %s settings data file could not be saved." % settingsType, 1 )

def settingsData_notFound(settingsType, dataFile=""):
	print_( "Warning: %s settings data file not found: %s" % (settingsType, dataFile), 2 )

def settingsData_convert(settingsInFile, settingsOutFile=None):
	if settingsOutFile is None:
		settingsOutFile = settingsInFile
	print_( "Converting %s.py to %s.xml" % (settingsInFile, settingsOutFile), 3 )

def shaderLinkError(shaderRelinkResult):
	print_( 'Shader link error: The following objects could not be relinked.\n%s' % shaderRelinkResult, 1 )

def shaderSupport():
	print_( 'The specified node is not a shading group', 2 )

def userPrefs_notWritten():
	print_( 'Warning: unable to write user prefs configuration file.', 2 )

def xmlData_readError(datafile):
	print_( "Warning: XML data file is invalid or doesn't exist: %s" % datafile, 2 )

