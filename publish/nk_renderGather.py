#!/usr/bin/python

# [Icarus] nk_renderGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Gather an asset of type 'render'.


import os
import nuke
from shared import os_wrapper


def gather(gatherPath):
	dialogPathLs = nuke.getClipname('Render Gather', default='%s/' % gatherPath, multiple=True)

	if dialogPathLs:
		for dialogPath in dialogPathLs:
			try:
				filePath, frameRange = dialogPath.split(' ')
				startFrame, endFrame = frameRange.split('-')
				filePathTail = os.path.split(filePath)[-1]
				fileName = '%s_%s' % (os.environ['IC_VENDOR_INITIALS'], filePathTail.split('.')[0])
			except ValueError:
				filePath = dialogPath
				startFrame, endFrame = os.environ['IC_STARTFRAME'], os.environ['IC_ENDFRAME']
				fileName = '%s_Render_Read' % os.environ['IC_VENDOR_INITIALS']

			# Make file path relative
			# filePath = os_wrapper.relativePath(filePath, 'IC_SHOTPUBLISHDIR', tokenFormat='nuke')

			readNode = nuke.createNode('Read', 'name %s' % fileName)
			readNode.knob('file').setValue(filePath)
			readNode.knob('cacheLocal').setValue('always')
			readNode.knob('cached').setValue('True')
			readNode.knob('first').setValue(int(startFrame))
			readNode.knob('last').setValue(int(endFrame))

		return readNode

