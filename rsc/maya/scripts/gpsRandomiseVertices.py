#!/usr/bin/python

# [GPS] Randomise Vertices
# v0.4
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2016 Gramercy Park Studios
#
# Randomises positions of points. Works on polygon vertices, CVs and lattice points.
# TODO: store values using optionVars and implement reset settings


import random, time
import maya.cmds as mc
import maya.mel as mel
from maya.OpenMaya import MVector
import gpsCommon as gps


class gpsRandomiseVertices():

	def __init__(self):
		self.winTitle = "Randomise Vertices"
		self.winName = "gpsRandomiseVertices"
		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')


	def UI(self):
		""" Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title="[GPS] %s" %self.winTitle, sizeable=True, menuBar=True, menuBarVisible=True)

		# Create menu bar
		mc.menu(label="Edit", tearOff=False)
		mc.menuItem(label="Reset Settings", command="") #c "rp_storeRecallUI reset; rndPoints";
		mc.menu(label="Help", tearOff=False)
		mc.menuItem(label="About...", command=lambda *args: self.aboutUI())

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.randomiseVerticesUI("randomiseVerticesOptions", "windowRoot")

		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Randomise Vertices", command=lambda *args: self.randomiseVertices())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		self.updateUI()

		mc.showWindow(self.winName)


	def randomiseVerticesUI(self, name, parent, collapse=False):
		""" Create randomise vertices options panel UI controls.
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.radioButtonGrp("offsetType1", label="Offset type: ", label1="Absolute", numberOfRadioButtons=1, columnWidth2=[140, 156], select=1, 
						  changeCommand=lambda *args: self.updateUI())
		mc.radioButtonGrp("offsetType2", label="", label1="Fractional (prevents intersections)", numberOfRadioButtons=1, columnWidth2=[140, 156], shareCollection="offsetType1")

		mc.separator(height=4, style="none")
		mc.radioButtonGrp("offsetSpace", label="Offset space: ", labelArray3=["World", "Object", "Normal"], numberOfRadioButtons=3, columnWidth4=[140, 78, 78, 78], select=1, 
						  changeCommand=lambda *args: self.updateUI())

		mc.separator(height=4, style="none")
		mc.floatSliderGrp("randomness", label="Random spread: ", value=1, field=True, precision=3, minValue=0, maxValue=10, fieldMinValue=0, fieldMaxValue=99999999, 
						  changeCommand=lambda *args: self.updateUI(), 
						  dragCommand=lambda *args: self.updateUI(), 
						  annotation="A random value within the specified range to be added to or subtracted from the offset value.")
		mc.floatSliderGrp("offset", label="Offset: ", value=0, field=True, precision=3, minValue=-10, maxValue=10, fieldMinValue=-99999999, fieldMaxValue=99999999, 
						  changeCommand=lambda *args: self.updateUI(), 
						  dragCommand=lambda *args: self.updateUI(), 
						  annotation="Amount to offset the vertex in the specified axes.")
		mc.floatFieldGrp("minMax", label="Offset min/max: ", numberOfFields=2, value=[0, 0, 0, 0], precision=3, changeCommand=lambda *args: self.updateUI(), enable=False)
		mc.checkBoxGrp("axes", label="Axes: ", labelArray3=['X', 'Y', 'Z'], valueArray3=[True, True, True], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("useSeed", label="Use random seed", value=1, changeCommand=lambda *args: self.updateUI(), annotation="Use a seed value to yield repeatable results.")
		mc.setParent(name)
		mc.intSliderGrp("seed", label="Seed: ", value=0, field=True, minValue=0, maxValue=9999, fieldMinValue=0, fieldMaxValue=99999999)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def updateUI(self):
		""" Adjust UI elements.
		"""
		# Enable/disable offset value
		if mc.radioButtonGrp("offsetType1", q=1, select=True):
			mc.floatSliderGrp("offset", e=1, enable=True)
		else:
			mc.floatSliderGrp("offset", e=1, enable=False)

		# Calculate min/max values
		randomness = mc.floatSliderGrp("randomness", q=1, value=True)
		offset = mc.floatSliderGrp("offset", q=1, value=True)
		mc.floatFieldGrp("minMax", e=1, value1=offset-(randomness/2))
		mc.floatFieldGrp("minMax", e=1, value2=offset+(randomness/2))

		# Change axis labels depending on offset space option
		if mc.radioButtonGrp("offsetSpace", q=1, select=True) == 3:
			mc.checkBoxGrp("axes", e=1, labelArray3=['U', 'V', 'N'])
		else:
			mc.checkBoxGrp("axes", e=1, labelArray3=['X', 'Y', 'Z'])

		# Enable/disable seed value
		mc.intSliderGrp("seed", e=1, enable=mc.checkBox("useSeed", q=1, value=True))


	def aboutUI(self):
		""" Create about window UI.
		"""
		message = """Randomise Vertices
v0.4

Mike Bonnington <mike.bonnington@gps-ldn.com>
(c) 2014-2016 Gramercy Park Studios

Randomises positions of points. Works on polygon vertices, CVs and lattice points.
"""
		mc.confirmDialog(parent=self.winName, title="About %s" %self.winTitle, message=message, button="OK")


	def randomiseVertices(self):
		""" Randomise vertices.
		"""
		# Get options
		fractional = mc.radioButtonGrp("offsetType2", q=1, select=True)
		if fractional:
			factor = mc.floatSliderGrp("randomness", q=1, value=True)
			if factor > 1:
				factor = 1
		offsetSpace = mc.radioButtonGrp("offsetSpace", q=1, select=True)
		min_ = mc.floatFieldGrp("minMax", q=1, value1=True)
		max_ = mc.floatFieldGrp("minMax", q=1, value2=True)
		enX = mc.checkBoxGrp("axes", q=1, value1=True)
		enY = mc.checkBoxGrp("axes", q=1, value2=True)
		enZ = mc.checkBoxGrp("axes", q=1, value3=True)

		# Generate random seed for repeatable results
		if mc.checkBox("useSeed", q=1, value=True):
			seed = mc.intSliderGrp("seed", q=1, value=True)
			random.seed(seed)

		# Filter selection so that only polygon vertices, CVs or lattice points are selected
		if offsetSpace == 3:
			vtxLs = mc.filterExpand(expand=True, selectionMask=(28, 31))
		else:
			vtxLs = mc.filterExpand(expand=True, selectionMask=(28, 31, 46))

		# Check selection
		if vtxLs == None:
			if offsetSpace == 3:
				mc.warning("Randomise in normal space only works on polygon vertices or CVs.")
			else:
				mc.warning("Randomise only works on polygon vertices, CVs or lattice points.")
			return False

		# Check offset values are nonzero
		elif (min_ == 0) and (max_ == 0):
			mc.warning("No offset value specified. Operation will have no effect.")
			return False

		# Check at least one axis checkbox is enabled
		elif enX+enY+enZ == 0:
			mc.warning("No offset axes enabled. Operation will have no effect.")
			return False

		# Perform offset/randomise operation
		# Initialise progress bar and start clock
		mc.progressBar(self.gMainProgressBar, e=1, beginProgress=True, isInterruptable=True, maxValue=len(vtxLs)) # Initialise progress bar
		startTime = time.time()
		#mc.waitCursor(state=True)

		for vtx in vtxLs:
			statusMsg = "Offsetting vertices..."

			# Progress bar
			if mc.progressBar(self.gMainProgressBar, q=1, isCancelled=True): # Cancel operation if esc key pressed
				mc.progressBar(self.gMainProgressBar, e=1, endProgress=True) # Complete progress bar
				mc.warning("Operation cancelled when partially completed. You may wish to undo.")
				return False
			else:
				mc.progressBar(self.gMainProgressBar, e=1, step=1, status=statusMsg) # Increment progress bar

				# Generate random x,y,z values and offset vertex
				xrand = yrand = zrand = 0
				if fractional:
					f = gps.fractionalOffset(vtx, offsetSpace)/2
					if enX:
						xrand = random.uniform(-f*factor, f*factor)
					if enY:
						yrand = random.uniform(-f*factor, f*factor)
					if enZ:
						zrand = random.uniform(-f*factor, f*factor)
				else:
					if enX:
						xrand = random.uniform(min_, max_)
					if enY:
						yrand = random.uniform(min_, max_)
					if enZ:
						zrand = random.uniform(min_, max_)

				if offsetSpace == 1: # World space
					mc.move(xrand, yrand, zrand, vtx, relative=True, worldSpace=True)

				elif offsetSpace == 2: # Object space
					mc.move(xrand, yrand, zrand, vtx, relative=True, objectSpace=True)

				elif offsetSpace == 3: # Normal (u,v,n)
					mc.moveVertexAlongDirection(vtx, n=zrand) # move along normal direction first
					mc.moveVertexAlongDirection(vtx, u=xrand)
					mc.moveVertexAlongDirection(vtx, v=yrand)

		# Complete progress bar and print completion message
		mc.progressBar(self.gMainProgressBar, e=1, endProgress=True) # Complete progress bar
		totalTime = time.time() - startTime;
		#mc.waitCursor(state=False)
		print "Offset %d vertices in %f seconds.\n" %(len(vtxLs), totalTime)
		return True

