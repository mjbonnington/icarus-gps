#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:nk_assetGather
#copyright	:Gramercy Park Studios

import os
import nuke

def gather(gatherPath):
	dialogPathLs = nuke.getClipname('Render Gather', default='%s/' % gatherPath, multiple=True)
	if dialogPathLs:
		for dialogPath in dialogPathLs:
			try:
				filePath, frameRange = dialogPath.split(' ')
				startFrame, endFrame = frameRange.split('-')
				filePathTail = filePath.split('/')[-1]
				fileName = 'GPS_%s' % filePathTail.split('.')[0]
			except ValueError:
				filePath = dialogPath
				startFrame, endFrame = os.environ['STARTFRAME'], os.environ['ENDFRAME']
				fileName = 'GPS_Render_Read'
				
			#making filePath relative
			if os.environ['SHOTPUBLISHDIR'] in filePath:
				filePath = filePath.replace(os.environ['SHOTPUBLISHDIR'], '[getenv SHOTPUBLISHDIR]')
				
			readNode = nuke.createNode('Read', 'name %s' % fileName)
			readNode.knob('file').setValue(filePath)
			readNode.knob('cacheLocal').setValue('always')
			readNode.knob('cached').setValue('True')
			readNode.knob('first').setValue(int(startFrame))
			readNode.knob('last').setValue(int(endFrame))
	
		return readNode