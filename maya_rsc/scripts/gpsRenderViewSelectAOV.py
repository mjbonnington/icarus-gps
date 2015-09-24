# [GPS] Render View Select AOV
# v0.3
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# This script adds a combo box to the Render View toolbar which enables you to view render passes / AOVs directly in the Render View.
# To initialise, run the script with 'import gpsRenderViewSelectAOV; gpsRenderViewSelectAOV.selectAOV()'
# Currently only works with Arnold Renderer.

import maya.cmds as mc
import maya.mel as mel


class selectAOV():

	def __init__(self):
		# Initialise some global variables
		self.renderer = "arnold"
		self.default_beauty_aov_name = "beauty"
		self.frame = mc.currentTime(query=True)

		# Load OpenEXR plugin
		mc.loadPlugin( "OpenEXRLoader" )

		# Set up common render settings
		pass

		# Add pre- and post-render commands
		mc.setAttr( "defaultRenderGlobals.preMel", 'python("gpsRenderViewSelectAOV.selectAOV().pre_render()")', type="string" )
		mc.setAttr( "defaultRenderGlobals.postMel", 'python("gpsRenderViewSelectAOV.selectAOV().post_render()")', type="string" )

		# Set up renderer-specific render settings
		if self.renderer == "arnold":
			# TODO - Check whether Arnold is set as the current renderer

			# Set output file type to exr (can't figure out how to do this)

			# Set file name prefix options
			imageFilePrefix = mc.getAttr( "defaultRenderGlobals.imageFilePrefix" )
			# Arnold doesn't like the '%x' style of tokens, so replace them
			if imageFilePrefix:
				imageFilePrefix = imageFilePrefix.replace("%s", "<Scene>" )
				imageFilePrefix = imageFilePrefix.replace("%l", "<RenderLayer>" )
			else:
				imageFilePrefix = "<Scene>"

			# Append RenderPass token, but only if Merge AOVs option is turned off
			if not mc.getAttr( "defaultArnoldDriver.mergeAOVs" ):
				if "<RenderPass>" not in imageFilePrefix:
					imageFilePrefix += "_<RenderPass>"

			# Store the updated prefix string
			mc.setAttr( "defaultRenderGlobals.imageFilePrefix", imageFilePrefix, type="string" ) # Store in render globals
			#mc.setAttr( "defaultArnoldDriver.prefix", imageFilePrefix, type="string" ) # Store as override in Arnold driver

			# Set correct output gamma
			mc.setAttr( "defaultArnoldRenderOptions.display_gamma", 1 )

		#elif self.renderer == "vray":
		#	pass

		# Set up Maya Render View for 32-bit float / linear
		mc.setAttr( "defaultViewColorManager.imageColorProfile", 2 )
		mc.setAttr( "defaultViewColorManager.displayColorProfile", 3 )
		# TODO - Check whether 32-bit mode is enabled

		self.create_ui()


	def create_ui(self):
		""" Add the AOV selector combo box to the Render View toolbar.
		"""
		iconSize = 26

		# Open the Render View window
		mel.eval( "RenderViewWindow;" )
		mc.setParent( "renderViewToolbar" )

		# Delete UI elements if they already exist
		if mc.separator( "aov_separator", exists=True ):
			mc.deleteUI( "aov_separator" )
		if mc.optionMenu( "aov_comboBox", exists=True ):
			mc.deleteUI( "aov_comboBox" )

		# Add the AOV / render pass selector
		mc.separator( "aov_separator", height=iconSize, horizontal=False, style="single" )
		mc.optionMenu( "aov_comboBox", height=iconSize, changeCommand=lambda *args: self.loadAOV(), annotation="Select AOV / render pass to display" )
		for aov in self.getAOVNames():
			mc.menuItem( label=aov )


	def pre_render(self):
		""" Function to execute when a render is started.
		"""
		# Disable the UI whilst a render is in progress
		mc.optionMenu( "aov_comboBox", edit=True, enable=False )

		# Store the current frame number
		self.frame = mc.currentTime( query=True )
	 

	def post_render(self):
		""" Function to execute when a render finishes.
		"""
		# Enable the UI when render completes
		mc.optionMenu( "aov_comboBox", edit=True, enable=True )

		# Rebuild the UI
		self.create_ui()


	def getAOVNames(self):
		"""Find all the active AOVs in the scene and return their names in a list.
		"""
		# Default beauty pass will always be added to the start of the list
		aov_name_ls = [self.default_beauty_aov_name]

		if self.renderer == "arnold":
			# List all Arnold AOV nodes
			aov_node_ls = mc.ls(type="aiAOV")

			for aov_node in aov_node_ls:
				# Only add to list if AOV is enabled
				if mc.getAttr("%s.enabled" %aov_node):
					aov_name_ls.append( mc.getAttr("%s.name" %aov_node) )

		#elif self.renderer == "vray":
		#	# List all Vray Render Element nodes
		#	aov_node_ls = mc.ls(type="VRayRenderElement")

		#	for aov_node in aov_node_ls:
		#		# We need to find the element's name, but as Vray isn't consistent we first need to find the attribute name to query.
		#		attr_ls = mc.listAttr(aov_node)
		#		for attr in attr_ls:
		#			if "vray_name_" in attr:
		#				aov_name_attr = attr
		#		aov_name_ls.append( mc.getAttr("%s.%s" %(aov_node, aov_name_attr)) )

		# Return list with duplicates removed
		return aov_name_ls


	def loadAOV(self):
		aov = mc.optionMenu( "aov_comboBox", query=True, value=True )
		#print aov

		padding = mc.getAttr("defaultRenderGlobals.extensionPadding")

		if self.renderer == "arnold":
			img_path = mc.renderSettings( fullPathTemp=True, leaveUnmatchedTokens=True, genericFrameImageName=str(int(self.frame)).zfill(padding) )
			img = img_path[0].replace( "<RenderPass>", aov )

		#elif self.renderer == "vray":
		#	img_path = mc.renderSettings( fullPathTemp=True, leaveUnmatchedTokens=True, genericFrameImageName=str(int(self.frame)).zfill(padding) )
		#	img = img_path[0].replace( "[CurrentFrame]", "%4d" %frame ) # <- FIX PADDING
		#	if aov == default_beauty_aov_name:
		#		img = img.replace( "_<RenderPass>", "" )
		#	else:
		#		img = img.replace( "_<RenderPass>", "_%s" %aov )

		#print img
		rview = mc.getPanel( scriptType="renderWindowPanel" )
		mc.renderWindowEditor( rview, edit=True, loadImage=img )

