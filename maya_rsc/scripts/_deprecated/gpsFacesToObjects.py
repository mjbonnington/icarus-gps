# GPS Faces to Objects
# v0.1
#
# Michael Bonnington 2014
# Gramercy Park Studios

import maya.cmds as mc


class gpsFacesToObjects():

	def __init__(self):
		self.winTitle = "GPS Faces to Objects"
		self.winName = "gpsFacesToObjectsWindow"


	def facesToObjects(self):
		history = mc.checkBox("history", query=True, value=True)
		keepOrig = mc.checkBox("keepOrig", query=True, value=True)

		objLs = mc.ls(selection=True)
		obj = objLs[0]

		# Check only one object is selected
		if not len(objLs) == 1:
			mc.error("More than one object selected.")
		else:
			# Check selection is poly mesh
			if not self.isMesh(obj):
				mc.error(obj + " is not a mesh.")
			else:
				groupName = "%s_faces" %(obj)
				faceName = "%s_face0" %(str(obj))
				if keepOrig:
					newName = mc.duplicate(obj, rr=True, name=groupName)
				else:
					newName = mc.rename(obj, groupName)
				mc.polyChipOff(newName, duplicate=False, keepFacesTogether=False)
				mc.polySeparate(newName, constructionHistory=history, name=faceName)


	def isMesh(self, obj):
		if mc.nodeType(obj) == "transform":
			shapeLs = mc.listRelatives(obj, shapes=True)
			if shapeLs == None:
				return False
			else:
				if mc.nodeType(shapeLs[0]) == "mesh":
					return True
				else:
					return False


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.facesToObjectsUI("facesToObjectsOptions", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button(width=198, height=28, label="Convert Faces to Objects", command=lambda *args: self.facesToObjects())
		mc.button(width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def facesToObjectsUI(self, name, parent, collapse=False):
		"""Create faces to objects panel UI controls"""

		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
		mc.text(label="Convert the currently selected object's faces to new objects.", wordWrap=True, align="left", width=392)
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.columnLayout()
		mc.checkBox("history", label="Keep construction history", value=0)
		mc.checkBox("keepOrig", label="Keep original object(s)", value=0)
		mc.setParent(name)
		mc.separator(height=8, style="none")
		mc.setParent(parent)
