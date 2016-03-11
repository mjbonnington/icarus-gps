#!/usr/bin/python

# [GPS] Randomise Vertices
# v0.3
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# (c) 2014-2016 Gramercy Park Studios
#
# Adds random deformation to points.
# Currently works on an mesh vertices, possible future support for NURBS CVs, lattice points, and maybe even UVs.
# TODO: add random seed for repeatability.


import random, time
import maya.cmds as mc
import maya.mel as mel
from maya.OpenMaya import MVector
import gpsCommon as gps


class gpsRandomiseVertices():

	def __init__(self):
		self.winTitle = "[GPS] Randomise Vertices"
		self.winName = "gpsRandomiseVertices"
		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')


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
		self.randomiseVerticesUI("randomiseVerticesOptions", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Randomise Vertices", command=lambda *args: self.randomiseVertices())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def randomiseVerticesUI(self, name, parent, collapse=False):
		""" Create randomise vertices options panel UI controls.
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.radioButtonGrp("offsetType1", label="Offset type: ", label1="Fractional (prevents intersections)", numberOfRadioButtons=1, columnWidth2=[140, 156], select=1, onCommand=lambda *args: self.tglOffsetControls(False), offCommand=lambda *args: self.tglOffsetControls(True))
		mc.radioButtonGrp("offsetType2", label="", label1="Absolute", numberOfRadioButtons=1, columnWidth2=[140, 156],	shareCollection="offsetType1")
		mc.separator(height=4, style="none")
		mc.radioButtonGrp("offsetSpace1", label="Offset space: ", label1="World (ignore object scaling)", numberOfRadioButtons=1, columnWidth2=[140, 156], select=1)
		mc.radioButtonGrp("offsetSpace2", label="", label1="Object", numberOfRadioButtons=1, columnWidth2=[140, 156], shareCollection="offsetSpace1")
		mc.separator(height=4, style="none")
		mc.floatSliderGrp("offset", label="Offset: ", value=0, field=True, precision=3, minValue=-10, maxValue=10, fieldMinValue=-99999999, fieldMaxValue=99999999, enable=False, annotation="Amount to offset the vertex in the specified axes.")
		mc.floatSliderGrp("randomness", label="Randomness: ", value=0.1, field=True, precision=3, minValue=0, maxValue=1, annotation="A random value within the specified range to be added to or subtracted from the offset value.")
		mc.checkBoxGrp("axes", label="Axes: ", labelArray3=['X', 'Y', 'Z'], valueArray3=[True, True, True], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("vtxNormal", label="Transform along vertex normal", value=0, onCommand=lambda *args: self.tglAxisControls(False), offCommand=lambda *args: self.tglAxisControls(True))
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def tglAxisControls(self, option):
		""" Toggle axis controls.
		"""
		mc.checkBoxGrp("axes", edit=True, enable=option)
		mc.radioButtonGrp("offsetSpace1", edit=True, enable=option)
		mc.radioButtonGrp("offsetSpace2", edit=True, enable=option)
		mc.radioButtonGrp("offsetSpace2", edit=True, select=1)


	def tglOffsetControls(self, option):
		""" Toggle offset controls.
		"""
		mc.floatSliderGrp("offset", edit=True, enable=option)


	def randomiseVertices(self):
		""" Randomise vertices.
		"""
		# Get options
		fractional = mc.radioButtonGrp("offsetType1", query=True, select=True)
		worldSpace = mc.radioButtonGrp("offsetSpace1", query=True, select=True)
		if fractional:
			offset = 0
		else:
			offset = mc.floatSliderGrp("offset", query=True, value=True)
		factor = mc.floatSliderGrp("randomness", query=True, value=True)
		trBX = mc.checkBoxGrp("axes", query=True, value1=True)
		trBY = mc.checkBoxGrp("axes", query=True, value2=True)
		trBZ = mc.checkBoxGrp("axes", query=True, value3=True)
		vtxNormal = mc.checkBox("vtxNormal", query=True, value=True)

		# Get current selection
		selLs = mc.ls(selection=True, flatten=True)

		# If poly mesh objects are selected, convert the selection to vertices
		for item in selLs:
			if gps.isMesh(item):
				vtxCount = mc.polyEvaluate(item, vertex=True)
				allVtx = "%s.vtx[0:%d]" %(item, vtxCount-1)
				mc.select(allVtx, add=True)

		# Filter selection so that only vertices are selected
		vtxLs = mc.filterExpand(expand=True, selectionMask=31)

		# Check selection
		if vtxLs == None:
			#gps.resetSelection(selLs)
			mc.warning("Randomise only works on vertices.")
			return False

		# Check offset value is nonzero
		elif offset+factor == 0:
			gps.resetSelection(selLs)
			mc.warning("No offset value specified. Operation will have no effect.")
			return False

		# Check at least one axis checkbox is enabled
		elif trBX+trBY+trBZ == 0:
			gps.resetSelection(selLs)
			mc.warning("No offset axes enabled. Operation will have no effect.")
			return False

		# Perform offset/randomise operation
		else:

			# Initialise progress bar and start clock
			mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=2*len(vtxLs)) # Initialise progress bar
			startTime = time.time()

			# Transform along vertex normal
			if vtxNormal:

				# Calculate averaged vertex normal vectors for each vertex
				statusMsg = "Calculating averaged vertex normals..."
				vtxNormalLs = []
				for vtx in vtxLs:
					# Progress bar
					if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
						mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
						gps.resetSelection(selLs)
						mc.warning("Operation cancelled when partially completed. You may wish to undo.")
						return False
					else:
						mc.progressBar(self.gMainProgressBar, edit=True, step=1, status=statusMsg) # Increment progress bar

						avg = gps.averageNormals(gps.getVertexNormals(vtx), normalise=True)
						vtxNormalLs.append(avg)

				# Apply offset and random values to each vector and move the vertex along it
				statusMsg = "Offsetting vertices along normal..."
				for i in range(len(vtxLs)):
					# Progress bar
					if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
						mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
						gps.resetSelection(selLs)
						mc.warning("Operation cancelled when partially completed. You may wish to undo.")
						return False
					else:
						mc.progressBar(self.gMainProgressBar, edit=True, step=1, status=statusMsg) # Increment progress bar

						if fractional:
							f = gps.fractionalOffset(vtxLs[i], worldSpace)/2
							avg = vtxNormalLs[i] * (f*random.uniform(-factor, factor))
						else:
							avg = vtxNormalLs[i] * (offset+random.uniform(-factor, factor))

						translate3 = avg.x, avg.y, avg.z # Convert MVector to tuple
						mc.xform(vtxLs[i], relative=True, t=translate3, ws=worldSpace)

			# Transform in XYZ
			else:
				statusMsg = "Offsetting vertices..."
				for vtx in vtxLs:
					# Progress bar
					if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
						mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
						gps.resetSelection(selLs)
						mc.warning("Operation cancelled when partially completed. You may wish to undo.")
						return False
					else:
						mc.progressBar(self.gMainProgressBar, edit=True, step=2, status=statusMsg) # Increment progress bar (step 2)

						if fractional:
							f = gps.fractionalOffset(vtx, worldSpace)/2
							translate3 = (f*random.uniform(-factor, factor)) * trBX, (f*random.uniform(-factor, factor)) * trBY, (f*random.uniform(-factor, factor)) * trBZ
						else:
							translate3 = (offset+random.uniform(-factor, factor)) * trBX, (offset+random.uniform(-factor, factor)) * trBY, (offset+random.uniform(-factor, factor)) * trBZ
						mc.xform(vtx, relative=True, t=translate3, ws=worldSpace)

			# Re-select items, complete progress bar and print completion message
			mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
			gps.resetSelection(selLs)
			totalTime = time.time() - startTime;
			print "Offset %d vertices in %f seconds.\n" %(len(vtxLs), totalTime)
			return True

