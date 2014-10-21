# GPS Import Terrain Data
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios

import math, time, re, os
import numpy as np
import maya.cmds as mc
import maya.mel as mel
#import gpsCommon as gps


class terrainMap():
	"""Holds terrain data in a 2D numpy array"""

	def __init__(self, dim=(10, 10), offset=(0, 0), res=1):
#		self.dim = dim															# Dimensions of the array (x, y) (tuple)
		self.size = (dim[0]-1)*res, (dim[1]-1)*res								# Actual size of the data in world units (x, y) (tuple)
		self.offset = offset													# Co-ordinates of the zero index of the data in world units (x, y) (tuple)
#		self.centre = offset[0]+self.size[0]/2, offset[1]+self.size[1]/2, 0		# Co-ordinates of the centre of the data in world units (x, y, z) (tuple)
		self.res = res															# Resolution of the data (float)
		self.data = np.zeros(dim)												# 2D array to hold the data (numpy float array)

		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')


	def getArrID(self, coord):
		"""Return the closest array index for the given x,y co-ordinates"""

		return int((coord[0]-self.offset[0]) / self.res), int((coord[1]-self.offset[1]) / self.res)


	def getCoord(self, arrID):
		"""Return the x,y co-ordinates of the given array index"""

		return (arrID[0]*self.res) + self.offset[0], (arrID[1]*self.res) + self.offset[1]


	def compileFromXYZ(self, inData):
		"""Compile the 2D array by reading values from data in X,Y,Z format
		inData is a numpy array generated from a text file."""

		for i in range(inData.shape[0]):
			x,y = self.getArrID((inData[i,0], inData[i,1]))
			z = inData[i,2]
			self.data[x,y] = z


	def compileFromSlice(self, inData):
		"""Compile the 2D array by sampling an area of a larger data set
		inData is a terrainMap object containing the data set to be sampled."""

		# Get world space coords of the current tile
		minXY = self.getCoord((0,0))
		maxXY = self.getCoord((self.data.shape[0],self.data.shape[1]))

		# Get array indices of the corresponding area in the input data set array
		minXID,minYID = inData.getArrID(minXY)
		maxXID,maxYID = inData.getArrID(maxXY)

		# Slice data from input array
		print minXID, maxXID, minYID, maxYID
		self.data = inData.data[minXID:maxXID,minYID:maxYID]

		# Resize data based on size of slice
		self.size = (self.data.shape[0]-1)*self.res, (self.data.shape[1]-1)*self.res


	def printMap(self):
		"""Prints a representation of the terrain data to stdout. Used for debugging"""

		print "Terrain map data:"
		print "    Array dimensions: %s" %str(self.data.shape)
		print "   Zero index offset: %s" %str(self.offset)
		print "     Data resolution: %s" %str(self.res)
		print self.data


	def createGeo(self, name, parent, status=""):
		"""Generate geometry from terrain data
		First, a poly plane is created with the correct dimensions and subdivisions.
		Then its vertices are offset to create the terrain.
		name - the name to give to the created geo (string)
		orient - whether to parent the geo under a world orient group node (boolean)
		status - additional message to print in the status line during the operation (string)
		"""

		# Initialise progress bar and start timer
		mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=self.data.size) # Initialise progress bar
		startTime = time.time()

		# Check dimensions
		if self.data.shape[0] < 2 or self.data.shape[1] < 2:
			mc.warning("Unable to create terrain - dimensions are too small." + str(self.data.shape))
			return True

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

#		if parent:
#			mc.parent(plane, "orient_scene", relative=True)

		# Complete progress bar and end timer
		mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
		totalTime = time.time() - startTime;
		print "Processed %d points in %f seconds.\n" %(self.data.size, totalTime)
		return plane


