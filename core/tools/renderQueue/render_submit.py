#!/usr/bin/python

# [Icarus] render_submit.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Batch Render Submitter
# A UI for creating render jobs to send to a render queue manager.


import os
import subprocess
import sys
import time

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import osOps
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
CREATE_NO_WINDOW = 0x08000000


# ----------------------------------------------------------------------------
# Main window class
# ----------------------------------------------------------------------------

class RenderSubmitUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Render submit UI.
	"""
	def __init__(self, parent=None):
		super(RenderSubmitUI, self).__init__(parent)
		self.parent = parent

		xml_data = os.path.join(os.environ['IC_USERPREFS'], 'icSubmissionData.xml')

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
		# self.shortcutReloadStyleSheet = QtWidgets.QShortcut(self)
		# self.shortcutReloadStyleSheet.setKey('Ctrl+R')
		# self.shortcutReloadStyleSheet.activated.connect(self.reloadStyleSheet)

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

		self.ui.frames_lineEdit.editingFinished.connect(self.calcFrameList)  # was textEdited
		self.ui.taskSize_spinBox.valueChanged.connect(self.calcFrameList)

		# # self.ui.pool_comboBox.currentIndexChanged.connect(self.storeComboBoxValue)
		# # self.ui.group_comboBox.currentIndexChanged.connect(self.storeComboBoxValue)
		# self.ui.pool_comboBox.editTextChanged.connect(self.storeComboBoxValue)
		# self.ui.group_comboBox.editTextChanged.connect(self.storeComboBoxValue)
		self.ui.getPools_toolButton.clicked.connect(self.getDeadlinePools)
		self.ui.getGroups_toolButton.clicked.connect(self.getDeadlineGroups)
		# self.ui.priority_spinBox.valueChanged.connect(self.storeSpinBoxValue)
		# self.ui.comment_lineEdit.textEdited.connect(self.storeLineEditValue)

		self.ui.submit_pushButton.clicked.connect(self.submit)
		self.ui.close_pushButton.clicked.connect(self.close)
		#self.ui.close_pushButton.clicked.connect(self.saveAndExit)

		# Context menus
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Shot default", self.getFrameRangeFromShotSettings)
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Render settings", self.getFrameRangeFromRenderSettings)
		self.addContextMenu(self.ui.frameListOptions_toolButton, "Sequential", self.setFrameListPreset)  #placeholder
		self.addContextMenu(self.ui.frameListOptions_toolButton, "First, last, sequential", self.setFrameListPreset)  #placeholder

		self.addContextMenu(self.ui.layerOptions_toolButton, "Current layer only", self.getCurrentRenderLayer)
		self.addContextMenu(self.ui.layerOptions_toolButton, "All renderable layers", self.getRenderLayers)

		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "Selected write node only", self.getCurrentRenderLayer)  #placeholder
		self.addContextMenu(self.ui.writeNodeOptions_toolButton, "All write nodes", self.getRenderLayers)  #placeholder

		# Set input validators
		layer_list_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w, ]+'), self.ui.layers_lineEdit)
		self.ui.layers_lineEdit.setValidator(layer_list_validator)

		frame_list_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\d\-, ]+'), self.ui.frames_lineEdit)
		self.ui.frames_lineEdit.setValidator(frame_list_validator)


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

		# Set job type from Icarus environment when possible
		if os.environ['IC_ENV'] == 'STANDALONE':
			self.jobType = userPrefs.query('rendersubmit', 'lastrenderjobtype', default=self.ui.type_comboBox.currentText())
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()
			self.setSceneList()

		elif os.environ['IC_ENV'] == 'MAYA':
			self.jobType = 'Maya'
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

			#self.ui.render_groupBox.setEnabled(False)
			self.ui.sceneBrowse_toolButton.hide()

			self.getRenderLayers()
			self.getRenderers()

			if layers:
				# self.ui.layers_groupBox.setChecked(True)
				self.ui.layers_lineEdit.setText(layers)

		elif os.environ['IC_ENV'] == 'NUKE':
			self.jobType = 'Nuke'
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()

			scriptName = nuke.value("root.name")
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

			#self.ui.render_groupBox.setEnabled(False)
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
			self.xd.loadXML(self.xmlData)
			self.setupWidgets(self.ui, updateOnly=True)


	# @QtCore.Slot()
	def setQueueManagerFromComboBox(self):
		""" Set queue manager to submit job to - called when the job type
			combo box value is changed.
		"""
		self.submitTo = self.ui.submitTo_comboBox.currentText()
		userPrefs.edit('rendersubmit', 'submitto', self.submitTo)
		self.ui.submit_pushButton.setText("Submit to %s" %self.submitTo)

		self.ui.group_label.setEnabled(False)
		self.ui.getGroups_toolButton.setEnabled(False)
		self.ui.group_comboBox.setEnabled(False)


	# @QtCore.Slot()
	def setJobTypeFromComboBox(self):
		""" Set job type - called when the job type combo box value is
			changed.
		"""
		self.jobType = self.ui.type_comboBox.currentText()
		userPrefs.edit('rendersubmit', 'lastrenderjobtype', self.jobType)
		self.setJobType()
		if os.environ['IC_ENV'] == 'STANDALONE':
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
			self.ui.frames_groupBox.setChecked(True)
		except KeyError:
			self.ui.frames_lineEdit.setText("")
			self.ui.frames_groupBox.setChecked(False)


	def getFrameRangeFromRenderSettings(self):
		""" Get frame range from Maya render settings (only from Maya
			environment).
		"""
		if os.environ['IC_ENV'] == 'MAYA':
			self.ui.frames_lineEdit.setText("%d-%d" %(int(mc.getAttr('defaultRenderGlobals.startFrame')), int(mc.getAttr('defaultRenderGlobals.endFrame'))))
			#self.ui.frames_lineEdit.setText("%d-%d" %(int(mc.playbackOptions(min=True, q=True)), int(mc.playbackOptions(max=True, q=True))))
			self.ui.frames_groupBox.setChecked(True)


	def getCurrentRenderLayer(self):
		""" Get current Maya render layer & populate widget (only from Maya
			environment).
		"""
		if os.environ['IC_ENV'] == 'MAYA':
			currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
			self.ui.layers_lineEdit.setText(currentLayer)


	def getRenderLayers(self):
		""" Get Maya render layers & populate widget (only from Maya
			environment).
		"""
		if os.environ['IC_ENV'] == 'MAYA':
			layerStr = ", ".join(n for n in self.getRenderableLayers())
			self.ui.layers_lineEdit.setText(layerStr)
			# currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
			# startFrame = int(mc.getAttr('defaultRenderGlobals.startFrame'))
			# endFrame = int(mc.getAttr('defaultRenderGlobals.endFrame'))
			# frames = "%d-%d" %(startFrame, endFrame)

			# self.ui.layers_treeWidget.clear()

			# for layer in layers:
			# 	item = QtWidgets.QTreeWidgetItem(self.ui.layers_treeWidget)
			# 	layerFrames = frames
			# 	adjustments = mc.editRenderLayerAdjustment(layer, query=True, layer=True)
			# 	# overrides = ['defaultRenderGlobals.startFrame', 'defaultRenderGlobals.endFrame']
			# 	if adjustments:
			# 		if 'defaultRenderGlobals.startFrame' in adjustments:
			# 			startFrame = "*"
			# 		if 'defaultRenderGlobals.endFrame' in adjustments:
			# 			endFrame = "*"
			# 		layerFrames = "%s-%s" %(startFrame, endFrame)
			# 	# item.setText(0, mc.getAttr('renderLayerManager.renderLayerId[%d]'))
			# 	item.setText(2, layer)
			# 	item.setText(3, layerFrames)

			# 	# Check renderable layers
			# 	if mc.getAttr(layer+'.renderable'):
			# 		item.setCheckState(1, QtCore.Qt.Checked)
			# 	else:
			# 		item.setCheckState(1, QtCore.Qt.Unchecked)

			# # Resize columns
			# self.ui.layers_treeWidget.resizeColumnToContents(0)
			# self.ui.layers_treeWidget.resizeColumnToContents(1)
			# self.ui.layers_treeWidget.resizeColumnToContents(2)

		# else:
		# 	self.ui.layers_groupBox.hide()


	def getDeadlinePools(self):
		""" Get Deadline pools & populate combo box.
		"""
		try:
			pools = subprocess.check_output([os.environ['DEADLINECMDVERSION'], '-pools'], creationflags=CREATE_NO_WINDOW)
			self.populateComboBox(self.ui.pool_comboBox, self.strToList(pools))
		except:
			verbose.warning("Could not retrieve Deadline pools.")


	def getDeadlineGroups(self):
		""" Get Deadline groups & populate combo box.
		"""
		try:
			groups = subprocess.check_output([os.environ['DEADLINECMDVERSION'], '-groups'], creationflags=CREATE_NO_WINDOW)
			self.populateComboBox(self.ui.group_comboBox, self.strToList(groups))
		except:
			verbose.warning("Could not retrieve Deadline groups.")


	def getRenderers(self):
		""" Get Maya renderers & populate combo box.
		"""
		renderers = self.getRenderer()
		rendererLs = [renderers]
		# verbose.print_(rendererLs)
		self.populateComboBox(self.ui.renderer_comboBox, rendererLs)


	# @QtCore.Slot()
	def setFrameListPreset(self):
		""" Set frame list from preset - TEMPORARY FUNCTION
		"""
		print(self.sender().text())


	def calcFrameList(self, quiet=True):
		""" Calculate list of frames to be rendered.
		"""
		self.numList = sequence.numList(self.ui.frames_lineEdit.text(), quiet=True)
		taskSize = self.ui.taskSize_spinBox.value()
		if self.numList == False:
			if not quiet:
				verbose.warning("Invalid entry for frame range.")
			self.ui.frames_lineEdit.setProperty("mandatoryField", True)
			self.ui.frames_lineEdit.style().unpolish(self.ui.frames_lineEdit)
			self.ui.frames_lineEdit.style().polish(self.ui.frames_lineEdit)
			return False
		else:
			self.ui.frames_lineEdit.setText(sequence.numRange(self.numList))
			nFrames = len(self.numList)
			if taskSize < nFrames:
				self.ui.taskSize_slider.setMaximum(nFrames)
				self.ui.taskSize_spinBox.setMaximum(nFrames)
				self.ui.taskSize_spinBox.setValue(taskSize)
			else:
				self.ui.taskSize_slider.setMaximum(nFrames)
				self.ui.taskSize_spinBox.setMaximum(nFrames)
				self.ui.taskSize_spinBox.setValue(nFrames)

			# Generate task list for rendering
			self.taskList = []
			sequences = list(sequence.seqRange(self.numList, gen_range=True))
			for seq in sequences:
				chunks = list(sequence.chunks(seq, taskSize))
				for chunk in chunks:
					#self.taskList.append(list(sequence.seqRange(chunk))[0])
					self.taskList.append(sequence.numRange(chunk))

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


	def getOutput(self, layer=None):
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


	def getOutputFilePath(self):
		""" Get Maya's render output file path from the Maya project.
		"""
		try:
			path = mc.workspace(expandName=mc.workspace(fileRuleEntry="images"))
		except:
			path = ""

		return path


	def getOutputFilePrefix(self):
		""" Get Maya's output file prefix from the render settings.
		"""
		try:
			prefix = mc.getAttr("defaultRenderGlobals.imageFilePrefix")
		except:
			prefix = ""

		return prefix


	def submit(self):
		""" Submit job.
		"""
		self.save()  # Save settings

		if self.submitTo == "Render Queue":
			self.submitToRenderQueue()
		if self.submitTo == "Deadline":
			self.submitToDeadline()


	def submitToRenderQueue(self):
		""" Submit job to render queue.
		"""
		timeFormatStr = "%Y/%m/%d %H:%M:%S" # "%a, %d %b %Y %H:%M:%S"

		if not self.calcFrameList(quiet=False):
			return

		# Instantiate render queue class and load data
		self.rq = renderQueue.renderQueue()
		self.rq.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'renderQueue.xml'))

		###################
		# Generic options #
		###################

		if self.ui.frames_groupBox.isChecked():
			frames = self.ui.frames_lineEdit.text()
			taskSize = self.ui.taskSize_spinBox.value()
			frames_msg = '%d %s to be rendered; %d %s to be submitted.\n' %(len(self.numList), verbose.pluralise("frame", len(self.numList)), len(self.taskList), verbose.pluralise("task", len(self.taskList)))
		else:
			frames = 'Unknown'
			taskSize = 'Unknown'
			self.numList = []
			self.taskList = [frames, ]
			frames_msg = 'The frame range was not specified so the job cannot be distributed into tasks. The job will be submitted as a single task and the frame range will be read from the scene at render time.\n'

		if self.ui.flags_groupBox.isChecked():
			flags = self.ui.flags_lineEdit.text()
		else:
			flags = ""

		priority = self.ui.priority_spinBox.value()
		comment = self.ui.comment_lineEdit.text()

		#############################
		# Renderer-specific options #
		#############################

		if self.jobType == 'Maya':
			renderCmdEnvVar = 'MAYARENDERVERSION'
			mayaScene = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")  # Implicit if submitting from Maya UI
			mayaProject = self.getMayaProject(mayaScene)
			jobName = os.path.splitext(os.path.basename(mayaScene))[0]
		elif self.jobType == 'Nuke':
			renderCmdEnvVar = 'NUKEVERSION'
			nukeScript = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")  # Implicit if submitting from Nuke UI
			jobName = os.path.splitext(os.path.basename(nukeScript))[0]

		try:
			renderCmd = os.environ[renderCmdEnvVar].replace("\\", "/")
		except KeyError:
			verbose.error("Path to %s render command executable not found. This can be set with the environment variable '%s'." %(self.jobType, renderCmdEnvVar))

		# Package option variables into tuples
		genericOpts = jobName, self.jobType, frames, taskSize, priority
		if self.jobType == 'Maya':
			renderOpts = mayaScene, mayaProject, flags, renderCmd
		elif self.jobType == 'Nuke':
			renderOpts = nukeScript, flags, renderCmd

		# Confirmation dialog
		import pDialog

		dialog_title = 'Submit Render - %s' %jobName
		dialog_msg = ''
		dialog_msg += 'Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n\n' %genericOpts
		# if self.jobType == 'Maya':
		# 	dialog_msg += 'Scene:\t%s\nProject:\t%s\nFlags:\t%s\nCommand:\t%s\n\n' %renderOpts
		# elif self.jobType == 'Nuke':
		# 	dialog_msg += 'Script:\t%s\nFlags:\t%s\nCommand:\t%s\n\n' %renderOpts
		dialog_msg += frames_msg
		dialog_msg += 'Do you want to continue?'

		dialog = pDialog.dialog()
		if dialog.display(dialog_msg, dialog_title):
			self.rq.newJob(genericOpts, renderOpts, self.taskList, os.environ['IC_USERNAME'], time.strftime(timeFormatStr), comment)

			# Post-confirmation dialog
			dialog_title = 'Submission Results - %s' %jobName
			dialog_msg = ''
			dialog_msg += 'Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n\n' %genericOpts
			dialog_msg += 'Render job submitted succesfully.'
			dialog.display(dialog_msg, dialog_title, conf=True)
		else:
			return


	def submitToDeadline(self):
		""" Submit job to Deadline.
		"""
		# pluginInfoFile = ""

		if not self.calcFrameList(quiet=False):
			return

		###################
		# Generic options #
		###################

		frames = self.ui.frames_lineEdit.text()
		taskSize = self.ui.taskSize_spinBox.value()
		frames_msg = '%d %s to be rendered; %d %s to be submitted.\n' %(len(self.numList), verbose.pluralise("frame", len(self.numList)), len(self.taskList), verbose.pluralise("task", len(self.taskList)))

		pool = self.ui.pool_comboBox.currentText()
		group = self.ui.group_comboBox.currentText()
		priority = self.ui.priority_spinBox.value()
		comment = self.ui.comment_lineEdit.text()

		#############################
		# Renderer-specific options #
		#############################

		if self.jobType == 'Maya':
			plugin = 'MayaBatch'
			version = os.environ['MAYA_VER']  #jobData.getAppVersion('Maya')
			renderer = self.ui.renderer_comboBox.currentText()  # Maya submit only
			scene = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")
			mayaProject = self.getMayaProject(scene)  # Maya submit only
			outputFilePath = self.getOutputFilePath()  # Maya submit only
			outputFilePrefix = self.getOutputFilePrefix()  # Maya submit only
			jobName = os.path.splitext(os.path.basename(scene))[0]
			renderLayers = self.ui.layers_lineEdit.text()
			output = []  # Maya submit only
			if os.environ['IC_ENV'] == 'MAYA':
				for layer in self.getRenderableLayers():
					output.append(os.path.split(self.getOutput(layer)))

		elif self.jobType == 'Nuke':
			plugin = 'Nuke'
			scene = self.makePathAbsolute(self.ui.scene_comboBox.currentText()).replace("\\", "/")
			jobName = os.path.splitext(os.path.basename(scene))[0]

		# Package option variables into tuples
		genericOpts = jobName, self.jobType, frames, taskSize, priority
		# if self.jobType == 'Maya':
		# 	renderOpts = scene, mayaProject, flags, renderCmd
		# elif self.jobType == 'Nuke':
		# 	renderOpts = scene, flags, renderCmd

		# Confirmation dialog
		import pDialog

		dialog_title = 'Submit Render to Deadline - %s' %jobName
		dialog_msg = ''
		dialog_msg += 'Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n\n' %genericOpts
		dialog_msg += frames_msg
		dialog_msg += 'Do you want to continue?'

		dialog = pDialog.dialog()
		if dialog.display(dialog_msg, dialog_title):
			try:
				# Generate submission info files
				jobInfoFile = self.getSettingsFile(scene, suffix="_deadlineJobInfo.txt")
				# jobInfoFile = os.path.splitext(scene)[0] + "_deadlineJobInfo.txt"
				fh = open(jobInfoFile, 'w')
				fh.write("Plugin=%s\n" %plugin)
				if renderLayers:
					fh.write("Name=%s - %s\n" %(jobName, renderLayer))
					fh.write("BatchName=%s\n" %jobName)
				else:
					fh.write("Name=%s\n" %jobName)
				fh.write("Comment=%s\n" %comment)
				fh.write("Frames=%s\n" %frames)
				fh.write("ChunkSize=%s\n" %taskSize)
				fh.write("Pool=%s\n" %pool)
				fh.write("Group=%s\n" %group)
				fh.write("Priority=%s\n" %priority)
				if priority == 0:
					fh.write("InitialStatus=Suspended\n")
				for i, outputPath in enumerate(output):
					fh.write("OutputDirectory%d=%s\n" %(i, outputPath[0]))
					fh.write("OutputFilename%d=%s\n" %(i, outputPath[1]))
				#fh.write("IncludeEnvironment=True\n")
				fh.write("ExtraInfo0=%s\n" %os.environ['JOB'])
				fh.write("ExtraInfo1=%s\n" %os.environ['SHOT'])
				fh.close()

				pluginInfoFile = self.getSettingsFile(scene, suffix="_deadlinePluginInfo.txt")
				# pluginInfoFile = os.path.splitext(scene)[0] + "_deadlinePluginInfo.txt"
				fh = open(pluginInfoFile, 'w')
				fh.write("Version=%s\n" %version)
				fh.write("Build=64bit\n")
				fh.write("Renderer=%s\n" %renderer)
				fh.write("StrictErrorChecking=1\n")
				fh.write("ProjectPath=%s\n" %mayaProject)
				fh.write("OutputFilePath=%s\n" %outputFilePath)
				fh.write("OutputFilePrefix=%s\n" %outputFilePrefix)
				fh.write("SceneFile=%s\n" %scene)
				if renderLayers:
					fh.write("UsingRenderLayers=1\n")
					fh.write("UseLegacyRenderLayers=1\n")
					fh.write("RenderLayer=%s\n" %renderLayer)
				fh.close()

				# Execute deadlinecommand
				cmd_output = subprocess.check_output([os.environ['DEADLINECMDVERSION'], jobInfoFile, pluginInfoFile], creationflags=CREATE_NO_WINDOW)
				output_str = cmd_output.decode()

				result_msg = "Successfully submitted job to Deadline."
				verbose.message(result_msg)

				# Delete submission info files - TEMPORARILY DISABLED FOR DEBUGGING PURPOSES
				# osOps.recurseRemove(jobInfoFile)
				# osOps.recurseRemove(pluginInfoFile)

			except:
				import traceback
				exc_type, exc_value, exc_traceback = sys.exc_info()
				traceback.print_exception(exc_type, exc_value, exc_traceback)
				result_msg = "Failed to submit job to Deadline."
				verbose.error(result_msg)
				output_str = "Either the Deadline executable could not be found, or the submission info files could not be written." #\n\n%s" % traceback.format_exc()

			# Post-confirmation dialog
			dialog_title = 'Submission Results - %s' %jobName
			dialog_msg = ''
			dialog_msg += 'Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n\n' %genericOpts
			dialog_msg += result_msg + "\n" + output_str
			dialog.display(dialog_msg, dialog_title, conf=True)
		else:
			return


	# def showEvent(self, event):
	# 	""" Event handler for when window is shown.
	# 	"""
	# 	self.setJobTypeFromComboBox()
	# 	# self.getFrameRangeFromShotSettings()
	# 	self.display()


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry


	# def save(self):
	# 	""" Save data.
	# 	"""
	# 	if self.xd.saveXML():
	# 		verbose.message("Submission settings saved.")
	# 		return True
	# 	else:
	# 		verbose.error("Submission settings could not be saved.")
	# 		return False


	# def saveAndExit(self):
	# 	""" Save data and exit dialog.
	# 	"""
	# 	if self.save():
	# 		self.returnValue = True
	# 		self.hide()
	# 	else:
	# 		self.exit()  # There's a bug where all property panel widgets become visible if a save fails. As a quick dodgy workaround we exit so we don't see it happen.


	# def exit(self):
	# 	""" Exit the dialog.
	# 	"""
	# 	self.returnValue = False
	# 	self.hide()

