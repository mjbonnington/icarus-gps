#!/usr/bin/python

# style__main__.py
# Template for PySide / Qt GUI application written in Python
#
# Directions for use:
# 
# Create your UI in Qt Designer and save as 'style.ui'
# Compile UI to Python with command: 'pyside-uic style.ui -o style_ui.py'
# 
# Save your resources file as 'style_rc.qrc'
# Compile resources to Python with command: 'pyside-rcc style.qrc -o style_rc.py'
# 
# Run with command: 'python style__main__.py'


from PySide import QtCore, QtGui
from submit_ui import *
import os, re, signal, subprocess, sys

sys.path.append(os.environ['ICWORKINGDIR'])
import env__init__
env__init__.appendSysPaths()
import sequence as seq
import recentFiles #; reload(recentFiles)

class gpsSubmitRender(QtGui.QDialog):

	def __init__(self, parent = None):
		super(gpsSubmitRender, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.init()

		# Connect signals and slots
		QtCore.QObject.connect(self.ui.frameRange_lineEdit, QtCore.SIGNAL('textEdited()'), self.validateFrameList)
		QtCore.QObject.connect(self.ui.frameRange_lineEdit, QtCore.SIGNAL('editingFinished()'), self.calcFrameList)
		QtCore.QObject.connect(self.ui.taskSize_spinBox, QtCore.SIGNAL('valueChanged()'), self.calcFrameList)

		QtCore.QObject.connect(self.ui.submit_pushButton, QtCore.SIGNAL('clicked()'), self.submit)
		QtCore.QObject.connect(self.ui.killComplete_pushButton, QtCore.SIGNAL('clicked()'), self.kill)
		QtCore.QObject.connect(self.ui.close_pushButton, QtCore.SIGNAL('clicked()'), self.exit)


	def init(self):
		self.numList = []
		self.resetFrameList()

		# Clear scene menu and populate with apps
		self.ui.scene_comboBox.clear()

		# List all Maya scenes in the current working directory
		#path = os.getcwd()
		#ls = os.listdir(path)
		#ls.sort()
		#filterRE = re.compile(r'(?i)\.m[ab]$')
		#for filename in ls:
		#	if filterRE.search(filename):
		#		self.ui.scene_comboBox.addItem(filename)

		for filename in recentFiles.getLs('maya'):
			self.ui.scene_comboBox.addItem(filename)



	def tglSubmit(self, option):
		self.ui.submit_pushButton.setEnabled(option)
		self.ui.killComplete_pushButton.setEnabled(option)


	def resetFrameList(self):
		"""Get frame range from shot settings
		"""
		rgStartFrame = int(os.environ['STARTFRAME'])
		rgEndFrame = int(os.environ['ENDFRAME'])
		nFrames = rgEndFrame - rgStartFrame + 1
		self.ui.frameRange_lineEdit.setText("%d-%d" %(rgStartFrame, rgEndFrame))
		self.ui.taskSize_spinBox.setMaximum(nFrames)
		self.ui.taskSize_spinBox.setValue(nFrames)
		self.calcFrameList()


	def validateFrameList(self):
		"""Validate the frame range list in realtime as the text field is edited
		"""
		self.numList = seq.numList(self.ui.frameRange_lineEdit.text(), quiet=True)
		if self.numList == False:
			self.tglSubmit(False)
		else:
			self.tglSubmit(True)


	def calcFrameList(self, quiet=True):
		"""Calculate list of frames to be rendered
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
		"""Kill the rendering process
		"""
		try:
			os.killpg(self.renderProcess.pid, signal.SIGTERM)
			#os.killpg(int(os.environ['MAYARENDERPID']), signal.SIGTERM)
		except (OSError, AttributeError):
			print "Warning: Cannot kill rendering process as there is no render in progress."

		# Re-enable UI
		self.ui.submit_pushButton.setEnabled(True)
		self.ui.overrideFrameRange_groupBox.setEnabled(True)
		self.ui.scene_horizontalLayout.setEnabled(True)


	def submit(self):
		"""Submit render
		"""
		self.calcFrameList(quiet=False)

		try:
			renderCmd = os.environ["MAYARENDERVERSION"]
		except KeyError:
			print "ERROR: Path to Maya Render command executable not found. This can be set with the environment variable 'MAYARENDERVERSION'."

		cmdStr = ""
		args = "-proj %s" %os.environ['MAYADIR']
		frameRangeArgs = ""

		# Additional command-line arguments
		#if mc.checkBox("skipExistingFrames", query=True, value=True):
		#	args = args + " -skipExistingFrames true"

		sceneName = os.environ['SHOTPATH'] + self.ui.scene_comboBox.currentText()

		# Check we're not working in an unsaved scene
		if sceneName:

			if self.ui.overrideFrameRange_groupBox.isChecked():
				for frame in self.taskList:
					frameRangeArgs = "-s %d -e %d" %(frame[0], frame[1])

					cmdStr = cmdStr + "%s %s %s %s; " %(renderCmd, args, frameRangeArgs, sceneName)

			else:
				cmdStr = "%s %s %s" %(renderCmd, args, sceneName)

			print cmdStr
			self.renderProcess = subprocess.Popen(cmdStr, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
			#os.environ['MAYARENDERPID'] = str(self.renderProcess.pid)

			# Disable UI to prevent new renders being submitted
			self.ui.submit_pushButton.setEnabled(False)
			self.ui.overrideFrameRange_groupBox.setEnabled(False)
			self.ui.scene_horizontalLayout.setEnabled(False)

		else:
			print "ERROR: Scene not specified."


	def exit(self):
		sys.exit()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	import rsc_rc

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	myApp = gpsSubmitRender()
	myApp.show()
	sys.exit(app.exec_())