class gpsImportTerrain():

	def __init__(self):
		self.winTitle = "GPS Import Terrain Data"
		self.winName = "gpsImportTerrain"

		self.format = "ASCII X,Y,Z (*.xyz)"
		self.res = 0


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
		self.fileOptUI("fileOpt", "windowRoot")
		self.dataOptUI("dataOpt", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnGenerate", width=198, height=28, label="Generate Terrain", command=lambda *args: self.generateTerrain(), enable=False)
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def fileOptUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Read Terrain Data")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Data file:", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		# text="/Volumes/hggl_SAN_1/RnD/rnd_job/Vfx/PC010/3D/maya/data/swiss_topo/swissalti3dxyzlv03/10m/swissALTI3D_.xyz"
		mc.textField("filePath", text="", width=360, height=24)
		mc.symbolButton(image="fileOpen.png", width=26, height=26, command=lambda *args: self.fileBrowse())
		mc.setParent(name)
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnOffset1=142)
		mc.button(width=116, label="Read data file", command=lambda *args: self.readFile(mc.textField("filePath", q=True, tx=True)))
		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.textFieldGrp("format", label="Format: ", text="", editable=False)
		mc.intFieldGrp("dpc", numberOfFields=1, label="Data point count: ", enable1=False)
		#mc.intFieldGrp("dim", numberOfFields=2, label="Data dimensions: ", enable1=False, enable2=False)
		#mc.textFieldGrp("rx", label="X range and size: ", text="", editable=False)
		#mc.textFieldGrp("ry", label="Y range and size: ", text="", editable=False)
		mc.floatFieldGrp("rx", numberOfFields=3, label="X min, max, size: ", enable1=False, enable2=False, enable3=False)
		mc.floatFieldGrp("ry", numberOfFields=3, label="Y min, max, size: ", enable1=False, enable2=False, enable3=False)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def dataOptUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		units = ["millimeter", "centimeter", "meter", "kilometer", "inch", "foot", "yard", "mile", "degrees"]
		defaultUnits = units[2]

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Data Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.floatFieldGrp("res", numberOfFields=1, label="Resolution: ", precision=3, enable1=False)
		mc.optionMenuGrp("units", label="Lat/long units: ")
		for item in units:
			mc.menuItem(label=item)
		mc.optionMenuGrp("units", edit=True, value=defaultUnits)
		mc.optionMenuGrp("heightUnits", label="Height units: ")
		for i in range(len(units)-1):
			mc.menuItem(label=units[i])
		mc.optionMenuGrp("heightUnits", edit=True, value=defaultUnits)
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("setUnits", label="Set scene units to match", value=1)
		mc.checkBox("orient", label="Orient scene", value=1)
		mc.setParent(name)

		mc.separator(width=396, height=16, style="in")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("tileSplit", label="Split into tiles", value=1)
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
		"""Updates info text box showing tiles to create."""

		tileSize = mc.intFieldGrp("tileSize", query=True, value=True)
		tilesX = int(math.ceil(self.DEM.size[0]/tileSize[0]))
		tilesY = int(math.ceil(self.DEM.size[1]/tileSize[1]))
		nTiles = tilesX*tilesY
		mc.textFieldGrp("tileInfo", edit=True, text="%d (%d x %d)" %(nTiles, tilesX, tilesY))


	def fileBrowse(self):
		"""Browse for a data file."""

		#dialogHome = os.environ['JOBPATH']
		#fileFilter = "ASCII X,Y,Z (*.xyz)"
		#startingDir = "/Users/mikebonnington/Downloads/swissalti3dxyzlv03/10m" # Remember this value
		startingDir = mc.workspace(expandName=mc.workspace(fileRuleEntry="translatorData"))
		filePath = mc.fileDialog2(dialogStyle=2, fileMode=1, dir=startingDir, fileFilter=self.format)
		if filePath:
			mc.textField("filePath", edit=True, text=filePath[0])


	def checkFileHeader(self, filePath):
		"""Check if data file contains header line(s).
		Returns number of lines to skip before data begins."""

		fileName = open(filePath, 'r')
		fileLine = fileName.readlines()
		pattern = re.compile(r"([-+]?([0-9]*\.[0-9]+|[0-9]+)\b){1,3}") # Regex for line containing 1-3 numbers separated by whitespace

		for i in range(len(fileLine)):
			match = pattern.match(fileLine[i])
			if match:
				return i

		mc.error("File is invalid")
		return -1


	def readFile(self, filePath):
		"""Read terrain file, but don't do anything with the data yet.
		Currently only works with ASCII X,Y,Z format data."""

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
				mc.intFieldGrp("dpc", edit=True, value=[count, 0, 0, 0])
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
				totalTime = time.time() - startTime;
				print "Read %d points in %f seconds.\n" %(data.shape[0], totalTime)
				#self.data = data

			else:
				mc.error("Resolution mismatch in X and Y axes.")
				return False

		else:
			mc.error("File doesn't exist: %s" %filePath)
			return False


	def getRes(self, data, tolerance=6):
		"""Calculate the resolution of the given data.

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


	def createOrientGroup(self, grpName):
		"""Create group for orienting scene correctly"""

		# Create empty group
		if not mc.objExists(grpName):
			grp = mc.group(name=grpName, empty=True, world=True)

			# Set and lock transforms
			mc.xform(grp, t=(0, 0, 0), ro=(-90, 0, 0), s=(1, 1, 1), absolute=True)
			mc.setAttr(grp+".t", lock=True)
			mc.setAttr(grp+".r", lock=True)
			mc.setAttr(grp+".s", lock=True)


	def generateTerrain(self):
		"""Generate the terrain"""

		# Get options
		tile = mc.checkBox("tileSplit", query=True, value=True)
		tileSize = mc.intFieldGrp("tileSize", query=True, value=True)
		#align = mc.checkBox("tileAlign", query=True, value=True)
		unit = mc.optionMenuGrp("units", query=True, value=True)
		setUnits = mc.checkBox("setUnits", query=True, value=True)
		orient = mc.checkBox("orient", query=True, value=True)
		#res = mc.floatFieldGrp("res", query=True, value=True)[0]
		res = self.res
		name = "%s_%d%s" %(os.path.splitext(os.path.basename(mc.textField("filePath", q=True, tx=True)))[0], res, unit)
		grp = "orient_scene"

		if setUnits:
			mc.currentUnit(linear=unit)
			print "Setting units to: %s" %unit
			mc.setAttr("perspShape.nearClipPlane", 1)
			mc.setAttr("perspShape.farClipPlane", 100000)

		if orient:
			self.createOrientGroup(grp)

		# Split into tiles and create geo
		if tile:
			#print res
			dim = (tileSize[0]/res)+1, (tileSize[1]/res)+1
			tilesX = int(math.ceil(self.DEM.size[0]/tileSize[0]))
			tilesY = int(math.ceil(self.DEM.size[1]/tileSize[1]))
			nTiles = tilesX*tilesY
			tileID = 1

#			if align:
#				startOffsetX = 600000 # the nearest (smaller) number to the start offset divisible by the grid size
#				startOffsetY = 196000
#			else:
			startOffsetX = self.DEM.offset[0]
			startOffsetY = self.DEM.offset[1]

			for j in range(tilesY):
				for i in range(tilesX):
					nameTile = "%s_tile%d_%d" %(name, i, j)
					status = "(tile %d of %d)" %(tileID, nTiles)
					offset = startOffsetX + i*tileSize[0], startOffsetY + j*tileSize[1]
					DEMTile = terrainMap(dim, offset, res)
					DEMTile.compileFromSlice(self.DEM)
					DEMTile.printMap()
					tileGeo = DEMTile.createGeo(nameTile, orient, status)
					if not tileGeo:
						return False
					if orient:
						mc.parent(tileGeo, grp, relative=True)
					tileID += 1

		# Else create geo for entire data set (can be slow!)
		else:
			self.DEM.createGeo(name, orient)
