#!/usr/bin/python

# [GPS] Import Terrain Data
# v0.3
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2015 Gramercy Park Studios
#
# Import terrain (DEM / DTM / DSM) data into Maya.


import math, time, re, os
import numpy as np
import maya.cmds as mc
import maya.mel as mel
#import gpsCommon as gps


class terrainMap():
	""" Holds terrain data in a 2D numpy array.
	"""
	def __init__(self, dim=(10, 10), offset=(0, 0), res=1, name=None):
		self.dim = dim															# Dimensions of the array (x,y) (int tuple)
		self.offset = offset													# Co-ordinates of the zero index of the data in world units (x,y) (float tuple)
		self.res = res															# Resolution of the data (float)
		self.name = name														# Name to identify the data, usually derived from the file name (string)

		self.size = (dim[0]-1)*res, (dim[1]-1)*res								# Actual size of the data in world units (x,y) (float tuple)
	#	self.centre = offset[0]+self.size[0]/2, offset[1]+self.size[1]/2, 0		# Co-ordinates of the centre of the data in world units (x,y,z) (float tuple)
		self.data = np.zeros(dim)												# 2D array to hold the data (numpy float array)

		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')			# Initialise progress bar


	def getArrID(self, coord):
		""" Return the closest array index for the given x,y co-ordinates.
		"""
		id_x = min( int((coord[0]-self.offset[0]) / self.res), self.dim[0]-1 )
		id_y = min( int((coord[1]-self.offset[1]) / self.res), self.dim[1]-1 )

		return id_x, id_y
		#return int((coord[0]-self.offset[0]) / self.res), int((coord[1]-self.offset[1]) / self.res)


	def getCoord(self, arrID):
		""" Return the x,y co-ordinates of the given array index.
		"""
		return (arrID[0]*self.res) + self.offset[0], (arrID[1]*self.res) + self.offset[1]


	def roundToRes(self, x):
		""" Round the value of 'x' to the nearest multiple of the data resolution.
		"""
		return round(x/self.res)*self.res


	def compileFromXYZ(self, inData):
		""" Compile the 2D array by reading values from data in X,Y,Z format.

			inData is a numpy array generated from a text file.
		"""
		for i in range(inData.shape[0]):
			x,y = self.getArrID((inData[i,0], inData[i,1]))
			z = inData[i,2]
			self.data[x,y] = z


	def compileFromSlice(self, inData):
		""" Compile the 2D array by sampling an area of a larger data set.

			inData is a terrainMap object containing the data set to be sampled.
		"""
		# Get world space coords of the current tile
		minXY = self.getCoord((0,0))
		maxXY = self.getCoord((self.data.shape[0],self.data.shape[1]))

		# Get array indices of the corresponding area in the input data set array
		minXID,minYID = inData.getArrID(minXY)
		maxXID,maxYID = inData.getArrID(maxXY)

		# Slice data from input array
		#print minXID, maxXID, minYID, maxYID
		self.data = inData.data[minXID:maxXID,minYID:maxYID]

		# Resize data based on size of slice
		self.size = (self.data.shape[0]-1)*self.res, (self.data.shape[1]-1)*self.res


	def checkDimensions(self):
		""" Check the dimensions of the data array. Must be 2x2 minimum to create plane.
		"""
		if self.data.shape[0] < 2 or self.data.shape[1] < 2:
			mc.warning("Unable to create terrain - dimensions are too small: " + str(self.data.shape))
			return False
		else:
			return True


	def printMap(self):
		""" Prints a representation of the terrain data to stdout. Useful for debugging.
		"""
		print "Terrain map data:"
		print "    Array dimensions: %s" %str(self.data.shape)
		print "   Zero index offset: %s" %str(self.offset)
		print "     Data resolution: %s" %str(self.res)
		print self.data


	def createPreview(self, name, tiles=(100,100)):
		""" Generate preview plane from terrain data.
		"""
		# Check dimensions
		if not self.checkDimensions():
			return False

		# Initialise progress bar and start timer
		mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=tiles[0]*tiles[1]) # Initialise progress bar
		startTime = time.time()

		# Delete preview plane if it already exists
		planeName = "%s_previewPlane" %name
		if mc.objExists(planeName):
			mc.delete(planeName)

		# Create preview plane with annotation
		size = (self.size[0]+self.res, self.size[1]+self.res)
		plane = mc.polyPlane(n=planeName, w=size[0], h=size[1], sx=tiles[0], sy=tiles[1], ax=[0,0,1], cuv=1, ch=0)

		annotationShape = mc.annotate(plane, tx=name, p=(0,0,0))
		annotation = mc.listRelatives(annotationShape, parent=True)
		mc.setAttr(annotationShape+".displayArrow", 0)
		mc.parent(annotation, plane[0], relative=True)
		mc.rename(annotation, "%s_annotation" %name)

		mc.xform(plane[0], t=(size[0]/2, size[1]/2, 0))
		mc.makeIdentity(plane[0], apply=True)
		mc.xform(plane[0], rotatePivot=(0,0,0), scalePivot=(0,0,0))
		mc.xform(plane[0], t=(self.offset[0], self.offset[1], 0))

		#mc.setAttr(plane[0]+".template", True)
		mc.setAttr(plane[0]+".t", lock=True)
		mc.setAttr(plane[0]+".r", lock=True)
		mc.setAttr(plane[0]+".s", lock=True)

		vtxID = 0

		for j in range(tiles[1]+1):
			for i in range(tiles[0]+1):

				# Progress bar
				if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
					mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
					mc.warning("Terrain generation cancelled when partially completed. You may wish to undo.")
					return False
				else:
					mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Generating preview...") # Increment progress bar

					vtxX, vtxY, vtxZ = mc.pointPosition("%s.vtx[%d]" %(plane[0], vtxID), world=True)
					x,y = self.getArrID((vtxX, vtxY))
					z = self.data[x][y]
					mc.xform("%s.vtx[%d]" %(plane[0], vtxID), t=(0,0,z), relative=True) #, worldSpace=True) # Test in local space
					vtxID += 1

		# Complete progress bar and end timer
		mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
		totalTime = time.time() - startTime
		print "Processed %d points in %f seconds.\n" %(vtxID, totalTime)
		return plane


	def createGeo(self, name, status=""):
		""" Generate geometry from terrain data.

			First, a poly plane is created with the correct dimensions and subdivisions.
			Then its vertices are offset to create the terrain.

			name - the name to give to the created geo (string)
			status - additional message to print in the status line during the operation (string)
		"""
		# Check dimensions
		if not self.checkDimensions():
			return False

		# Initialise progress bar and start timer
		mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=self.data.size) # Initialise progress bar
		startTime = time.time()

		# Create poly plane
		plane = mc.polyPlane(n=name, w=self.size[0], h=self.size[1], sx=self.data.shape[0]-1, sy=self.data.shape[1]-1, ax=[0,0,1], cuv=1, ch=0)
		centreX = self.offset[0] + (self.size[0]/2)
		centreY = self.offset[1] + (self.size[1]/2)
		mc.move(centreX, centreY, 0)
		#mc.makeIdentity(apply=True)
		vtxID = 0

		for j in range(self.data.shape[1]):
			for i in range(self.data.shape[0]):

				# Progress bar
				if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
					mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
					mc.warning("Terrain generation cancelled when partially completed. You may wish to undo.")
					return False
				else:
					mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Generating terrain %s..." %status) # Increment progress bar

					#z = str(self.data[i][j]) + unit
					z = self.data[i][j]
					mc.xform("%s.vtx[%d]" %(plane[0], vtxID), t=(0,0,z), relative=True) #, worldSpace=True) # Test in local space
					vtxID += 1

		# Complete progress bar and end timer
		mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
		totalTime = time.time() - startTime
		print "Processed %d points in %f seconds.\n" %(self.data.size, totalTime)
		return plane


