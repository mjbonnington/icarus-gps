#!/usr/bin/python

# [GPS] nukeOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Nuke operations module.


import os
import nuke


def createBackdrop(bckdName, nodeLs):
	""" Creates a custom backdrop for selection.
	"""
	#getting bounds of selected nodes
	bdX = min([node.xpos() for node in nodeLs])
	bdY = min([node.ypos() for node in nodeLs])
	bdW = max([node.xpos() + node.screenWidth() for node in nodeLs]) - bdX
	bdH = max([node.ypos() + node.screenHeight() for node in nodeLs]) - bdY
	#expanding borders
	left, top, right, bottom = (-80, -90, 80, 20)
	bdX += left
	bdY += top
	bdW += (right - left)
	bdH += (bottom - top)
	resolveNameConflict(bckdName)
	icBackdrop = nuke.nodes.BackdropNode(
	name = bckdName, 
	xpos = bdX, 
	bdwidth = bdW, 
	ypos = bdY, 
	bdheight = bdH)
	return icBackdrop


def createGroup(grpName, show=False):
	""" Creates a custom group from selection.
	"""
	#creating group and adding custom attributes
	resolveNameConflict(grpName)
	icGroup = nuke.makeGroup(show)
	icGroup['name'].setValue(grpName)
	return icGroup


def exportSelection(pathToPblAsset):
	""" Exports selection.
	"""
	return nuke.nodeCopy(pathToPblAsset)


def launchDjv():
	""" Launches djv_view, if a read or write node is selected the appropriate sequence will be loaded.
		TODO: Evaluate [getenv VARIABLE] inside string to get the correct path.
	"""
	import djvOps

	filePath = ''
	selectedNodes = nuke.selectedNodes()
	for selectedNode in selectedNodes:
		if (selectedNode.Class() == 'Read') or (selectedNode.Class() == 'Write'):
			# try:
			# 	import nukescripts
			# 	filePath = nukescripts.replaceHashes( selectedNode['file'].value() ) % nuke.frame()
			# except TypeError:
			# 	filePath = selectedNode.knob('file').getValue()
			filePath = selectedNode.knob('file').evaluate()

	#nuke.message(filePath)
	djvOps.viewer(filePath)


def resolveNameConflict(name):
	""" Bypasses Nuke name conflict behaviour by appending '_' to the original node name.
	"""
	if nuke.exists(name):
		node = nuke.toNode(name)
		solvedName = '%s_' % node['name'].value()
		while nuke.exists(solvedName):
			solvedName += '_'
		node['name'].setValue(solvedName)


def saveAs(pathToPblAsset):
	""" Saves script.
	"""
	return nuke.scriptSaveAs(pathToPblAsset)


def submitRender():
	""" Launches GPS Render Submitter window.
	"""
	import submit__main__
	reload(submit__main__)
	#frameRange = "%s-%s" %(int(mc.getAttr('defaultRenderGlobals.startFrame')), int(mc.getAttr('defaultRenderGlobals.endFrame')))
	renderSubmitApp=submit__main__.gpsRenderSubmitApp(flags='-i') # the -i flag tells Nuke to use an interactive license rather than a render license
	renderSubmitApp.exec_()


def submitRenderSelected():
	""" Launches GPS Render Submitter window, for rendering the currently selected write nodes only.
	"""
	import submit__main__
	reload(submit__main__)
	#frameRange = "%s-%s" %(int(mc.getAttr('defaultRenderGlobals.startFrame')), int(mc.getAttr('defaultRenderGlobals.endFrame')))

	writeNodes = ''
	selectedNodes = nuke.selectedNodes()
	for selectedNode in selectedNodes:
		if selectedNode.Class() == 'Write':
			writeNodes = '-X %s ' %selectedNode.name()

	# selectedNode = nuke.selectedNode()
	# if selectedNode.Class() == 'Write':
	# 	writeNodes = '-X %s ' %selectedNode.name()

	renderSubmitApp=submit__main__.gpsRenderSubmitApp(flags='-i %s' %writeNodes)
	renderSubmitApp.exec_()


def viewerSnapshot(pblPath):
	""" Takes a snapshot from the active viewer.
	"""
	try:
		writeNode = ''
		pblPath = os.path.join(pblPath, 'preview.%04d.jpg')
		#getting viewer to set as write input
		viewer = nuke.activeViewer()
		actFrame = int(nuke.knob("frame"))
		actInput = nuke.ViewerWindow.activeInput(viewer)
		viewNode = nuke.activeViewer().node()
		selInput = nuke.Node.input(viewNode, actInput)
		#creating custom write node
		writeNode = nuke.createNode('Write', 'name pblSnapshot_Write')
		writeNode.setInput(0, selInput)
		writeNode.knob('file').setValue(pblPath)
		#writeNode.knob('beforeRender').setValue('gpsNodes.createWriteDir()')
		writeNode.knob('channels').setValue('rgb')
		writeNode.knob('file_type').setValue('jpg')
		#snapshoting
		nuke.execute(writeNode.name(), actFrame, actFrame)
		#deleting write node
		nuke.delete(writeNode)
	except (RuntimeError, TypeError):
		#deleting write node
		if writeNode:
			nuke.delete(writeNode)
		return

