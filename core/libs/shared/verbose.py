#!/usr/bin/python

# [Icarus] verbose.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# This module handles the output of messages, warnings and errors.


import os


# Define some ANSI colour codes
# class bcolors:
# 	HEADER = '\033[95m'
# 	OKBLUE = '\033[94m'
# 	OKGREEN = '\033[92m'
# 	WARNING = '\033[93m'
# 	FAIL = '\033[91m'
# 	ENDC = '\033[0m'
# 	BOLD = '\033[1m'
# 	UNDERLINE = '\033[4m'

statusBar = None


def message(message):
	""" Print a message.
	"""
	print_(message, 3)

def warning(message):
	""" Print a warning message.
	"""
	#print_(bcolors.WARNING + "Warning: " + message + bcolors.ENDC, 2)
	print_("Warning: " + message, 2)

def error(message):
	""" Print an error message.
	"""
	#print_(bcolors.FAIL + "ERROR: " + message + bcolors.ENDC, 1)
	print_("ERROR: " + message, 1)


def print_(message, verbosityLevel=3, status=True, log=False):
	""" Print the message to the console.
		If 'status' is True, the message will be shown on the main UI status
		bar.
		If 'log' is True, the message will be written to a logfile (not yet
		implemented).

		Verbosity Levels:
		0 - Nothing is output
		1 - Errors and messages requiring user action
		2 - Errors and warning messages
		3 - Info message (default)
		4 - Detailed info messages
	"""
	global statusBar

	try:
		verbositySetting = int(os.environ['IC_VERBOSITY'])
	except KeyError:
		verbositySetting = 3

	# Print message to the console
	if verbosityLevel <= verbositySetting:
		print(message)

	# Print message to the status bar
	if verbosityLevel <= 3 and status and statusBar is not None:
		timeout = 1800 + max(2400, len(message)*60)
		statusBar.showMessage(message, timeout)


def registerStatusBar(statusBarObj):
	""" Register a QStatusBar object with this module so that messages can be
		printed to the appropriate UI status bar.
	"""
	global statusBar
	statusBar = statusBarObj


def pluralise(noun, count=None):
	""" Pluralise nouns.
		if 'count' variable is given, return singular if count is 1, otherwise
		return plural form.
		In the name of simplicity, this function is far from exhaustive.
	"""
	if count is not None:
		if count == 1:
			return noun

	import re

	if re.search('[^fhms][ei]x$', noun):
		return re.sub('[ei]x$', 'ices', noun)
	elif re.search('[sxz]$', noun):
		return re.sub('$', 'es', noun)
	elif re.search('[^aeioudgkprt]h$', noun):
		return re.sub('$', 'es', noun)
	elif re.search('[^aeiou]y$', noun):
		return re.sub('y$', 'ies', noun)
	elif re.search('ies$', noun):
		return noun
	else:
		return noun + 's'


# Messages follow in alphabetical order...
def appPaths_noApp(app):
	warning("Application '%s' does not exist." %app)

def appPaths_noVersion(app, ver):
	warning("Application '%s' has no '%s' version." %(app, ver))

def appPaths_enterVersion():
	print_("Please enter a version.", 1)

def appPaths_guessPathFailed(os):
	warning("Failed to guess %s path." %os)

def animRequires(asset):
	print_("Requires %s" %asset, 1)

def assetConflict():
	error("Asset already exists in scene.")

def assetUpdateMatch():
	warning("Assets do not match. Update cancelled.")

def chkDirSize():
	message("Comparing directory sizes...")

def concurrentPublish():
	return "Another publish for the same asset is currently under progress. Please check your settings or try again later."

def dailyFail():
	return "Could not verify dailies files."

def gpsPreview_uiValues():
	warning("Not all GPS Preview UI values could be read.")

def gpsToolDeploy(status):
	message("Deploying GPS tools... %s" %status)

def icarusLaunch(name, version, vendor="", location="", user=""):
	print_("%s %s" %(name, version), 0)
	print_(vendor, 0)
	print_('[Running from "%s"]' %location, 4)
	print_('[User: %s]' %user, 4)
	print_('', 0)

def ignored(asset):
	warning("%s ignored" %asset)

def illegalCharacters(string=''):
	error('"%s" contains illegal characters.' %string)

def integersInput(input_):
	error("%s input must be integers." %input_)

def itemSel():
	print_("Please select one item.", 1)

def launchApp(application):
	message("Launching %s..." %application)

def launchAppNotFound(application):
	error("Unable to launch %s - the executable could not be found." %application)

def launchAppNotSet(application):
	error("Unable to launch %s - executable path not set. Please set the correct location from the Job Settings dialog." %application)

def jobSet(job, shot):
	message("Shot set: Now working on %s - %s" %(job, shot))

def lightLinkError(lightRelinkResult):
	print_('Light link error: The following objects could not be relinked.\n%s' %lightRelinkResult, 1)

def locatorsOnly():
	warning("Only locators can be published as nulls.")

def lodARequired():
	raise("lodA level required.")

def nameConflict(assetName):
	warning('Asset with name "%s" already exists in scene. Existing asset has been renamed.' %assetName)

def noAsset():
	error("Could not find any compatible assets.")

def noDir():
	error("Could not find the specified directory.")

def noDirContents():
	warning("The specified directory is empty.")

def noFile():
	error("Could not find the specified file.")

def noGetTranforms():
	error("Could not get object transforms.")

def noICSetsPbl():
	error("ICSets cannot be selected for publishing")

def noMainLayer():
	print_("Please set a main layer.", 1)

def noNotes():
	warning("No notes found.")

def noPermissionsSet():
	warning("Permissions could not be set.")

def noReference():
	error("The specified node is not a reference.")

def noRefPbl():
	error("Cannot publish referenced assets.")

def noRefTag():
	error("No reference tag found.")

def noRendersPbl():
	error("No renders have been published.")

def noSel():
	warning("Nothing selected.")

def noSeq(dir):
	print_('"%s": No sequence or bad sequence format.\nSequences must be in the format [<filename>.<padding>.<extension>]' %dir, 2)

def noSetsPbl():
	error("Sets cannot be selected for publishing.")

def notCamera():
	warning("The current selection is not a camera.")

def noVersion():
	error("No versioning detected.")

def notVersionManagerCompatible(icSet):
	error("The selected ICSet is not compatible with Version Manager.")

def pblFeed(msg=None, begin=None, end=None):
	if msg:
		print_(msg, 3)
		return
	if begin:
		print_("Publishing...", 3)
		return
	if end:
		print_("Done.", 3)
		return

def pblRollback():
	msg = "Current publish has been rolled back. No changes made.\nCheck console output for details."
	print_(msg, 1)
	return msg

def pblAssetReq():
	error("Animation can only be published from published assets.")

def pblSaveSnapshot():
	message("Saving snapshot...")

def pointCloudParticle():
	error("pointCloud publishing requires a particle or nParticle object.")

def processing(asset=None):
	message("Processing: %s..." %asset)

def recentFiles_notWritten():
	warning("Unable to write recent files configuration file.")

def redFields():
	print_("All fields in red are mandatory", 1)

def renderElements(layer=None, pass_=None, versionHeader=False):
	if versionHeader:
		print_('\n\nRENDER PUBLISH INFO: %s\n--\n[<layer>_<pass>]\n--' %versionHeader, 3)
		return
	else:
		print_('[%s_%s]' %(layer, pass_), 3)

def shaderLinkError(shaderRelinkResult):
	print_("Shader link error: The following objects could not be relinked.\n%s" %shaderRelinkResult, 1)

def shaderSupport():
	warning("The specified node is not a shading group.")

