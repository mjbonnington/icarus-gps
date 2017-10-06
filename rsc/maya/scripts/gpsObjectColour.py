#!/usr/bin/python

# [GPS] Object Colour
# v0.1
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Sets object wireframe colour and matching outliner colour.


import maya.cmds as mc


class gpsObjectColour():

	def __init__(self):
		self.winTitle = "Object Colour"
		self.winName = "gpsObjectColour"


	def UI(self):
		""" Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title="[GPS] %s" %self.winTitle, sizeable=True, menuBar=True, menuBarVisible=True)

		# Create menu bar
		# mc.menu(label="Edit", tearOff=False)
		# mc.menuItem(label="Reset Settings", command="")
		# mc.menu(label="Help", tearOff=False)
		# mc.menuItem(label="About...", command=lambda *args: self.aboutUI())

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.objectColourUI("objectColourOptions", "windowRoot")

		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Apply", command=lambda *args: self.setObjectColour())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def objectColourUI(self, name, parent, collapse=False):
		""" Create randomise vertices options panel UI controls.
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)

		mc.separator(height=4, style="none")
		mc.colorSliderGrp("colour", label="Colour: ", rgb=(0, 0, 0))
		#mc.colorInputWidgetGrp(label="Colour: ", rgb=(0, 0, 0))
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.checkBox("setOutliner", label="Set Outliner colour to match", value=1)
		mc.setParent(name)

		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def aboutUI(self):
		""" Create about window UI.
		"""
		message = """Object Colour
v0.1

Mike Bonnington <mike.bonnington@gps-ldn.com>
(c) 2017 Gramercy Park Studios

Sets object wireframe colour and matching outliner colour.
"""
		mc.confirmDialog(parent=self.winName, title="About %s" %self.winTitle, message=message, button="OK")


	def setObjectColour(self):
		""" Set object colour.
		"""
		selLs = mc.ls(sl=1)
		for obj in selLs:
			self.setColour(obj)
			shapes = mc.listRelatives(obj, shapes=True, fullPath=True)
			for shape in shapes:
				self.setColour(shape)


	def setColour(self, obj):
		""" Set object colour.
		"""
		# Get options
		col = mc.colorSliderGrp("colour", q=1, rgb=True)
		setOutlinerColour = mc.checkBox("setOutliner", q=1, value=True)

		mc.setAttr(obj+".useObjectColor", 2)  # RGB
		mc.setAttr(obj+".objectColorR", col[0])
		mc.setAttr(obj+".objectColorG", col[1])
		mc.setAttr(obj+".objectColorB", col[2])

		mc.setAttr(obj+".wireColorR", col[0])
		mc.setAttr(obj+".wireColorG", col[1])
		mc.setAttr(obj+".wireColorB", col[2])

		if setOutlinerColour:
			mc.setAttr(obj+".useOutlinerColor", 1)
			mc.setAttr(obj+".outlinerColor", col[0], col[1], col[2])

