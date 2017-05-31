#!/usr/bin/python

# [Icarus] edit_root_paths.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2017 Gramercy Park Studios
#
# A dialog for editing filesystem root paths.
# This provides a mechanism for OS portability.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets, QtCompat

# Import custom modules
import osOps


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Edit Root Paths"
WINDOW_OBJECT = "editRootPathsUI"

# Set the UI and the stylesheet
UI_FILE = "edit_root_paths_ui.ui"
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
		self.ui.jobRootPathWin_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathOSX_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathLinux_lineEdit.textChanged.connect(self.updateUI)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)


	def dialogWindow(self, winPath, osxPath, linuxPath, jobsRelPath):
		""" Show the dialog.
		"""
		self.dialogReturn = False

		if winPath is not None:
			self.ui.jobRootPathWin_lineEdit.setText(winPath)
		if osxPath is not None:
			self.ui.jobRootPathOSX_lineEdit.setText(osxPath)
		if linuxPath is not None:
			self.ui.jobRootPathLinux_lineEdit.setText(linuxPath)
		if jobsRelPath is not None:
			self.ui.jobsRelPath_lineEdit.setText(jobsRelPath)

		self.ui.exec_()


	def updateUI(self):
		""" Disables the OK button if any of the text fields are empty.
		"""
		if self.ui.jobRootPathWin_lineEdit.text() == "" or self.ui.jobRootPathOSX_lineEdit.text() == "" or self.ui.jobRootPathLinux_lineEdit.text() == "":
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
		else:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)


	def ok(self):
		""" Dialog accept function.
		"""
		self.dialogReturn = True
		# Normalise paths and strip trailing slash
		self.winPath = osOps.absolutePath(self.ui.jobRootPathWin_lineEdit.text(), stripTrailingSlash=True)
		self.osxPath = osOps.absolutePath(self.ui.jobRootPathOSX_lineEdit.text(), stripTrailingSlash=True)
		self.linuxPath = osOps.absolutePath(self.ui.jobRootPathLinux_lineEdit.text(), stripTrailingSlash=True)
		self.jobsRelPath = self.ui.jobsRelPath_lineEdit.text()
		self.ui.accept()
		return #True


	def cancel(self):
		""" Dialog cancel function.
		"""
		self.dialogReturn = False
		self.ui.accept()
		return #False

