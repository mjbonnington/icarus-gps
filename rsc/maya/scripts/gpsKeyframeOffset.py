# GPS Keyframe Offset
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios

import maya.cmds as mc
import random
from . import gpsSelectionSort


class gpsKeyframeOffset():

	def __init__(self):
		self.winTitle = "GPS Keyframe Offset"
		self.winName = "gpsKeyframeOffsetWindow"


	def offsetKeys(self):
		"""Offset keyframes on selected objects"""

		globalOffset = mc.floatSliderGrp("globalOffset", query=True, value=True)
		keySeparation = mc.floatSliderGrp("keySeparation", query=True, value=True)
		randomAmount = mc.floatSliderGrp("randomAmount", query=True, value=True)
		timeUnits = mc.radioButtonGrp("timeUnits", query=True, select=True)

		# If individual channels option is selected, get values
		channels = mc.checkBox("channels", query=True, value=True)
		if channels:
			channelList = []
			if mc.checkBoxGrp("translate", query=True, value1=True):
				channelList.append("tx")
			if mc.checkBoxGrp("translate", query=True, value2=True):
				channelList.append("ty")
			if mc.checkBoxGrp("translate", query=True, value3=True):
				channelList.append("tz")
			if mc.checkBoxGrp("rotate", query=True, value1=True):
				channelList.append("rx")
			if mc.checkBoxGrp("rotate", query=True, value2=True):
				channelList.append("ry")
			if mc.checkBoxGrp("rotate", query=True, value3=True):
				channelList.append("rz")
			if mc.checkBoxGrp("scale", query=True, value1=True):
				channelList.append("sx")
			if mc.checkBoxGrp("scale", query=True, value2=True):
				channelList.append("sy")
			if mc.checkBoxGrp("scale", query=True, value3=True):
				channelList.append("sz")
			if mc.checkBox("visibility", query=True, value=True):
				channelList.append("v")

		objLs = mc.ls(selection=True)

		for i in range(len(objLs)):

			# Set offset value
			offsetValue = globalOffset + (keySeparation * i) + random.uniform(-randomAmount, randomAmount)

			# Set time units (frames or seconds)
			if timeUnits == 1:
				timeChange = offsetValue
			elif timeUnits == 2:
				timeChange=str(offsetValue)+"sec"

			# Move keys
			if not channels:
				mc.keyframe(objLs[i], tc=timeChange, animation="objects", relative=True, includeUpperBound=True, option="over")
			else:
				for attribute in channelList:
					mc.keyframe(objLs[i], at=attribute, tc=timeChange, animation="objects", relative=True, includeUpperBound=True, option="over")


	def toggleControls(self, option):
		mc.checkBoxGrp("translate", edit=True, enable=option)
		mc.checkBoxGrp("rotate", edit=True, enable=option)
		mc.checkBoxGrp("scale", edit=True, enable=option)
		mc.checkBox("visibility", edit=True, enable=option)


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		#Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.keyOffsetPanelUI("keyframeOffsetOptions", "windowRoot")
		self.advOptPanelUI("keyframeOffsetAdvOptions", "windowRoot", collapse=True)
		gpsSelectionSort.gpsSelectionSort().selectionSortUI("sortSelectionOptions", "windowRoot", collapse=True)
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Offset Keyframes", command=lambda *args: self.offsetKeys())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def keyOffsetPanelUI(self, name, parent, collapse=False):
		"""Create UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Keyframe Offset Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Offset keys on selected objects.")
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.floatSliderGrp("globalOffset", label="Global Offset: ", value=0, field=True, precision=3, minValue=-50, maxValue=50, fieldMinValue=-99999999, fieldMaxValue=99999999, annotation="Animation keys on all selected objects will be offset by this value.")
		mc.floatSliderGrp("keySeparation", label="Increment: ", value=0, field=True, precision=3, minValue=-10, maxValue=10, fieldMinValue=-99999999, fieldMaxValue=99999999, annotation="Animation keys will be incremented by this value for each selected object.")
		mc.floatSliderGrp("randomAmount", label="Random Amount: ", value=0, field=True, precision=3, minValue=0, maxValue=10, fieldMinValue=-99999999, fieldMaxValue=99999999, annotation="Random value to be added or subracted to the offset for each key.")
		mc.separator(height=4, style="none")
		mc.radioButtonGrp("timeUnits", label="Units: ", labelArray2=['Frames', 'Seconds'], numberOfRadioButtons=2, columnWidth3=[140, 78, 156], select=1)
		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def advOptPanelUI(self, name, parent, collapse=False):
		"""Create UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Keyframe Offset Advanced Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("channels", label="Apply to individual channels", value=0, onCommand=lambda *args: self.toggleControls(True), offCommand=lambda *args: self.toggleControls(False))
		mc.setParent(name)
		mc.checkBoxGrp("translate", label="Translate: ", labelArray3=['X', 'Y', 'Z'], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.checkBoxGrp("rotate", label="Rotate: ", labelArray3=['X', 'Y', 'Z'], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.checkBoxGrp("scale", label="Scale: ", labelArray3=['X', 'Y', 'Z'], numberOfCheckBoxes=3, columnWidth4=[140, 78, 78, 78])
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("visibility", label="Visibility")
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.setParent(parent)

		self.toggleControls(False)
