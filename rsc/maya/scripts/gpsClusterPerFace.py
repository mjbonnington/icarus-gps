#!/usr/bin/python

# [Icarus] gpsClusterperFace.py
#
# Peter Bartfay <peter.bartfay@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Maya Tool

import maya.cmds as cmds

def gpsClusterPerFace():

	selectionList = cmds.ls (selection = True)
	n = 0

	if selectionList:
		
		while len(selectionList) > n:
		
			cmds.cluster(selectionList[n])
			n+=1
	else:
		cmds.warning ("Please select objects or components!")