#!/usr/bin/python

# [Icarus] edit_job.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# A dialog for editing job settings.


from PySide import QtCore, QtGui
from edit_job_ui import *
import os, sys

# Import custom modules
import osOps

class dialog(QtGui.QDialog):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Connect signals & slots
		self.ui.jobName_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPath_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPathBrowse_toolButton.clicked.connect(self.browse)
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\w\.-]+'), self.ui.jobName_lineEdit)
		self.ui.jobName_lineEdit.setValidator(alphanumeric_validator)


	def dialogWindow(self, jobName, jobPath, jobActive):
		self.dialogReturn = False
		# self.jobName = jobName
		# self.jobPath = jobPath
		# self.jobActive = jobActive

		self.setWindowTitle("Edit Job: %s" %jobName)
		self.ui.jobName_lineEdit.setText(jobName)
		self.ui.jobPath_lineEdit.setText(jobPath)
		self.ui.jobEnabled_checkBox.setChecked(jobActive)

		self.exec_()


	def updateUI(self):
		""" Disables the OK button if either of the text fields are empty.
		"""
		if self.ui.jobName_lineEdit.text() == "" or self.ui.jobPath_lineEdit.text() == "":
			self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
		else:
			self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)


	def browse(self):
		""" Opens a dialog from which to select a folder.
		"""
		startingDir = osOps.absolutePath(self.ui.jobPath_lineEdit.text())
		if os.path.isdir(startingDir):
			dialogHome = startingDir
		else:
			dialogHome = fsroot

		dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)

		if dialog:
			jobPath = osOps.relativePath(dialog, 'JOBSROOT')
			jobName = jobPath.split('/')[1]
			self.ui.jobPath_lineEdit.setText(jobPath)
			self.ui.jobName_lineEdit.setText(jobName)
		#return dialog


	def ok(self):
		self.dialogReturn = True
		self.jobName = self.ui.jobName_lineEdit.text()
		self.jobPath = self.ui.jobPath_lineEdit.text()
		if self.ui.jobEnabled_checkBox.checkState() == QtCore.Qt.Checked:
			self.jobActive = True
		else:
			self.jobActive = False
		self.accept()
		return #True


	def cancel(self):
		self.dialogReturn = False
		self.accept()
		return #False

