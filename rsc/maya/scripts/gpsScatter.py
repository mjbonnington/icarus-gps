# GPS Scatter
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios

import maya.cmds as mc
import random


class gpsScatter():

	def __init__(self):
		self.winTitle = "GPS Scatter"
		self.winName = "gpsScatterWindow"


	def scatter(self):
		mode = mc.radioCollection("mode", query=True, select=True)

		objLs = mc.ls(selection=True)

		if mode == "duplicateScatter":
			nCopies = mc.intSliderGrp("nCopies", query=True, value=True)
			geoType = mc.radioButtonGrp("geoType", query=True, select=True)
			newGroup = mc.checkBox("newGroup", query=True, value=True)
			keepOrig = mc.checkBox("keepOrig", query=True, value=True)

			for obj in objLs:
				if newGroup:
					groupName = obj + "_scatter"
					parent = mc.listRelatives(obj, parent=True)
					if parent == None:
						mc.group(empty=True, n=groupName)
					else:
						mc.group(empty=True, n=groupName, p=parent[0])
				for i in range(nCopies):
					# Copies
					if geoType == 1:
						if mc.checkBox("duplicateInputGraph", query=True, value=True):
							sel = mc.duplicate(obj, rr=True, un=True)
						elif mc.checkBox("duplicateInputConnections", query=True, value=True):
							sel = mc.duplicate(obj, rr=True, ic=True)
						else:
							sel = mc.duplicate(obj, rr=True)
					# Instances
					elif geoType == 2:
						sel = mc.instance(obj)
					self.scatterObjects(sel)
					if newGroup:
						mc.parent(sel, groupName)
				if not keepOrig:
					mc.delete(obj)

		elif mode == "scatterSelected":
			self.scatterObjects(objLs)


	def scatterObjects(self, objLs):
		"""Scatter objects"""

		trEnable = mc.checkBox("translateEnable", query=True, value=True)
		trRand = mc.floatSliderGrp("translateRand", query=True, value=True)
		#trAxes = mc.checkBoxGrp("translateAxes", query=True, valueArray3=True)
		trBX = mc.checkBoxGrp("translateAxes", query=True, value1=True)
		trBY = mc.checkBoxGrp("translateAxes", query=True, value2=True)
		trBZ = mc.checkBoxGrp("translateAxes", query=True, value3=True)
		roEnable = mc.checkBox("rotateEnable", query=True, value=True)
		roRand = mc.floatSliderGrp("rotateRand", query=True, value=True)
		#roAxes = mc.checkBoxGrp("rotateAxes", query=True, valueArray3=True)
		roBX = mc.checkBoxGrp("rotateAxes", query=True, value1=True)
		roBY = mc.checkBoxGrp("rotateAxes", query=True, value2=True)
		roBZ = mc.checkBoxGrp("rotateAxes", query=True, value3=True)
		scEnable = mc.checkBox("scaleEnable", query=True, value=True)
		scRand = mc.floatSliderGrp("scaleRand", query=True, value=True)
		#scAxes = mc.checkBoxGrp("scaleAxes", query=True, valueArray3=True)
		scBX = mc.checkBoxGrp("scaleAxes", query=True, value1=True)
		scBY = mc.checkBoxGrp("scaleAxes", query=True, value2=True)
		scBZ = mc.checkBoxGrp("scaleAxes", query=True, value3=True)
		scaleUniform = mc.checkBox("scaleUniform", query=True, value=True)

		for obj in objLs:
			translate3 = random.uniform(-trRand, trRand) * trBX, random.uniform(-trRand, trRand) * trBY, random.uniform(-trRand, trRand) * trBZ
			rotate3 = random.uniform(-roRand, roRand) * roBX, random.uniform(-roRand, roRand) * roBY, random.uniform(-roRand, roRand) * roBZ

			scaleCurrent = mc.xform(obj, query=True, relative=True, scale=True)
			scaleFactorX = scaleCurrent[0] * scRand
			scaleFactorY = scaleCurrent[1] * scRand
			scaleFactorZ = scaleCurrent[2] * scRand
			if scaleUniform:
				scaleRand = random.uniform(-1, 1)
				scaleRandX = scaleRand * scaleFactorX * scBX
				scaleRandY = scaleRand * scaleFactorY * scBY
				scaleRandZ = scaleRand * scaleFactorZ * scBZ
			else:
				scaleRandX = random.uniform(-1, 1) * scaleFactorX * scBX
				scaleRandY = random.uniform(-1, 1) * scaleFactorY * scBY
				scaleRandZ = random.uniform(-1, 1) * scaleFactorZ * scBZ
			scale3 = scaleCurrent[0]+scaleRandX, scaleCurrent[1]+scaleRandY, scaleCurrent[2]+scaleRandZ

			# Apply the transformations
			if trEnable:
				mc.xform(obj, relative=True, t=translate3)
			if roEnable:
				mc.xform(obj, relative=True, ro=rotate3)
			if scEnable:
				mc.xform(obj, relative=False, s=scale3)


	def toggleControls(self, option):
		mc.intSliderGrp("nCopies", edit=True, enable=option)
		mc.radioButtonGrp("geoType", edit=True, enable=option, select=1)
		mc.checkBox("duplicateInputGraph", edit=True, enable=option, value=0)
		mc.checkBox("duplicateInputConnections", edit=True, enable=option, value=0)
		mc.checkBox("newGroup", edit=True, enable=option)
		mc.checkBox("keepOrig", edit=True, enable=option)


	def toggleDuplicateControls(self, option):
		mc.checkBox("duplicateInputGraph", edit=True, enable=option)
		mc.checkBox("duplicateInputConnections", edit=True, enable=option)


	def toggleDuplicateIGControls(self, option):
		mc.radioButtonGrp("geoType", edit=True, enable=option)
		mc.checkBox("duplicateInputConnections", edit=True, enable=option)


	def toggleDuplicateICControls(self, option):
		mc.radioButtonGrp("geoType", edit=True, enable=option)
		mc.checkBox("duplicateInputGraph", edit=True, enable=option)


	def toggleTranslateControls(self, option):
		mc.floatSliderGrp("translateRand", edit=True, enable=option)
		mc.checkBoxGrp("translateAxes", edit=True, enable=option)


	def toggleRotateControls(self, option):
		mc.floatSliderGrp("rotateRand", edit=True, enable=option)
		mc.checkBoxGrp("rotateAxes", edit=True, enable=option)


	def toggleScaleControls(self, option):
		mc.floatSliderGrp("scaleRand", edit=True, enable=option)
		mc.checkBoxGrp("scaleAxes", edit=True, enable=option)
		mc.checkBox("scaleUniform", edit=True, enable=option)


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.scatterPanelUI("scatterPanel", "windowRoot")
		self.optionsPanelUI("optionsPanel", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Scatter Objects", command=lambda *args: self.scatter())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def scatterPanelUI(self, name, parent, collapse=False):
		"""Create scatter panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Distribution")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Distribute objects randomly by scattering.", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(width=396, height=12, style="in")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("translateEnable", label="Translate", value=True, onCommand=lambda *args: self.toggleTranslateControls(True), offCommand=lambda *args: self.toggleTranslateControls(False))
		mc.setParent(name)
		mc.floatSliderGrp("translateRand", label="Translate random: ", value=50, field=True, minValue=0, maxValue=100, fieldMinValue=0, fieldMaxValue=99999999)
		mc.checkBoxGrp("translateAxes", label="Axes: ", labelArray3=['X', 'Y', 'Z'], valueArray3=[True, False, True], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.separator(width=396, height=12, style="in")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("rotateEnable", label="Rotate", value=True, onCommand=lambda *args: self.toggleRotateControls(True), offCommand=lambda *args: self.toggleRotateControls(False))
		mc.setParent(name)
		mc.floatSliderGrp("rotateRand", label="Rotate random: ", value=180, field=True, minValue=0, maxValue=360, fieldMinValue=0, fieldMaxValue=360)
		mc.checkBoxGrp("rotateAxes", label="Axes: ", labelArray3=['X', 'Y', 'Z'], valueArray3=[False, True, False], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.separator(width=396, height=12, style="in")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("scaleEnable", label="Scale", value=True, onCommand=lambda *args: self.toggleScaleControls(True), offCommand=lambda *args: self.toggleScaleControls(False))
		mc.setParent(name)
		mc.floatSliderGrp("scaleRand", label="Scale random: ", value=0.5, precision=3, field=True, minValue=0, maxValue=1)
		mc.checkBoxGrp("scaleAxes", label="Axes: ", labelArray3=['X', 'Y', 'Z'], valueArray3=[True, True, True], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("scaleUniform", label="Uniform scale", value=True)
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def optionsPanelUI(self, name, parent, collapse=False):
		"""Create options panel UI controls"""

		popupHelp = "For more options, duplicate your objects first using Edit>Duplicate Special, then use the Scatter Selected Objects option."

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.radioCollection("mode")
		mc.radioButton("scatterSelected", label="Scatter Selected Objects", select=True)
		mc.radioButton("duplicateScatter", label="Duplicate and Scatter", onCommand=lambda *args: self.toggleControls(True), offCommand=lambda *args: self.toggleControls(False))
		mc.setParent(name)
		mc.separator(width=396, height=12, style="in")
		mc.intSliderGrp("nCopies", label="Number of copies: ", value=50, field=True, minValue=1, maxValue=100, fieldMinValue=0, fieldMaxValue=1000)
		mc.radioButtonGrp("geoType", label="Geometry type: ", labelArray2=['Copy', 'Instance'], numberOfRadioButtons=2, columnWidth3=[140, 78, 156], select=1, annotation=popupHelp, onCommand1=lambda *args: self.toggleDuplicateControls(True), onCommand2=lambda *args: self.toggleDuplicateControls(False))
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("duplicateInputGraph", label="Duplicate input graph", value=0, annotation=popupHelp, onCommand=lambda *args: self.toggleDuplicateIGControls(False), offCommand=lambda *args: self.toggleDuplicateIGControls(True))
		mc.checkBox("duplicateInputConnections", label="Duplicate input connections", value=0, annotation=popupHelp, onCommand=lambda *args: self.toggleDuplicateICControls(False), offCommand=lambda *args: self.toggleDuplicateICControls(True))
		mc.separator(height=4, style="none")
		mc.checkBox("newGroup", label="Parent objects under new group", value=1)
		mc.checkBox("keepOrig", label="Keep original object(s)", value=1)
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.setParent(parent)

		# If single object is selected, automatically enter duplicate mode
		if len(mc.ls(selection=True)) == 1:
			mc.radioCollection("mode", edit=True, select="duplicateScatter")
			self.toggleControls(True)
		else:
			mc.radioCollection("mode", edit=True, select="scatterSelected")
			self.toggleControls(False)
			
