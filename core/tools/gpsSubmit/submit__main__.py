#!/usr/bin/python

# GPS Submit Render
# v0.3.2
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Front end for submitting command-line renders


from PySide import QtCore, QtGui
from submit_ui import *
import os, re, signal, subprocess, sys

# Initialise Icarus environment
sys.path.append(os.environ['ICWORKINGDIR'])
import env__init__
env__init__.appendSysPaths()

import sequence as seq
import recentFiles; reload(recentFiles)


class gpsSubmitRender(QtGui.QDialog):

	def __init__(self, parent = None):
		super(gpsSubmitRender, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.relativeScenesDir = os.path.normpath( '%s/%s' %(os.environ['MAYADIR'], 'scenes') )
		self.relativeScenesToken = '...' # representative string to replace the path specified above
		self.numList = []
		self.resetFrameList()

		# Clear scene menu and populate with recent scenes
		self.ui.scene_comboBox.clear()
		for filePath in recentFiles.getLs('maya'):
			fullPath = os.path.normpath( os.environ['SHOTPATH'] + filePath )
			relPath = self.relativePath(fullPath)
			if relPath:
				self.ui.scene_comboBox.addItem(relPath)

		# Connect signals and slots
		QtCore.QObject.connect(self.ui.sceneBrowse_toolButton, QtCore.SIGNAL('clicked()'), self.sceneBrowse)

		#QtCore.QObject.connect(self.ui.frameRange_lineEdit, QtCore.SIGNAL('textEdited()'), self.validateFrameList) # can't get this to work
		QtCore.QObject.connect(self.ui.frameRange_lineEdit, QtCore.SIGNAL('editingFinished()'), self.calcFrameList)
		QtCore.QObject.connect(self.ui.taskSize_spinBox, QtCore.SIGNAL('valueChanged()'), self.calcFrameList)

		QtCore.QObject.connect(self.ui.submit_pushButton, QtCore.SIGNAL('clicked()'), self.submit)
		QtCore.QObject.connect(self.ui.killComplete_pushButton, QtCore.SIGNAL('clicked()'), self.kill)
		QtCore.QObject.connect(self.ui.close_pushButton, QtCore.SIGNAL('clicked()'), self.exit)


	def tglUI(self, option):
		self.ui.main_frame.setEnabled(option)
		self.ui.submit_pushButton.setEnabled(option)
		self.ui.close_pushButton.setEnabled(option)


	def tglSubmit(self, option):
		self.ui.submit_pushButton.setEnabled(option)
		self.ui.killComplete_pushButton.setEnabled(option)


	def relativePath(self, absPath):
		if absPath.startswith(self.relativeScenesDir):
			return absPath.replace(self.relativeScenesDir, self.relativeScenesToken)
		else:
			return False


	def absolutePath(self, relPath):
		return relPath.replace(self.relativeScenesToken, self.relativeScenesDir)


	def sceneBrowse(self):
		""" Browse for a scene file
		"""
		currentDir = os.path.dirname(self.absolutePath(self.ui.scene_comboBox.currentText()))
		if os.path.exists(currentDir):
			startingDir = currentDir
		else:
			startingDir = os.environ['MAYASCENESDIR']

		filePath = QtGui.QFileDialog.getOpenFileName(gpsSubmitRenderApp, self.tr('Files'), startingDir, 'Maya files (*.ma *.mb)')
		if filePath[0]:
			newEntry = self.relativePath( os.path.normpath(filePath[0]) )
			if newEntry:
				self.ui.scene_comboBox.removeItem(self.ui.scene_comboBox.findText(newEntry)) # if the entry already exists in the list, delete it
				self.ui.scene_comboBox.insertItem(0, newEntry)
				self.ui.scene_comboBox.setCurrentIndex(0) # always insert the new entry at the top of the list and select it
			else:
				print "Warning: Only scenes belonging to the current shot can be submitted."


	def resetFrameList(self):
		""" Get frame range from shot settings
		"""
		rgStartFrame = int(os.environ['STARTFRAME'])
		rgEndFrame = int(os.environ['ENDFRAME'])
		nFrames = rgEndFrame - rgStartFrame + 1
		self.ui.frameRange_lineEdit.setText("%d-%d" %(rgStartFrame, rgEndFrame))
		self.ui.taskSize_spinBox.setMaximum(nFrames)
		self.ui.taskSize_spinBox.setValue(nFrames)
		self.calcFrameList()


	def validateFrameList(self):
		""" Validate the frame range list in realtime as the text field is edited
		"""
		self.numList = seq.numList(self.ui.frameRange_lineEdit.text(), quiet=True)
		if self.numList == False:
			self.tglSubmit(False)
		else:
			self.tglSubmit(True)


	def calcFrameList(self, quiet=True):
		""" Calculate list of frames to be rendered
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
				self.ui.taskSize_spinBox.setMaximum(nFrames)
				self.ui.taskSize_spinBox.setValue(taskSize)
			else:
				self.ui.taskSize_spinBox.setMaximum(nFrames)
				self.ui.taskSize_spinBox.setValue(nFrames)

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


	def kill(self):
		""" Kill the rendering process
		"""
		try:
			print "Attempting to kill rendering process (PID=%s)" %self.renderProcess.pid
			if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
				os.killpg(self.renderProcess.pid, signal.SIGTERM)
			else:
				os.kill(self.renderProcess.pid, signal.CTRL_C_EVENT)

		except (OSError, AttributeError):
			print "Warning: Cannot kill rendering process as there is no render in progress."

		# Re-enable UI
		self.tglUI(True)


	def submit(self):
		""" Submit render
		"""
		self.calcFrameList(quiet=False)

		try:
			renderCmd = '"%s"' %os.environ['MAYARENDERVERSION']
		except KeyError:
			print "ERROR: Path to Maya Render command executable not found. This can be set with the environment variable 'MAYARENDERVERSION'."

		cmdStr = ''
		args = '-proj "%s"' %os.environ['MAYADIR']
		frameRangeArgs = ''

		if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
			cmdSep = ' & '
		else:
			cmdSep = '; '
		# Additional command-line arguments
		#if mc.checkBox("skipExistingFrames", query=True, value=True):
		#	args = args + " -skipExistingFrames true"

		sceneName = '"%s"' %self.absolutePath(self.ui.scene_comboBox.currentText())

		# Check we're not working in an unsaved scene
		if sceneName:

			if self.ui.overrideFrameRange_groupBox.isChecked():
				for frame in self.taskList:
					frameRangeArgs = '-s %d -e %d' %(frame[0], frame[1])

					cmdStr = cmdStr + '%s %s %s %s%s' %(renderCmd, args, frameRangeArgs, sceneName, cmdSep)

			else:
				cmdStr = '%s %s %s%s' %(renderCmd, args, sceneName, cmdSep)

			if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
				#print cmdStr
				self.renderProcess = subprocess.Popen(cmdStr, shell=True) #, stdout=subprocess.PIPE, shell=True)
			else:
				#print cmdStr
				self.renderProcess = subprocess.Popen(cmdStr, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

			# Disable UI to prevent new renders being submitted
			self.tglUI(False)

		else:
			print "ERROR: Scene not specified."


	def exit(self):
		""" Exit the dialog
		"""
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	import rsc_rc

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	gpsSubmitRenderApp = gpsSubmitRender()
	gpsSubmitRenderApp.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint )

	gpsSubmitRenderApp.show()
	sys.exit(gpsSubmitRenderApp.exec_())

else:
	gpsSubmitRenderApp = gpsSubmitRender()
	gpsSubmitRenderApp.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint )

	gpsSubmitRenderApp.show()
