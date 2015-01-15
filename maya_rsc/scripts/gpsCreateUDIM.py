# GPS Create UDIM
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios

import re, os
import maya.cmds as mc
#import maya.mel as mel
#from pymel.core import *
#import gpsCommon as gps


class gpsCreateUDIM():

	def __init__(self):
		self.winTitle = "GPS Create UDIM Texture"
		self.winName = "gpsCreateUDIM"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		#self.txTypeItemList = ["+/- Average", "Layered Texture"]
		self.txTypeItemList = ['plusMinusAverage', 'layeredTexture']

		self.imageFileTypes = "*.exr *.tif *.tiff *.tga *.jpg *.jpeg *.png *.gif *.iff *.sgi *.rla *.bmp"
		self.txDir = ""
		self.lsUDIM = []


	def UI(self):
		"""Create UI"""

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.fileUI("fileOpt", "windowRoot")
		self.procUI("fileOpt", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnCreate", width=198, height=28, label="Create", command=lambda *args: self.createUDIM(), enable=False)
		mc.button("btnClose", width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def fileUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Texture Files")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Texture File: (UDIM tiles will be detected automatically)", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("txPath", text="", width=360, height=24, changeCommand=lambda *args: self.detectUDIM())
		mc.symbolButton(image="fileOpen.png", width=26, height=26, command=lambda *args: self.fileBrowse("txPath", "Image files (%s)" %self.imageFileTypes))
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text("labelUDIM", label="UDIM Tiles:", wordWrap=True, align="left", width=392, enable=False)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.iconTextScrollList("txList", width=360, height=108, allowMultiSelection=True, append=self.lsUDIM, enable=False)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def procUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Processing")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.optionMenuGrp("txType", label="Texture Type: ")
		for item in self.txTypeItemList:
			mc.menuItem(label=item)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def fileBrowse(self, value, format):
		"""Browse for a data file."""

		# If no file is specified, start in the project's sourceimages directory
		currentDir = os.path.dirname(mc.textField(value, query=True, text=True))
		if currentDir:
			startingDir = currentDir
		else:
			startingDir = mc.workspace(expandName=mc.workspace(fileRuleEntry="sourceImages"))

		filePath = mc.fileDialog2(dialogStyle=2, fileMode=1, dir=startingDir, fileFilter=format)
		if filePath:
			mc.textField(value, edit=True, text=filePath[0])
			self.detectUDIM()


	def detectUDIM(self):
		self.lsUDIM = [] # Clear UDIM file list
		filePath = mc.textField("txPath", query=True, text=True)

		fileCheckPass = self.checkFilename(filePath)

		if fileCheckPass:
			self.txDir = os.path.dirname(filePath)

			#prefix = os.path.basename(filePath).rsplit(".")[0]
			prefix = self.splitFilename(os.path.basename(filePath))[0]

			for item in os.listdir(self.txDir):
				if item.startswith(prefix):
					self.lsUDIM.append(item)

		msg = "Found %d UDIM tiles:" %len(self.lsUDIM)

		self.lsUDIM.sort()
		mc.text("labelUDIM", edit=True, label=msg, enable=fileCheckPass)
		mc.iconTextScrollList("txList", edit=True, removeAll=True, deselectAll=True, enable=fileCheckPass)
		mc.iconTextScrollList("txList", edit=True, append=self.lsUDIM)
		mc.button("btnCreate", edit=True, enable=fileCheckPass)


	def checkFilename(self, pathname):
		"""Check specified file a) exists and b) is correctly formatted."""

		if os.path.isfile(pathname):
			filename = os.path.basename(pathname)
			root, ext = os.path.splitext(filename)
			matcher = re.compile(r"^[\w-]+\.\d{4}$")
			return matcher.match(root) is not None
			#if matcher.match(root):
			#	return True
			#else:
			#	mc.error("Bad filename: %s. Filenames must conform to the following format: alphanumeric_name.####.ext" %filename)
			#	return False
		else:
			#mc.error("File doesn't exist: %s" %pathname)
			return False


	def splitFilename(self, filename):
		"""Split filename into elements."""

		#try:
		#	root, ext = os.path.splitext(filename)
		#	ext = ext.rsplit(".")[1]

		#	match = re.search(r"\.\d{4}$", root)
		#	udim = match.group().rsplit(".")[1]

		#	prefix = root.rsplit(".")[0]

		#	return prefix, udim, ext

		#except AttributeError:
		#	mc.error("Bad filename. Filenames must conform to the following format: name.####.ext")
		#	return False

		return filename.split(".")


	def getUVOffset(self, udim):
		"""Convert UDIM to UV offset."""

		u = (udim-1001)%10
		v = (udim-1001)/10
		return u, v


	def createUDIM(self):
		prefix, udim, ext = self.splitFilename(self.lsUDIM[0])

		#txOpt = mc.optionMenuGrp("txType", query=True, value=True)
		#if txOpt == self.txTypeItemList[0]: # "+/- Average"
		#	txCombinedNodeType = 'plusMinusAverage'
		#elif txOpt == self.txTypeItemList[0]: # "Layered Texture"
		#	txCombinedNodeType = 'layeredTexture'
		txCombinedNodeType = mc.optionMenuGrp("txType", query=True, value=True)
		if txCombinedNodeType == 'plusMinusAverage':
			txCombinedNode = mc.shadingNode(txCombinedNodeType, name=prefix+'_UDIM_'+ext, asUtility=True)
		elif txCombinedNodeType == 'layeredTexture':
			txCombinedNode = mc.shadingNode(txCombinedNodeType, name=prefix+'_UDIM_'+ext, asTexture=True)


		for i, item in enumerate(self.lsUDIM):
			prefix, udim, ext = self.splitFilename(item)

			# Create place2dTexture nodes
			nodeType = 'place2dTexture'
			place2dTextureNode = mc.shadingNode(nodeType, name=nodeType+'_'+prefix+'_'+udim+'_'+ext, asUtility=True)
			mc.setAttr(place2dTextureNode+'.translateFrameU', self.getUVOffset(int(udim))[0])
			mc.setAttr(place2dTextureNode+'.translateFrameV', self.getUVOffset(int(udim))[1])
			mc.setAttr(place2dTextureNode+'.wrapU', 0)
			mc.setAttr(place2dTextureNode+'.wrapV', 0)

			# Create file nodes
			nodeType = 'file'
			fileNode = mc.shadingNode(nodeType, name=nodeType+'_'+prefix+'_'+udim+'_'+ext, asTexture=True)
			mc.setAttr(fileNode+'.filterType', 0)
			mc.setAttr(fileNode+'.fileTextureName', os.path.join(self.txDir, item), type="string")
			mc.setAttr(fileNode+'.defaultColor', 0, 0, 0, type="double3")

			# Connect up attributes
			mc.defaultNavigation(connectToExisting=True, source=place2dTextureNode, destination=fileNode)
			if txCombinedNodeType == 'plusMinusAverage':
				mc.connectAttr(fileNode+'.outColor', txCombinedNode+'.input3D[%d]' %i, force=True)
			elif txCombinedNodeType == 'layeredTexture':
				mc.connectAttr(fileNode+'.outColor', txCombinedNode+'.inputs[%d].color' %i, force=True)
				mc.setAttr(txCombinedNode+'.inputs[%d].blendMode' %i, 4)

		return
