# GPS Import Terrain Data
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios

import os, math, time
import maya.cmds as mc
import maya.mel as mel
#import gpsCommon as gps
from numpy import *


class terrainMap():
	""""""
	def __init__(self):
		self.data = [] # List to hold the data
		self.dim_x = 0 # The size of the terrain data in the X axis
		self.dim_y = 0 # The size of the terrain data in the Y axis
		self.height = 0


class gpsImportTerrain():

	def __init__(self):
		self.winTitle = "GPS Import Terrain Data"
		self.winName = "gpsImportTerrain"
		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
		self.data = []
		self.dim = 0
		self.lenX = 0
		self.lenY = 0
		#DEM = terrainMap():


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
		self.importTerrainUI("importTerrainOptions", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Import Terrain", command=lambda *args: self.importTerrain())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def importTerrainUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Data file:", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.textField("filePath", width=360, height=24)
		mc.symbolButton(image="fileOpen.png", width=26, height=26, command=lambda *args: self.fileBrowse())
		mc.setParent(name)
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnOffset1=142)
		mc.button(width=116, label="Read data file", command=lambda *args: self.readFile(mc.textField("filePath", q=True, tx=True)))
		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.textFieldGrp(label="Format: ", text="ASCII X,Y,Z", editable=False)
		mc.intFieldGrp("dpc", numberOfFields=1, label="Data point count: ", enable1=False)
		mc.intFieldGrp("dim", numberOfFields=2, label="Data dimensions: ", enable1=False, enable2=False)
		mc.floatFieldGrp("rx", numberOfFields=2, label="X range: ", precision=1, enable1=False, enable2=False)
		mc.floatFieldGrp("ry", numberOfFields=2, label="Y range: ", precision=1, enable1=False, enable2=False)
		mc.floatFieldGrp("res", numberOfFields=1, label="Resolution: ", precision=1, enable1=False)

		mc.separator(width=396, height=16, style="in")


		unitMenuItems = ["millimeter", "centimeter", "meter", "kilometer", "inch", "foot", "yard", "mile"]

		mc.optionMenuGrp("units", label="Units: ")
		for item in unitMenuItems:
			mc.menuItem(label=item)
		mc.optionMenuGrp("units", edit=True, value="meter")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("setScale", label="Set scene scale to match", value=1)
		mc.setParent(name)

		mc.separator(width=396, height=16, style="in")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("tileSplit", label="Split into tiles", value=1)
		mc.setParent(name)
		mc.intFieldGrp("tileSize", numberOfFields=2, label="Tile size: ", value=[1000, 1000, 0, 0])
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("tileAlign", label="Align to grid", value=1)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def fileBrowse(self):
		"""Browse for a data file"""

		#dialogHome = os.environ['JOBPATH']
		fileFilter = "ASCII X,Y,Z (*.xyz)"
		#startingDir = "/Users/mikebonnington/Downloads/swissalti3dxyzlv03/10m" # Remember this value
		startingDir = mc.workspace(expandName=mc.workspace(fileRuleEntry="translatorData"))
		filePath = mc.fileDialog2(dialogStyle=2, fileMode=1, dir=startingDir, ff=fileFilter)
		if filePath:
			mc.textField("filePath", edit=True, text=filePath[0])


	def readFile(self, filePath):
		"""Read data file, but don't do anything with the data yet
		Currently only works with ASCII X,Y,Z format data"""

		if os.path.isfile(filePath):
			xyzFile = open(filePath, 'r')
			xyzFileLine = xyzFile.readlines()
			#pattern = re.compile("^X Y Z\s$")
			#if xyzFileLine[0] == "^X Y Z\s$":
			#xyzParticle = mc.particle(n="topo")

			# Initialise progress bar and start clock
			mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=len(xyzFileLine)) # Initialise progress bar
			startTime = time.time()

			data = []
			xLs = []
			yLs = []

			for i in range(0, len(xyzFileLine)):
				# Progress bar
				if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
					mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
					mc.warning("File read cancelled by user. Data will be incomplete.")
					return False
				else:
					mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Reading file...") # Increment progress bar

					#check
					x,y,z = xyzFileLine[i].split(" ")
					point = float(x), float(y), float(z)
					data.append(point)
					xLs.append(float(x))
					yLs.append(float(y))
					#mc.xform("pPlane1.vtx[%d]" %(i-1), absolute=True, t=(float(x),float(y),float(z)), worldSpace=True)
					#mc.emit(object="topo", position=(float(x),float(y),float(z)))

			#assumes data is square
			count = len(data)
			xMin = min(xLs)
			yMin = min(yLs)
			dim = math.sqrt(count)
			self.dim = dim-1
			self.lenX = data[count-1][0] - data[0][0]
			self.lenY = data[count-1][1] - data[0][1]
			res = self.lenX/self.dim
			mc.intFieldGrp("dpc", edit=True, value=[count, 0, 0, 0])
			mc.intFieldGrp("dim", edit=True, value=[dim, dim, 0, 0])
			mc.floatFieldGrp("rx", edit=True, value=[data[0][0], data[count-1][0], 0, 0])
			mc.floatFieldGrp("ry", edit=True, value=[data[0][1], data[count-1][1], 0, 0])
			mc.floatFieldGrp("res", edit=True, value=[res, 0, 0, 0])

			# Complete progress bar and end clock
			mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
			totalTime = time.time() - startTime;
			print "Read %d points in %f seconds.\n" %(count, totalTime)
			self.data = data
		else:
			mc.error("File doesn't exist: %s" %filePath)
			return False


	def importTerrain(self):
		""""""

		# Get options
		unit = mc.optionMenuGrp("units", query=True, value=True)

		if self.data:
			# Initialise progress bar and start clock
			mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=len(self.data)) # Initialise progress bar
			startTime = time.time()

			plane = mc.polyPlane(w=self.lenX, h=self.lenY, sx=self.dim, sy=self.dim, ax=[0,1,0], cuv=1, ch=0)

			for i in range(len(self.data)):
				# Progress bar
				if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
					mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
					mc.warning("Terrain generation cancelled when partially completed. You may wish to undo.")
					return False
				else:
					mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Generating terrain...") # Increment progress bar

					#x = str(self.data[i][0])+unit
					#y = str(self.data[i][1])+unit
					#z = str(self.data[i][2])+unit
					x = self.data[i][0]
					y = self.data[i][1]
					z = self.data[i][2]
					mc.xform("%s.vtx[%d]" %(plane[0], i), absolute=True, t=(x,y,z), worldSpace=True)

			# Complete progress bar and end clock
			mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
			totalTime = time.time() - startTime;
			print "Processed %d points in %f seconds.\n" %(len(self.data), totalTime)
		else:
			mc.error("No data loaded.")
			return False
