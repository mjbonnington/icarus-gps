#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:confDlg


#confirmation dialog module
import maya.cmds as cmds

def dialog(asset, version, episode, sequence, shot_, category):
	confirm = cmds.confirmDialog(title="RELEASE CONFIRMATION", 
	message= " \n\n%s\n\nversion: %s\n\nepisode: %s\n\nsequence: %s\n\nshot: %s\n\ncategory: %s\n\n" % (asset, version, episode, sequence, shot_, category),
	button=["Confirm","Cancel"], 
	defaultButton="Confirm", 
	cancelButton="Cancel", 
	dismissString="Cancel" )
	
	return confirm
