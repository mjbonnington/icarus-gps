#!/usr/bin/python

# [Icarus] nk_renderGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Gather an asset of type 'render'.


import os
import osOps
import nuke


def gather(gatherPath):
	dialogPathLs = nuke.getClipname('Render Gather', default='%s/' % gatherPath, multiple=True)

	if dialogPathLs:
		for dialogPath in dialogPathLs:
			try:
				filePath, frameRange = dialogPath.split(' ')
				startFrame, endFrame = frameRange.split('-')
				filePathTail = os.path.split(filePath)[-1]
				fileName = 'GPS_%s' % filePathTail.split('.')[0]
			except ValueError:
				filePath = dialogPath
				startFrame, endFrame = os.environ['STARTFRAME'], os.environ['ENDFRAME']
				fileName = 'GPS_Render_Read'

			# Make file path relative
			# filePath = osOps.relativePath(filePath, 'SHOTPUBLISHDIR', tokenFormat='nuke')

			readNode = nuke.createNode('Read', 'name %s' % fileName)
			readNode.knob('file').setValue(filePath)
			readNode.knob('cacheLocal').setValue('always')
			readNode.knob('cached').setValue('True')
			readNode.knob('first').setValue(int(startFrame))
			readNode.knob('last').setValue(int(endFrame))

		return readNode

