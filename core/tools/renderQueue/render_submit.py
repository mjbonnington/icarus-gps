#!/usr/bin/python

# [Icarus] render_submit.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Batch Render Submitter
# A UI for creating render jobs to send to a render queue manager.


import os
# import subprocess
# import sys
import time

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import osOps
import pDialog
import render_submit_deadline as deadline
import renderQueue
import sequence
# import settingsData
import userPrefs
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Render Submit"
WINDOW_OBJECT = "renderSubmitUI"

# Set the UI and the stylesheet
UI_FILE = "render_submit_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True

# Prevent spawned processes from opening a shell window
# CREATE_NO_WINDOW = 0x08000000


# ----------------------------------------------------------------------------
# Main window class
# ----------------------------------------------------------------------------

class RenderSubmitUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Render submit UI.
	"""
	def __init__(self, parent=None):
		super(RenderSubmitUI, self).__init__(parent)
		self.parent = parent

		xml_data = os.path.join(os.environ['IC_USERPREFS'], 'renderSubmit.xml')

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             xml_data=xml_data, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Set other Qt attributes
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Set up keyboard shortcuts
		self.shortcutExpertMode = QtWidgets.QShortcut(self)
		self.shortcutExpertMode.setKey('Ctrl+E')
		self.shortcutExpertMode.activated.connect(self.toggleExpertMode)

		# Connect signals & slots
		self.ui.submitTo_comboBox.currentIndexChanged.connect(self.setQueueManagerFromComboBox)
		self.ui.type_comboBox.currentIndexChanged.connect(self.setJobTypeFromComboBox)
		self.ui.scene_comboBox.currentIndexChanged.connect(self.applySettings)
		self.ui.sceneBrowse_toolButton.clicked.connect(self.sceneBrowse)

		# self.ui.layers_groupBox.toggled.connect(self.getRenderLayers)
		# self.ui.layers_lineEdit.editingFinished.connect(self.checkRenderLayers)

		# self.setupWidgets(self.ui.submitOptions_scrollAreaWidgetContents)
		# self.ui.renderer_comboBox.currentIndexChanged.connect(self.storeComboBoxValue)
		# self.ui.layers_lineEdit.textEdited.connect(self.storeLineEditValue)

		#self.ui.frames_lineEdit.editingFinished.connect(self.calcFrameList)
		self.ui.frames_lineEdit.textChanged.connect(self.calcFrameList)
		self.ui.taskSize_spinBox.valueChanged.connect(self.calcFrameList)

		# # self.ui.pool_comboBox.currentIndexChanged.connect(self.storeComboBoxValue)
		# # self.ui.group_comboBox.currentIndexChanged.connect(self.storeComboBoxValue)
		# self.ui.pool_comboBox.editTextChanged.connect(self.storeComboBoxValue)
		# self.ui.group_comboBox.editTextChanged.connect(self.storeComboBoxValue)
		self.ui.getPools_toolButton.clicked.connect(self.getPools)
		self.ui.getGroups_toolButton.clicked.connect(self.getGroups)
		# self.ui.priority_spinBox.valueChanged.connect(self.storeSpinBoxValue)
		# self.ui.comment_lineEdit.textEdited.connect(self.storeLineEditValue)

		self.ui.submit_pushButton.clicked.connect(self.submit)
		self.ui.close_pushButton.clicked.connect(self.close)
		#self.ui.close_pushButton.clicked.connect(self.saveAndExit)

		# Context menus
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Shot default", self.getFrameRangeFromShotSettings)
		if os.environ['IC_ENV'] != "STANDALONE":
			self.addContextMenu(self.ui.frameListOptions_toolButton, "Render settings", self.getFrameRangeFromRenderSettings)
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Sequential", self.setFrameListPreset)  #placeholder
		#self.addContextMenu(self.ui.frameListOptions_toolButton, "Reverse order", self.setFrameListPreset)  #placeholder
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Render first and last frames before others", self.setFrameListPreset)  #placeholder

		#self.addContextMenu(self.ui.layerOptions_toolButton, "Clear", self.clearRenderLayers)
		self.addContextMenu(self.ui.layerOptions_toolButton, "Current layer only", self.getCurrentRenderLayer)
		self.addContextMenu(self.ui.layerOptions_toolButton, "All renderable layers", self.getRenderLayers)

		#self.addContextMenu(self.ui.layerOptions_toolButton, "Clear", self.clearRenderLayers)
		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "Selected write node only", self.getCurrentRenderLayer)  #placeholder
		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "All write nodes", self.getRenderLayers)  #placeholder

		# Set input validators
		layer_list_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w, ]+'), self.ui.layers_lineEdit)
		self.ui.layers_lineEdit.setValidator(layer_list_validator)

		frame_list_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\d\-x, ]+'), self.ui.frames_lineEdit)
		self.ui.frames_lineEdit.setValidator(frame_list_validator)

		self.expertMode = False


	def display(self, frameRange=None, layers=None, flags=None):
		""" Display the window.
		"""
		self.returnValue = False

		# Read user prefs config file - if it doesn't exist it will be created
		userPrefs.read()

		# Set 'Submit to' option depending on the parent window, or user prefs
		if self.parent.windowTitle() == "Render Queue":
			self.submitTo = "Render Queue"
			self.ui.submitTo_frame.setEnabled(False)
			self.ui.submitTo_frame.hide()
		else:
			self.submitTo = userPrefs.query('rendersubmit', 'submitto', default=self.ui.submitTo_comboBox.currentText())
			self.ui.submitTo_frame.setEnabled(True)
			self.ui.submitTo_frame.show()
		self.ui.submitTo_comboBox.setCurrentIndex(self.ui.submitTo_comboBox.findText(self.submitTo))
		self.ui.submit_pushButton.setText("Submit to %s" %self.submitTo)
		self.setQueueManagerFromComboBox()

		# Set job type from Icarus environment when possible
		if os.environ['IC_ENV'] == "STANDALONE":
			self.jobType = userPrefs.query('rendersubmit', 'lastrenderjobtype', default=self.ui.type_comboBox.currentText())
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.ui.layerOptions_toolButton.setEnabled(False)
			self.ui.writeNodeOptions_toolButton.setEnabled(False)
			self.setJobType()
			self.setSceneList()

		elif os.environ['IC_ENV'] == "MAYA":
			self.jobType = "Maya"
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()

			sceneName = mc.file(query=True, sceneName=True)
			if sceneName:  # Check we're not working in an unsaved scene
				relPath = self.makePathRelative(osOps.absolutePath(sceneName))
				if relPath:
					self.ui.scene_comboBox.addItem(relPath)
			else:
				msg = "Scene must be saved before submitting render."
				mc.warning(msg)
				#mc.confirmDialog(title="Scene not saved", message=msg, icon="warning", button="Close")
				self.ui.scene_comboBox.addItem(msg)
				self.ui.submit_pushButton.setToolTip(msg)
				self.ui.submit_pushButton.setEnabled(False)

			self.ui.render_groupBox.setEnabled(False)
			self.ui.sceneBrowse_toolButton.hide()

			self.getRenderLayers()
			self.getRenderers()

			if layers:
				# self.ui.layers_groupBox.setChecked(True)
				self.ui.layers_lineEdit.setText(layers)

		elif os.environ['IC_ENV'] == "NUKE":
			self.jobType = "Nuke"
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()

			scriptName = nuke.value('root.name')
			if scriptName:  # Check we're not working in an unsaved script
				relPath = self.makePathRelative(osOps.absolutePath(scriptName))
				if relPath:
					self.ui.scene_comboBox.addItem(relPath)
			else:
				msg = "Script must be saved before submitting render."
				nuke.warning(msg)
				#nuke.message(msg)
				self.ui.scene_comboBox.addItem(msg)
				self.ui.submit_pushButton.setToolTip(msg)
				self.ui.submit_pushButton.setEnabled(False)

			self.ui.render_groupBox.setEnabled(False)
			self.ui.sceneBrowse_toolButton.hide()

		self.numList = []
		if frameRange:
			self.ui.frames_lineEdit.setText(frameRange)
		else:
			pass
			#self.getFrameRangeFromShotSettings()
		self.calcFrameList()

		if flags:
			# self.ui.flags_groupBox.setChecked(True)
			self.ui.flags_lineEdit.setText(flags)

		# self.ui.show()
		self.show()
		self.raise_()

		return self.returnValue


	def toggleExpertMode(self):
		""" Toggle expert mode where additional UI items are visible.
		"""
		self.expertMode = not self.expertMode
		self.ui.render_groupBox.setEnabled(self.expertMode)
		self.ui.render_groupBox.setVisible(self.expertMode)


	def getSettingsFile(self, scene, suffix=""):
		""" Determine the path to the settings file based on the full path of
			the scene file.
		"""
		if os.path.isfile(scene):
			sceneDir, sceneFile = os.path.split(scene)
			settingsDir = os.path.join(sceneDir, os.environ['DATAFILESRELATIVEDIR'])
			#settingsFile = os.path.splitext(sceneFile)[0] + suffix
			settingsFile = osOps.sanitize(sceneFile, replace='_') + suffix

			# Create settings directory if it doesn't exist
			if not os.path.isdir(settingsDir):
				osOps.createDir(settingsDir)

			return os.path.join(settingsDir, settingsFile)

		else:
			return False


	# @QtCore.Slot()
	def applySettings(self):
		""" Apply the specific settings for the scene/script file.
		"""
		scene = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")
		self.xmlData = self.getSettingsFile(scene, suffix="_icSubmissionData.xml")
		if self.xmlData:
			self.xd.loadXML(self.xmlData, use_template=False)
			self.setupWidgets(self.ui, updateOnly=True)


	# @QtCore.Slot()
	def setQueueManagerFromComboBox(self):
		""" Set queue manager to submit job to - called when the job type
			combo box value is changed.
		"""
		self.submitTo = self.ui.submitTo_comboBox.currentText()
		userPrefs.edit('rendersubmit', 'submitto', self.submitTo) # deprecated
		self.ui.submit_pushButton.setText("Submit to %s" %self.submitTo)

		rq_show_list = [self.ui.flags_label, self.ui.flags_lineEdit]
		dl_show_list = [self.ui.pool_label, self.ui.group_label, 
		                self.ui.pool_comboBox, self.ui.group_comboBox, 
		                self.ui.getPools_toolButton, self.ui.getGroups_toolButton]

		for item in rq_show_list + dl_show_list:
			item.setEnabled(False)
		if self.submitTo == "Render Queue":
			for item in rq_show_list:
				item.setEnabled(True)
		if self.submitTo == "Deadline":
			for item in dl_show_list:
				item.setEnabled(True)


	# @QtCore.Slot()
	def setJobTypeFromComboBox(self):
		""" Set job type - called when the job type combo box value is
			changed.
		"""
		self.jobType = self.ui.type_comboBox.currentText()
		userPrefs.edit('rendersubmit', 'lastrenderjobtype', self.jobType)
		self.setJobType()
		if os.environ['IC_ENV'] == "STANDALONE":
			self.setSceneList()


	def setJobType(self):
		""" Setup some global variables and UI elements depending on the job
			type.
		"""
		if self.jobType == 'Generic command':
			# try:
			# 	self.relativeScenesDir = osOps.absolutePath('%s/%s' %(os.environ['MAYADIR'], 'scenes'))
			# except KeyError:
			# 	self.relativeScenesDir = ""
			self.ui.scene_label.setText("Command:")
			self.ui.mayaOptions_groupBox.hide()
			self.ui.nukeOptions_groupBox.hide()
		elif self.jobType == 'Maya':
			try:
				self.relativeScenesDir = osOps.absolutePath('%s/%s' %(os.environ['MAYADIR'], 'scenes'))
			except KeyError:
				self.relativeScenesDir = ""
			self.ui.scene_label.setText("Scene:")
			self.ui.mayaOptions_groupBox.show()
			self.ui.nukeOptions_groupBox.hide()
		elif self.jobType == 'Nuke':
			try:
				self.relativeScenesDir = osOps.absolutePath('%s/%s' %(os.environ['NUKEDIR'], 'scripts'))
			except KeyError:
				self.relativeScenesDir = ""
			self.ui.scene_label.setText("Script:")
			self.ui.nukeOptions_groupBox.show()
			self.ui.mayaOptions_groupBox.hide()

		# Representative string to replace the path specified above
		self.relativeScenesToken = '...'


	def setSceneList(self):
		""" Clear scene menu and populate from recent file list. Only used in
			standalone mode.
		"""
		self.ui.scene_comboBox.clear()

		try:
			import recentFiles
			for filePath in recentFiles.getLs(self.jobType):
				fullPath = osOps.absolutePath(os.environ['SHOTPATH'] + filePath)
				relPath = self.makePathRelative(fullPath)
				if relPath:
					self.ui.scene_comboBox.addItem(relPath)
		except:
			pass


	def makePathRelative(self, absPath):
		""" Convert an absolute path to a relative path.
		"""
		if absPath.startswith(self.relativeScenesDir):
			return absPath.replace(self.relativeScenesDir, self.relativeScenesToken)
		else:
			return False


	def makePathAbsolute(self, relPath):
		""" Convert a relative path to an absolute path.
		"""
		return relPath.replace(self.relativeScenesToken, self.relativeScenesDir)


	def sceneBrowse(self):
		""" Browse for a scene/script file.
		"""
		if self.jobType == 'Maya':
			fileDir = os.environ.get('MAYASCENESDIR', '.')  # Go to current dir if env var is not set
			fileFilter = 'Maya files (*.ma *.mb)'
			fileTerminology = 'scenes'
		elif self.jobType == 'Nuke':
			fileDir = os.environ.get('NUKESCRIPTSDIR', '.')  # Go to current dir if env var is not set
			fileFilter = 'Nuke files (*.nk)'
			fileTerminology = 'scripts'
		else:
			fileDir = os.environ.get('JOBPATH', '.')  # Go to current dir if env var is not set
			fileFilter = 'All files (*.*)'
			fileTerminology = 'commands'

		currentDir = os.path.dirname(self.makePathAbsolute(self.ui.scene_comboBox.currentText()))
		if os.path.exists(currentDir):
			startingDir = currentDir
		else:
			startingDir = fileDir

		# filePath = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), startingDir, fileFilter)[0]
		filePath = self.fileDialog(startingDir, fileFilter)

		if filePath:
			newEntry = self.makePathRelative(osOps.absolutePath(filePath))
			#newEntry = osOps.absolutePath(filePath)
			if newEntry:
				self.ui.scene_comboBox.removeItem(self.ui.scene_comboBox.findText(newEntry))  # If the entry already exists in the list, delete it
				self.ui.scene_comboBox.insertItem(0, newEntry)
				self.ui.scene_comboBox.setCurrentIndex(0)  # Always insert the new entry at the top of the list and select it
			else:
				verbose.warning("Only %s belonging to the current shot can be submitted." %fileTerminology)


	def getFrameRangeFromShotSettings(self):
		""" Get frame range from shot settings.
		"""
		try:
			self.ui.frames_lineEdit.setText("%d-%d" %(int(os.environ['STARTFRAME']), int(os.environ['ENDFRAME'])))
		except KeyError:
			self.ui.frames_lineEdit.setText("")


	def getFrameRangeFromRenderSettings(self):
		""" Get frame range from Maya or Nuke render settings.
		"""
		if os.environ['IC_ENV'] == "MAYA":
			start_frame = int(mc.getAttr('defaultRenderGlobals.startFrame'))
			end_frame = int(mc.getAttr('defaultRenderGlobals.endFrame'))

		elif os.environ['IC_ENV'] == "NUKE":
			start_frame = nuke.Root()['first_frame'].getValue()
			end_frame = nuke.Root()['last_frame'].getValue()

		self.ui.frames_lineEdit.setText("%d-%d" %(start_frame, end_frame))


	def getCurrentRenderLayer(self):
		""" Get current Maya render layer or selected Nuke write nodes &
			populate widget.
		"""
		if os.environ['IC_ENV'] == "MAYA":
			currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
			self.ui.layers_lineEdit.setText(currentLayer)

		elif os.environ['IC_ENV'] == "NUKE":
			writeNodeStr = ", ".join(n for n in self.getWriteNodes(selected=True))
			self.ui.writeNodes_lineEdit.setText(writeNodeStr)


	def getRenderLayers(self):
		""" Get Maya render layers or Nuke write nodes & populate widget.
		"""
		if os.environ['IC_ENV'] == "MAYA":
			layerStr = ", ".join(n for n in self.getRenderableLayers())
			self.ui.layers_lineEdit.setText(layerStr)

		elif os.environ['IC_ENV'] == "NUKE":
			writeNodeStr = ", ".join(n for n in self.getWriteNodes(selected=False))
			self.ui.writeNodes_lineEdit.setText(writeNodeStr)


	def getPools(self):
		""" Get Deadline pools & populate combo box.
		"""
		self.populateComboBox(self.ui.pool_comboBox, deadline.get_pools())


	def getGroups(self):
		""" Get Deadline groups & populate combo box.
		"""
		self.populateComboBox(self.ui.group_comboBox, deadline.get_groups())


	def getRenderers(self):
		""" Get Maya renderers & populate combo box.
		"""
		renderers = self.getRenderer()
		rendererLs = [renderers]
		# print(rendererLs)
		self.populateComboBox(self.ui.renderer_comboBox, rendererLs)


	# @QtCore.Slot()
	def setFrameListPreset(self):
		""" Modify frame list from preset menu.
		"""
		#print(self.sender().text())
		if self.sender().text() == "Sequential":
			num_list = sequence.numList(self.ui.frames_lineEdit.text(), sort=True, quiet=True)
			self.ui.frames_lineEdit.setText(sequence.numRange(num_list))

		elif self.sender().text() == "Reverse order":
			pass

		elif self.sender().text() == "Render first and last frames before others":
			frames_str = self.ui.frames_lineEdit.text()
			num_list = sequence.numList(frames_str, sort=True, quiet=True)
			first = min(num_list)
			last = max(num_list)
			self.ui.frames_lineEdit.setText("%d, %d, %s" %(first, last, frames_str))


	def calcFrameList(self, quiet=True):
		""" Calculate list of frames to be rendered.
		"""
		self.numList = sequence.numList(self.ui.frames_lineEdit.text(), sort=False, quiet=True)
		taskSize = self.ui.taskSize_spinBox.value()
		if self.numList == False:
			if not quiet:
				verbose.warning("Invalid entry for frame range.")
			# self.ui.frames_lineEdit.setProperty("mandatoryField", True)
			# self.ui.frames_lineEdit.style().unpolish(self.ui.frames_lineEdit)
			# self.ui.frames_lineEdit.style().polish(self.ui.frames_lineEdit)
			self.numList = []
			self.taskList = ["Unknown", ]
			return False
		else:
			#self.ui.frames_lineEdit.setText(sequence.numRange(self.numList))
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

		# print(self.numList)
		# print(self.taskList)
		return True


	def getMayaProject(self, scene):
		""" Get the Maya project. If the environment variable is not set, try
			to guess the Maya project directory based on the scene name.
		"""
		try:  # Project is implicit if job is set
			mayaProject = os.environ['MAYADIR'].replace("\\", "/")
		except KeyError:
			mayaProject = scene.split('/scenes')[0]

		return mayaProject


	def getRenderer(self):
		""" Get the current Maya renderer.
		"""
		try:
			renderer = mc.getAttr("defaultRenderGlobals.currentRenderer")
		except:
			renderer = ""

		return renderer


	def getRenderableLayers(self):
		""" Get Maya render layers that are enabled (renderable).
		"""
		layers = mc.ls(type='renderLayer')
		renderableLayers = []
		for layer in layers:
			if mc.getAttr(layer+'.renderable'):
				renderableLayers.append(layer)

		return renderableLayers


	def getWriteNodes(self, selected=True):
		""" Get Nuke write nodes.
			If 'selected' is True, only return selected nodes.
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
		"""
		try:
			padding = "#" * mc.getAttr("defaultRenderGlobals.extensionPadding")
			if layer is None:
				path = mc.renderSettings(fullPath=True, 
				                         leaveUnmatchedTokens=True, 
				                         genericFrameImageName=padding)
			else:
				path = mc.renderSettings(fullPath=True, 
				                         layer=layer, 
				                         leaveUnmatchedTokens=True, 
				                         genericFrameImageName=padding)
		except:
			path = ""

		return path[0]


	def getNukeRenderOutput(self, writeNode):
		""" Get the output path from a Nuke write node.
		"""
		# try:
		node = nuke.toNode(writeNode)
		path = node.knob('file').evaluate()

		#path = osOps.absolutePath(node.knob('file'))
		# except:
		# 	path = ""

		return path


	def getOutputFilePath(self):
		""" Get Maya's render output file path from the Maya project.
		"""
		try:
			path = mc.workspace(expandName=mc.workspace(fileRuleEntry="images"))
		except:
			#path = ""
			path = osOps.absolutePath("$MAYADIR/renders")

		return path


	def getOutputFilePrefix(self):
		""" Get Maya's output file prefix from the render settings.
		"""
		try:
			prefix = mc.getAttr("defaultRenderGlobals.imageFilePrefix")
		except:
			#prefix = ""
			prefix = "%s/<Scene>/<RenderLayer>/%s_<RenderLayer>" %(os.environ['IC_USERNAME'], os.environ['SHOT'])

		return prefix


	def submit(self):
		""" Submit job.
		"""
		self.save()  # Save settings

		submit_args = self.getSubmissionOptions()
		if submit_args:

			# Generate confirmation message(s)
			if self.submitTo == "Render Queue":
				if submit_args['frames']:
					submit_args['taskSize'] = self.ui.taskSize_spinBox.value()
					frames_msg = "%d %s to be rendered; %d %s to be submitted.\n" %(len(self.numList), verbose.pluralise("frame", len(self.numList)), len(self.taskList), verbose.pluralise("task", len(self.taskList)))
				else:
					submit_args['frames'] = "Unknown"
					submit_args['taskSize'] = "Unknown"
					self.numList = []
					self.taskList = [submit_args['frames'], ]
					frames_msg = "The frame range was not specified so the job cannot be distributed into tasks. The job will be submitted as a single task and the frame range will be read from the scene at render time.\n"
			else:
				if submit_args['frames']:
					frames_msg = ""
				else:
					submit_args['frames'] = "Unknown"
					frames_msg = "No frame range specified.\n"
			job_info_msg = "Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n" %(submit_args['jobName'], self.jobType, submit_args['frames'], submit_args['taskSize'], submit_args['priority'])

			# Show confirmation dialog
			dialog_title = "Submit to %s - %s" %(self.submitTo, submit_args['jobName'])
			dialog_msg = job_info_msg + "\n" + frames_msg + "Do you want to continue?"
			dialog = pDialog.dialog()

			if dialog.display(dialog_msg, dialog_title):
				if self.submitTo == "Render Queue":
					result, result_msg = self.submitToRenderQueue(**submit_args)
					#result, result_msg, output_str = self.rq.submit_job(**submit_args)
				if self.submitTo == "Deadline":
					result, result_msg = deadline.submit_job(**submit_args)

				# Show post-confirmation dialog
				dialog_title = "Submission Results - %s" %submit_args['jobName']
				dialog_msg = job_info_msg + "\n" + result_msg
				dialog.display(dialog_msg, dialog_title, conf=True)


	def getSubmissionOptions(self):
		""" Get all values from UI widgets and return them as a dictionary.
		"""
		submit_args = {}

		if self.submitTo == "Render Queue":
			self.calcFrameList(quiet=False)
			# if not self.calcFrameList(quiet=False):
			# 	return None

		###################
		# Generic options #
		###################

		submit_args['frames'] = self.ui.frames_lineEdit.text()
		submit_args['taskSize'] = self.ui.taskSize_spinBox.value()
		submit_args['pool'] = self.ui.pool_comboBox.currentText()  # Deadline only
		submit_args['group'] = self.ui.group_comboBox.currentText()  # Deadline only
		submit_args['priority'] = self.ui.priority_spinBox.value()
		submit_args['comment'] = self.ui.comment_lineEdit.text()

		submit_args['envVars'] = ['JOB', 'SHOT', 'JOBPATH', 'SHOTPATH']

		#############################
		# Renderer-specific options #
		#############################

		if self.jobType == "Maya":
			submit_args['plugin'] = "MayaBatch"  # Deadline only
			submit_args['renderCmdEnvVar'] = 'MAYARENDERVERSION'  # RQ only
			submit_args['flags'] = self.ui.flags_lineEdit.text()  # RQ only
			submit_args['version'] = os.environ['MAYA_VER']  #jobData.getAppVersion('Maya')
			submit_args['renderer'] = self.ui.renderer_comboBox.currentText()  # Maya submit only
			scene = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")
			submit_args['scene'] = scene
			submit_args['mayaProject'] = self.getMayaProject(scene)
			submit_args['outputFilePath'] = self.getOutputFilePath()  # Maya submit only
			submit_args['outputFilePrefix'] = self.getOutputFilePrefix()  # Maya submit only
			submit_args['jobName'] = os.path.splitext(os.path.basename(scene))[0]
			submit_args['renderLayers'] = self.ui.layers_lineEdit.text()
			output = []  # Maya submit only
			if os.environ['IC_ENV'] == "MAYA":
				for layer in self.getRenderableLayers():
					output.append(os.path.split(self.getMayaRenderOutput(layer)))
			submit_args['output'] = output

			submit_args['envVars'] += ['MAYADIR', 'MAYASCENESDIR', 'MAYARENDERSDIR']

		elif self.jobType == "Nuke":
			submit_args['plugin'] = "Nuke"  # Deadline only
			submit_args['renderCmdEnvVar'] = 'NUKEVERSION'  # RQ only
			submit_args['flags'] = self.ui.flags_lineEdit.text()  # RQ only
			submit_args['version'] = os.environ['NUKE_VER'].split('v')[0]  #jobData.getAppVersion('Nuke')
			submit_args['nukeX'] = False  # Deadline only
			submit_args['isMovie'] = False  # Deadline only - TO BE IMPLEMENTED
			scene = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")
			submit_args['scene'] = scene
			submit_args['jobName'] = os.path.splitext(os.path.basename(scene))[0]
			#submit_args['writeNodes'] = self.ui.writeNodes_lineEdit.text()
			submit_args['renderLayers'] = self.ui.writeNodes_lineEdit.text()
			output = []  # Nuke submit only
			if os.environ['IC_ENV'] == "NUKE":
				for writeNode in self.getWriteNodes(selected=False):
					output.append(os.path.split(self.getNukeRenderOutput(writeNode)))
			submit_args['output'] = output

			submit_args['envVars'] += ['NUKEDIR', 'NUKESCRIPTSDIR', 'NUKERENDERSDIR']

		return submit_args


	def submitToRenderQueue(self, **kwargs):
		""" Submit job to render queue.
		"""
		timeFormatStr = "%Y/%m/%d %H:%M:%S" #"%a, %d %b %Y %H:%M:%S"

		# Check render command is valid
		renderCmdEnvVar = kwargs['renderCmdEnvVar']
		try:
			renderCmd = os.environ[renderCmdEnvVar].replace("\\", "/")
		except KeyError:
			error_msg = "Path to %s render command executable not found. This can be set with the environment variable '%s'." %(self.jobType, renderCmdEnvVar)
			verbose.error(error_msg)
			return False, "Failed to submit job.\n%s" %error_msg

		# Package option variables into tuples
		genericOpts = kwargs['jobName'], self.jobType, kwargs['frames'], kwargs['taskSize'], kwargs['priority']
		if self.jobType == "Maya":
			renderOpts = kwargs['scene'], kwargs['mayaProject'], kwargs['flags'], renderCmd
		elif self.jobType == "Nuke":
			renderOpts = kwargs['scene'], kwargs['flags'], renderCmd

		# Instantiate render queue class, load data, and create new job
		rq = renderQueue.renderQueue()
		rq.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'renderQueue.xml'), use_template=False)
		rq.newJob(genericOpts, renderOpts, self.taskList, os.environ['IC_USERNAME'], time.strftime(timeFormatStr), kwargs['comment'])

		return True, "Successfully submitted job."


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

# def run_(**kwargs):
# 	# for key, value in kwargs.iteritems():
# 	# 	print "%s = %s" % (key, value)
# 	renderSubmitUI = RenderSubmitUI(**kwargs)
# 	#renderSubmitUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
# 	print renderSubmitUI
# 	renderSubmitUI.show()
# 	#renderSubmitUI.raise_()
# 	#renderSubmitUI.exec_()


def run_maya(**kwargs):
	""" Run in Maya.
	"""
	UI._maya_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any existing UI
	renderSubmitUI = RenderSubmitUI(parent=UI._maya_main_window())

	renderSubmitUI.display(**kwargs)  # Show the UI


def run_nuke(**kwargs):
	""" Run in Nuke.
	"""
	UI._nuke_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any existing UI
	renderSubmitUI = RenderSubmitUI(parent=UI._nuke_main_window())

	renderSubmitUI.display(**kwargs)  # Show the UI


# Detect environment and run application
if os.environ['IC_ENV'] == "STANDALONE":
	verbose.print_("[GPS] %s" %WINDOW_TITLE)
elif os.environ['IC_ENV'] == "MAYA":
	import maya.cmds as mc
	verbose.print_("[GPS] %s for Maya" %WINDOW_TITLE)
	# run_maya()
elif os.environ['IC_ENV'] == "NUKE":
	import nuke
	import nukescripts
	verbose.print_("[GPS] %s for Nuke" %WINDOW_TITLE)
	# run_nuke()
# elif __name__ == '__main__':
# 	run_standalone()