class gpsImportTerrain():

	def __init__(self):
		self.winTitle = "[GPS] Import Terrain Data"
		self.winName = "gpsImportTerrain"

		self.dataFormats = "ESRI ASCII Raster (*.asc);;ASCII X,Y,Z (*.xyz)"
		#self.res = 0


	def UI(self):
		""" Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=True)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.fileOptUI("File_Options", "windowRoot")
		self.dataOptUI("Data_Options", "windowRoot")
		self.genOptUI("Terrain_Generation_Options", "windowRoot")

		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnGenerate", width=198, height=28, label="Generate Terrain", command=lambda *args: self.generateTerrain(), enable=False)
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		self.checkDataFile()
		mc.showWindow(self.winName)


	def fileOptUI(self, name, parent, collapse=False):
		""" Create panel UI controls.
		"""
		if mc.optionVar(exists="GPSTerrainDataFile"):
			filePathText = mc.optionVar(query="GPSTerrainDataFile")
		else:
			filePathText = ""

		#mc.frameLayout(width=400, collapsable=False, cl=collapse, borderStyle="etchedIn", label="Read Terrain Data")
		mc.frameLayout(width=400, collapsable=False, cl=collapse, label=name.replace("_", " "))
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Data file:", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("filePath", text=filePathText, width=360, height=24, changeCommand=lambda *args: self.checkDataFile())
		mc.symbolButton(image="fileOpen.png", width=26, height=26, command=lambda *args: self.fileBrowse("filePath", self.dataFormats))
		mc.setParent(name)

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("prv", label="Preview", value=1, onCommand=lambda *args: self.tglPrv(True), offCommand=lambda *args: self.tglPrv(False), annotation="Generate a low-resolution preview of the terrain.")
		mc.setParent(name)
		mc.intFieldGrp("prvSubds", numberOfFields=2, label="Preview subdivisions: ", value=[50, 50, 0, 0])
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnOffset1=142)
		mc.button("btnReadFile", width=116, label="Read data file", command=lambda *args: self.readFile(mc.textField("filePath", q=True, tx=True)), enable=False)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def dataOptUI(self, name, parent, collapse=False):
		""" Create panel UI controls.
		"""
		units = ["millimeter", "centimeter", "meter", "kilometer", "inch", "foot", "yard", "mile", "degree"]
		defaultUnits = units[2]

		#mc.frameLayout(width=400, collapsable=False, cl=collapse, borderStyle="etchedIn", label="Data Options")
		mc.frameLayout(width=400, collapsable=False, cl=collapse, label=name.replace("_", " "))
		mc.columnLayout(name, enable=False)
		mc.separator(height=4, style="none")

		mc.textFieldGrp("format", label="Format: ", text="", editable=False)
		mc.textFieldGrp("arr_dim", label="Data dimensions: ", text="", editable=False)
		mc.floatFieldGrp("rx", numberOfFields=3, label="X min, max, size: ", enable1=False, enable2=False, enable3=False)
		mc.floatFieldGrp("ry", numberOfFields=3, label="Y min, max, size: ", enable1=False, enable2=False, enable3=False)
		mc.floatFieldGrp("res", numberOfFields=1, label="Resolution: ", precision=3, enable1=False)
		mc.optionMenuGrp("units", label="Lat/long units: ")
		for item in units:
			mc.menuItem(label=item)
		mc.optionMenuGrp("units", edit=True, value=defaultUnits, enable=True)
		mc.optionMenuGrp("heightUnits", label="Height units: ")
		for i in range(len(units)-1):
			mc.menuItem(label=units[i])
		mc.optionMenuGrp("heightUnits", edit=True, value=defaultUnits, enable=True)
	#	mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
	#	mc.columnLayout()
	#	mc.checkBox("setUnits", label="Set scene units to match", value=1)
	#	mc.checkBox("orient", label="Orient scene", value=0)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def genOptUI(self, name, parent, collapse=False):
		""" Create panel UI controls.
		"""
		mc.frameLayout(width=400, collapsable=False, cl=collapse, label=name.replace("_", " "))
		mc.columnLayout(name, enable=False)
		mc.separator(height=4, style="none")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("crop", label="Crop region", value=0, changeCommand=lambda *args: self.toggleCrop(), annotation="Crop to the specified region.\nEdit the values directly here, or manipulate the 'crop_area' object in the viewport.\nWhen done, press the 'Update' button to update the values.\nTo reset, delete the 'crop_area' object.")
		mc.setParent(name)
		mc.floatFieldGrp("cropX", numberOfFields=2, label="X min, max: ", value=[0, 0, 0, 0], changeCommand=lambda *args: self.updateCrop(), enable=False)
		mc.floatFieldGrp("cropY", numberOfFields=2, label="Y min, max: ", value=[0, 0, 0, 0], changeCommand=lambda *args: self.updateCrop(), enable=False)
		mc.setParent(name)
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnOffset1=142)
		mc.button("btnUpdateCrop", width=116, label="Update", command=lambda *args: self.toggleCrop(), enable=False)
		mc.setParent(name)

		mc.separator(width=396, height=12, style="none")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("tileSplit", label="Split into tiles", value=1, changeCommand=lambda *args: self.updateTileInfo(), annotation="Split the region into tiles.\nThe dimensions specified here are in world units.")
		mc.setParent(name)
		mc.intFieldGrp("tileSize", numberOfFields=2, label="Tile size: ", value=[1000, 1000, 0, 0], changeCommand=lambda *args: self.updateTileInfo())
		#mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		#mc.checkBox("tileAlign", label="Align to grid", value=0)
		#mc.setParent(name)
		mc.textFieldGrp("tileInfo", label="Tiles to create: ", text="", editable=False)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def updateTileInfo(self):
		""" Updates info text box showing tiles to create.
		"""
		if mc.checkBox("tileSplit", query=True, value=True):
			tileSize = mc.intFieldGrp("tileSize", query=True, value=True)
			mc.intFieldGrp("tileSize", edit=True, enable=True)
		else:
			tileSize = self.DEM.size[0], self.DEM.size[1]
			mc.intFieldGrp("tileSize", edit=True, enable=False)
		tilesX = int(math.ceil(self.DEM.size[0]/tileSize[0]))
		tilesY = int(math.ceil(self.DEM.size[1]/tileSize[1]))
		nTiles = tilesX*tilesY
		mc.textFieldGrp("tileInfo", edit=True, text="%d (%d x %d)" %(nTiles, tilesX, tilesY))


	def tglPrv(self, enable):
		""" 
		"""
		mc.intFieldGrp("prvSubds", edit=True, enable=enable)


	def toggleCrop(self):
		""" 
		"""
		uiEnable = mc.checkBox("crop", query=True, value=True)

		if uiEnable:
			# Generate cropping plane if it doesn't already exist
			if not mc.objExists("crop_area"):
				size = (self.DEM.size[0]+self.DEM.res, self.DEM.size[1]+self.DEM.res)
				plane = mc.polyPlane(n="crop_area", w=size[0], h=size[1], sx=1, sy=1, ax=[0,0,1], cuv=1, ch=0)
				mc.move(self.DEM.offset[0]+(size[0]/2), self.DEM.offset[1]+(size[1]/2), 0)
				mc.makeIdentity(apply=True)
				mc.setAttr("crop_area.tz", lock=True)
				mc.setAttr("crop_area.r", lock=True)
				mc.setAttr("crop_area.sz", lock=True)

			#mc.select("crop_area")

			# Get crop plane dimensions
			#bbox = mc.exactWorldBoundingBox()
			bbox = mc.xform("crop_area", query=True, boundingBox=True)

			# Round values off
			x_min = self.DEM.roundToRes(bbox[0])
			y_min = self.DEM.roundToRes(bbox[1])
			x_max = self.DEM.roundToRes(bbox[3])
			y_max = self.DEM.roundToRes(bbox[4])

			# Updade fields with rounded values
			mc.floatFieldGrp("cropX", edit=True, value=[x_min, x_max, 0, 0])
			mc.floatFieldGrp("cropY", edit=True, value=[y_min, y_max, 0, 0])

		# Toggle UI elements
		mc.floatFieldGrp("cropX", edit=True, enable=uiEnable)
		mc.floatFieldGrp("cropY", edit=True, enable=uiEnable)
		mc.button("btnUpdateCrop", edit=True, enable=uiEnable)


	def updateCrop(self):
		""" 
		"""
		# Get values from fields
		x_dim = mc.floatFieldGrp("cropX", query=True, value=True)
		y_dim = mc.floatFieldGrp("cropY", query=True, value=True)

		# Round values off
		x_min = self.DEM.roundToRes(x_dim[0])
		y_min = self.DEM.roundToRes(y_dim[0])
		x_max = self.DEM.roundToRes(x_dim[1])
		y_max = self.DEM.roundToRes(y_dim[1])

		# Updade fields with rounded values
		mc.floatFieldGrp("cropX", edit=True, value=[x_min, x_max, 0, 0])
		mc.floatFieldGrp("cropY", edit=True, value=[y_min, y_max, 0, 0])

		# Adjust size of crop area plane in viewport
		mc.select("crop_area")
		mc.xform("crop_area.vtx[0]", t=(x_min, y_min, 0), absolute=True, worldSpace=True)
		mc.xform("crop_area.vtx[1]", t=(x_max, y_min, 0), absolute=True, worldSpace=True)
		mc.xform("crop_area.vtx[2]", t=(x_min, y_max, 0), absolute=True, worldSpace=True)
		mc.xform("crop_area.vtx[3]", t=(x_max, y_max, 0), absolute=True, worldSpace=True)
		mc.xform("crop_area", centerPivots=True)
		mc.setAttr("crop_area.tz", lock=False)
		mc.setAttr("crop_area.r", lock=False)
		mc.setAttr("crop_area.sz", lock=False)
		mc.makeIdentity(apply=True)
		mc.setAttr("crop_area.tz", lock=True)
		mc.setAttr("crop_area.r", lock=True)
		mc.setAttr("crop_area.sz", lock=True)


	def setSceneUnits(self):
		""" Set the linear unit to match the data.
		"""
		unit = mc.optionMenuGrp("units", query=True, value=True)

		mc.currentUnit(linear=unit)
		print "Scene units set to: %s" %unit
		mc.setAttr("perspShape.nearClipPlane", 1)
		mc.setAttr("perspShape.farClipPlane", 100000)


	def fileBrowse(self, textFieldName, dataFormat):
		""" Browse for a data file.
		"""
		# If no file is specified, start in the project's data directory
		currentDir = os.path.dirname(mc.textField(textFieldName, query=True, text=True))
		if currentDir:
			startingDir = currentDir
		else:
			startingDir = mc.workspace(expandName=mc.workspace(fileRuleEntry="translatorData"))

		filePath = mc.fileDialog2(dialogStyle=2, fileMode=1, dir=startingDir, fileFilter=dataFormat, returnFilter=True)
		if filePath:
			mc.textField(textFieldName, edit=True, text=filePath[0])
			#self.format = filePath[1]
			self.checkDataFile(filePath[0])


	def checkDataFile(self, filePath=None):
		""" Check if specified data file exists.
		"""
		if filePath is None:
			filePath = mc.textField("filePath", query=True, text=True)

		# Check file exists
		if os.path.isfile(filePath):
			# Store file path in optionVar
			mc.optionVar( sv=('GPSTerrainDataFile', filePath) )
			self.format = self.checkDataFileFormat(filePath)
			mc.button("btnReadFile", edit=True, enable=True)
			#mc.columnLayout("dataOpt", edit=True, enable=True)
			return True

		else:
			mc.warning("File doesn't exist: %s" %filePath)
			mc.button("btnReadFile", edit=True, enable=False)
			#mc.columnLayout("dataOpt", edit=True, enable=False)
			return False


	def checkDataFileFormat(self, filePath):
		""" Determine format of supplied data file based on the file extension.
		"""
		availableFormats = self.dataFormats.split(";;")
		ext = os.path.splitext(filePath)[1]

		for fileFormat in availableFormats:
			if ext in fileFormat:
				return fileFormat

		return None


	def checkFileHeader(self, filePath):
		""" Check if data file contains header line(s).
			Returns number of lines to skip before data begins.
		"""
		fileName = open(filePath, 'r')
		fileLine = fileName.readlines()
		pattern = re.compile(r"([-+]?([0-9]*\.[0-9]+|[0-9]+)\b){1,3}") # Regex for line containing 1-3 numbers separated by whitespace

		for i in range(len(fileLine)):
			match = pattern.match(fileLine[i])
			if match:
				return i

		mc.error("File is invalid")
		return -1


	def getESRIHeaderData(self, filePath):
		""" Detect file header and read data.
			Returns a dictionary containing header data values.
		"""
		fileName = open(filePath, 'r')
		fileLine = fileName.readlines()
		reVarName = r"[a-zA-Z_]\w*" # Regex for a variable name (can only begin with a letter or underscore)
		reNumVal = r"[+-]?((\d*\.\d+)|(\d+))" # Regex a numeric value (positive or negative signs, decimal point optional)
		patternVarName = re.compile(reVarName)
		patternNumVal = re.compile(reNumVal)
		pattern = re.compile(r"^%s\s+%s$" %(reVarName, reNumVal))
		output = {}

		for i in range(len(fileLine)):
			match = pattern.match(fileLine[i])
			if match:
				varName = patternVarName.search(fileLine[i])
				numVal = patternNumVal.search(fileLine[i])
				if "." in numVal.group():
					outputNumVal = float(numVal.group())
				else:
					outputNumVal = int(numVal.group())
				#print varName.group(), outputNumVal, type(outputNumVal)
				output[varName.group()] = outputNumVal
			else:
				return output#, i

		mc.error("File is invalid")
		return -1


	def _readFile(self, filePath):
		""" Read terrain file, but don't do anything with the data yet.
			Currently only works with ASCII X,Y,Z format data.
		"""
		if os.path.isfile(filePath): # Check file exists
			startTime = time.time()
			data = np.genfromtxt(filePath, skip_header=self.checkFileHeader(filePath))

			# Calculate metadata
			count = data.shape[0]
			minX = min(data[:,0])
			minY = min(data[:,1])
			minZ = min(data[:,2])
			maxX = max(data[:,0])
			maxY = max(data[:,1])
			maxZ = max(data[:,2])
			lenX = maxX - minX
			lenY = maxY - minY
			resX = self.getRes(data[:,0])
			resY = self.getRes(data[:,1])
			dimX = (lenX/resX)+1
			dimY = (lenY/resY)+1

			if resX == resY: # Check X and Y resolution match
				self.res = res = resX
				mc.textFieldGrp("format", edit=True, text=self.format)
				mc.intFieldGrp("arr_dim", edit=True, value=[count, 0, 0, 0])
				#mc.textFieldGrp("rx", edit=True, text="%.1f - %.1f (%.1f)" %(minX, maxX, lenX))
				#mc.textFieldGrp("ry", edit=True, text="%.1f - %.1f (%.1f)" %(minY, maxY, lenY))
				#mc.intFieldGrp("dim", edit=True, value=[lenX, lenY, 0, 0])
				mc.floatFieldGrp("rx", edit=True, value=[minX, maxX, lenX, 0])
				mc.floatFieldGrp("ry", edit=True, value=[minY, maxY, lenY, 0])
				mc.floatFieldGrp("res", edit=True, value=[res, 0, 0, 0])
				#print res
				mc.button("btnGenerate", edit=True, enable=True)

				# Create terrain data (instance of terrainMap class)
				self.DEM = terrainMap((dimX, dimY), (minX, minY), res)
				self.DEM.compileFromXYZ(data)
				self.DEM.printMap()
				self.updateTileInfo()

				# Complete progress bar and end clock
				#mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
				totalTime = time.time() - startTime
				print "Read %d points in %f seconds.\n" %(count, totalTime)
				#self.data = data

			else:
				mc.error("Resolution mismatch in X and Y axes.")
				return False

		else:
			mc.error("File doesn't exist: %s" %filePath)
			return False


	def readFile(self, filePath):
		""" Read terrain file, but don't do anything with the data yet.
			ESRI .asc raster data.
		"""
		startTime = time.time()
		hdata = self.getESRIHeaderData(filePath)
		data = np.genfromtxt(filePath, skip_header=len(hdata))

		# Calculate metadata
		count = data.size
		minX = float( hdata['xllcorner'] )
		minY = float( hdata['yllcorner'] )
		maxX = float( minX + ( hdata['cellsize'] * ( hdata['ncols']-1 ) ) )
		maxY = float( minY + ( hdata['cellsize'] * ( hdata['nrows']-1 ) ) )
		lenX = maxX - minX
		lenY = maxY - minY
		dimX = hdata['ncols']
		dimY = hdata['nrows']
		res = float( hdata['cellsize'] )
		name = os.path.splitext(os.path.basename(mc.textField("filePath", q=True, tx=True)))[0]

		# Update info text fields
		mc.textFieldGrp("format", edit=True, text=self.format)
		mc.textFieldGrp("arr_dim", edit=True, text="%d (%d x %d)" %(count, dimX, dimY))
		mc.floatFieldGrp("rx", edit=True, value=[minX, maxX, lenX, 0])
		mc.floatFieldGrp("ry", edit=True, value=[minY, maxY, lenY, 0])
		mc.floatFieldGrp("res", edit=True, value=[res, 0, 0, 0])

		# Create terrain data (instance of terrainMap class)
		self.DEM = terrainMap((dimX, dimY), (minX, minY), res, name)
		self.DEM.data = np.rot90(data, 3)
		self.DEM.printMap()
		self.updateTileInfo()

		# Complete progress bar and end clock
		#mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
		totalTime = time.time() - startTime
		print "Read %d points in %f seconds.\n" %(count, totalTime)
		#self.data = data

		# Enable UI once data is loaded
		mc.columnLayout("Data_Options", edit=True, enable=True)
		mc.columnLayout("Terrain_Generation_Options", edit=True, enable=True)
		mc.button("btnGenerate", edit=True, enable=True)

		#if mc.checkBox("setUnits", query=True, value=True):
		self.setSceneUnits()
		self.createGroup(name)

		# Generate preview plane
		if mc.checkBox("prv", query=True, value=True):
			previewSubdivs = mc.intFieldGrp("prvSubds", query=True, value=True)
			previewPlane = self.DEM.createPreview(name, (previewSubdivs[0], previewSubdivs[1]))
			if previewPlane:
				mc.parent(previewPlane[0], "%s|%s" %("terrain_grp", name), relative=True)
				#mel.eval("FrameSelected;")
				print "Preview plane created. Press the 'F' key to frame the viewport."


	def getRes(self, data, tolerance=6):
		""" Calculate the resolution of the given data.

			data - a list of values to compare (list)
			tolerance - number of decimal places to compare values to (int)
			Returns the resolution value (float)
		"""
		# Sort the unique values in the given list and store in list a
		a = np.sort(np.unique(data))
		b = np.zeros((a.size-1))

		# Calculate the differences between each item in list a and store in list b
		for i in range(b.size):
			b[i] = round(abs(a[i+1] - a[i]), tolerance)

		# If data is valid, all the values in list b should be equal
		c = np.unique(b)

		if c.size == 1:
			return c[0]
		else:
			print c
			mc.error("Unable to calculate resolution.")
			return -1


	def createGroup(self, grpName, masterGrpName="terrain_grp"):
		""" Create group for terrain tiles and parent under the master group.
		"""
		# Create master group
		if not mc.objExists(masterGrpName):
			master_grp = mc.group(name=masterGrpName, empty=True, world=True)

			# Set and lock transforms
			mc.xform(master_grp, t=(0, 0, 0), ro=(-90, 0, 0), s=(1, 1, 1), absolute=True)
			mc.setAttr(master_grp+".t", lock=True)
			mc.setAttr(master_grp+".r", lock=True)
			mc.setAttr(master_grp+".s", lock=True)

			#print "Created master group for correct scene orientation."

		# Create terrain tile group
		if not mc.objExists("%s|%s" %(masterGrpName, grpName)):
			tile_grp = mc.group(name=grpName, empty=True, parent=masterGrpName)

			# Set and lock transforms
			mc.setAttr(tile_grp+".t", lock=True)
			mc.setAttr(tile_grp+".r", lock=True)
			mc.setAttr(tile_grp+".s", lock=True)

			#print "Created group for terrain: %s" %grpName


#	def previewTerrain(self):
#		""" Preview the terrain by undersampling the data.
#		"""
#		startTime = time.time()
#
#		# Get options
#		unit = mc.optionMenuGrp("units", query=True, value=True)
#		setUnits = mc.checkBox("setUnits", query=True, value=True)
#		orient = mc.checkBox("orient", query=True, value=True)
#		#res = mc.floatFieldGrp("res", query=True, value=True)[0]
#		res = self.DEM.res
#		name = "%s_%d%s" %(os.path.splitext(os.path.basename(mc.textField("filePath", q=True, tx=True)))[0], res, unit)
#		grp = "orient_scene"
#
#		self.setSceneUnits()
#
#		if orient:
#			self.createOrientGroup(grp)
#
#		fullGeo = self.DEM.createPreview(name, (100,100))
#		if not fullGeo:
#			return False
#		if orient:
#			mc.parent(fullGeo, grp, relative=True)
#
#		totalTime = time.time() - startTime
#		print "Generated preview in %f seconds.\n" %totalTime


	def generateTerrain(self):
		""" Generate the terrain.
		"""
		startTime = time.time()

		# Get options
		tile = mc.checkBox("tileSplit", query=True, value=True)
		tileSize = mc.intFieldGrp("tileSize", query=True, value=True)
		#align = mc.checkBox("tileAlign", query=True, value=True)
		crop = mc.checkBox("crop", query=True, value=True)
		unit = mc.optionMenuGrp("units", query=True, value=True)
		#setUnits = mc.checkBox("setUnits", query=True, value=True)
		#orient = mc.checkBox("orient", query=True, value=True)
		#res = mc.floatFieldGrp("res", query=True, value=True)[0]
		res = self.DEM.res
		grpName = os.path.splitext(os.path.basename(mc.textField("filePath", q=True, tx=True)))[0]
		name = "%s_%d%s" %(os.path.splitext(os.path.basename(mc.textField("filePath", q=True, tx=True)))[0], res, unit)
		grp = "orient_scene"
		tilesProcessed = 0

		self.setSceneUnits()
		self.createGroup(grpName)

		if crop:
			#x_dim = mc.floatFieldGrp("cropX", query=True, value=True)
			#y_dim = mc.floatFieldGrp("cropY", query=True, value=True)

			#mc.select("crop_area")
			#bbox = mc.exactWorldBoundingBox()
			bbox = mc.xform("crop_area", query=True, boundingBox=True)

			# Round values off
			x_min = self.DEM.roundToRes(bbox[0])
			y_min = self.DEM.roundToRes(bbox[1])
			x_max = self.DEM.roundToRes(bbox[3])
			y_max = self.DEM.roundToRes(bbox[4])

			offset = max(x_min, self.DEM.offset[0]), max(y_min, self.DEM.offset[1])
			dim = ((x_max-offset[0])/res)+1, ((y_max-offset[1])/res)+1

			DEMTile = terrainMap(dim, offset, res)
			DEMTile.compileFromSlice(self.DEM)
			DEMTile.printMap()
			cropGeo = DEMTile.createGeo("%s_crop" %name)
			if not cropGeo:
				return False
			mc.parent(cropGeo, "%s|%s" %("terrain_grp", grpName), relative=True)
			tilesProcessed += 1


		# Split into tiles and create geo
		elif tile:
			#print res
			dim = (tileSize[0]/res)+1, (tileSize[1]/res)+1
			tilesX = int(math.ceil(self.DEM.size[0]/tileSize[0]))
			tilesY = int(math.ceil(self.DEM.size[1]/tileSize[1]))
			nTiles = tilesX*tilesY
			#tileID = 1

