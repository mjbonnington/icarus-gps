#!/usr/bin/python

# [renderqueue] submit.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2016-2019
#
# Render Submitter
# A UI for creating render jobs to send to a render queue manager.


import getpass
import os
import re
import sys

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from . import submit_deadline as deadline
from shared import os_wrapper
from shared import sequence

if __name__ == "__main__":
	import argparse

try:
	import maya.cmds as mc
except ImportError:
	pass

try:
	import hou
except ImportError:
	pass

try:
	import nuke
	import nukescripts
except ImportError:
	pass

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

VERSION = "0.2.11"

cfg = {}

# Set window title and object names
cfg['window_object'] = "renderSubmitUI"
if os.environ['RQ_VENDOR_INITIALS']:
	cfg['window_title'] = "%s Render Submitter" % os.environ['RQ_VENDOR_INITIALS']
else:
	cfg['window_title'] = "Render Submitter"

# Set the UI and the stylesheet
cfg['ui_file'] = 'render_submit.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
cfg['prefs_file'] = os.path.join(
	os.environ['RQ_USER_PREFS_DIR'], 'submit_prefs.json')
cfg['store_window_geometry'] = True

# ----------------------------------------------------------------------------
# Begin main window class
# ----------------------------------------------------------------------------

class RenderSubmitUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Render Submit UI.
	"""
	def __init__(self, parent=None):
		super(RenderSubmitUI, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui)

		# Set window icon, flags and other Qt attributes
		if parent == None:
			self.setWindowIcon(self.iconSet('icon_render.png', tintNormal=False))
			self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
			self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
		else:
			self.setWindowFlags(QtCore.Qt.Tool)

		# Set icons
		self.ui.monitor_toolButton.setIcon(self.iconSet('app_icon_deadlinemonitor.png'))
		self.ui.about_toolButton.setIcon(self.iconSet('icon_info.png'))

		self.ui.mayaSceneBrowse_toolButton.setIcon(self.iconSet('folder-open-symbolic.svg'))
		self.ui.houdiniSceneBrowse_toolButton.setIcon(self.iconSet('folder-open-symbolic.svg'))
		self.ui.nukeScriptBrowse_toolButton.setIcon(self.iconSet('folder-open-symbolic.svg'))
		self.ui.commandBrowse_toolButton.setIcon(self.iconSet('folder-open-symbolic.svg'))

		self.ui.getMayaScene_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.getHoudiniScene_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.getNukeScript_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.getCameras_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.getOutputDrivers_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.getPools_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.getGroups_toolButton.setIcon(self.iconSet('icon_refresh.png'))

		self.ui.frameListOptions_toolButton.setIcon(self.iconSet('icon_settings.png'))
		self.ui.layerOptions_toolButton.setIcon(self.iconSet('icon_settings.png'))
		self.ui.writeNodeOptions_toolButton.setIcon(self.iconSet('icon_settings.png'))

		# Connect signals & slots
		self.ui.jobType_comboBox.currentIndexChanged.connect(self.setJobTypeFromComboBox)
		self.ui.monitor_toolButton.clicked.connect(deadline.monitor)
		self.ui.about_toolButton.clicked.connect(self.about)

		self.ui.mayaScene_comboBox.currentIndexChanged.connect(self.applySettings)
		self.ui.mayaScene_comboBox.editTextChanged.connect(self.applySettings)
		self.ui.mayaSceneBrowse_toolButton.clicked.connect(self.sceneBrowse)
		self.ui.getMayaScene_toolButton.clicked.connect(self.getScene)
		self.ui.getCameras_toolButton.clicked.connect(self.getCameras)

		self.ui.houdiniScene_comboBox.currentIndexChanged.connect(self.applySettings)
		self.ui.houdiniScene_comboBox.editTextChanged.connect(self.applySettings)
		self.ui.houdiniSceneBrowse_toolButton.clicked.connect(self.sceneBrowse)
		self.ui.getHoudiniScene_toolButton.clicked.connect(self.getScene)
		self.ui.getOutputDrivers_toolButton.clicked.connect(self.getOutputDrivers)

		self.ui.nukeScript_comboBox.currentIndexChanged.connect(self.applySettings)
		self.ui.nukeScript_comboBox.editTextChanged.connect(self.applySettings)
		self.ui.nukeScriptBrowse_toolButton.clicked.connect(self.sceneBrowse)
		self.ui.getNukeScript_toolButton.clicked.connect(self.getScene)

		self.ui.commandBrowse_toolButton.clicked.connect(self.sceneBrowse)

		self.ui.frames_lineEdit.editingFinished.connect(self.calcFrameList)  # was textChanged
		self.ui.taskSize_spinBox.valueChanged.connect(self.calcFrameList)
		self.ui.getPools_toolButton.clicked.connect(self.getPools)
		self.ui.getGroups_toolButton.clicked.connect(self.getGroups)

		self.ui.submit_pushButton.clicked.connect(self.submit)
		self.ui.close_pushButton.clicked.connect(self.close)

		# Context menus
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Clear (auto-detect frame range)", self.ui.frames_lineEdit.clear)
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Shot default", self.getFrameRangeFromShotSettings)
		if os.environ['RQ_APP'] != "STANDALONE":
			self.addContextMenu(self.ui.frameListOptions_toolButton, "Render settings", self.getFrameRangeFromRenderSettings)
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Sort ascending", self.setFrameListPreset)
		#self.addContextMenu(self.ui.frameListOptions_toolButton, "Sort descending", self.setFrameListPreset)
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Render first and last frames before others", self.setFrameListPreset)

		self.addContextMenu(self.ui.layerOptions_toolButton, "Clear (auto-detect renderable layers)", self.ui.layers_lineEdit.clear)
		self.addContextMenu(self.ui.layerOptions_toolButton, "Current layer only", self.getCurrentRenderLayer)
		self.addContextMenu(self.ui.layerOptions_toolButton, "All renderable layers", self.getRenderLayers)

		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "Clear (all)", self.ui.writeNodes_lineEdit.clear)
		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "Selected write node only", self.getCurrentRenderLayer)
		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "All write nodes", self.getRenderLayers)

		# Set input validators
		layer_list_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w, ]+'), self.ui.layers_lineEdit)
		self.ui.layers_lineEdit.setValidator(layer_list_validator)

		frame_list_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\d\-x, ]+'), self.ui.frames_lineEdit)
		self.ui.frames_lineEdit.setValidator(frame_list_validator)

		# Show initialisation message
		info_ls = []
		for key, value in self.getInfo().items():
			info_ls.append("{} {}".format(key, value))
		info_str = " | ".join(info_ls)
		print("%s v%s\n%s" % (cfg['window_title'], VERSION, info_str))


	def display(self, submitTo=None, jobtype=None, scene=None, frameRange=None, layers=None, safeSubmission=True):
		""" Display the window.
		"""
		self.returnValue = False

		# Set job type from pipeline environment when possible
		if os.environ['RQ_APP'] == "STANDALONE":
			if jobtype:  # Set job type
				self.jobType = jobtype
			else:
				self.jobType = self.ui.jobType_comboBox.currentText()
			self.ui.jobType_comboBox.setCurrentIndex(self.ui.jobType_comboBox.findText(self.jobType))

			if scene:  # For drag-n-drop submissions
				if self.jobType == "Maya":
					self.addSceneEntry(self.ui.mayaScene_comboBox, scene)
				elif self.jobType == "Houdini":
					self.addSceneEntry(self.ui.houdiniScene_comboBox, scene)
				elif self.jobType == "Nuke":
					self.addSceneEntry(self.ui.nukeScript_comboBox, scene)

			# Enable/disable UI elements
			self.ui.getMayaScene_toolButton.hide()
			self.ui.getHoudiniScene_toolButton.hide()
			self.ui.getNukeScript_toolButton.hide()
			self.ui.getCameras_toolButton.setEnabled(False)
			self.ui.layerOptions_toolButton.setEnabled(False)
			self.ui.getOutputDrivers_toolButton.setEnabled(False)
			self.ui.writeNodeOptions_toolButton.setEnabled(False)
			self.setJobType()

		elif os.environ['RQ_APP'] == "MAYA":
			self.jobType = "Maya"
			self.ui.jobType_comboBox.setCurrentIndex(self.ui.jobType_comboBox.findText(self.jobType))
			self.setJobType()

			self.getScene()

			# Enable/disable UI elements
			self.ui.header_frame.hide()
			# self.ui.jobType_label.setEnabled(False)
			# self.ui.jobType_comboBox.setEnabled(False)
			self.ui.mayaScene_comboBox.setEnabled(False)
			#self.toggleFormField(self.ui.maya_groupBox, self.ui.mayaScene_frame, False)
			self.toggleFormField(self.ui.maya_groupBox, self.ui.renderer_frame, False)
			self.ui.mayaSceneBrowse_toolButton.hide()
			self.ui.camera_comboBox.setEditable(False)

			self.getCameras()
			#self.getRenderLayers()
			self.getRenderers()

			if layers:
				self.ui.layers_lineEdit.setText(layers)

		elif os.environ['RQ_APP'] == "HOUDINI":
			self.jobType = "Houdini"
			self.ui.jobType_comboBox.setCurrentIndex(self.ui.jobType_comboBox.findText(self.jobType))
			self.setJobType()

			self.getScene()

			# Enable/disable UI elements
			self.ui.header_frame.hide()
			# self.ui.jobType_label.setEnabled(False)
			# self.ui.jobType_comboBox.setEnabled(False)
			self.ui.houdiniScene_comboBox.setEnabled(False)
			#self.toggleFormField(self.ui.houdini_groupBox, self.ui.houdiniScene_frame, False)
			self.ui.houdiniSceneBrowse_toolButton.hide()

		elif os.environ['RQ_APP'] == "NUKE":
			self.jobType = "Nuke"
			self.ui.jobType_comboBox.setCurrentIndex(self.ui.jobType_comboBox.findText(self.jobType))
			self.setJobType()

			self.getScene()

			# Enable/disable UI elements
			self.ui.header_frame.hide()
			# self.ui.jobType_label.setEnabled(False)
			# self.ui.jobType_comboBox.setEnabled(False)
			self.ui.nukeScript_comboBox.setEnabled(False)
			#self.toggleFormField(self.ui.nuke_groupBox, self.ui.nukeScript_frame, False)
			self.ui.nukeScriptBrowse_toolButton.hide()

			if layers:
				self.ui.writeNodes_lineEdit.setText(layers)

		# Set up frame list
		self.numList = []
		if frameRange:
			self.ui.frames_lineEdit.setText(frameRange)
		else:
			pass
			#self.getFrameRangeFromShotSettings()
		self.calcFrameList()

		self.show()
		self.raise_()

		return self.returnValue


	# @QtCore.Slot()
	def applySettings(self):
		""" Apply the saved submission settings for the chosen scene/script
			file.
			*** TO BE RE-IMPLEMENTED ***
		"""
		if self.jobType == "Maya":
			comboBox = self.ui.mayaScene_comboBox

		elif self.jobType == "Houdini":
			comboBox = self.ui.houdiniScene_comboBox

		elif self.jobType == "Nuke":
			comboBox = self.ui.nukeScript_comboBox

		# Check if scene exists
		scene = comboBox.currentText().replace("\\", "/")

		if os.path.isfile(scene):
			self.ui.submit_pushButton.setToolTip("")
			self.ui.submit_pushButton.setEnabled(True)
		else:
			msg = "The specified file doesn't exist."
			#print("Warning: %s %s" % (msg, scene))
			self.ui.submit_pushButton.setToolTip(msg)
			self.ui.submit_pushButton.setEnabled(False)

		# self.prefs.read_new(common.settings_file(scene, suffix="_submissionData.json"))
		# if self.prefs:
		# 	#print(self.prefs)
		# 	#self.prefs.read()
		# 	self.setupWidgets(self.ui, updateOnly=True)


	# @QtCore.Slot()
	def setJobTypeFromComboBox(self):
		""" Set job type - called when the job type combo box value is
			changed.
		"""
		self.jobType = self.ui.jobType_comboBox.currentText()
		self.setJobType()


	def setJobType(self):
		""" Setup some global variables and UI elements depending on the job
			type.
		"""
		self.ui.generic_groupBox.hide()
		self.ui.maya_groupBox.hide()
		self.ui.houdini_groupBox.hide()
		self.ui.nuke_groupBox.hide()

		if self.jobType == "Generic":
			self.ui.generic_groupBox.show()

		elif self.jobType == "Maya":
			self.ui.maya_groupBox.show()

		elif self.jobType == "Houdini":
			self.ui.houdini_groupBox.show()

		elif self.jobType == "Nuke":
			self.ui.nuke_groupBox.show()


	def sceneBrowse(self):
		""" Browse for a scene/script file.
		"""
		if self.jobType == "Generic":
			comboBox = self.ui.command_comboBox
			fileDir = os.environ.get('RQ_JOBPATH', '.')  # Go to current dir if env var is not set
			fileFilter = "All files (*.*)"

		elif self.jobType == "Maya":
			comboBox = self.ui.mayaScene_comboBox
			fileDir = os.environ.get('RQ_MAYA_SCENES_DIR', '.')  # Go to current dir if env var is not set
			fileFilter = "Maya files (*.ma *.mb)"

		elif self.jobType == "Houdini":
			comboBox = self.ui.houdiniScene_comboBox
			fileDir = os.environ.get('RQ_HOUDINI_SCENES_DIR', '.')  # Go to current dir if env var is not set
			fileFilter = "Houdini files (*.hip)"

		elif self.jobType == "Nuke":
			comboBox = self.ui.nukeScript_comboBox
			fileDir = os.environ.get('RQ_NUKE_SCRIPTS_DIR', '.')  # Go to current dir if env var is not set
			fileFilter = "Nuke files (*.nk)"

		currentDir = os.path.dirname(comboBox.currentText())
		if os.path.exists(currentDir):
			startingDir = currentDir
		else:
			startingDir = fileDir

		filePath = self.fileDialog(startingDir, fileFilter)
		if filePath:
			self.addSceneEntry(comboBox, filePath)


	def addSceneEntry(self, comboBox, filePath):
		""" Add the scene file path as the first entry to the appropriate
			combo box and set it as the current item. If the entry already
			exists in the list, delete it.
		"""
		new_entry = os_wrapper.absolutePath(filePath)
		if os.path.isfile(new_entry):
			comboBox.removeItem(comboBox.findText(new_entry))
			comboBox.insertItem(0, new_entry)
			comboBox.setCurrentIndex(0)
		else:
			comboBox.blockSignals(True)
			comboBox.setEditText(filePath)
			comboBox.blockSignals(False)


	def getFrameRangeFromShotSettings(self):
		""" Get frame range from shot settings.
		"""
		try:
			# Check pipeline environment variables
			start_frame = int(os.environ['RQ_STARTFRAME'])
			end_frame = int(os.environ['RQ_ENDFRAME'])

			frame_range = "%d-%d" % (start_frame, end_frame)
			self.ui.frames_lineEdit.setText(frame_range)

		except KeyError:
			self.ui.frames_lineEdit.setText("")
			print("Warning: Could not get frame range from shot environment.")


	def getFrameRangeFromRenderSettings(self, update_field=True):
		""" Get frame range from DCC app settings.
		"""
		if os.environ['RQ_APP'] == "MAYA":
			start_frame = int(mc.getAttr('defaultRenderGlobals.startFrame'))
			end_frame = int(mc.getAttr('defaultRenderGlobals.endFrame'))

		elif os.environ['RQ_APP'] == "HOUDINI":
			# Attempt to get the frame range from the selected output driver.
			# If no output driver is selected, get the time slider (playbar)
			# range.
			try:
				output_driver = self.ui.outputDriver_comboBox.currentText()
				start_frame = hou.node(output_driver).parm('f1').eval()
				end_frame = hou.node(output_driver).parm('f2').eval()
			except AttributeError:
				start_frame = hou.playbar.playbackRange()[0]
				end_frame = hou.playbar.playbackRange()[1]

		elif os.environ['RQ_APP'] == "NUKE":
			start_frame = nuke.Root()['first_frame'].getValue()
			end_frame = nuke.Root()['last_frame'].getValue()

		frame_range = "%d-%d" % (start_frame, end_frame)
		if update_field:
			self.ui.frames_lineEdit.setText(frame_range)
		else:
			return frame_range


	def getCurrentRenderLayer(self):
		""" Get current Maya render layer or selected Nuke write nodes and
			populate widget.
		"""
		if os.environ['RQ_APP'] == "MAYA":
			currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
			self.ui.layers_lineEdit.setText(currentLayer)

		elif os.environ['RQ_APP'] == "NUKE":
			writeNodeStr = ", ".join(n for n in self.getWriteNodes(selected=True))
			self.ui.writeNodes_lineEdit.setText(writeNodeStr)


	def getRenderLayers(self):
		""" Get Maya render layers or Nuke write nodes and populate widget.
		"""
		if os.environ['RQ_APP'] == "MAYA":
			layerStr = ", ".join(n for n in self.getRenderableLayers())
			self.ui.layers_lineEdit.setText(layerStr)

			# Set Render Setup / Legacy Render Layers option
			checkBox = self.ui.useRenderSetup_checkBox
			checkBox.setChecked(not self.getCheckBoxValue(checkBox))  # Toggle value to force update
			checkBox.setChecked(mc.optionVar(query="renderSetupEnable"))

		elif os.environ['RQ_APP'] == "NUKE":
			writeNodeStr = ", ".join(n for n in self.getWriteNodes(selected=False))
			self.ui.writeNodes_lineEdit.setText(writeNodeStr)


	def getPools(self):
		""" Get Deadline pools and populate combo boxes for primary and
			secondary pools.
		"""
		pools = deadline.get_pools()
		if pools:
			self.populateComboBox(self.ui.pool_comboBox, pools)
			self.populateComboBox(self.ui.pool2_comboBox, pools)


	def getGroups(self):
		""" Get Deadline groups and populate combo box.
		"""
		groups = deadline.get_groups()
		if groups:
			self.populateComboBox(self.ui.group_comboBox, groups)


	def getRenderers(self):
		""" Get Maya renderers and populate combo box.
			***MAYA-SPECIFIC***
		"""
		renderers = self.getRenderer()
		rendererLs = [renderers]
		self.populateComboBox(self.ui.renderer_comboBox, rendererLs)


	def getCameras(self, renderable_only=False):
		""" Return list of cameras in the scene and populate combo box.
			***MAYA-SPECIFIC***
		"""
		no_select_text = ""
		camera_list = [no_select_text, ]

		if os.environ['RQ_APP'] == "MAYA":
			persp_cameras = mc.listCameras(perspective=True)
			ortho_cameras = mc.listCameras(orthographic=True)
			cameras = persp_cameras + ortho_cameras
			for camera in cameras:
				if renderable_only:
					if mc.getAttr(camera+'.renderable'):
						camera_list.append(camera)
				else:
					camera_list.append(camera)

		self.populateComboBox(self.ui.camera_comboBox, camera_list, addEmptyItems=True)


	def getOutputDrivers(self):
		""" Return list of render output drivers in the scene and populate
			combo box.
			***HOUDINI-SPECIFIC***
		"""
		no_select_text = ""
		rop_list = [no_select_text, ]

		if os.environ['RQ_APP'] == "HOUDINI":
			for rop_node in hou.node('/').recursiveGlob('*', hou.nodeTypeFilter.Rop):
				rop_list.append(rop_node.path())

		self.populateComboBox(self.ui.outputDriver_comboBox, rop_list, addEmptyItems=True)


	def getScene(self):
		""" Check if we're working in an unsaved scene, if not get the current
			scene/script file path and populate combo box.
		"""
		if os.environ['RQ_APP'] == "STANDALONE":
			pass  # Do nothing

		elif os.environ['RQ_APP'] == "MAYA":
			scenePath = mc.file(query=True, sceneName=True)
			if scenePath:
				self.addSceneEntry(self.ui.mayaScene_comboBox, scenePath)
				self.ui.submit_pushButton.setEnabled(True)
				# self.setDynamicProperty(self.ui.mayaScene_comboBox, "warning", False)
			else:
				msg = "Please save scene before submitting render."
				mc.warning(msg)
				self.addSceneEntry(self.ui.mayaScene_comboBox, msg)
				self.ui.submit_pushButton.setToolTip(msg)
				self.ui.submit_pushButton.setEnabled(False)
				# self.setDynamicProperty(self.ui.mayaScene_comboBox, "warning", True)

		elif os.environ['RQ_APP'] == "HOUDINI":
			sceneName = hou.hipFile.name()
			scenePath = hou.hipFile.path()
			if sceneName != 'untitled.hip':
				self.addSceneEntry(self.ui.houdiniScene_comboBox, scenePath)
				self.ui.submit_pushButton.setEnabled(True)
				# self.setDynamicProperty(self.ui.houdiniScene_comboBox, "warning", False)
			else:
				msg = "Please save scene before submitting render."
				print("Warning: %s" % msg)
				self.addSceneEntry(self.ui.houdiniScene_comboBox, msg)
				self.ui.submit_pushButton.setToolTip(msg)
				self.ui.submit_pushButton.setEnabled(False)
				# self.setDynamicProperty(self.ui.houdiniScene_comboBox, "warning", True)

		elif os.environ['RQ_APP'] == "NUKE":
			scriptPath = nuke.value('root.name')
			if scriptPath:
				self.addSceneEntry(self.ui.nukeScript_comboBox, scriptPath)
				self.ui.submit_pushButton.setEnabled(True)
				# self.setDynamicProperty(self.ui.nukeScript_comboBox, "warning", False)
			else:
				msg = "Please save script before submitting render."
				#nuke.warning(msg) #nuke.message(msg)
				print("Warning: %s" % msg)
				self.addSceneEntry(self.ui.nukeScript_comboBox, msg)
				self.ui.submit_pushButton.setToolTip(msg)
				self.ui.submit_pushButton.setEnabled(False)
				# self.setDynamicProperty(self.ui.nukeScript_comboBox, "warning", True)


	def getAppVersion(self, app):
		""" Check the specified version of the given app, by processing
			environment variables.
		"""
		if app == 'Maya':
			ver = os.environ['RQ_MAYA_VERSION']

		elif app == 'Houdini':
			ver = os.environ['RQ_HOUDINI_VERSION']

		elif app == 'Nuke':
			ver = os.environ['RQ_NUKE_VERSION']

		return ver


	# @QtCore.Slot()
	def setFrameListPreset(self):
		""" Modify frame list from preset menu.
		"""
		if self.sender().text() == "Sort ascending":
			num_list = sequence.numList(self.ui.frames_lineEdit.text(), sort=True, quiet=True)
			if num_list:
				self.ui.frames_lineEdit.setText(sequence.numRange(num_list))
			else:
				pass

		elif self.sender().text() == "Sort descending":
			pass  # TODO: implement

		elif self.sender().text() == "Render first and last frames before others":
			frames_str = self.ui.frames_lineEdit.text()
			num_list = sequence.numList(frames_str, sort=True, quiet=True)
			if num_list:
				first = min(num_list)
				last = max(num_list)
				frames_str_prefix = "%d, %d" % (first, last)
				if not frames_str.startswith(frames_str_prefix):
					self.ui.frames_lineEdit.setText("%s, %s" % (frames_str_prefix, frames_str))
			else:
				pass


	def calcFrameList(self, quiet=True):
		""" Calculate list of frames to be rendered.
			TODO: perhaps run on a separate thread to keep UI snappy?
		"""
		try:
			self.numList = sequence.numList(self.ui.frames_lineEdit.text(), sort=False, quiet=quiet)
			if self.numList is False:
				#raise RuntimeError("Invalid entry for frame range.")
				if not quiet:
					print("Warning: Invalid entry for frame range.")
				# self.ui.frames_lineEdit.setProperty("mandatoryField", True)
				# self.ui.frames_lineEdit.style().unpolish(self.ui.frames_lineEdit)
				# self.ui.frames_lineEdit.style().polish(self.ui.frames_lineEdit)
				self.numList = []
				self.taskList = ["Unknown", ]

				# msg = "Invalid entry for frame range."
				# #mc.warning(msg)
				# #mc.confirmDialog(title="Scene not saved", message=msg, icon="warning", button="Close")
				# self.ui.submit_pushButton.setToolTip(msg)
				# self.ui.submit_pushButton.setEnabled(False)

				return False

			elif self.numList is None:
				#raise RuntimeError("No frame range specified.")
				if not quiet:
					print("Warning: No frame range specified.")
				# self.ui.frames_lineEdit.setProperty("mandatoryField", True)
				# self.ui.frames_lineEdit.style().unpolish(self.ui.frames_lineEdit)
				# self.ui.frames_lineEdit.style().polish(self.ui.frames_lineEdit)
				self.numList = []
				self.taskList = ["Unknown", ]

				# msg = "No frame range specified."
				# #mc.warning(msg)
				# #mc.confirmDialog(title="Scene not saved", message=msg, icon="warning", button="Close")
				# self.ui.submit_pushButton.setToolTip(msg)
				# self.ui.submit_pushButton.setEnabled(False)

				return False

			else:
				# Update task size slider
				#self.ui.frames_lineEdit.setText(sequence.numRange(self.numList))
				taskSize = self.ui.taskSize_spinBox.value()
				nFrames = len(self.numList)
				if taskSize < nFrames:
					self.ui.taskSize_slider.setMaximum(nFrames)
					self.ui.taskSize_spinBox.setMaximum(nFrames)
					self.ui.taskSize_spinBox.setValue(taskSize)
				else:
					self.ui.taskSize_slider.setMaximum(nFrames)
					self.ui.taskSize_spinBox.setMaximum(nFrames)
					self.ui.taskSize_spinBox.setValue(nFrames)
				if nFrames == 1:
					self.ui.taskSize_slider.setEnabled(False)
					self.ui.taskSize_spinBox.setEnabled(False)
				else:
					self.ui.taskSize_slider.setEnabled(True)
					self.ui.taskSize_spinBox.setEnabled(True)

				# Generate task list for rendering
				self.taskList = []
				sequences = list(sequence.seqRange(self.numList, gen_range=True))
				for seq in sequences:
					chunks = list(sequence.chunks(seq, taskSize))
					for chunk in chunks:
						#self.taskList.append(list(sequence.seqRange(chunk))[0])
						self.taskList.append(sequence.numRange(chunk))

				return True

		except (MemoryError, OverflowError):
			print("Warning: Specified frame range value(s) too large to process.")
			return False

		# except RuntimeError:
		# 	if not quiet:
		# 		print("Warning: Invalid entry for frame range.")
		# 	# self.ui.frames_lineEdit.setProperty("mandatoryField", True)
		# 	# self.ui.frames_lineEdit.style().unpolish(self.ui.frames_lineEdit)
		# 	# self.ui.frames_lineEdit.style().polish(self.ui.frames_lineEdit)
		# 	self.numList = []
		# 	self.taskList = ["Unknown", ]
		# 	return False

		# finally:
		# 	pass


	def getMayaProject(self, scene_path=None):
		""" Get the Maya project. First try to query the Maya workspace
			command. If that fails, try the pipeline environment variable.
			Finally, attempt to guess the Maya project directory based on the
			scene name.
		"""
		try:
			maya_project = mc.workspace(q=True, active=True)
		except NameError:
			try:  # Project is implicit if job is set
				maya_project = os.environ['RQ_MAYA_PROJECT_DIR']
			except KeyError:
				try:  # Make a guess
					scene_path = scene_path.replace("\\", "/")
					maya_project = scene_path.split('/scenes')[0]
				except AttributeError:
					print("Warning: Failed to get Maya project directory.")
					maya_project = ""

		return maya_project.replace("\\", "/")


	def getRenderer(self):
		""" Get the current Maya renderer.
			***MAYA-SPECIFIC***
		"""
		try:
			renderer = mc.getAttr("defaultRenderGlobals.currentRenderer")
		except:
			renderer = ""

		return renderer


	def getRenderableLayers(self, allLayers=False):
		""" Get Maya render layers that are enabled (renderable).
			If 'allLayers' is True, return all (not just renderable) layers.
			***MAYA-SPECIFIC***
		"""
		layers = mc.ls(type='renderLayer')

		if(allLayers):
			return layers

		else:
			renderableLayers = []
			for layer in layers:
				if mc.getAttr(layer+'.renderable'):
					renderableLayers.append(layer)

			return renderableLayers


	def getWriteNodes(self, selected=True):
		""" Get Nuke write nodes.
			If 'selected' is True, only return selected nodes.
			NUKE-SPECIFIC
		"""
		writeNodes = []

		if selected:
			nodeLs = nuke.selectedNodes('Write')
		else:
			nodeLs = nuke.allNodes('Write')

		for node in nodeLs:
			writeNodes.append(node.name())

		return writeNodes


	def getMayaRenderOutput(self, layer=None):
		""" Get the path of Maya's render output.
			***MAYA-SPECIFIC***
		"""
		try:
			padding = "#" * mc.getAttr("defaultRenderGlobals.extensionPadding")
			if layer is None:
				path = mc.renderSettings(fullPath=True, 
					leaveUnmatchedTokens=True, genericFrameImageName=padding)
			else:
				path = mc.renderSettings(fullPath=True, layer=layer, 
					leaveUnmatchedTokens=True, genericFrameImageName=padding)
		except:
			path = [""]

		# Quick hack to get correct file type extension to work around VRay's
		# inconsistency...
		if self.getRenderer() == 'vray':
			new_file_ext = mc.getAttr("vraySettings.imageFormatStr")
			path[0] = "%s.%s" % (os.path.splitext(path[0])[0], new_file_ext)

		return path[0]


	def getHoudiniRenderOutput(self, output_driver):
		""" Get the output path from a Houdini ROP.
			***HOUDINI-SPECIFIC***
		"""
		try:
			#path = hou.node(output_driver).parm('vm_picture').unexpandedString()  # Gets the unprocessed output file path string
			path = hou.node(output_driver).parm('vm_picture').eval()  # Evaluates the path as an expression
			path = os_wrapper.absolutePath(path)  # Expand env vars
			path = self.replacePadding(path)

		except AttributeError:
			path = ""

		return path


	def getNukeRenderOutput(self, write_node):
		""" Get the output path from a Nuke write node.
			***NUKE-SPECIFIC***
		"""
		node = nuke.toNode(write_node)

		try:
			#path = node.knob('file').value()  # Gets the unprocessed output file path string
			path = node.knob('file').evaluate()  # Evaluates the path as a Nuke TCL expression
			#path = os_wrapper.absolutePath(node.knob('file'))  # Preserves padding but doesn't expand environment variables
			path = self.replacePadding(path)

		except:
			path = ""

		return path


	def replacePadding(self, path, padding=4):
		""" Replace the frame number in a path with hashes so that Deadline
			can link to the correct output filename for a given frame/task.
			4-digit padding is assumed.
		"""
		hashes = "#" * padding
		basepath, ext = os.path.splitext(path)
		new_path = re.sub(r"\d*$", hashes, basepath) + ext
		return new_path


	def getMayaOutputFilePath(self, scene_path=None):
		""" Get Maya's render output file path from the Maya project.
			***MAYA-SPECIFIC***
		"""
		try:
			path = mc.workspace(expandName=mc.workspace(fileRuleEntry="images"))
		except NameError:  # Make a guess
			path = os.path.join(self.getMayaProject(scene_path), "renders")

		return path


	def getOutputFilePrefix(self, renderer):
		""" Get Maya's output file prefix from the render settings.
			***MAYA-SPECIFIC***
		"""
		if renderer == 'vray':
			try:
				prefix = mc.getAttr("vraySettings.fileNamePrefix")
			except:  # Make a guess
				prefix = os.environ['RQ_MAYA_OUTPUT_FORMAT_VRAY']

		else:
			try:
				prefix = mc.getAttr("defaultRenderGlobals.imageFilePrefix")
			except:  # Make a guess
				prefix = os.environ['RQ_MAYA_OUTPUT_FORMAT']

		return prefix


	def getAOVs(self, renderer):
		""" Get AOVs from Maya depending on renderer.
			Currently returns all AOVs, regardless of whether they are
			individually enabled or not. This is because the only way to test
			this per render layer is to actually change to each render layer
			in turn and check their status. This is a pain and amounts to a
			modification of the scene which is undesirable for all kinds of
			reasons.
			***MAYA-SPECIFIC***
		"""
		# Default beauty pass will always be added to the start of the list
		aov_name_ls = ["beauty"]

		if renderer == "arnold":
			for aov_node in mc.ls(type="aiAOV"):
				#if mc.getAttr("%s.enabled" % aov_node):
				aov_name_ls.append(mc.getAttr("%s.name" % aov_node))

		elif renderer == "redshift":
			# Only if global AOV mode is enabled
			if mc.getAttr("redshiftOptions.aovGlobalEnableMode") == 1:
				for aov_node in mc.ls(type="RedshiftAOV"):
					#if mc.getAttr("%s.enabled" % aov_node):
					aov_name_ls.append(mc.getAttr("%s.name" % aov_node))

		elif renderer == "vray":
			#aov_name_ls[0] = ""  # Empty name for beauty pass
			for aov_node in mc.ls(type="VRayRenderElement"):
				# Read all attributes and find name attribute, because VRay
				# uses a different name for the name attribute depending on
				# the type of element, just to be difficult...
				#if mc.getAttr("%s.enabled" % aov_node):
				for attr in mc.listAttr(aov_node):
					if attr.startswith("vray_name_"):
						aov_name_ls.append(mc.getAttr("%s.%s" % (aov_node, attr)))

		# elif renderer == "mentalRay":
		# 	# Get the current render layer
		# 	current_layer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
		# 	for aov_node in mc.ls(type="renderPass"):
		# 		# Only add to list if render pass is connected to current
		# 		# render layer and is renderable
		# 		associated_layers = mc.listConnections("%s.owner" % aov_node)
		# 		if associated_layers is not None:
		# 			if current_layer in associated_layers:
		# 				if mc.getAttr("%s.renderable" % aov_node):
		# 					aov_name_ls.append(aov_node)

		# Return list
		return aov_name_ls


	def getOutputs(self):
		""" Get the file output(s) from a render. Return as a dictionary with
			the render layer / write node name as the key, and the value as a
			tuple containing the dirname and basename.
		"""
		outputs = {}

		if os.environ['RQ_APP'] == "MAYA":
			for entry in self.getRenderableLayers(allLayers=False):
				output = self.getMayaRenderOutput(entry)
				if self.getRenderer() != "vray":
					output = output.replace("<RenderPass>", "beauty")
				outputs[entry] = os.path.split(output)

		elif os.environ['RQ_APP'] == "HOUDINI":
			output_driver = self.ui.outputDriver_comboBox.currentText()
			output = self.getHoudiniRenderOutput(output_driver)
			outputs['main'] = os.path.split(output)
			# print(output)

		elif os.environ['RQ_APP'] == "NUKE":
			for entry in self.getWriteNodes(selected=False):
				outputs[entry] = os.path.split(self.getNukeRenderOutput(entry))

		return outputs


	# def guessOutputs(self, path, prefix, scene=None, camera=None, layers=[], useRenderSetup=False):
	# 	""" Parse Maya's output file prefix and return a full path.
	# 		This is all a bit hacky right now.
	# 	"""
	# 	outputs = {}
	# 	print(layers)

	# 	for layer in layers:
	# 		prefix2 = prefix

	# 		if useRenderSetup:
	# 			if layer.startswith('rs_'):
	# 				layer2 = layer.replace('rs_', '', 1)
	# 		else:
	# 			layer2 = layer

	# 		# Replace tokens...
	# 		if scene:
	# 			prefix2 = prefix2.replace('<Scene>', scene)
	# 		if layer2:
	# 			prefix2 = prefix2.replace('<RenderLayer>', layer2)
	# 			prefix2 = prefix2.replace('<Layer>', layer2)
	# 		if camera:
	# 			prefix2 = prefix2.replace('<Camera>', camera)

	# 		filepath = os_wrapper.absolutePath("%s/%s.####.exr" % (path, prefix2))
	# 		outputs[layer] = os.path.split(filepath)

	# 	return outputs


	def getJobName(self, scene_path):
		""" Return a string for the job name based on the job/scene/script
			name.
		"""
		scene_base = os.path.basename(scene_path)
		try:
			job = os.environ['RQ_JOB']
			job_name = "%s | %s" % (job, scene_base)
		except KeyError:
			job_name = scene_base

		return job_name


	def saveScene(self):
		""" Save the current scene/script if it has been modified.
		"""
		if os.environ['RQ_APP'] == "STANDALONE":
			pass  # Do nothing

		elif os.environ['RQ_APP'] == "MAYA":
			# Check if scene is modified before saving, as Maya scene files
			# can be quite large and saving can be slow.
			if mc.file(q=True, modified=True):
				mc.file(save=True)

		elif os.environ['RQ_APP'] == "HOUDINI":
			hou.hipFile.save()

		elif os.environ['RQ_APP'] == "NUKE":
			nuke.scriptSave()


	# def incrementScene(self):
	# 	""" Increment the minor version number. For Maya, don't save as this
	# 		can be slow for large scenes. Instead copy the previous scene
	# 		file via the OS.
	# 	"""
	# 	if os.environ['RQ_APP'] == "STANDALONE":
	# 		pass  # Do nothing

	# 	elif os.environ['RQ_APP'] == "MAYA":
	# 		# As the scene will have just been saved, we create a copy of the
	# 		# scene and increment the minor version, and point the Maya file
	# 		# to the updated scene file. This gives us a performance gain by
	# 		# avoiding the overhead of a second save operation, which can be
	# 		# slow for large Maya ASCII scenes.
	# 		current_scene = mc.file(query=True, expandName=True)
	# 		ext = os.path.splitext(current_scene)[1]
	# 		updated_scene = session.scnmgr.convention.version_up()
	# 		if updated_scene:
	# 			updated_scene += ext
	# 			os_wrapper.copy(current_scene, updated_scene)
	# 			mc.file(rename=updated_scene)
	# 			# self.addSceneEntry(self.ui.mayaScene_comboBox, updated_scene)
	# 			self.getScene()

	# 	elif os.environ['RQ_APP'] == "HOUDINI":
	# 		if session.scnmgr.convention.version_up():
	# 			self.getScene()

	# 	elif os.environ['RQ_APP'] == "NUKE":
	# 		if session.scnmgr.convention.version_up():
	# 			self.getScene()


	def about(self):
		""" Show about dialog.
		"""
		from . import about

		info_ls = []
		sep = " | "
		for key, value in self.getInfo().items():
			if key in ['Environment', 'OS']:
				pass
			else:
				info_ls.append("{} {}".format(key, value))
		info_str = sep.join(info_ls)

		about_msg = """
%s
v%s

A unified tool for submitting render jobs to a render queue manager.

Developer: Mike Bonnington
(c) 2016-2019

%s
""" % (cfg['window_title'], VERSION, info_str)

		aboutDialog = about.AboutDialog(parent=self)
		aboutDialog.display(
			bg_color=QtGui.QColor('#5b6368'), 
			icon_pixmap=self.iconTint(
				'icon_render.png', 
				tint=QtGui.QColor('#6e777d')), 
			message=about_msg)


	def submit(self):
		""" Submit job.
		"""
		self.save()  # Save dialog settings

		submit_args = self.getSubmissionOptions()
		if submit_args:

			# Generate confirmation message(s)
			if submit_args['frames']:
				frames_msg = ""
			else:
				if os.environ['RQ_APP'] == "STANDALONE":
					submit_args['frames'] = "Unknown"
					frames_msg = "Warning: No frame range specified.\n"
				else:
					submit_args['frames'] = self.getFrameRangeFromRenderSettings(update_field=False)
					frames_msg = ""

			job_info_msg = "%s\n\nType: %s (%s)\nFrames: %s\nTask size: %s\nPriority: %s\n" % (submit_args['jobName'], self.jobType, submit_args['version'], submit_args['frames'], submit_args['taskSize'], submit_args['priority'])

			# Show confirmation dialog
			dialog_title = "Submit to Deadline"
			dialog_msg = job_info_msg + "\n" + frames_msg + "Do you want to continue?"
			if self.promptDialog(dialog_msg, title=dialog_title):

				# Save scene/script if submitting from DCC app
				self.saveScene()

				# Actually submit the job
				result, result_msg = deadline.submit_job(**submit_args)

				# Version up if successfully submitted from DCC app
				# if result:
				# 	self.incrementScene()

				# Show post-confirmation dialog
				dialog_title = "Submission Results"
				dialog_msg = job_info_msg + "\n" + result_msg
				self.promptDialog(dialog_msg, title=dialog_title, conf=True)


	def getSubmissionOptions(self):
		""" Get all values from UI widgets and return them as a dictionary.
		"""
		submit_args = {}

		##################
		# Common options #
		##################

		submit_args['frames'] = self.ui.frames_lineEdit.text()
		submit_args['taskSize'] = self.ui.taskSize_spinBox.value()
		submit_args['priority'] = self.ui.priority_spinBox.value()
		submit_args['pool'] = self.ui.pool_comboBox.currentText()
		submit_args['secondaryPool'] = self.ui.pool2_comboBox.currentText()
		submit_args['group'] = self.ui.group_comboBox.currentText()
		submit_args['comment'] = self.ui.comment_lineEdit.text()
		submit_args['username'] = os.environ.get('RQ_USER', getpass.getuser())
		submit_args['submitter'] = "Submitted with %s v%s" % (cfg['window_title'], VERSION)

		# Environment variables...
		envVarKeys = []
		envVarKeys.append('IC_JOBPATH')
		envVarKeys.append('IC_SHOTPATH')

		################################
		# Application-specific options #
		################################

		# Maya ---------------------------------------------------------------
		if self.jobType == "Maya":
			submit_args['plugin'] = "MayaBatch"
			submit_args['version'] = self.getAppVersion(self.jobType)
			submit_args['camera'] = self.ui.camera_comboBox.currentText()
			submit_args['renderLayers'] = self.ui.layers_lineEdit.text()
			submit_args['renderer'] = self.ui.renderer_comboBox.currentText()
			submit_args['useRenderSetup'] = self.getCheckBoxValue(self.ui.useRenderSetup_checkBox)

			scene = self.ui.mayaScene_comboBox.currentText().replace("\\", "/")
			submit_args['scene'] = scene
			submit_args['jobName'] = self.getJobName(scene)
			submit_args['mayaProject'] = self.getMayaProject(scene)
			submit_args['outputFilePath'] = self.getMayaOutputFilePath(scene)
			submit_args['outputFilePrefix'] = self.getOutputFilePrefix(submit_args['renderer'])

			# File output location(s)...
			if os.environ['RQ_APP'] == "STANDALONE":
				pass
				# submit_args['output'] = self.guessOutputs(self.jobType, **submit_args)
			else:
				submit_args['output'] = self.getOutputs()

			# Environment variables...
			for key in os.environ.keys():
				if key.upper().startswith('IC_MAYA'):
					envVarKeys.append(key)
			if submit_args['renderer'] == "redshift":
				envVarKeys.append('REDSHIFT_COREDATAPATH')

		# Houdini ------------------------------------------------------------
		elif self.jobType == "Houdini":
			submit_args['plugin'] = "Houdini"
			submit_args['version'] = self.getAppVersion(self.jobType)
			submit_args['outputDriver'] = self.ui.outputDriver_comboBox.currentText()
			submit_args['renderLayers'] = None  # Use renderLayers for takes?

			scene = self.ui.houdiniScene_comboBox.currentText().replace("\\", "/")
			submit_args['scene'] = scene
			submit_args['jobName'] = self.getJobName(scene)

			# File output location(s)...
			if os.environ['RQ_APP'] == "STANDALONE":
				pass
				# submit_args['output'] = self.guessOutputs(self.jobType, **submit_args)
			else:
				submit_args['output'] = self.getOutputs()

			# Environment variables...
			for key in os.environ.keys():
				if key.upper().startswith('IC_HOUDINI'):
					envVarKeys.append(key)

		# Nuke ---------------------------------------------------------------
		elif self.jobType == "Nuke":
			submit_args['plugin'] = "Nuke"
			submit_args['version'] = self.getAppVersion(self.jobType)
			submit_args['renderLayers'] = self.ui.writeNodes_lineEdit.text()  # Use renderLayers for writeNodes
			submit_args['isMovie'] = self.getCheckBoxValue(self.ui.isMovie_checkBox)
			if submit_args['isMovie']:  # Override task size if output is movie
				submit_args['taskSize'] = len(self.numList)
			submit_args['nukeX'] = self.getCheckBoxValue(self.ui.useNukeX_checkBox)
			submit_args['interactiveLicense'] = self.getCheckBoxValue(self.ui.interactiveLicense_checkBox)

			scene = self.ui.nukeScript_comboBox.currentText().replace("\\", "/")
			submit_args['scene'] = scene
			submit_args['jobName'] = self.getJobName(scene)

			# File output location(s)...
			if os.environ['RQ_APP'] == "STANDALONE":
				pass
				# submit_args['output'] = self.guessOutputs(self.jobType, **submit_args)
			else:
				submit_args['output'] = self.getOutputs()

			# Environment variables...
			# (exporting the entire pipeline env works best in this case)
			for key in os.environ.keys():
				# if 'NUKE' in key.upper():
				# 	envVarKeys.append(key)
				envVarKeys.append('NUKE_PATH')
				if key.upper().startswith('IC'):
					envVarKeys.append(key)

		# Remove duplicate env var keys
		submit_args['envVars'] = list(set(envVarKeys))

		return submit_args


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main window class
# ============================================================================
# Run functions
# ----------------------------------------------------------------------------

