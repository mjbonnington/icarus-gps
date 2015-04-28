# GPS Submit Render
# v0.15
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Front end for submitting command-line and distributed renders from within Maya
#
# TODO: Allow Render executable path to be set if relevant env var is not set
# TODO: skipExistingFrames flag not working
# TODO: Batch rendering sometimes exits after rendering only one frame
# TODO: Add support for Deadline and Smedge submission

import os, signal, subprocess
import maya.cmds as mc


class gpsSubmitRender():

	def __init__(self):
		self.winTitle = "GPS Submit Render"
		self.winName = "gpsSubmitRenderWindow"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.commonOptUI("commonOptPanel", "windowRoot")
		#self.specificOptUI("specificOptPanel", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=3)
		mc.button(width=131, height=28, label="Submit", command=lambda *args: self.submit())
		mc.button(width=131, height=28, label="Kill", command=lambda *args: self.kill())
		mc.button(width=131, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def commonOptUI(self, name, parent, collapse=False):
		"""Create common options panel UI controls
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Common Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.optionMenuGrp("renamePresets", label="Submit to: ", changeCommand=lambda *args: self.showSpecificOptions())
		mc.menuItem(label="Command-line (local)")
		#for item in self.presetItemList:
		#	mc.menuItem(label=item)
		mc.separator(width=396, height=12, style="in")

		rgStartFrame = mc.getAttr("defaultRenderGlobals.startFrame")
		rgEndFrame = mc.getAttr("defaultRenderGlobals.endFrame")
		nFrames = rgEndFrame - rgStartFrame + 1

		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		mc.checkBox("overrideFrameRange", label="Override frame range", value=0, onCommand=lambda *args: self.tglFrameRange(True), offCommand=lambda *args: self.tglFrameRange(False))
		mc.setParent(name)
		mc.intFieldGrp("startFrame", label="Start frame: ", value1=rgStartFrame, enable=False)
		mc.intFieldGrp("endFrame", label="End frame: ", value1=rgEndFrame, enable=False)
		#mc.textFieldGrp("frameRange", label="Frame range: ")
		mc.intSliderGrp("taskSize", label="Task size: ", value=nFrames, field=True, minValue=1, maxValue=nFrames, fieldMinValue=1, fieldMaxValue=nFrames, enable=False)
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		mc.checkBox("skipExistingFrames", label="Skip existing frames", value=0, enable=False)

		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.setParent(parent)


	def specificOptUI(self, name, parent, collapse=False):
		"""Create render manager specific options panel UI controls
		"""
		mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Command-line Specific Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
		mc.button(width=116, label="Full Submitter", command=lambda *args: self.renumber(), enable=False)
		mc.setParent(name)

		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		mc.setParent(name)

		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.setParent(parent)


	def showSpecificOptions(self):
		return


	def tglFrameRange(self, option):
		mc.intFieldGrp("startFrame", edit=True, enable=option)
		mc.intFieldGrp("endFrame", edit=True, enable=option)


	def sceneCheck(self):
		"""Return True if the scene has been saved
		"""
		if mc.file(query=True, sceneName=True): # and not mc.file(query=True, modified=True):
			return True
		else:
			return False


	def kill(self):
		"""Kill the rendering process
		"""
		try:
			#self.renderProcess.kill()
			os.killpg(self.renderProcess.pid, signal.SIGTERM)
		except (OSError, AttributeError):
			mc.warning("Cannot kill rendering process as there is no render in progress.")


	def submit(self):
		"""Submit render
		"""
		try:
			renderCmd = os.environ["MAYARENDERVERSION"]
		except KeyError:
			mc.error("Path to Maya Render command executable not found. This can be set with the environment variable 'MAYARENDERVERSION'.")

		args = "-proj %s" %mc.workspace(query=True, rootDirectory=True)
		if mc.checkBox("overrideFrameRange", query=True, value=True):
			args = args + " -s %d" %mc.intFieldGrp("startFrame", query=True, value1=True)
			args = args + " -e %d" %mc.intFieldGrp("endFrame", query=True, value1=True)
		if mc.checkBox("skipExistingFrames", query=True, value=True):
			args = args + " -skipExistingFrames true"

		sceneName = mc.file(query=True, sceneName=True)

		if self.sceneCheck():
			cmdStr = "%s %s %s" %(renderCmd, args, sceneName)
			print cmdStr
			print "Starting render..."
			#os.system(cmdStr)
			self.renderProcess = subprocess.Popen(cmdStr, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
		else:
			mc.warning("Scene must be saved before submitting render.")
