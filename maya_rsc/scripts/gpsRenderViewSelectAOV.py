# GPS Render View Select AOV
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# This script adds a combo box to the Render View toolbar which enables you to view render passes / AOVs directly in the Render View.

import os
import maya.cmds as mc
import maya.mel as mel


renderer="arnold"

def getAOVNames():
	# Default pass will anways be named 'beauty'
	aov_name_ls = ["beauty"]

	if renderer == "vray":
		aov_node_ls = mc.ls(type="VRayRenderElement")

		for aov_node in aov_node_ls:
			attr_ls = mc.listAttr(aov_node)
			for attr in attr_ls:
				if "vray_name_" in attr:
					aov_name_attr = attr
			aov_name_ls.append( mc.getAttr("%s.%s" %(aov_node, aov_name_attr) ) )

	elif renderer == "arnold":
		aov_node_ls = mc.ls(type="aiAOV")

		for aov_node in aov_node_ls:
			aov_name_ls.append( mc.getAttr("%s.name" %aov_node ) )

	return aov_name_ls


def loadAOV():
	aov = mc.optionMenu( "aov_comboBox", query=True, value=True )
	#print aov

	#img_folder = "%s/tmp" %( mc.workspace( expandName=mc.workspace(fileRuleEntry="images") ) )
	#filename_prefix = 
	#img_path = "%s/tmp/%s%s%s.exr" %(img_folder, file_output, separator, aov)
	if renderer == "vray":
		pass
	elif renderer == "arnold":

		img_path = mc.renderSettings( fullPathTemp=True, leaveUnmatchedTokens=True, genericFrameImageName="[CurrentFrame]" )
		img = img_path[0].replace( "[CurrentFrame]", "0001" )
		if aov == "beauty":
			img = img.replace( "_<RenderPass>", "" )
		else:
			img = img.replace( "_<RenderPass>", "_%s" %aov )

	rview = mc.getPanel( scriptType="renderWindowPanel" )
	print img
	mc.renderWindowEditor( rview, edit=True, loadImage=img )


mel.eval('RenderViewWindow;')
iconSize = 26
mc.setParent( "renderViewToolbar" )

mc.separator( "aov_separator", height=iconSize, horizontal=False, style="single" )

# GPS - AOV / render pass selector
mc.optionMenu( "aov_comboBox", height=iconSize, changeCommand=lambda *args: loadAOV(), annotation="Select AOV / render pass to display" )

for aov in getAOVNames():
	mc.menuItem( label=aov, enableCommandRepeat=True )
