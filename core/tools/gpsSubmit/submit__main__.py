#!/usr/bin/python

# [Icarus] Batch Render Submitter submit__main__.py
# v0.5
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Front end for submitting command-line renders.


from PySide import QtCore, QtGui
from submit_ui import * # <- import your app's UI file (as generated by pyside-uic)
import os, sys, time

# Import custom modules
import renderQueue
import sequence as seq


class gpsRenderSubmitApp(QtGui.QDialog):

	def __init__(self, parent = None):
		super(gpsRenderSubmitApp, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.relativeScenesDir = os.path.normpath( '%s/%s' %(os.environ['MAYADIR'], 'scenes') )
		self.relativeScenesToken = '...' # representative string to replace the path specified above
		self.numList = []
		self.resetFrameList()

		# Instantiate render queue class and load data
		self.rq = renderQueue.renderQueue()
		self.rq.loadXML(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'renderQueue.xml'))

		# Clear scene menu and populate with recent scenes
		self.ui.scene_comboBox.clear()
		try:
			import recentFiles; reload(recentFiles)
			for filePath in recentFiles.getLs('maya'):
				fullPath = os.path.normpath( os.environ['SHOTPATH'] + filePath )
				relPath = self.relativePath(fullPath)
				if relPath:
					self.ui.scene_comboBox.addItem(relPath)
		except:
			pass

		# Connect signals & slots
		self.ui.sceneBrowse_toolButton.clicked.connect(self.sceneBrowse)

		self.ui.frameRange_lineEdit.editingFinished.connect(self.calcFrameList) # was textEdited
		self.ui.taskSize_spinBox.valueChanged.connect(self.calcFrameList)

		self.ui.submit_pushButton.clicked.connect(self.submit)
		self.ui.close_pushButton.clicked.connect(self.exit)

		# Set input validators
		frame_list_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\d\-, ]+'), self.ui.frameRange_lineEdit)
		self.ui.frameRange_lineEdit.setValidator(frame_list_validator)


	# def tglUI(self, option):
	# 	self.ui.main_frame.setEnabled(option)
	# 	self.ui.submit_pushButton.setEnabled(option)
	# 	self.ui.close_pushButton.setEnabled(option)


	def tglSubmit(self, option):
		self.ui.submit_pushButton.setEnabled(option)


	def relativePath(self, absPath):
		if absPath.startswith(self.relativeScenesDir):
			return absPath.replace(self.relativeScenesDir, self.relativeScenesToken)
		else:
			return False


	def absolutePath(self, relPath):
		return relPath.replace(self.relativeScenesToken, self.relativeScenesDir)


	def sceneBrowse(self):
		""" Browse for a scene file.
		"""
		currentDir = os.path.dirname(self.absolutePath(self.ui.scene_comboBox.currentText()))
		if os.path.exists(currentDir):
			startingDir = currentDir
		else:
			startingDir = os.environ['MAYASCENESDIR']

		filePath = QtGui.QFileDialog.getOpenFileName(self, self.tr('Files'), startingDir, 'Maya files (*.ma *.mb)')
		if filePath[0]:
			newEntry = self.relativePath( os.path.normpath(filePath[0]) )
			if newEntry:
				self.ui.scene_comboBox.removeItem(self.ui.scene_comboBox.findText(newEntry)) # if the entry already exists in the list, delete it
				self.ui.scene_comboBox.insertItem(0, newEntry)
				self.ui.scene_comboBox.setCurrentIndex(0) # always insert the new entry at the top of the list and select it
			else:
				print "Warning: Only scenes belonging to the current shot can be submitted."


	def resetFrameList(self):
		""" Get frame range from shot settings.
		"""
		rgStartFrame = int(os.environ['STARTFRAME'])
		rgEndFrame = int(os.environ['ENDFRAME'])
		nFrames = rgEndFrame - rgStartFrame + 1
		self.ui.frameRange_lineEdit.setText("%d-%d" %(rgStartFrame, rgEndFrame))
		self.ui.taskSize_slider.setMaximum(nFrames)
		self.ui.taskSize_spinBox.setMaximum(nFrames)
		self.ui.taskSize_spinBox.setValue(nFrames) # store this value in userPrefs or something?
		self.calcFrameList()


	def validateFrameList(self):
		""" Validate the frame range list in realtime as the text field is edited.
		"""
		self.numList = seq.numList(self.ui.frameRange_lineEdit.text(), quiet=True)
		if self.numList == False:
			self.tglSubmit(False)
		else:
			self.tglSubmit(True)


	def calcFrameList(self, quiet=True):
		""" Calculate list of frames to be rendered.
		"""
		self.numList = seq.numList(self.ui.frameRange_lineEdit.text())
		taskSize = self.ui.taskSize_spinBox.value()
		if self.numList == False:
			if not quiet:
				print "Warning: Invalid entry for frame range."
			self.tglSubmit(False)
		else:
			self.tglSubmit(True)
			self.ui.frameRange_lineEdit.setText(seq.numRange(self.numList))
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
			sequences = list(seq.seqRange(self.numList, gen_range=True))
			for sequence in sequences:
				chunks = list(seq.chunks(sequence, taskSize))
				for chunk in chunks:
					#self.taskList.append(list(seq.seqRange(chunk))[0])
					self.taskList.append(seq.numRange(chunk))
					
			if not quiet:
				print "%d frames to be rendered; %d task(s) to be submitted:" %(len(self.numList), len(self.taskList))


	def submit(self):
		""" Submit render to queue.
		"""
		timeFormatStr = "%Y/%m/%d %H:%M:%S" # "%a, %d %b %Y %H:%M:%S"

		self.calcFrameList(quiet=True)

		taskLs = []
		mayaScene = self.absolutePath(self.ui.scene_comboBox.currentText()) # implicit if submitting from Maya UI
		mayaProject = os.environ['MAYADIR'] # implicit if job is set
		jobName = os.path.basename(mayaScene)
		priority = self.ui.priority_spinBox.value()
		if self.ui.overrideFrameRange_groupBox.isChecked():
			frames = self.ui.frameRange_lineEdit.text()
			taskSize = self.ui.taskSize_spinBox.value()
			# for frame in self.taskList:
			# 	taskLs.append(frame)
			framesMsg = '%d frames to be rendered; %d task(s) to be submitted.\n' %(len(self.numList), len(self.taskList))
		else:
			frames = 'Unknown'
			taskSize = 'Unknown'
			self.numList = []
			self.taskList = []
			framesMsg = 'The frame range was not specified so the job cannot be distributed into tasks. The job will be submitted as a single task and the frame range will be read from the scene at render time.\n'
		if self.ui.flags_groupBox.isChecked():
			mayaFlags = self.ui.flags_lineEdit.text()
		else:
			mayaFlags = ""

		genericOpts = jobName, priority, frames, taskSize
		mayaOpts = mayaScene, mayaProject, mayaFlags

		# Confirmation dialog
		import pDialog

		dialogTitle = 'Submit Render'
		dialogMsg = ''
		dialogMsg += 'Name:\t%s\nPriority:\t%s\nFrames:\t%s\nTask size:\t%s\n\n' %genericOpts
		#dialogMsg += 'Scene:\t%s\nProject:\t%s\nFlags:\t%s\n\n' %mayaOpts
		dialogMsg += framesMsg
		dialogMsg += 'Do you wish to continue?'

		dialog = pDialog.dialog()
		if dialog.dialogWindow(dialogMsg, dialogTitle):
			self.rq.newJob(genericOpts, mayaOpts, self.taskList, os.environ['USERNAME'], time.strftime(timeFormatStr))
		else:
			return


	def exit(self):
		""" Exit the dialog.
		"""
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	# Initialise Icarus environment
	os.environ['ICWORKINGDIR'] = "N:\Dev\icarus\core\ui" # temp assignment
	sys.path.append(os.environ['ICWORKINGDIR'])
	import env__init__
	env__init__.setEnv()

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	#app.setStyle('fusion') # Set UI style - you can also use a flag e.g. '-style plastique'

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	renderSubmitApp = gpsRenderSubmitApp()
	renderSubmitApp.show()
	sys.exit(app.exec_())

else:
	renderSubmitApp = gpsRenderSubmitApp()
	print renderSubmitApp
	renderSubmitApp.show()

