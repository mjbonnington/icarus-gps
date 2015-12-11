# [GPS] Render View Select AOV
# v0.5
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# This script adds a combo box to the Render View toolbar which enables you to view render passes / AOVs directly in the Render View.
# To initialise, run the script with 'import gpsRenderViewSelectAOV; gpsRenderViewSelectAOV.selectAOV()'
# The Render View must be set to 32-bit mode.
# Currently supports the following renderers: Arnold, Redshift, MentalRay.
# Removed VRay support as this functionality already exists in the VRay Framebuffer.
# Multi-channel EXRs are not supported.

import maya.cmds as mc
import maya.mel as mel


class selectAOV():

	def __init__(self):
		# Initialise some global variables
		self.renderer = mc.getAttr( "defaultRenderGlobals.currentRenderer" )
		self.default_beauty_aov_name = "beauty"
		self.frame = mc.currentTime( query=True )

		# Load OpenEXR plugin
		mc.loadPlugin( "OpenEXRLoader" )

		# Set up common render settings
		pass

		# Set up renderer-specific render settings
		# Arnold...
		if self.renderer == "arnold":
			# Set output file type to exr (can't figure out how to do this)
			pass

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
			mc.setAttr( "defaultRenderGlobals.imageFilePrefix", imageFilePrefix, type="string" )

			# Set correct output gamma
			mc.setAttr( "defaultArnoldRenderOptions.display_gamma", 1 )

			# Add pre- and post-render commands
			mc.setAttr( "defaultRenderGlobals.preMel", 'python("gpsRenderViewSelectAOV.selectAOV().pre_render()")', type="string" )
			mc.setAttr( "defaultRenderGlobals.postMel", 'python("gpsRenderViewSelectAOV.selectAOV().post_render()")', type="string" )

		# Redshift...
		elif self.renderer == "redshift":
			# Set output file type to exr
			mc.setAttr( "redshiftOptions.imageFormat", 1 )

			# Set file name prefix options
			imageFilePrefix = mc.getAttr( "defaultRenderGlobals.imageFilePrefix" )
			if not imageFilePrefix:
				imageFilePrefix = "<Scene>"

			# Append RenderPass token
			if "<RenderPass>" not in imageFilePrefix:
				imageFilePrefix += "_<RenderPass>"

			# Store the updated prefix string
			mc.setAttr( "defaultRenderGlobals.imageFilePrefix", imageFilePrefix, type="string" )

			# Set correct output gamma
			mc.setAttr( "redshiftOptions.displayGammaValue", 2.2 )

			# Add pre- and post-render commands
			mc.setAttr( "redshiftOptions.preRenderMel", 'python("gpsRenderViewSelectAOV.selectAOV().pre_render()")', type="string" )
			mc.setAttr( "redshiftOptions.postRenderMel", 'python("gpsRenderViewSelectAOV.selectAOV().post_render()")', type="string" )

		# MentalRay...
		elif self.renderer == "mentalRay":

			# Set output file type to exr (can't figure out how to do this)
			pass

			# Set file name prefix options
			imageFilePrefix = mc.getAttr( "defaultRenderGlobals.imageFilePrefix" )
			if not imageFilePrefix:
				imageFilePrefix = "<Scene>"

			# Append RenderPass token
			if "<RenderPass>" not in imageFilePrefix:
				imageFilePrefix += "_<RenderPass>"

			# Store the updated prefix string
			mc.setAttr( "defaultRenderGlobals.imageFilePrefix", imageFilePrefix, type="string" )

			# Set correct output gamma
			pass

			# Add pre- and post-render commands
			mc.setAttr( "defaultRenderGlobals.preMel", 'python("gpsRenderViewSelectAOV.selectAOV().pre_render()")', type="string" )
			mc.setAttr( "defaultRenderGlobals.postMel", 'python("gpsRenderViewSelectAOV.selectAOV().post_render()")', type="string" )

		# No supported renderer...
		else:
			mc.error( "The renderer %s is not supported" %self.renderer )

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
		""" Find all the active AOVs in the scene and return their names in a list.
		"""
		# Default beauty pass will always be added to the start of the list
		aov_name_ls = [self.default_beauty_aov_name]

		if self.renderer == "arnold":
			# List all Arnold AOV nodes
			aov_node_ls = mc.ls( type="aiAOV" )

			for aov_node in aov_node_ls:
				# Only add to list if AOV is enabled
				if mc.getAttr( "%s.enabled" %aov_node ):
					aov_name_ls.append( mc.getAttr( "%s.name" %aov_node ) )

		elif self.renderer == "redshift":
			# List all Redshift AOV nodes
			aov_node_ls = mc.ls( type="RedshiftAOV" )

			for aov_node in aov_node_ls:
				# Only add to list if AOV is enabled
				if mc.getAttr( "%s.enabled" %aov_node ):
					aov_name_ls.append( mc.getAttr( "%s.name" %aov_node ) )

		elif self.renderer == "mentalRay":
			# Get the current render layer
			current_layer = mc.editRenderLayerGlobals( query=True, currentRenderLayer=True )

			# List all MentalRay render pass nodes
			aov_node_ls = mc.ls( type="renderPass" )

			for aov_node in aov_node_ls:
				# Only add to list if render pass is connected to current render layer and is renderable
				associated_layers = mc.listConnections( "%s.owner" %aov_node )
				if associated_layers is not None:
					if current_layer in associated_layers:
						if mc.getAttr( "%s.renderable" %aov_node ):
							aov_name_ls.append( aov_node )

		# Return list
		return aov_name_ls


	def loadAOV(self):
		""" Load the selected AOV into the Render View framebuffer.
		"""
		# Get the name of the selected AOV by querying the combo box
		aov = mc.optionMenu( "aov_comboBox", query=True, value=True )

		frame_str = str( int( self.frame ) ).zfill( mc.getAttr("defaultRenderGlobals.extensionPadding") )
		img_path = mc.renderSettings( fullPathTemp=True, leaveUnmatchedTokens=True, genericFrameImageName=frame_str )

		if self.renderer == "arnold":
			img = img_path[0].replace( "<RenderPass>", aov )

		elif self.renderer == "redshift":
			if aov == self.default_beauty_aov_name:
				img = img_path[0].replace( "<RenderPass>", "Beauty" )
			else:
				img = img_path[0].replace( "<RenderPass>", "Beauty.%s" %aov )

		elif self.renderer == "mentalRay":
			if aov == self.default_beauty_aov_name:
				img = img_path[0].replace( "<RenderPass>", "MasterBeauty" )
			else:
				img = img_path[0].replace( "<RenderPass>", aov )

		#print img

		# Load the image
		rview = mc.getPanel( scriptType="renderWindowPanel" )
		mc.renderWindowEditor( rview, edit=True, loadImage=img )

