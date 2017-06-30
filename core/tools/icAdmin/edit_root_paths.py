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

from Qt import QtCompat, QtCore, QtWidgets

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
		self.ui.jobRootPathWin_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathOSX_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathLinux_lineEdit.textChanged.connect(self.updateUI)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)


	def display(self, winPath, osxPath, linuxPath, jobsRelPath):
		""" Display the dialog.
		"""
		self.returnValue = False

		if winPath is not None:
			self.ui.jobRootPathWin_lineEdit.setText(winPath)
		if osxPath is not None:
			self.ui.jobRootPathOSX_lineEdit.setText(osxPath)
		if linuxPath is not None:
			self.ui.jobRootPathLinux_lineEdit.setText(linuxPath)
		if jobsRelPath is not None:
			self.ui.jobsRelPath_lineEdit.setText(jobsRelPath)

		self.ui.exec_()
		return self.returnValue


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
		self.returnValue = True
		# Normalise paths and strip trailing slash
		self.winPath = osOps.absolutePath(self.ui.jobRootPathWin_lineEdit.text(), stripTrailingSlash=True)
		self.osxPath = osOps.absolutePath(self.ui.jobRootPathOSX_lineEdit.text(), stripTrailingSlash=True)
		self.linuxPath = osOps.absolutePath(self.ui.jobRootPathLinux_lineEdit.text(), stripTrailingSlash=True)
		self.jobsRelPath = self.ui.jobsRelPath_lineEdit.text()
		self.ui.accept()


	def cancel(self):
		""" Dialog cancel function.
		"""
		self.returnValue = False
		self.ui.reject()

