#!/usr/bin/python

# [Icarus] edit_job.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2017 Gramercy Park Studios
#
# A dialog for editing job settings.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets, QtCompat

# Import custom modules
import osOps


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Edit Job"
WINDOW_OBJECT = "editJobUI"

# Set the UI and the stylesheet
UI_FILE = "edit_job_ui.ui"
STYLESHEET = None  # Set to None to use the parent app's stylesheet


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog):
	""" Main dialog class.
	"""
	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)

		# Set object name and window title
		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle(WINDOW_TITLE)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Load UI
		self.ui = QtCompat.load_ui(fname=os.path.join(os.path.dirname(os.path.realpath(__file__)), UI_FILE))
		if STYLESHEET is not None:
			with open(STYLESHEET, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Connect signals & slots
		self.ui.jobName_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPath_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPathBrowse_toolButton.clicked.connect(self.browseDir)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\w\.-]+'), self.ui.jobName_lineEdit)
		self.ui.jobName_lineEdit.setValidator(alphanumeric_validator)


	def dialogWindow(self, jobName, jobPath, jobActive):
		""" Show the dialog.
		"""
		self.dialogReturn = False

		if jobName:
			self.ui.setWindowTitle("%s: %s" %(WINDOW_TITLE, jobName))
		else:
			self.ui.setWindowTitle("Add New Job")
		self.ui.jobName_lineEdit.setText(jobName)
		self.ui.jobPath_lineEdit.setText(jobPath)
		self.ui.jobEnabled_checkBox.setChecked(jobActive)

		self.ui.exec_()


	def updateUI(self):
		""" Disables the OK button if either of the text fields are empty.
		"""
		if self.ui.jobName_lineEdit.text() == "" or self.ui.jobPath_lineEdit.text() == "":
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
		else:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)


	def browseDir(self):
		""" Opens a dialog from which to select a folder.
		"""
		startingDir = osOps.translatePath(self.ui.jobPath_lineEdit.text())
		if os.path.isdir(startingDir):
			dialogHome = startingDir
		else:
			dialogHome = os.environ['JOBSROOT']

		# Append slash to path if it's a Windows drive letter, otherwise file
		# dialog won't open the correct location
		if dialogHome.endswith(':'):
			dialogHome += '/'

		dialogPath = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)
		# dialog = QtWidgets.QFileDialog(self)

		if dialogPath:
		# if dialog.exec_():
		# 	dialogPath = dialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)
			jobPath = osOps.relativePath(dialogPath, 'JOBSROOT')
			self.ui.jobPath_lineEdit.setText(jobPath)
			# Only autofill job name field it it's empty
			if not self.ui.jobName_lineEdit.text():
				try:
					jobName = jobPath.split('/')[1]
					self.ui.jobName_lineEdit.setText(jobName)
				except IndexError:
					pass
		# return dialogPath


	def ok(self):
		""" Dialog accept function.
		"""
		self.dialogReturn = True
		self.jobName = self.ui.jobName_lineEdit.text()
		self.jobPath = self.ui.jobPath_lineEdit.text()
		if self.ui.jobEnabled_checkBox.checkState() == QtCore.Qt.Checked:
			self.jobActive = True
		else:
			self.jobActive = False
		self.ui.accept()
		return #True


	def cancel(self):
		""" Dialog cancel function.
		"""
		self.dialogReturn = False
		self.ui.accept()
		return #False

