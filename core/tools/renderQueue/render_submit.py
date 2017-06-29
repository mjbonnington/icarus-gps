#!/usr/bin/python

# [Icarus] render_submit.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Batch Render Submitter
# A UI for creating render jobs to send to the render queue.


import os
import sys
import time

from Qt import QtCompat, QtCore, QtGui, QtWidgets

# Import custom modules
import osOps
import renderQueue
import sequence
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


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class renderSubmitDialog(QtWidgets.QDialog):
	""" Main dialog class.
	"""
	def __init__(self, parent=None):
		super(renderSubmitDialog, self).__init__(parent)

		# Set object name and window title
		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle(WINDOW_TITLE)

		# Load UI & stylesheet
		self.ui = QtCompat.load_ui(fname=os.path.join(os.environ['IC_FORMSDIR'], UI_FILE))
		if STYLESHEET is not None:
			qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
			with open(qss, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.ui.setWindowFlags(QtCore.Qt.CustomizeWindowHint | 
			                   QtCore.Qt.WindowTitleHint)

		# Connect signals & slots
		self.ui.type_comboBox.currentIndexChanged.connect(self.setJobTypeFromComboBox)
		self.ui.sceneBrowse_toolButton.clicked.connect(self.sceneBrowse)

		self.ui.frameRange_lineEdit.editingFinished.connect(self.calcFrameList)  # was textEdited
		self.ui.taskSize_spinBox.valueChanged.connect(self.calcFrameList)

		self.ui.submit_pushButton.clicked.connect(self.submit)
		self.ui.close_pushButton.clicked.connect(self.exit)

		# Set input validators
		frame_list_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\d\-, ]+'), self.ui.frameRange_lineEdit)
		self.ui.frameRange_lineEdit.setValidator(frame_list_validator)

		# Instantiate render queue class and load data
		self.rq = renderQueue.renderQueue()
		self.rq.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'renderQueue.xml'))


	def display(self, frameRange=None, flags=None):
		""" Display the dialog.
		"""
		self.returnValue = False

		# Read user prefs config file - if it doesn't exist it will be created
		userPrefs.read()

		# Set job type from Icarus environment when possible
		if os.environ['IC_ENV'] == 'STANDALONE':
			try:
				self.jobType = userPrefs.config.get('renderqueue', 'lastrenderjobtype')
			except:
				self.jobType = self.ui.type_comboBox.currentText()

			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()
			self.setSceneList()

		elif os.environ['IC_ENV'] == 'MAYA':
			self.jobType = 'Maya'
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()

			import maya.cmds as mc
			sceneName = mc.file(query=True, sceneName=True)
			if sceneName:  # Check we're not working in an unsaved scene
				relPath = self.relativePath(osOps.absolutePath(sceneName))
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

		elif os.environ['IC_ENV'] == 'NUKE':
			self.jobType = 'Nuke'
			self.ui.type_comboBox.setCurrentIndex(self.ui.type_comboBox.findText(self.jobType))
			self.setJobType()

			import nuke
			scriptName = nuke.value("root.name")
			if scriptName:  # Check we're not working in an unsaved script
				relPath = self.relativePath(osOps.absolutePath(scriptName))
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
			self.ui.frameRange_lineEdit.setText(frameRange)
		else:
			self.getFrameList()
		self.calcFrameList()

		if flags:
			self.ui.flags_groupBox.setChecked(True)
			self.ui.flags_lineEdit.setText(flags)

		self.ui.show()
		self.ui.raise_()
		return self.returnValue


	def setJobTypeFromComboBox(self):
		""" Set job type - called when the job type combo box value is
			changed.
		"""
		self.jobType = self.ui.type_comboBox.currentText()
		userPrefs.edit('renderqueue', 'lastrenderjobtype', self.jobType)
		self.setJobType()
		self.setSceneList()


	def setJobType(self):
		""" Setup some global variables and UI elements depending on the job
			type.
		"""
		if self.jobType == 'Maya':
			try:
				self.relativeScenesDir = osOps.absolutePath( '%s/%s' %(os.environ['MAYADIR'], 'scenes') )
			except KeyError:
				self.relativeScenesDir = ""
			self.ui.scene_label.setText("Scene:")
		elif self.jobType == 'Nuke':
			try:
				self.relativeScenesDir = osOps.absolutePath( '%s/%s' %(os.environ['NUKEDIR'], 'scripts') )
			except KeyError:
				self.relativeScenesDir = ""
			self.ui.scene_label.setText("Script:")

		self.relativeScenesToken = '...'  # Representative string to replace the path specified above


	def setSceneList(self):
		""" Clear scene menu and populate from recent file list. Only used in
			standalone mode.
		"""
		self.ui.scene_comboBox.clear()

		try:
			import recentFiles
			for filePath in recentFiles.getLs(self.jobType):
				fullPath = osOps.absolutePath( os.environ['SHOTPATH'] + filePath )
				relPath = self.relativePath(fullPath)
				if relPath:
					self.ui.scene_comboBox.addItem(relPath)
		except:
			pass


	def relativePath(self, absPath):
		""" Convert an absolute path to a relative path.
		"""
		if absPath.startswith(self.relativeScenesDir):
			return absPath.replace(self.relativeScenesDir, self.relativeScenesToken)
		else:
			return False


	def absolutePath(self, relPath):
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

		currentDir = os.path.dirname(self.absolutePath(self.ui.scene_comboBox.currentText()))
		if os.path.exists(currentDir):
			startingDir = currentDir
		else:
			startingDir = fileDir

		filePath = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), startingDir, fileFilter)
		if filePath[0]:
			newEntry = self.relativePath( osOps.absolutePath(filePath[0]) )
			#newEntry = osOps.absolutePath(filePath[0])
			if newEntry:
				self.ui.scene_comboBox.removeItem(self.ui.scene_comboBox.findText(newEntry))  # If the entry already exists in the list, delete it
				self.ui.scene_comboBox.insertItem(0, newEntry)
				self.ui.scene_comboBox.setCurrentIndex(0)  # Always insert the new entry at the top of the list and select it
			else:
				verbose.print_("Warning: Only %s belonging to the current shot can be submitted." %fileTerminology, 2)


	def getFrameList(self):
		""" Get frame range from shot settings.
		"""
		try:
			self.ui.frameRange_lineEdit.setText("%d-%d" %(int(os.environ['STARTFRAME']), int(os.environ['ENDFRAME'])))
			self.ui.overrideFrameRange_groupBox.setChecked(True)
		except KeyError:
			self.ui.frameRange_lineEdit.setText("")
			self.ui.overrideFrameRange_groupBox.setChecked(False)



	def calcFrameList(self, quiet=True):
		""" Calculate list of frames to be rendered.
		"""
		self.numList = sequence.numList(self.ui.frameRange_lineEdit.text(), quiet=True)
		taskSize = self.ui.taskSize_spinBox.value()
		if self.numList == False:
			if not quiet:
				verbose.print_("Warning: Invalid entry for frame range.", 2)
			return False
		else:
			self.ui.frameRange_lineEdit.setText(sequence.numRange(self.numList))
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
					

	def guessMayaProject(self, scene):
		""" Try to guess the Maya project directory based on the scene name.
		"""
		try:
			mayaProject = os.environ['MAYADIR'].replace("\\", "/")  # Project is implicit if job is set
		except KeyError:
			mayaProject = scene.split('/scenes')[0]

		return mayaProject


	def submit(self):
		""" Submit job to render queue.
		"""
		timeFormatStr = "%Y/%m/%d %H:%M:%S" # "%a, %d %b %Y %H:%M:%S"

		if not self.calcFrameList(quiet=False):
			return

		###################
		# Generic options #
		###################

		if self.ui.overrideFrameRange_groupBox.isChecked():
			frames = self.ui.frameRange_lineEdit.text()
			taskSize = self.ui.taskSize_spinBox.value()
			framesMsg = '%d %s to be rendered; %d %s to be submitted.\n' %(len(self.numList), verbose.pluralise("frame", len(self.numList)), len(self.taskList), verbose.pluralise("task", len(self.taskList)))
		else:
			frames = 'Unknown'
			taskSize = 'Unknown'
			self.numList = []
			self.taskList = [frames, ]
			framesMsg = 'The frame range was not specified so the job cannot be distributed into tasks. The job will be submitted as a single task and the frame range will be read from the scene at render time.\n'

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
			mayaScene = self.absolutePath(self.ui.scene_comboBox.currentText()).replace("\\", "/")  # Implicit if submitting from Maya UI
			mayaProject = self.guessMayaProject(mayaScene)
			jobName = os.path.basename(mayaScene)
		elif self.jobType == 'Nuke':
			renderCmdEnvVar = 'NUKEVERSION'
			nukeScript = self.absolutePath(self.ui.scene_comboBox.currentText()).replace("\\", "/")  # Implicit if submitting from Nuke UI
			jobName = os.path.basename(nukeScript)

		try:
			renderCmd = os.environ[renderCmdEnvVar].replace("\\", "/")
		except KeyError:
			verbose.print_("ERROR: Path to %s render command executable not found. This can be set with the environment variable '%s'." %(self.jobType, renderCmdEnvVar), 2)

		# Package option variables into tuples
		genericOpts = jobName, self.jobType, frames, taskSize, priority
		if self.jobType == 'Maya':
			renderOpts = mayaScene, mayaProject, flags, renderCmd
		elif self.jobType == 'Nuke':
			renderOpts = nukeScript, flags, renderCmd

		# Confirmation dialog
		import pDialog

		dialogTitle = 'Submit Render - %s' %jobName
		dialogMsg = ''
		dialogMsg += 'Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n\n' %genericOpts
		# if self.jobType == 'Maya':
		# 	dialogMsg += 'Scene:\t%s\nProject:\t%s\nFlags:\t%s\nCommand:\t%s\n\n' %renderOpts
		# elif self.jobType == 'Nuke':
		# 	dialogMsg += 'Script:\t%s\nFlags:\t%s\nCommand:\t%s\n\n' %renderOpts
		dialogMsg += framesMsg
		dialogMsg += 'Do you want to continue?'

		dialog = pDialog.dialog()
		if dialog.display(dialogMsg, dialogTitle):
			self.rq.newJob(genericOpts, renderOpts, self.taskList, os.environ['IC_USERNAME'], time.strftime(timeFormatStr), comment)

			# Post-confirmation dialog
			dialogTitle = 'Submitted Render - %s' %jobName
			dialogMsg = ''
			dialogMsg += 'Name:\t%s\nType:\t%s\nFrames:\t%s\nTask size:\t%s\nPriority:\t%s\n\n' %genericOpts
			dialogMsg += 'Render job submitted succesfully.'
			dialog.display(dialogMsg, dialogTitle, conf=True)
		else:
			return


	def showEvent(self, event):
		""" Event handler for when window is shown.
		"""
		self.setJobTypeFromComboBox()
		self.getFrameList()
		# self.display()


	def exit(self):
		""" Exit the dialog.
		"""
		self.ui.hide()


# def run_(**kwargs):
# 	# for key, value in kwargs.iteritems():
# 	# 	print "%s = %s" % (key, value)
# 	renderSubmitDialog = renderSubmitDialog(**kwargs)
# 	#renderSubmitDialog.setAttribute( QtCore.Qt.WA_DeleteOnClose )
# 	print renderSubmitDialog
# 	renderSubmitDialog.show()
# 	#renderSubmitDialog.raise_()
# 	#renderSubmitDialog.exec_()

