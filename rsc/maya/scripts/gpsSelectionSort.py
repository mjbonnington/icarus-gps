# GPS Sort Selection
# v0.2
#
# Michael Bonnington 2014
# Gramercy Park Studios

import operator
import maya.cmds as mc
import maya.mel as mel
from . import gpsCommon as gps


class gpsSelectionSort():

	def __init__(self):
		self.winTitle = "GPS Sort Selection"
		self.winName = "gpsSelectionSortWindow"
		self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
		self.locName = "sortSelection_loc"
		self.grpName = "unsorted"

		# Remove locator from selection
		self.deselectLocator(self.locName)

		# Store original selection
		self.selOrig = mc.ls(selection=True, flatten=True)


	def sortSelection(self):
		"""Re-order the selection list based on various criteria"""

		# Remove locator from selection
		self.deselectLocator(self.locName)

		# Create list from selection, and dictionary for sorting
		sel = mc.ls(selection=True, flatten=True)
		selDic = {}

		# Get options
		mode1 = mc.radioButtonGrp("sortBy1", query=True, select=True)
		mode2 = mc.radioButtonGrp("sortBy2", query=True, select=True)
		mode = mode1 + mode2*10
		rev = mc.checkBox("reverse", query=True, value=True)

		# Check locator exists if in proximity mode
		if mode==20 and not mc.objExists(self.locName):
			mc.error("Create locator before sorting by proximity.")
			#self.createLocator(self.locName)
			return False

		# Construct name to give to new group
		self.grpName = "sortedBy"
		if mode==1:
			self.grpName += "X"
		elif mode==2:
			self.grpName += "Y"
		elif mode==3:
			self.grpName += "Z"
		elif mode==10:
			self.grpName += "Name"
		elif mode==20:
			self.grpName += "Distance"
		if rev:
			self.grpName += "Inv"

		# Populate the selection dictionary based on the sort criteria
		for i in range(len(sel)):
			if mode==1:
				selDic[sel[i]] = (mc.objectCenter(sel[i], x=True))
			elif mode==2:
				selDic[sel[i]] = (mc.objectCenter(sel[i], y=True))
			elif mode==3:
				selDic[sel[i]] = (mc.objectCenter(sel[i], z=True))
			elif mode==10:
				selDic[sel[i]] = sel[i]
			elif mode==20:
				p = mc.objectCenter(sel[i])
				q = mc.xform(self.locName, query=True, translation=True)
				selDic[sel[i]] = gps.distanceBetween(p, q)

		# Sort the dictionary based on the values and save to a new sorted list
		selSorted = sorted(selDic.iteritems(), key=operator.itemgetter(1), reverse=rev)

		# Re-select objects from sorted list
		mc.select(clear=True)
		for selObj in selSorted:
			mc.select(selObj[0], add=True)


	def groupSelection(self, grpName):
		"""Add the selected items to a new group"""

		# Remove locator from selection
		self.deselectLocator(self.locName)

		sel = mc.ls(selection=True, flatten=True)
		mc.group(name=grpName, world=True)
		mc.select(sel, replace=True)


	def createLocator(self, locName):
		"""Create locator used for reordering objects based on proximity"""

		obj = locName + "*"
		if mc.objExists(obj):
			mc.delete(obj)

		mc.spaceLocator(name=locName)


	def deselectLocator(self, locName):
		"""Remove locator from selection list"""

		obj = locName + "*"
		if mc.objExists(obj):
			mc.select(obj, deselect=True)


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
		self.selectionSortUI("sortSelectionOptions", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Sort Selection", command=lambda *args: self.sortSelection())
		mc.button(width=198, height=28, label=resetButtonlabel, command=lambda *args: gps.resetSelection(self.selOrig))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def selectionSortUI(self, name, parent, collapse=False):
		"""Create UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Sort Selection")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(align="left", label="Sort objects in the current selection.")
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.radioButtonGrp("sortBy1", label='Sort by: ', labelArray3=['X-axis', 'Y-axis', 'Z-axis'], numberOfRadioButtons=3, columnWidth4=[140, 78, 78, 78], select=1)
		mc.radioButtonGrp("sortBy2", label='', labelArray2=['Name', 'Proximity to locator'], numberOfRadioButtons=2, columnWidth3=[140, 78, 156], shareCollection="sortBy1")
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("reverse", label="Reverse order", value=0)
		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnOffset1=142)
		mc.columnLayout()
		if collapse: # Only show in-panel sort button if panel was created collapsed
			mc.button(width=116, label="Sort Selection", command=lambda *args: self.sortSelection())
		createLocEnable = not mc.objExists(self.locName) # If locator exists disable create locator button
		mc.button(width=116, label="Create Locator", command=lambda *args: self.createLocator(self.locName), enable=createLocEnable)
		mc.button(width=116, label="New Group", command=lambda *args: self.groupSelection(self.grpName))
		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.setParent(parent)
