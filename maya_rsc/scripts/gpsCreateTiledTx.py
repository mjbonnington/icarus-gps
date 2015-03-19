# GPS Create Tiled Texture
# v0.3
#
# Michael Bonnington 2015
# Gramercy Park Studios

import re, os
import operator
import maya.cmds as mc
import maya.mel as mel
#from pymel.core import *
#import gpsCommon as gps


class gpsCreateTiledTx():

	def __init__(self):
		self.winTitle = "GPS Create Tiled Texture"
		self.winName = "gpsCreateTiledTx"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		self.txTypeItemList = ['layeredTexture', 'plusMinusAverage']
		self.tileMethodItemList = ['UDIM (Mari)', 'UV offset base 1 (Mudbox)', 'UV offset base 0']

		self.imageFileTypes = "*.exr *.tif *.tiff *.tga *.jpg *.jpeg *.png *.gif *.iff *.sgi *.rla *.bmp"
		self.txDir = ""
		self.lsTiles = []
		self.prefix = ""
		#self.tileRE = ""
		self.ext = ""


	def UI(self):
		"""Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.fileUI("fileOpt", "windowRoot")
		self.procUI("procOpt", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnCreate", width=198, height=28, label="Create", command=lambda *args: self.genTiledTx(), enable=False)
		mc.button("btnClose", width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def fileUI(self, name, parent, collapse=False):
		"""Create panel UI controls - texture files.
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Texture Files")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.optionMenuGrp("tileMethod", label="Tiling Method: ", changeCommand=lambda *args: self.detectTiles())
		for item in self.tileMethodItemList:
			mc.menuItem(label=item)

		mc.separator(width=396, height=12, style="in")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Texture File: (tiles will be detected automatically)", wordWrap=True, align="left", width=392)
		mc.setParent(name)

		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("txPath", text="", width=360, height=24, changeCommand=lambda *args: self.detectTiles())
		mc.symbolButton(image="navButtonBrowse.png", width=26, height=26, command=lambda *args: self.fileBrowse("txPath", "Image files (%s)" %self.imageFileTypes))
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text("labelTiles", label="Tiles:", wordWrap=True, align="left", width=392, enable=False)
		mc.setParent(name)

		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.iconTextScrollList("txList", width=360, height=108, allowMultiSelection=True, enable=False)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def procUI(self, name, parent, collapse=False):
		"""Create panel UI controls - processing.
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Processing")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("asset", label="Group into Asset Container", value=True)
		mc.setParent(name)

		mc.separator(width=396, height=12, style="in")
		mc.checkBoxGrp("vrayAttr", label="Add Vray Attributes: ", labelArray2=['Gamma', 'Negative Colours'], valueArray2=[False, False], numberOfCheckBoxes=2, columnWidth3=[140, 78, 156])

		mc.separator(height=4, style="none")
		mc.optionMenuGrp("txType", label="Combined Texture: ")
		for item in self.txTypeItemList:
			mc.menuItem(label=item)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def fileBrowse(self, value, format):
		"""Browse for an image file.
		"""
		# If no file is specified, start in the project's sourceimages directory
		currentDir = os.path.dirname(mc.textField(value, query=True, text=True))
		if currentDir:
			startingDir = currentDir
		else:
			startingDir = mc.workspace(expandName=mc.workspace(fileRuleEntry="sourceImages"))

		filePath = mc.fileDialog2(dialogStyle=2, fileMode=1, dir=startingDir, fileFilter=format)
		if filePath:
			mc.textField(value, edit=True, text=filePath[0])
			self.detectTiles()


	def detectTiles(self):
		"""Detect all other texture tiles from the selected filename.
		"""
		self.lsTiles = [] # Clear list of tiles
		lsTilesDisplay = [] # Create a new list purely for viewing to display the UV offset coords
		filePath = mc.textField("txPath", query=True, text=True)
		method = mc.optionMenuGrp("tileMethod", query=True, value=True)
		if method.startswith('UDIM'): # UDIM method
			tileRegex = r'\.\d{4}$'
		elif method.startswith('UV'): # UV offset method
			tileRegex = r'_[uU]\d+_[vV]\d+$'
		self.tileRE = re.compile(tileRegex)

		fileCheckPass = self.checkFilename(filePath, tileRegex) # Check filename conforms

		if fileCheckPass:
			self.txDir = os.path.dirname(filePath)

			for item in os.listdir(self.txDir):
				if self.checkTile(item, tileRegex):
					self.lsTiles.append(item)
					lsTilesDisplay.append(item + ' [%d, %d]' %self.getUVOffset(item))

		msg = "Found %d tiles:" %len(self.lsTiles)

		self.lsTiles.sort()
		lsTilesDisplay.sort()

		# Feed back to UI elements
		mc.text("labelTiles", edit=True, label=msg, enable=fileCheckPass)
		mc.iconTextScrollList("txList", edit=True, removeAll=True, deselectAll=True)
		mc.iconTextScrollList("txList", edit=True, append=lsTilesDisplay, enable=fileCheckPass)
		mc.button("btnCreate", edit=True, enable=fileCheckPass)
		if(self.ext == '.exr'):
			mc.checkBoxGrp("vrayAttr", edit=True, value1=False)
		else:
			mc.checkBoxGrp("vrayAttr", edit=True, value1=True)


	def checkFilename(self, pathname, regex):
		"""Check specified file a) exists and b) is correctly formatted for the specified tiling method.
		"""
		if os.path.isfile(pathname): # Make sure file exists
			filename = os.path.basename(pathname)
			root, self.ext = os.path.splitext(filename)
			match = self.tileRE.search(root)
			if match is not None:
				self.prefix = root[:root.rfind(match.group())]
			rootRE = re.compile(r"^[\w-]+" + regex)
			return rootRE.match(root) is not None # Return True if the filename matches the criteria
		else:
			return False # Always return False if the file does not exist


	def checkTile(self, filename, regex):
		"""Check specified file is a tile connected to the user selected file.
		"""
		if filename.endswith(self.ext): # Make sure only files with the same extension are included
			root = os.path.splitext(filename)[0]
			rootRE = re.compile(r"^" + self.prefix + regex)
			return rootRE.match(root) is not None # Return True if the filename matches the criteria
		else:
			return False # Always return False if the extension does not match


	def getUVOffset(self, filename):
		"""Get UV offset from tile filename. Presumes filenames conform to naming convention.
		"""
		root = os.path.splitext(filename)[0]
		match = self.tileRE.search(root)

		method = mc.optionMenuGrp("tileMethod", query=True, value=True)
		if method == 'UDIM (Mari)':
			temp = match.group().split('.')
			u, v = self.UDIMtoUV(int(temp[1]))
		elif method == 'UV offset base 1 (Mudbox)':
			temp = match.group().split('_')
			u = int(temp[1][1:]) - 1
			v = int(temp[2][1:]) - 1
		elif method == 'UV offset base 0':
			temp = match.group().split('_')
			u = int(temp[1][1:])
			v = int(temp[2][1:])

		return u, v


	def UDIMtoUV(self, udim):
		"""Convert UDIM to UV offset.
		"""
		u = (udim-1001)%10
		v = (udim-1001)/10
		return u, v


	def sanitise(self, instr):
		"""Remove all non-alphanumeric characters from string.
		"""
		return re.sub('\W', '_', instr)


	def genTiledTx(self):
		"""Generate shading network for tiled texture.
		"""

		# Create combined texture node
		txCombinedNodeType = mc.optionMenuGrp("txType", query=True, value=True)
		commonName = self.sanitise(self.prefix+self.ext)

		if txCombinedNodeType == 'plusMinusAverage':
			txCombinedNode = mc.shadingNode(txCombinedNodeType, name=txCombinedNodeType+'_'+commonName, asUtility=True)
		elif txCombinedNodeType == 'layeredTexture':
			txCombinedNode = mc.shadingNode(txCombinedNodeType, name=txCombinedNodeType+'_'+commonName, asTexture=True)

		for i, item in enumerate(self.lsTiles):
			u, v = self.getUVOffset(item)
			name = self.sanitise(item)

			# Create place2dTexture nodes
			nodeType = 'place2dTexture'
			place2dTextureNode = mc.shadingNode(nodeType, name=nodeType+'_'+name, asUtility=True)
			mc.setAttr(place2dTextureNode+'.translateFrameU', u)
			mc.setAttr(place2dTextureNode+'.translateFrameV', v)
			mc.setAttr(place2dTextureNode+'.wrapU', 0)
			mc.setAttr(place2dTextureNode+'.wrapV', 0)

			# Create file nodes
			nodeType = 'file'
			fileNode = mc.shadingNode(nodeType, name=nodeType+'_'+name, asTexture=True)
			mc.setAttr(fileNode+'.filterType', 0)
			mc.setAttr(fileNode+'.fileTextureName', os.path.join(self.txDir, item), type="string")
			mc.setAttr(fileNode+'.defaultColor', 0, 0, 0, type="double3")

			# Add custom Vray attributes to file nodes
			if mc.checkBoxGrp("vrayAttr", query=True, value1=True):
				mel.eval('vray addAttributesFromGroup %s vray_file_gamma 1;' %fileNode)
			if mc.checkBoxGrp("vrayAttr", query=True, value2=True):
				mel.eval('vray addAttributesFromGroup %s vray_file_allow_neg_colors 1;' %fileNode)

			# Connect up attributes
			mc.defaultNavigation(connectToExisting=True, source=place2dTextureNode, destination=fileNode)
			if txCombinedNodeType == 'plusMinusAverage':
				mc.connectAttr(fileNode+'.outColor', txCombinedNode+'.input3D[%d]' %i, force=True)
			elif txCombinedNodeType == 'layeredTexture':
				mc.connectAttr(fileNode+'.outColor', txCombinedNode+'.inputs[%d].color' %i, force=True)
				mc.setAttr(txCombinedNode+'.inputs[%d].blendMode' %i, 4)

		# Create asset container then remove combined texture node from container for easy connections to shaders
		if mc.checkBox("asset", query=True, value=True):
			containerNode = mc.container(name='tiles_'+commonName, addNode=txCombinedNode, includeNetwork=True, includeShaders=True, includeHierarchyAbove=True, includeHierarchyBelow=True)
			mc.container(containerNode, edit=True, removeNode=txCombinedNode)

		mc.select(txCombinedNode)

		return
