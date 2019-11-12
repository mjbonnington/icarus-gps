# GPS Create Tiled Texture
# v0.3.6
#
# Michael Bonnington 2015
# Gramercy Park Studios

import re, os
import maya.cmds as mc
import maya.mel as mel
#from pymel.core import *
#from . import gpsCommon as gps


class gpsCreateTiledTx():

	def __init__(self):
		self.winTitle = "GPS Create Tiled Texture"
		self.winName = "gpsCreateTiledTx"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		self.txTypeItemList = ['layeredTexture', 'plusMinusAverage']

		self.imageFileTypes = "*.exr *.tif *.tiff *.tga *.jpg *.jpeg *.png *.gif *.iff *.sgi *.rla *.bmp"
		self.lsTiles = []
		self.txDir = ""
		self.prefix = ""
		self.ext = ""
		self.tileRegex = ""
		self.method = "Not detected"


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
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Texture File: (tiles will be detected automatically)", wordWrap=True, align="left", width=392)
		mc.setParent(name)

		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("txPath", text="", width=360, height=24, changeCommand=lambda *args: self.detectTileMethod())
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

		mc.separator(width=396, height=12, style="in")
		mc.textFieldGrp("tileMethod", label="Tiling Method: ", text=self.method, editable=False)
		mc.radioButtonGrp("uvOffset", label="UV Tile Coordinates: ", labelArray2=['0-based', '1-based'], numberOfRadioButtons=2, columnWidth3=[140, 78, 156], select=2, 
		                  annotation="Select 0-based if the UV tile numbering starts from zero, or 1-based if is starts from one", enable=False, 
		                  changeCommand=lambda *args: self.detectTiles())
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
		mc.checkBoxGrp("vrayAttr", label="Add Vray Attributes: ", labelArray2=['Gamma', 'Negative Colours'], valueArray2=[False, False], 
		               numberOfCheckBoxes=2, columnWidth3=[140, 78, 156])

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
			self.detectTileMethod()


	def detectTileMethod(self):
		"""Attempt to auto-detect texture tiling method.
		"""
		filepath = mc.textField("txPath", query=True, text=True)
		filename = os.path.basename(filepath)
		self.txDir = os.path.dirname(filepath)

		# Compile Regular Expressions to match each texture tiling method
		reUDIM = re.compile(r"^[\.\w-]+\.\d{4}$")
		reUV = re.compile(r"^[\.\w-]+_[uU]\d+_[vV]\d+$")

		# Store filename root and extension
		root, self.ext = os.path.splitext(filename)
		self.prefix = root

		# Check file exists
		fileExists = os.path.isfile(filepath)
		if fileExists:

			# UDIM method:
			if reUDIM.match(root) is not None:
				self.tileRegex = r'\.\d{4}$'
				tileRE = re.compile(self.tileRegex)
				match = tileRE.search(root)

				# Store filename prefix
				if match is not None:
					self.prefix = root[:root.rfind(match.group())]

				# Set tiling method to UDIM
				self.method = "UDIM"

				mc.radioButtonGrp("uvOffset", edit=True, enable=False)
				print "Auto-detected UDIM texture tiling method."

	 		# UV offset method:
			elif reUV.match(root) is not None:
				self.tileRegex = r'_[uU]\d+_[vV]\d+$'
				tileRE = re.compile(self.tileRegex)
				match = tileRE.search(root)

				# Store filename prefix
				if match is not None:
					self.prefix = root[:root.rfind(match.group())]

				# Set tiling method to UV
				self.method = "UV"

				# Detect numbering start based on selected file
				temp = match.group().split('_')
				u = int(temp[1][1:])
				v = int(temp[2][1:])

				# Base 1:
				if u or v:
					mc.radioButtonGrp("uvOffset", edit=True, select=2, enable=True)
					print "Auto-detected UV (1-based) texture tiling method."

				# Base 0:
				else:
					mc.radioButtonGrp("uvOffset", edit=True, select=1, enable=True)
					print "Auto-detected UV (0-based) texture tiling method."

			# Method could not be determined:
			else:
				self.tileRegex = ""
				mc.radioButtonGrp("uvOffset", edit=True, enable=False)
				self.method = "Not detected"
				mc.warning("Unable to auto-detect texture tiling method.")

		# File doesn't exist:
		else:
			self.tileRegex = ""
			mc.radioButtonGrp("uvOffset", edit=True, enable=False)
			self.method = "Not detected"
			mc.warning("File doesn't exist: %s" %filepath)

		# Find other texture tiles
		fileCheckPass = self.detectTiles()

		# Update UI elements
		mc.text("labelTiles", edit=True, enable=fileCheckPass)
		mc.iconTextScrollList("txList", edit=True, enable=fileCheckPass)
		mc.textFieldGrp("tileMethod", edit=True, text=self.method)
		mc.button("btnCreate", edit=True, enable=fileCheckPass)

		# Select Vray Gamma checkbox if filetype is not OpenEXR
		if(self.ext == '.exr'):
			mc.checkBoxGrp("vrayAttr", edit=True, value1=False)
		else:
			mc.checkBoxGrp("vrayAttr", edit=True, value1=True)

		#print "[Exists: %s] %s/ %s <%s> %s [%d]" %(fileExists, self.txDir, self.prefix, self.method, self.ext, fileCheckPass)


	def detectTiles(self):
		"""Detect all other texture tiles from the selected filename.
		"""
		self.lsTiles = []   # Clear list of texture tiles
		lsTilesDisplay = [] # Create a new list purely to display the UV offset coords

		# List directory contents and find tiles relating to current file
		if self.method != "Not detected":
			for item in os.listdir(self.txDir):
				if self.checkTile(item):
					self.lsTiles.append(item)
					lsTilesDisplay.append(item + ' [%d, %d]' %self.getUVOffset(item))

		msg = "Found %d tiles:" %len(self.lsTiles)

		self.lsTiles.sort()
		lsTilesDisplay.sort()

		# Update UI elements
		mc.text("labelTiles", edit=True, label=msg)
		mc.iconTextScrollList("txList", edit=True, removeAll=True, deselectAll=True)
		mc.iconTextScrollList("txList", edit=True, append=lsTilesDisplay)

		return len(self.lsTiles)


	def checkTile(self, filename):
		"""Check specified file is a tile related to the user selected file.
		"""
		if filename.endswith(self.ext): # Make sure only files with the same extension are included
			root = os.path.splitext(filename)[0]
			rootRE = re.compile(r"^" + self.prefix + self.tileRegex)
			return rootRE.match(root) is not None
		else:
			return False


	def getUVOffset(self, filename):
		"""Get UV offset from tile filename. Presumes filenames conform to naming convention.
		"""
		tileRE = re.compile(self.tileRegex)
		root = os.path.splitext(filename)[0]
		match = tileRE.search(root)

		if self.method == "UDIM":
			temp = match.group().split('.')
			u, v = self.UDIMtoUV(int(temp[1]))
		elif self.method == "UV":
			temp = match.group().split('_')
			offset = mc.radioButtonGrp("uvOffset", query=True, select=True) - 1
			u = int(temp[1][1:]) - offset
			v = int(temp[2][1:]) - offset
		elif self.method == "Not detected":
			return False

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
		commonName = self.sanitise(self.prefix+self.ext)

		# Create combined texture node
		txCombinedNodeType = mc.optionMenuGrp("txType", query=True, value=True)
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
			containerNode = mc.container(name='tiles_'+commonName, 
			                             addNode=txCombinedNode, 
			                             includeNetwork=True, 
			                             includeShaders=True, 
			                             includeHierarchyAbove=True, 
			                             includeHierarchyBelow=True)
			mc.container(containerNode, edit=True, removeNode=txCombinedNode)

		mc.select(txCombinedNode)

		return