def run_maya(session, **kwargs):
	""" Run in Maya.
	"""
	try:  # Show the UI
		session.renderSubmitUI.display(**kwargs)
	except:  # Create the UI
		UI._maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.renderSubmitUI = RenderSubmitUI(parent=UI._maya_main_window())
		session.renderSubmitUI.display(**kwargs)


def run_houdini(session, **kwargs):
	""" Run in Houdini.
	"""
	try:  # Show the UI
		session.renderSubmitUI.display(**kwargs)
	except:  # Create the UI
		#UI._houdini_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		#session = UI._houdini_get_session()
		session.renderSubmitUI = RenderSubmitUI(parent=UI._houdini_main_window())
		session.renderSubmitUI.display(**kwargs)


def run_nuke(session, **kwargs):
	""" Run in Nuke.
	"""
	try:  # Show the UI
		session.renderSubmitUI.display(**kwargs)
	except:  # Create the UI
		UI._nuke_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.renderSubmitUI = RenderSubmitUI(parent=UI._nuke_main_window())
		session.renderSubmitUI.display(**kwargs)


# Run as standalone app
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# Set up and parse command-line arguments
	parser = argparse.ArgumentParser(description="Submit a scene or script file to the render farm")
	parser.add_argument('file', nargs='*', help="The filename of the scene or script to be submitted.")
	args = parser.parse_args()

	clargs = {}
	if args.file:
		fname = os.path.abspath(args.file[0])
		if os.path.isfile(fname):
			clargs['scene'] = fname
			filetype = os.path.splitext(fname)[1]
			if filetype in ['.ma', '.mb']:
				clargs['jobtype'] = 'Maya'
			if filetype in ['.hip']:
				clargs['jobtype'] = 'Houdini'
			if filetype in ['.nk']:
				clargs['jobtype'] = 'Nuke'
		else:
			print("Warning: File doesn't exist: %s" % fname)

	# Instantiate main application class
	rsApp = RenderSubmitUI()

	# Show the application UI
	rsApp.display(**clargs)

	sys.exit(app.exec_())
