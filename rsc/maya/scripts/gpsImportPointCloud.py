#!/usr/bin/python

# [GPS] Import Point Cloud
# v0.3
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# (c) 2014-2015 Gramercy Park Studios
#
# Import point cloud and photogrammetry camera position data into Maya.


import math, time, re, os
import numpy as np
import maya.cmds as mc
import maya.mel as mel
#import gpsCommon as gps


class gpsImportPointCloud():

	def __init__(self):
		self.winTitle = "[GPS] Import Point Cloud"
		self.winName = "gpsImportPointCloud"
		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		#self.dataFormats = "Plain text (*.txt);;ASCII X,Y,Z (*.xyz)"

		self.pcExt = ".txt"
		self.camExt = ".chan"


	def UI(self):
		""" Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.fileOptUI("fileOpt", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnImport", width=198, height=28, label="Import", command=lambda *args: self.importData(), enable=False)
		mc.button("btnClose", width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def fileOptUI(self, name, parent, collapse=False):
		""" Create panel UI controls.
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Read Data")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Point cloud data file:", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("pointCloudPath", text="", width=360, height=24, changeCommand=lambda *args: self.checkFileExists())
		mc.symbolButton(image="fileOpen.png", width=26, height=26, command=lambda *args: self.fileBrowse("pointCloudPath", "Point cloud files (*%s)" %self.pcExt))
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Camera data file: (optional)", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("cameraDataPath", text="", width=360, height=24)
		mc.symbolButton(image="fileOpen.png", width=26, height=26, command=lambda *args: self.fileBrowse("cameraDataPath", "Camera data files (*%s)" %self.camExt))
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def checkFileExists(self):
		""" Check specified point cloud file exists, and attempt to load associated camera data file.
		"""
		filePath = mc.textField("pointCloudPath", query=True, text=True)
		chanPath = filePath.replace(self.pcExt, self.camExt)

		if os.path.isfile(chanPath):
			mc.textField("cameraDataPath", edit=True, text=chanPath)

		mc.button("btnImport", edit=True, enable=os.path.isfile(filePath))


	def fileBrowse(self, value, format):
		""" Browse for a data file.
		"""
		startingDir = mc.workspace(expandName=mc.workspace(fileRuleEntry="translatorData"))
		filePath = mc.fileDialog2(dialogStyle=2, fileMode=1, dir=startingDir, fileFilter=format)
		if filePath:
			mc.textField(value, edit=True, text=filePath[0])
			self.checkFileExists()


	def importData(self):
		""" Import data.
		"""
		pointCloudPath = mc.textField("pointCloudPath", query=True, text=True)
		cameraDataPath = mc.textField("cameraDataPath", query=True, text=True)

		if pointCloudPath:
			pCloudGroup = self.importPointCloud(pointCloudPath)
		if cameraDataPath:
			camGroup = self.importCameraData(cameraDataPath)

		# Parent cameras under point cloud group
		#if pCloudGroup and camGroup:
			#mc.parent(camGroup, pCloudGroup)


	def importPointCloud(self, filePath):
		""" Read data from file and generate point cloud.
		"""
		if os.path.isfile(filePath): # Check file exists

			# Read data into numpy array
			startTime = time.time()
			data = np.genfromtxt(filePath)
			count = data.shape[0]

			# Create group and particles etc.
			fileName = os.path.splitext(os.path.basename(filePath))[0]
			pCloudGroup = mc.group(name="%s_grp" %fileName, empty=True)
			pCloudParticle = mc.particle(name="%s_pCloud" %fileName)

			mc.addAttr(pCloudParticle[1], longName="rgbPP", dataType="vectorArray")
			mc.addAttr(pCloudParticle[1], longName="rgbPP0", dataType="vectorArray")

			pos = data[:,0:3]
			pos1D = pos.reshape(pos.size)
			posStr = "%s" %pos1D.tolist()
			posStr2 = re.sub(r'[\n\[\],]', '', posStr)
			posExec = 'setAttr ".pos0" -type "vectorArray" %s %s ;' %(count, posStr2)
			#print posExec
			mel.eval(posExec)

			rgb = data[:,3:6]/255
			rgb1D = rgb.reshape(rgb.size)
			rgbStr = "%s" %rgb1D.tolist()
			rgbStr2 = re.sub(r'[\n\[\],]', '', rgbStr)
			rgbExec = 'setAttr ".rgbPP0" -type "vectorArray" %s %s ;' %(count, rgbStr2)
			#print rgbExec
			mel.eval(rgbExec)

			#mc.saveInitialState(pCloudParticle[0])
			mc.currentTime(1)
			mc.setAttr("%s.isDynamic" %pCloudParticle[1], 0)
			mc.parent(pCloudParticle[0], pCloudGroup)

			# Complete progress bar and end clock
			totalTime = time.time() - startTime;
			print "Read %d points in %f seconds.\n" %(count, totalTime)

			return pCloudGroup
		else:
			mc.error("File doesn't exist: %s" %filePath)
			return False


	def importCameraData(self, filePath):
		""" Read data from file and generate projection cameras.
		"""
		if os.path.isfile(filePath): # Check file exists

			# Read data into numpy array
			startTime = time.time()
			data = np.genfromtxt(filePath)
			count = data.shape[0]

			# Create cameras
			fileName = os.path.splitext(os.path.basename(filePath))[0]
			camGroup = mc.group(name="%s_cam_grp" %fileName, empty=True)

			for i in range(count):
				#cn = data[i,0]
				#tx = data[i,1]
				#ty = data[i,2]
				#tz = data[i,3]
				t = data[i,1:4].tolist()
				#rx = data[i,4]
				#ry = data[i,5]
				#rz = data[i,6]
				r = data[i,4:7].tolist()
				fl = data[i,7]
				activeCam = mc.camera(name="%s_cam1" %fileName, focalLength=fl, p=t, rot=r)
				mc.parent(activeCam[0], camGroup)

			# Complete progress bar and end clock
			totalTime = time.time() - startTime;
			print "Read %d cameras in %f seconds.\n" %(count, totalTime)

			return camGroup
		else:
			mc.error("File doesn't exist: %s" %filePath)
			return False


