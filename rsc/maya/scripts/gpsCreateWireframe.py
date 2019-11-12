# GPS Create Wireframe
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios
#
# Generates wireframe geometry with spheres and cylinders from a mesh


import time, re
import maya.cmds as mc
import maya.mel as mel
from . import gpsCommon as gps


class gpsCreateWireframe():

	def __init__(self):
		self.winTitle = "GPS Create Wireframe"
		self.winName = "gpsCreateWireframe"
		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')


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
		self.createWireframeUI("createWireframe", "windowRoot")
		self.advOptUI("dataOpt", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnGenerate", width=198, height=28, label="Create", enable=False, command=lambda *args: self.generateWireframe())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		# Load source mesh
		self.loadSel("srcObj", True)

		mc.showWindow(self.winName)


	def createWireframeUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Create Wireframe")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text("srcInfo", label="No source mesh selected.", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(width=396, height=12, style="in")

		mc.floatSliderGrp("rad", label="Radius: ", value=0.5, field=True, precision=3, minValue=0, maxValue=100, fieldMinValue=0, fieldMaxValue=99999999)
		mc.intSliderGrp("div", label="Axis divisions: ", value=8, field=True, minValue=2, maxValue=100, fieldMinValue=0, fieldMaxValue=9999)
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("onlyHard", label="Hard edges only", value=0) # TODO: IMPLEMENT
		mc.checkBox("combine", label="Combine mesh", value=0, annotation="This option will also delete history on the combined mesh.")#, onCommand=lambda *args: self.toggleSeparateControls(True), offCommand=lambda *args: self.toggleSeparateControls(False))
		#mc.checkBox("separate", label="Separate components", value=0, enable=False)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def advOptUI(self, name, parent, collapse=False):
		"""Create panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Advanced Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.rowLayout(numberOfColumns=3, columnWidth3=[140, 220, 26], columnAttach3=["right", "left", "left"], columnAlign3=["both", "both", "both"], columnOffset3=[4, 0, 0])
		mc.text(label="Source mesh:", wordWrap=False, align="right")
		mc.textField("srcObj", text="", width=220)
		mc.symbolButton("srcLoadSel", image="openObject.png", width=26, height=26, annotation="Load selection", command=lambda *args: self.loadSel("srcObj", True))
		mc.setParent(name)
		mc.separator(width=396, height=12, style="in")

		items = ["Sphere", "Locator", "Empty Group", "Instance of..."]
		self.componentUI(name, True, "vertex", items, 0)
		items[0] = "Cylinder"
		self.componentUI(name, True, "edge", items, 0)
		self.componentUI(name, False, "face", items[1:], 0)

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("orient", label="Orient to normals", value=1)
		mc.checkBox("keepOrig", label="Keep original object(s)", value=1)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def componentUI(self, name, enable, componentType, itemList, defaultSelection=0):
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.checkBox("%sCheck" %componentType, label="For each %s, create:" %componentType, value=enable, onCommand=lambda *args: self.toggleComponentControls(componentType, True), offCommand=lambda *args: self.toggleComponentControls(componentType, False))
		mc.setParent(name)
		mc.rowLayout(numberOfColumns=3, columnWidth3=[140, 220, 26], columnAttach3=["right", "left", "left"], columnAlign3=["both", "both", "both"], columnOffset3=[4, 0, 0])
		mc.optionMenuGrp("%sItems" %componentType)
		for item in itemList:
			mc.menuItem(label=item)
		mc.optionMenuGrp("%sItems" %componentType, edit=True, value=itemList[defaultSelection], changeCommand=lambda *args: self.toggleComponentSubControls(componentType))
		mc.textField("%sInstObj" %componentType, text="", width=220)
		mc.symbolButton("%sLoadSel" %componentType, image="openObject.png", width=26, height=26, annotation="Load selection", command=lambda *args: self.loadSel("%sInstObj" %componentType))
		mc.setParent(name)

		mc.separator(width=396, height=12, style="in")

		self.toggleComponentControls(componentType, enable)
		self.toggleComponentSubControls(componentType)


	def toggleComponentControls(self, componentType, option):
		mc.optionMenuGrp("%sItems" %componentType, edit=True, enable=option)
		if option == True:
			self.toggleComponentSubControls(componentType)
		else:
			mc.textField("%sInstObj" %componentType, edit=True, enable=False)
			mc.symbolButton("%sLoadSel" %componentType, edit=True, enable=False)


	def toggleComponentSubControls(self, componentType):
		selOpt = mc.optionMenuGrp("%sItems" %componentType, query=True, value=True)
		if selOpt == "Instance of...":
			mc.textField("%sInstObj" %componentType, edit=True, enable=True)
			mc.symbolButton("%sLoadSel" %componentType, edit=True, enable=True)
		else:
			mc.textField("%sInstObj" %componentType, edit=True, enable=False)
			mc.symbolButton("%sLoadSel" %componentType, edit=True, enable=False)


	def toggleSeparateControls(self, option):
		mc.checkBox("separate", edit=True, enable=option)


	def loadSel(self, loadInto, updSrc=False):
		"""Loads last selected object into specified text field"""

		selLs = mc.ls(selection=True, tail=True)
		if selLs:
			sel = selLs[0]
			# TODO: Check selection type is valid
			mc.textField(loadInto, edit=True, text=sel)
			if updSrc:
				# TODO: Check if selection type is mesh
				mc.text("srcInfo", edit=True, label="Generate wireframe geometry from mesh: %s" %sel)
				mc.button("btnGenerate", edit=True, enable=True)
		else:
			mc.warning("Nothing selected.")


	def generateWireframe(self):
		"""Generate wireframe"""

		# Get options
		src = mc.textField("srcObj", query=True, text=True)
		#vtxCheck = mc.checkBox("vertexCheck", query=True, value=True)
		#vtxObjType = mc.optionMenuGrp("vertexItems", query=True, value=True)
		#vtxInstObj = mc.textField("vertexInstObj", query=True, text=True)
		#edgeCheck = mc.checkBox("edgeCheck", query=True, value=True)
		#edgeObjType = mc.optionMenuGrp("edgeItems", query=True, value=True)
		#edgeInstObj = mc.textField("edgeInstObj", query=True, text=True)
		#faceCheck = mc.checkBox("faceCheck", query=True, value=True)
		#faceObjType = mc.optionMenuGrp("faceItems", query=True, value=True)
		#faceInstObj = mc.textField("faceInstObj", query=True, text=True)
		combine = mc.checkBox("combine", query=True, value=True)
		#separate = mc.checkBox("separate", query=True, value=True)

		self.generateComponents(src, "vertex")
		self.generateComponents(src, "edge")
		#self.generateComponents(src, "face")


	def generateComponents(self, src, componentType):
		"""Generate objects at specified components"""

		check = mc.checkBox("%sCheck" %componentType, query=True, value=True)
		objType = mc.optionMenuGrp("%sItems" %componentType, query=True, value=True)
		instObj = mc.textField("%sInstObj" %componentType, query=True, text=True)
		orient = mc.checkBox("orient", query=True, value=True)
		keepOrig = mc.checkBox("keepOrig", query=True, value=True)
		radius = mc.floatSliderGrp("rad", query=True, value=True)
		divs = mc.intSliderGrp("div", query=True, value=True)

		if check:

			# Count the number of components (vertices, edges or faces)
			count = eval("mc.polyEvaluate(src, %s=True)" %componentType)
			#print "%s: %d" %(componentType, count)

			# Initialise progress bar and start clock
			mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=count) # Initialise progress bar
			startTime = time.time()

			# Create objects to instance (if applicable)
			if objType == "Sphere":
				obj = mc.polySphere(name="pSphere", radius=radius, subdivisionsX=divs, subdivisionsY=divs)
				mc.polySoftEdge(obj, angle=180, constructionHistory=False)
			elif objType == "Cylinder":
				obj = mc.polyCylinder(name="pCylinder", radius=radius, height=1, subdivisionsX=divs, subdivisionsY=1, subdivisionsZ=0)
				mc.polySoftEdge(obj, angle=90, constructionHistory=False)
				mc.xform(obj, t=[0, 0.5, 0], piv=[0, -0.5, 0])
				mc.makeIdentity(apply=True)
			elif objType == "Instance of...":
				obj = instObj

			statusMsg = "Creating %s for %d %s..." %(gps.pluralise(objType), count, gps.pluralise(componentType))

			# Loop through all the source object's components
			for i in range(count):

				# Progress bar
				if mc.progressBar(self.gMainProgressBar, query=True, isCancelled=True): # Cancel operation if esc key pressed
					mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
					gps.resetSelection(selLs)
					mc.warning("Operation cancelled when partially completed. You may wish to undo.")
					return False
				else:
					mc.progressBar(self.gMainProgressBar, edit=True, step=1, status=statusMsg) # Increment progress bar

				if componentType == "vertex":
					vtx = "%s.vtx[%d]" %(src, i)
					pos = mc.pointPosition(vtx, world=True)
				elif componentType == "edge":
					edge = mc.polyInfo("%s.e[%d]" %(src, i), edgeToVertex=True)
					vtxs = edge[0].split()
					vtx = "%s.vtx[%d]" %(src, int(vtxs[2]))
					pos = mc.pointPosition(vtx, world=True)
					vtx2 = "%s.vtx[%d]" %(src, int(vtxs[3]))
					pos2 = mc.pointPosition(vtx2, world=True)
				elif componentType == "face":
					edge = mc.polyInfo("%s.f[%d]" %(src, i), edgeToVertex=True)

				if objType == "Locator":
					loc = mc.spaceLocator()
				elif objType == "Empty Group":
					loc = mc.group(empty=True)
				else:
					loc = mc.instance(obj)

				mc.xform(loc, a=True, t=pos)

				if orient:
					if componentType == "vertex":
						con = mc.normalConstraint(src, loc, weight=1, aimVector=[0, 1, 0], upVector=[0, 1, 0], worldUpType="vector", worldUpVector=[0, 1, 0])
						mc.delete(con)
					elif componentType == "edge":
						edgeLen = gps.distanceBetween(pos, pos2)
						mc.xform(loc, s=[1, edgeLen, 1])
						loc2 = mc.spaceLocator()
						mc.xform(loc2, t=pos2)
						con = mc.aimConstraint(loc2, loc, weight=1, aimVector=[0, 1, 0], upVector=[0, 1, 0], worldUpType="vector", worldUpVector=[0, 1, 0])
						mc.delete(con, loc2)

			if not keepOrig:
				mc.delete(obj)

			# Complete progress bar and print completion message
			mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
			totalTime = time.time() - startTime;
			print "Created %d %s in %f seconds.\n" %(count, gps.pluralise(objType), totalTime)
			return True
