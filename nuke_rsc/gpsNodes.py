#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsNodes
#copyright	:Gramercy Park Studios

import os
import nuke
import gpsSave, vCtrl
	
#gps write
def write_():
	scriptName = gpsSave.getWorkingScriptName()
	if not scriptName:
		scriptName = 'untitled'
	paddingExt = '%04d.exr'
	fileName = '%s_%s.%s' % (os.environ['SHOT'], scriptName, paddingExt)
	writeDir = '%s/%s' % (os.environ['NUKERENDERSDIR'], scriptName)
	version = vCtrl.version(writeDir)
	filePath = os.path.join('[getenv NUKERENDERSDIR]', scriptName, version, fileName)
	startFrame = os.environ['STARTFRAME']
	endFrame = os.environ['ENDFRAME']
	writeNode = nuke.createNode('Write', 'name GPS_Write')
	writeNode.knob('file').setValue(filePath)
	writeNode.knob('beforeRender').setValue('gpsNodes.createWriteDir()')
	writeNode.knob('channels').setValue('rgba')
	writeNode.knob('file_type').setValue('exr')
	writeNode.knob('datatype').setValue('16 bit half')
	writeNode.knob('compression').setValue('Zip (16 scanlines)')
	writeNode.knob('use_limit').setValue('True')
	writeNode.knob('first').setValue(int(startFrame))
	writeNode.knob('last').setValue(int(endFrame))
	
	return writeNode
	
#gps read
def read_():
	readDir = '%s/' % os.environ['SHOTPATH']
	dialogPathLs = nuke.getClipname('Read File(s)', default=readDir, multiple=True)
	if dialogPathLs:
		for dialogPath in dialogPathLs:
			try:
				filePath, frameRange = dialogPath.split(' ')
				startFrame, endFrame = frameRange.split('-')
			except ValueError:
				filePath = dialogPath
				startFrame, endFrame = os.environ['STARTFRAME'], os.environ['ENDFRAME']
				
			#making filePath relative
			if os.environ['SHOTPATH'] in filePath:
				filePath = filePath.replace(os.environ['SHOTPATH'], '[getenv SHOTPATH]')
				
			readNode = nuke.createNode('Read', 'name GPS_Read')
			readNode.knob('file').setValue(filePath)
			readNode.knob('cacheLocal').setValue('always')
			readNode.knob('cached').setValue('True')
			readNode.knob('first').setValue(int(startFrame))
			readNode.knob('last').setValue(int(endFrame))
	
		return readNode
			
#creates write node directory	
def createWriteDir():
	path = os.path.dirname(nuke.filename(nuke.thisNode()))
	if not os.path.isdir(path):
		os.system('mkdir -p %s' % path)
	



	