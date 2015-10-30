# GPS Extract Faces
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios

import maya.cmds as mc
import maya.mel as mel


class gpsExtractFaces():

	def __init__(self):
		self.winTitle = "GPS Extract Faces"
		self.winName = "gpsExtractFaces"


	def extractFaces(self):
		"""Extract faces"""

		# Get options
		sef = mc.checkBox("sef", query=True, value=True)
		dup = mc.checkBox("dup", query=True, value=True)
		kft = mc.checkBox("kft", query=True, value=True)
		off = mc.floatSliderGrp("off", query=True, value=True)
		ran = mc.floatSliderGrp("ran", query=True, value=True)
		t  = mc.floatFieldGrp("t",  query=True, value=True)
		ro = mc.floatFieldGrp("ro", query=True, value=True)
		s  = mc.floatFieldGrp("s",  query=True, value=True)
		lt = mc.floatFieldGrp("lt", query=True, value=True)
		lr = mc.floatFieldGrp("lr", query=True, value=True)
		ls = mc.floatFieldGrp("ls", query=True, value=True)

		# Perform extraction
		mc.polyChipOff(duplicate=dup, keepFacesTogether=kft, offset=off, random=ran, translate=t, rotate=ro, scale=s, localTranslate=lt, localRotate=lr, localScale=ls)

		# Separate
		if sef:
			mel.eval("SelectToggleMode; performPolyShellSeparate();")


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.extractFacesUI("extractFacesOptions", "windowRoot")
		self.transformUI("transformOptions", "windowRoot", collapse=True)
		self.localTransformUI("localTransformOptions", "windowRoot", collapse=True)
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Extract Faces", command=lambda *args: self.extractFaces())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def extractFacesUI(self, name, parent, collapse=False):
		"""Create extract face options panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("sef", label="Separate extracted faces", value=1)
		mc.setParent(name)
		mc.separator(width=396, height=12, style="in")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("dup", label="Duplicate faces", value=0)
		mc.checkBox("kft", label="Keep faces together", value=0)
		mc.setParent(name)
		mc.floatSliderGrp("off", label="Offset: ", value=0, field=True, precision=3, minValue=-2, maxValue=2, fieldMinValue=-9999, fieldMaxValue=9999)
		mc.floatSliderGrp("ran", label="Randomness: ", value=0, field=True, precision=3, minValue=0, maxValue=1)
		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def transformUI(self, name, parent, collapse=False):
		"""Create transform options panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Transform")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.floatFieldGrp("t", numberOfFields=3, label="Translate: ", value=[0, 0, 0, 0], precision=3)
		mc.floatFieldGrp("ro", numberOfFields=3, label="Rotate: ", value=[0, 0, 0, 0], precision=3)
		mc.floatFieldGrp("s", numberOfFields=3, label="Scale: ", value=[1, 1, 1, 0], precision=3)
		mc.separator(height=8, style="none")
		mc.setParent(parent)


	def localTransformUI(self, name, parent, collapse=False):
		"""Create local transform options panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Local Transform")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.floatFieldGrp("lt", numberOfFields=3, label="Local Translate: ", value=[0, 0, 0, 0], precision=3)
		mc.floatFieldGrp("lr", numberOfFields=3, label="Local Rotate: ", value=[0, 0, 0, 0], precision=3)
		mc.floatFieldGrp("ls", numberOfFields=3, label="Local Scale: ", value=[1, 1, 1, 0], precision=3)
		mc.separator(height=8, style="none")
		mc.setParent(parent)
