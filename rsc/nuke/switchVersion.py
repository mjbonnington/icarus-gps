#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:switchVersion
#copyright	:Gramercy Park Studios


import nuke, nukescripts

def versionUp():
	getSelectedNodes()
	nukescripts.version_up()
	
def versionDown():
	getSelectedNodes()
	nukescripts.version_down()

def versionLatest():
	getSelectedNodes()
	nukescripts.version_latest()
	
def getSelectedNodes():
	selNodes = nuke.selectedNodes()
	if not selNodes:
	    selNodes = nuke.allNodes()
	for node_ in selNodes:
	    if node_.Class() == 'Read':
		   node_['selected'].setValue(True)