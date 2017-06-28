#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:versionUp
#copyright	:Gramercy Park Studios

#This module versions up the realflow project properly by copying the entire project up-versioning

import os

def version(scene, GUIMessageDialog, GUIFormDialog):
	dialog = GUIFormDialog.new()
	dialog.setTitle('GPS - Up Version Project')
	dialog.addStringField('Current project and all data will be duplicated and versioned up. Contiue?','')
	dialogResult = dialog.show()
	if not dialogResult:
		return
	#getting scene and project name and blocking execution if not saved
	sceneName = scene.getFileName()
	if sceneName == None:
		dialog = GUIMessageDialog.new()
		dialog.show(bool('ALERT_TYPE_WARNING'), "Scene must be saved before up-versioning the project")
		return
	projPath = scene.getRootPath()
	projName = os.path.split(projPath)[-1]
	#gets current and new version
	currentVersion, newVersion = vCtrl(os.environ['REALFLOWSCENESDIR'], projName)
	
	#removing version naming convention from project name
	projName = projName.replace('_%s' % currentVersion, "")
	
	newProjPath = '%s/%s_%s' % (os.environ['REALFLOWSCENESDIR'], projName, newVersion)
	
	#saving current scene and 
	scene.save('%s/%s' % (projPath, sceneName))
	
	#user message
	scene.message('Up-versioning project...')
	#creating directoties and copying project
	os.system('mkdir %s' % newProjPath)
	os.system('cp -r %s/* %s' % (projPath, newProjPath))
	
	#loading new project scene
	scene.load('%s/%s' % (newProjPath, sceneName))
	
	#report dialog
	dialog = GUIMessageDialog.new()
	dialog.show(bool('ALERT_TYPE_INFORMATION'), "Project has been up-versioned to %s" % newVersion)


#version control
def vCtrl(path, stringMatch=None):
	pathContents = os.listdir(path)
	projVersionLs = []
	for content in pathContents:
		vSplit = content.split('_')[-1]
		if vSplit.startswith('v'):
			digitSplit = vSplit.replace('v', '')
			if digitSplit.isdigit():
				nameBody = content.split('_')[:-1]
				if stringMatch:
					if stringMatch in content:
						projVersionLs.append(int(digitSplit))
				else:
					projVersionLs.append(int(digitSplit))
	if len(projVersionLs) == 0:
		currentVersion = 0
	else:
		currentVersion = max(projVersionLs)
	
	padding = '00'
	newVersion = currentVersion + 1
	if newVersion > 9:
		nvPadding = '0'
	else:
		nvPadding = padding
	if currentVersion > 9:
		cvPadding = '0'
	else:
		cvPadding = padding
	
	##APPEDING "v" AND PADDING TO VERSION##
	newVersion = "v%s%s" % (nvPadding, newVersion)
	currentVersion = "v%s%s" % (cvPadding, currentVersion)
	return currentVersion, newVersion
