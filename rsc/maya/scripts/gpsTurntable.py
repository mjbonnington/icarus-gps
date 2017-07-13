#!/usr/bin/python

# [Icarus] gpsTurntable.py
#
# Peter Bartfay <peter.bartfay@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Maya Tool

import maya.cmds as cmds

def gpsTurntable():
    # Set up framerange
    startTime = cmds.playbackOptions ( query = True, minTime = True )
    endTime = cmds.playbackOptions ( query = True, maxTime = True )

    # Get current selection
    selectionList = cmds.ls (selection = True)

    if selectionList:

        # Get centre of selection
        bbox = cmds.exactWorldBoundingBox()

        centre_x = (bbox[0] + bbox[3]) / 2.0
        centre_y = (bbox[1] + bbox[4]) / 2.0
        centre_z = (bbox[2] + bbox[5]) / 2.0
        
        # Create new group
        new_grp = cmds.group(empty=True, name="Turntable_%s_grp#" %selectionList[0])
        cmds.move(centre_x, centre_y, centre_z, new_grp)

         # Create Turntable camera
        new_cam = cmds.camera()
        cmds.select (selectionList, r = True)
        cmds.viewFit (new_cam[0], allObjects = False)
        cmds.parent (new_cam[0], new_grp)
        cmds.setKeyframe (new_grp, time = startTime-1, attribute = "rotateY", value=0)
        cmds.setKeyframe (new_grp, time = endTime, attribute = "rotateY", value=360)
        cmds.selectKey (new_grp, time = (startTime-1, endTime), attribute = "rotateY", keyframe = True)
        cmds.keyTangent (inTangentType = "linear", outTangentType = "linear")
        cmds.rename ("Turntable_%s_cam#" %selectionList[0])
        
    else:
        cmds.warning("Please select an object!")
