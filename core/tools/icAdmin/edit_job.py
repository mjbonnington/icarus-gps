#!/usr/bin/python

# [Icarus] edit_job.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2017 Gramercy Park Studios
#
# A dialog for editing job settings.


import os
import sys

from Qt import QtCompat, QtCore, QtGui, QtWidgets

# Import custom modules
import osOps
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Edit Job"
WINDOW_OBJECT = "editJobUI"

# Set the UI and the stylesheet
UI_FILE = "edit_job_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet


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

		# Load UI & stylesheet
		self.ui = QtCompat.load_ui(fname=os.path.join(os.environ['IC_FORMSDIR'], UI_FILE))
		if STYLESHEET is not None:
			qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
			with open(qss, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Connect signals & slots
		self.ui.jobName_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPath_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPathBrowse_toolButton.clicked.connect(self.browseDir)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-]+'), self.ui.jobName_lineEdit)
		self.ui.jobName_lineEdit.setValidator(alphanumeric_validator)
		# path_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-/\\\:\$\{\}]+'), self.ui.jobName_lineEdit)
		# self.ui.jobPath_lineEdit.setValidator(path_validator)


	def display(self, jobName, jobPath, jobActive):
		""" Display the dialog.
		"""
		self.returnValue = False

		if jobName:
			self.ui.setWindowTitle("%s: %s" %(WINDOW_TITLE, jobName))
		else:
			self.ui.setWindowTitle("Add New Job")
		self.ui.jobName_lineEdit.setText(jobName)
		self.ui.jobPath_lineEdit.setText(jobPath)
		self.ui.jobEnabled_checkBox.setChecked(jobActive)

		self.ui.exec_()
		return self.returnValue


	def updateUI(self):
		""" Disables the OK button if either of the text fields are empty or
			the job path is invalid.
		"""
		enable = True
		jobPath = osOps.translatePath(self.ui.jobPath_lineEdit.text())

		if self.ui.jobName_lineEdit.text() == "":
			enable = False
		if self.ui.jobPath_lineEdit.text() == "":
			enable = False
		if not osOps.checkIllegalChars(jobPath):
			verbose.illegalCharacters(jobPath)
			enable = False

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(enable)


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
			if osOps.checkIllegalChars(dialogPath): #, r'[^\w\.-]'):
				jobPath = osOps.relativePath(dialogPath, 'JOBSROOT')
				self.ui.jobPath_lineEdit.setText(jobPath)
				# Only autofill job name field it it's empty
				if not self.ui.jobName_lineEdit.text():
					try:
						# if os.environ['JOBSROOT'] in osOps.absolutePath(jobPath):
						#       jobName = jobPath.split('/')[1]
						# else:
						#       jobName = jobPath.split('/')[-1]
						jobName = jobPath.split('/')[1]
						self.ui.jobName_lineEdit.setText(jobName)
					except IndexError:
						pass

			else:
				verbose.illegalCharacters(dialogPath)

				# Warning dialog
				import pDialog
				dialogTitle = "Path contains illegal characters"
				dialogMsg = "The path \"%s\" contains illegal characters. File and folder names must be formed of alphanumeric characters, underscores, hyphens and dots only." %dialogPath
				dialog = pDialog.dialog()
				dialog.display(dialogMsg, dialogTitle, conf=True)

		# return dialogPath
		self.ui.raise_()  # Keep the dialog in front


	def ok(self):
		""" Dialog accept function.
		"""
		self.returnValue = True
		self.jobName = self.ui.jobName_lineEdit.text()
		self.jobPath = self.ui.jobPath_lineEdit.text()
		if self.ui.jobEnabled_checkBox.checkState() == QtCore.Qt.Checked:
			self.jobActive = True
		else:
			self.jobActive = False
		self.ui.accept()


	def cancel(self):
		""" Dialog cancel function.
		"""
		self.returnValue = False
		self.ui.reject()

