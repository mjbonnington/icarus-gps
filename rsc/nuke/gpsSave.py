#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title		:gpsSave
#copyright	:Gramercy Park Studios

import os
import nuke
import recentFiles, osOps


def updateRecentFilesMenu(menu):
	""" Populates the recent files menu, disables it if no recent files in list
	"""
	enable = True;
	fileLs = recentFiles.getLs('nuke') # explicitly stating 'nuke' environment to get around 'nuke_tmp' fix

	# Delete all items in the pop-up menu
	menu.clearMenu()

	# Re-populate the items in the pop-up menu
	for item in fileLs:
		openRecentCmdStr = 'nuke.scriptOpen(\"%s%s\")' %(os.environ["SHOTPATH"], item)
		menu.addCommand(item.replace('/', '\/'), openRecentCmdStr.replace('\\', '/')) # forward slashes need escaping to prevent Nuke from interpreting them as sub-menus

	# If recent file list contains no entries, disable menu
	if len(fileLs)==0:
		enable = False
	if len(fileLs)==1 and fileLs[0]=="":
		enable = False

	menu.setEnabled(enable)


def updateRecentFiles(script=None):
	""" Adds a script to the recent files list config file. If script is not specified use current script name
	"""
	if script == None:
		script = os.path.abspath( nuke.value("root.name") )

	#nuke.tprint('Adding script %s to recent files list.' %script)

	# Add entry to recent files config file
	recentFiles.updateLs(script, 'nuke') # explicitly stating 'nuke' environment to get around 'nuke_tmp' fix

	# Update GPS custom recent files menu(s)
	updateRecentFilesMenu( nuke.menu('Nuke').menu('File').menu('[GPS] Open Recent') )
	updateRecentFilesMenu( nuke.menu('Nodes').menu('Open').menu('Open Recent') )


#strips all naming conventions and returns script name
def getWorkingScriptName():
	workingScript = nuke.root().name()
	if not os.path.isfile(workingScript):
		return
	try:
		#spliting path and getting file name only
		scriptName = os.path.split(workingScript)[1]
		#getting rid of all naming conventions to get script name only
		scriptName = scriptName.split('%s_' % os.environ['SHOT'])[-1]
		version = scriptName.split('_')[-1]
		scriptName = scriptName.split('_%s' % version)[0]
		#getting rid of padding and extension
		scriptName = scriptName.split('.')[0]
		return scriptName
	except:
		return


#prompts for script name
def getInputName():
	#gets script name from input and strips white spaces
	defaultName  = getWorkingScriptName()
	if not defaultName:
		defaultName = 'preComp'
	scriptName = nuke.getInput( 'Script Name', defaultName)
	if scriptName:
		scriptName = scriptName.replace( ' ', '' )
		return scriptName
	else:
		return


#saves script, saves As or incremental
def save(incr=False, saveAs=False):
	#getting script name
	if saveAs:
		scriptName = getInputName()
		incr=True
	else:
		scriptName = getWorkingScriptName()
		if not scriptName:
			scriptName = getInputName()
			incr=True
	if not scriptName:
		return
	#saving file
	if incr:
		fileSaved = False
		version = 1
		while not fileSaved:
			#file path
			nkPath = os.path.join(os.environ['NUKESCRIPTSDIR'], '%s_%s_v%03d.nk' % (os.environ['SHOT'], scriptName, version))
			#versioning
			if os.path.isfile( nkPath ):
				version += 1
				continue
			#saving script
			nuke.scriptSaveAs( nkPath )
			#updating recent files list
			updateRecentFiles( nkPath )
			fileSaved = True
			#opening permissions on written file
			osOps.setPermissions(nkPath)

	else:
		nuke.scriptSave()
		nkPath = getWorkingScriptName()
	return nkPath