# ----------------------------------------------------------------------------
# End of main window class
# ----------------------------------------------------------------------------


# def run_(**kwargs):
# 	# for key, value in kwargs.iteritems():
# 	# 	print "%s = %s" % (key, value)
# 	renderSubmitUI = RenderSubmitUI(**kwargs)
# 	#renderSubmitUI.setAttribute( QtCore.Qt.WA_DeleteOnClose )
# 	print renderSubmitUI
# 	renderSubmitUI.show()
# 	#renderSubmitUI.raise_()
# 	#renderSubmitUI.exec_()


# ----------------------------------------------------------------------------
# Run functions - MOVE TO TEMPLATE MODULE?
# ----------------------------------------------------------------------------

def run_maya(**kwargs):
	""" Run in Maya.
	"""
	UI._maya_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any already existing UI
	renderSubmitUI = RenderSubmitUI(parent=UI._maya_main_window())

	renderSubmitUI.display(**kwargs)  # Show the UI


def run_nuke(**kwargs):
	""" Run in Nuke.
	"""
	UI._nuke_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any already existing UI
	renderSubmitUI = RenderSubmitUI(parent=UI._nuke_main_window())

	renderSubmitUI.display(**kwargs)  # Show the UI


# Detect environment and run application
if os.environ['IC_ENV'] == 'STANDALONE':
	verbose.print_("[GPS] %s" %WINDOW_TITLE)
elif os.environ['IC_ENV'] == 'MAYA':
	import maya.cmds as mc
	verbose.print_("[GPS] %s for Maya" %WINDOW_TITLE)
	# run_maya()
elif os.environ['IC_ENV'] == 'NUKE':
	import nuke
	import nukescripts
	verbose.print_("[GPS] %s for Nuke" %WINDOW_TITLE)
	# run_nuke()
# elif __name__ == '__main__':
# 	run_standalone()

