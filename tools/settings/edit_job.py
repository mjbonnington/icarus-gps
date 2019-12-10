#!/usr/bin/python

# [Icarus] edit_job.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# A dialog for editing job settings.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
from shared import os_wrapper
from shared import prompt
from shared import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Edit Job"
WINDOW_OBJECT = "editJobUI"

# Set the UI and the stylesheet
UI_FILE = "edit_job_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = False


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Edit Job dialog class.
	"""
	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		self.conformFormLayoutLabels(self.ui)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.jobName_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPath_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobPathBrowse_toolButton.clicked.connect(self.browseDir)
		self.ui.takeOwnership_toolButton.clicked.connect(self.takeOwnership)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-]+'), self.ui.jobName_lineEdit)
		self.ui.jobName_lineEdit.setValidator(alphanumeric_validator)
		# path_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-/\\\:\$\{\}]+'), self.ui.jobName_lineEdit)
		# self.ui.jobPath_lineEdit.setValidator(path_validator)


	def display(self, jobName, jobPath, jobActive):
		""" Display the dialog.
		"""
		if jobName:
			self.setWindowTitle("%s: %s" %(WINDOW_TITLE, jobName))
		else:
			self.setWindowTitle("Add New Job")
		self.ui.jobName_lineEdit.setText(jobName)
		self.ui.jobPath_lineEdit.setText(jobPath)
		self.ui.jobEnabled_checkBox.setChecked(jobActive)

		self.ui.private_groupBox.hide()  # Private jobs not yet implemented
		self.setFixedHeight(self.minimumSizeHint().height())

		return self.exec_()


	def updateUI(self):
		""" Disables the OK button if either of the text fields are empty or
			the job path is invalid.
		"""
		enable = True
		jobPath = os_wrapper.translatePath(self.ui.jobPath_lineEdit.text())

		if self.ui.jobName_lineEdit.text() == "":
			enable = False
		if self.ui.jobPath_lineEdit.text() == "":
			enable = False
		if not os_wrapper.checkIllegalChars(jobPath):
			verbose.illegalCharacters(jobPath)
			enable = False

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(enable)


	def browseDir(self):
		""" Opens a dialog from which to select a folder.
		"""
		startingDir = os_wrapper.translatePath(self.ui.jobPath_lineEdit.text())
		if os.path.isdir(startingDir):
			dialogHome = startingDir
		else:
			dialogHome = os.environ['IC_JOBSROOT']

		# Append slash to path if it's a Windows drive letter, otherwise file
		# dialog won't open the correct location
		if dialogHome.endswith(':'):
			dialogHome += '/'

		#dialogPath = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)
		##dialog = QtWidgets.QFileDialog(self)
		dialogPath = self.folderDialog(dialogHome)

		if dialogPath:
		# if dialog.exec_():
		# 	dialogPath = dialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)
			if os_wrapper.checkIllegalChars(dialogPath): #, r'[^\w\.-]'):
				jobPath = os_wrapper.relativePath(dialogPath, 'IC_JOBSROOT')
				self.ui.jobPath_lineEdit.setText(jobPath)
				# Only autofill job name field it it's empty
				if not self.ui.jobName_lineEdit.text():
					try:
						# if os.environ['IC_JOBSROOT'] in os_wrapper.absolutePath(jobPath):
						#       jobName = jobPath.split('/')[1]
						# else:
						#       jobName = jobPath.split('/')[-1]
						jobName = os.path.basename(jobPath)
						self.ui.jobName_lineEdit.setText(jobName)
					except IndexError:
						pass

			else:
				verbose.illegalCharacters(dialogPath)

				# Warning dialog
				dialogTitle = "Path contains illegal characters"
				dialogMsg = "The path \"%s\" contains illegal characters. File and folder names must be formed of alphanumeric characters, underscores, hyphens and dots only." %dialogPath
				dialog = prompt.dialog()
				dialog.display(dialogMsg, dialogTitle, conf=True)

		# return dialogPath
		#self.ui.raise_()  # Keep the dialog in front


	def takeOwnership(self):
		""" Sets the owner of the job to the current user.
		"""
		self.ui.owner_lineEdit.setText(os.environ['IC_USERNAME'])


	def ok(self):
		""" Dialog accept function.
		"""
		self.jobName = self.ui.jobName_lineEdit.text()
		self.jobPath = self.ui.jobPath_lineEdit.text()
		if self.ui.jobEnabled_checkBox.checkState() == QtCore.Qt.Checked:
			self.jobActive = True
		else:
			self.jobActive = False
		self.accept()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			return


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.storeWindow()  # Store window geometry

