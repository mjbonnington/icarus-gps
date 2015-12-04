#!/usr/bin/python

# [GPS] nukeOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Nuke operations module.


import os
import nuke

#creates a custom backdrop for selection
def createBackdrop(bckdName, nodeLs):
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


#creates a custom group from selection
def createGroup(grpName, show=False):
	#creating group and adding custom attributes
	resolveNameConflict(grpName)
	icGroup = nuke.makeGroup(show)
	icGroup['name'].setValue(grpName)
	return icGroup


#exports selection
def exportSelection(pathToPblAsset):
	return nuke.nodeCopy(pathToPblAsset)
	
#bypasses nuke name conflict behaviour by appending '_' the original node name
def resolveNameConflict(name):
	if nuke.exists(name):
		node = nuke.toNode(name)
		solvedName = '%s_' % node['name'].value()
		while nuke.exists(solvedName):
			solvedName += '_'
		node['name'].setValue(solvedName)
	
#saves script
def saveAs(pathToPblAsset):
	return nuke.scriptSaveAs(pathToPblAsset)
	
#takes a snapshot from the active viewer	
def viewerSnapshot(pblPath):
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

	