#			if align:
#				startOffsetX = 600000 # the nearest (smaller) number to the start offset divisible by the grid size
#				startOffsetY = 196000
#			else:
			startOffsetX = self.DEM.offset[0]
			startOffsetY = self.DEM.offset[1]

			for j in range(tilesY):
				for i in range(tilesX):
					nameTile = "%s_tile%d_%d" %(name, i, j)
					status = "(tile %d of %d)" %(tilesProcessed+1, nTiles)
					offset = startOffsetX + i*tileSize[0], startOffsetY + j*tileSize[1]
					DEMTile = terrainMap(dim, offset, res)
					DEMTile.compileFromSlice(self.DEM)
					DEMTile.printMap()
					tileGeo = DEMTile.createGeo(nameTile, status)
					if not tileGeo:
						return False
					mc.parent(tileGeo, "%s|%s" %("terrain_grp", grpName), relative=True)
					tilesProcessed += 1

		# Else create geo for entire data set (can be slow!)
		else:
			fullGeo = self.DEM.createGeo(name)
			if not fullGeo:
				return False
			mc.parent(fullGeo, "%s|%s" %("terrain_grp", grpName), relative=True)
			tilesProcessed += 1

		totalTime = time.time() - startTime
		print "Generated %d tiles in %f seconds.\n" %(tilesProcessed, totalTime)

