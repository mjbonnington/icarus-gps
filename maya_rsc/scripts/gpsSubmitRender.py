# GPS Submit Render
# v0.2
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
# TODO: Add warning if submitting a render and scene has been modified

import os, signal, subprocess
import maya.cmds as mc
import sequence as seq


class gpsSubmitRender():

	def __init__(self):
		self.winTitle = "GPS Submit Render"
		self.winName = "gpsSubmitRenderWindow"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		self.numList = []


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
		mc.button("btnSubmit", width=131, height=28, label="Submit", command=lambda *args: self.submit())
		mc.button("btnKill", width=132, height=28, label="Kill/Complete", command=lambda *args: self.kill())
		mc.button("btnClose", width=131, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		self.tglFrameRange(False)
		mc.showWindow(self.winName)


	def commonOptUI(self, name, parent, collapse=False):
		"""Create common options panel UI controls
		"""
		mc.frameLayout("commonOptRollout", width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Common Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.optionMenuGrp("renamePresets", label="Submit to: ", changeCommand=lambda *args: self.showSpecificOptions())
		mc.menuItem(label="Command-line (local)")
		#for item in self.presetItemList:
		#	mc.menuItem(label=item)
		mc.separator(width=396, height=12, style="in")

		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		mc.checkBox("overrideFrameRange", label="Override frame range", value=0, onCommand=lambda *args: self.tglFrameRange(True), offCommand=lambda *args: self.tglFrameRange(False))
		mc.setParent(name)
		mc.textFieldGrp("frameRange", label="Frame range: ", textChangedCommand=lambda *args: self.validateFrameList(), changeCommand=lambda *args: self.calcFrameList(), annotation="List of frames to be rendered. Individual frames should be separated with commas, and sequences can be specified using a hyphen, e.g. 1, 5-10")
		mc.intSliderGrp("taskSize", label="Task size: ", value=1, field=True, minValue=1, maxValue=10, fieldMinValue=1, fieldMaxValue=10, changeCommand=lambda *args: self.calcFrameList(), annotation="How many frames to submit for each task")
		#mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		#mc.checkBox("skipExistingFrames", label="Skip existing frames", value=0)

		mc.setParent(name)
		mc.separator(height=4, style="none")
		mc.setParent(parent)


	#def specificOptUI(self, name, parent, collapse=False):
	#	"""Create render manager specific options panel UI controls
	#	"""
	#	mc.frameLayout(width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Command-line Specific Options")
	#	mc.columnLayout(name)
	#	mc.separator(height=4, style="none")

	#	mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=142)
	#	mc.button(width=116, label="Full Submitter", command=lambda *args: self.fullSubmitter(), enable=False)

	#	mc.setParent(name)
	#	mc.separator(height=4, style="none")
	#	mc.setParent(parent)


	#def showSpecificOptions(self):
	#	return


	def tglSubmit(self, option):
		mc.button("btnSubmit", edit=True, enable=option)
		mc.button("btnKill", edit=True, enable=option)


	def tglFrameRange(self, option):
		mc.textFieldGrp("frameRange", edit=True, enable=option)
		mc.intSliderGrp("taskSize", edit=True, enable=option)
		if option == False:
			self.resetFrameList()
		else:
			self.calcFrameList()


	def resetFrameList(self):
		"""Get frame range from render globals
		"""
		rgStartFrame = mc.getAttr("defaultRenderGlobals.startFrame")
		rgEndFrame = mc.getAttr("defaultRenderGlobals.endFrame")
		nFrames = rgEndFrame - rgStartFrame + 1
		mc.textFieldGrp("frameRange", edit=True, text="%d-%d" %(rgStartFrame, rgEndFrame))
		mc.intSliderGrp("taskSize", edit=True, value=nFrames, maxValue=nFrames, fieldMaxValue=nFrames)
		self.calcFrameList()


	def validateFrameList(self):
		"""Validate the frame range list in realtime as the text field is edited
		"""
		self.numList = seq.numList(mc.textFieldGrp("frameRange", query=True, text=True), quiet=True)
		if self.numList == False:
			self.tglSubmit(False)
		else:
			self.tglSubmit(True)


	def calcFrameList(self, quiet=True):
		"""Calculate list of frames to be rendered
		"""
		self.numList = seq.numList(mc.textFieldGrp("frameRange", query=True, text=True))
		taskSize = mc.intSliderGrp("taskSize", query=True, value=True)
		if self.numList == False:
			mc.warning("Invalid entry for frame range.")
			self.tglSubmit(False)
		else:
			self.tglSubmit(True)
			mc.textFieldGrp("frameRange", edit=True, text=seq.numRange(self.numList))
			nFrames = len(self.numList)
			if taskSize < nFrames:
				mc.intSliderGrp("taskSize", edit=True, value=taskSize, maxValue=nFrames, fieldMaxValue=nFrames)
			else:
				mc.intSliderGrp("taskSize", edit=True, value=nFrames, maxValue=nFrames, fieldMaxValue=nFrames)

			# Generate task list for rendering
			self.taskList = []
			sequences = list(seq.seqRange(self.numList, gen_range=True))
			for sequence in sequences:
				chunks = list(seq.chunks(sequence, taskSize))
				for chunk in chunks:
					self.taskList.append(list(seq.seqRange(chunk))[0])

			if not quiet:
				print "%d frames to be rendered; %d task(s) to be submitted:" %(len(self.numList), len(self.taskList))
			#print self.numList
			#print self.taskList


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
			os.killpg(self.renderProcess.pid, signal.SIGTERM)
		except (OSError, AttributeError):
			mc.warning("Cannot kill rendering process as there is no render in progress.")

		# Re-enable UI
		mc.button("btnSubmit", edit=True, enable=True)
		mc.frameLayout("commonOptRollout", edit=True, enable=True)


	def submit(self):
		"""Submit render
		"""
		self.calcFrameList(quiet=False)

		try:
			renderCmd = os.environ["MAYARENDERVERSION"]
		except KeyError:
			mc.error("Path to Maya Render command executable not found. This can be set with the environment variable 'MAYARENDERVERSION'.")

		args = "-proj %s" %mc.workspace(query=True, rootDirectory=True)
		farg = ""

		# Additional command-line arguments
		#if mc.checkBox("skipExistingFrames", query=True, value=True):
		#	args = args + " -skipExistingFrames true"

		sceneName = mc.file(query=True, sceneName=True)
		cmdStr = ""

		if self.sceneCheck():

			if mc.checkBox("overrideFrameRange", query=True, value=True):
				for frame in self.taskList:
					farg = "-s %d -e %d" %(frame[0], frame[1])

					cmdStr = cmdStr + "%s %s %s %s; " %(renderCmd, args, farg, sceneName)

			else:
				cmdStr = "%s %s %s" %(renderCmd, args, sceneName)

			print cmdStr
			self.renderProcess = subprocess.Popen(cmdStr, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

			# Disable UI to prevent new renders being submitted
			mc.button("btnSubmit", edit=True, enable=False)
			mc.frameLayout("commonOptRollout", edit=True, enable=False)

		else:
			mc.warning("Scene must be saved before submitting render.")
