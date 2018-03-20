#!/usr/bin/python

# [GPS] switchVersion.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Version up / down / latest.


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