def createImagePlanes(self, arg):
	""" NOT YET IMPLEMENTED
    	The idea is to find a way to store camera names in the .chan file from
    	Photoscan, based on the photo filename, then use that to automatically
    	create image planes with the appropriate images.
    """

	path = "/Volumes/hggl_SAN_1/Project_Media/110053_The_Louvre/2009753_The_Louvre/Vfx/PC010/3D/photoscan/sourceImages/charles/atrium_Undistorted/atrium_undistorted/proxy"
	portrait = True

	camLs = mc.ls(sl=True)

	for cam in camLs:
		if portrait:
			hfa = mc.getAttr("%sShape.horizontalFilmAperture" %cam)
			vfa = mc.getAttr("%sShape.verticalFilmAperture" %cam)
			mc.setAttr("%sShape.horizontalFilmAperture" %cam, vfa)
			mc.setAttr("%sShape.verticalFilmAperture" %cam, hfa)
			mc.setAttr("%sShape.filmFit" %cam, 2)

		imagePlane = mc.imagePlane(c="%sShape" %cam,
		                           lt=cam,
		                           n="%s_imagePlane" %cam,
		                           fn="%s/%s.jpg" %(path, cam),
		                           sia=False)
		mc.setAttr("%s.displayOnlyIfCurrent" %imagePlane[1], True)
		mc.setAttr("%s.alphaGain" %imagePlane[1], 0.8)
		mc.setAttr("%s.depth" %imagePlane[1], 256)


	def importPointCloudX(self, filePath):
		""" Read data from file - old method.
			Kept here for completeness.
		"""
		if os.path.isfile(filePath): # Check file exists

			# Read data into numpy array
			data = np.genfromtxt(filePath)
			count = data.shape[0]

			# Initialise progress bar and start timer
			mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=count) # Initialise progress bar
			startTime = time.time()

			# Create group and particles etc.
			fileName = os.path.splitext(os.path.basename(filePath))[0]
			pCloudGroup = mc.group(name="%s_pointCloud_GRP" %fileName, empty=True)
			pCloudParticle = mc.particle(name="pCloud_%s" %fileName)

			#mel.eval('addAttr -ln "rgbPP" -dt vectorArray %s' %pCloudParticle[1])
			#mel.eval('addAttr -ln "rgbPP0" -dt vectorArray %s' %pCloudParticle[1])
			mc.addAttr(pCloudParticle[1], longName="rgbPP", dataType="vectorArray")
			mc.addAttr(pCloudParticle[1], longName="rgbPP0", dataType="vectorArray")

			for i in range(count):

#				# Progress bar
#				if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
#					mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
#					mc.warning("Operation interrupted. You may wish to undo.")
#					return False
#				else:
#					mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Generating point cloud...") # Increment progress bar

				pX = data[i,0]
				pY = data[i,1]
				pZ = data[i,2]
				pR = data[i,3]/255.0
				pG = data[i,4]/255.0
				pB = data[i,5]/255.0
#				xyz = data[i,0:3]
#				rgb = data[i,3:6]/255

				mel.eval('emit -o %s -at "rgbPP" -pos %s %s %s -vv %s %s %s' %(pCloudParticle[0], pX, pY, pZ, pR, pG, pB))
				#mc.emit(object=pCloudParticle[0], position=xyz, attribute="rgbPP", vectorValue=rgb)

			mc.saveInitialState(pCloudParticle[0])
			mc.setAttr("%s.isDynamic" %pCloudParticle[1], 0)
			mc.parent(pCloudParticle[0], pCloudGroup)

			# Complete progress bar and end clock
			mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
			totalTime = time.time() - startTime;
			print "Read %d points in %f seconds.\n" %(count, totalTime)

			return pCloudGroup
		else:
			mc.error("File doesn't exist: %s" %filePath)
			return False

