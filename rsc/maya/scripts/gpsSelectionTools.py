# GPS Selection Tools
# v0.2
#
# Michael Bonnington 2014
# Gramercy Park Studios

import maya.cmds as mc
import random
from rsc.maya.scripts import gpsSelectionSort


class gpsSelectionTools():

	def __init__(self):
		self.winTitle = "GPS Selection Tools"
		self.winName = "gpsSelectionToolsWindow"

		# Store original selection
		self.selOrig = mc.ls(selection=True, flatten=True)


	def periodicSelection(self, selectN, ofEvery):
		"""Periodic selection - select X out of every Y items within current selection"""

		if selectN > ofEvery:
			errorMsg = "Unable to select %d out of every %d items. The first parameter must be smaller than the second." %(selectN, ofEvery)
			mc.error(errorMsg)
		else:
			sel = mc.ls(selection=True, flatten=True)
			mc.select(clear=True)

			for i in range(len(sel)):
				if (i % ofEvery) < selectN:
					mc.select(sel[i], add=True)


	def randomSelection(self, percentage):
		"""Random selection - randomly select items within current selection"""

		sel = mc.ls(selection=True, flatten=True)
		mc.select(clear=True)

		for i in range(len(sel)):
			if random.uniform(0, 100) < percentage:
				mc.select(sel[i], add=True)


	def resetSelection(self, selOrig):
		"""Reset selection - to original set of items before this script was run"""

		mc.select(selOrig, replace=True)


	def invertSelection(self, selOrig):
		"""Invert selection - mask current selection with original selection"""

		mc.select(selOrig, toggle=True)


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		#Create controls
		resetButtonlabel = "Reset Selection (%d items)" %len(self.selOrig)
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.periodicSelectionPanelUI("periodicSelectionOptions", "windowRoot")
		self.randomSelectionPanelUI("randomSelectionOptions", "windowRoot")
		gpsSelectionSort.gpsSelectionSort().selectionSortUI("sortSelectionOptions", "windowRoot", collapse=True)
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Invert Selection", command=lambda *args: self.invertSelection(self.selOrig))
		mc.button(width=198, height=28, label=resetButtonlabel, command=lambda *args: self.resetSelection(self.selOrig))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def periodicSelectionPanelUI(self, name, parent, collapse=False):
		"""Create periodic selection UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Periodic Selection")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Select specifed number of items from within the current selection.")
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.intSliderGrp("selectN", label="Select: ", value=1, field=True, minValue=1, maxValue=10, fieldMinValue=1, fieldMaxValue=99999999)
		mc.intSliderGrp("ofEvery", label="From every: ", value=2, field=True, minValue=1, maxValue=10, fieldMinValue=1, fieldMaxValue=99999999)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.button(width=116, label="Periodic Selection", command=lambda *args: self.periodicSelection(mc.intSliderGrp('selectN', q=True, v=True), mc.intSliderGrp('ofEvery', q=True, v=True)))
		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.setParent(parent)


	def randomSelectionPanelUI(self, name, parent, collapse=False):
		"""Create random selection UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Random Selection")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Randomly select items from within the current selection.")
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.floatSliderGrp("randomPercentage", label="Percentage: ", value=50, field=True, minValue=0, maxValue=100, fieldMinValue=0, fieldMaxValue=100)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.button(width=116, label="Random Selection", command=lambda *args: self.randomSelection(mc.floatSliderGrp('randomPercentage', q=True, v=True)))
		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.setParent(parent)
