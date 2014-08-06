#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsSave
#copyright	:Gramercy Park Studios

import os
import nuke

#strips all naming conventions and returns script name
def getWorkingScriptName():
	workingScript = nuke.root().name()
	if not os.path.isfile(workingScript):
		return
	try:
		#spliting path and getting file name only
		scriptName = os.path.split(workingScript)[1]
		#getting rid of all conventions
		scriptName = scriptName.split('_')[-2]
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
		   nkPath = '%s/%s_%s_%s_v%03d.nk' % (os.environ['NUKESCRIPTSDIR'], os.environ['JOB'], os.environ['SHOT'], scriptName, version )
		   #versioning
		   if os.path.isfile( nkPath ):
			  version += 1
			  continue
		   #saving script
		   nuke.scriptSaveAs( nkPath )
		   fileSaved = True

	else:
		nuke.scriptSave()
		nkPath = getWorkingScriptName()
	return nkPath
	
	