#!/usr/bin/python

# [Icarus] edit_root_paths.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# A dialog for editing filesystem root paths.
# This provides a mechanism for OS portability.


import os
import sys

from Qt import QtCore, QtWidgets
import ui_template as UI

# Import custom modules
from shared import osOps


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Edit Root Paths"
WINDOW_OBJECT = "editRootPathsUI"

# Set the UI and the stylesheet
UI_FILE = "edit_root_paths_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = False


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Edit Root Paths dialog class.
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
		self.ui.jobRootPathWin_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathOSX_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathLinux_lineEdit.textChanged.connect(self.updateUI)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)


	def display(self, winPath, osxPath, linuxPath, jobsRelPath):
		""" Display the dialog.
		"""
		if winPath is not None:
			self.ui.jobRootPathWin_lineEdit.setText(winPath)
		if osxPath is not None:
			self.ui.jobRootPathOSX_lineEdit.setText(osxPath)
		if linuxPath is not None:
			self.ui.jobRootPathLinux_lineEdit.setText(linuxPath)
		if jobsRelPath is not None:
			self.ui.jobsRelPath_lineEdit.setText(jobsRelPath)

		return self.exec_()


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
		# Normalise paths and strip trailing slash
		self.winPath = osOps.absolutePath(self.ui.jobRootPathWin_lineEdit.text(), stripTrailingSlash=True)
		self.osxPath = osOps.absolutePath(self.ui.jobRootPathOSX_lineEdit.text(), stripTrailingSlash=True)
		self.linuxPath = osOps.absolutePath(self.ui.jobRootPathLinux_lineEdit.text(), stripTrailingSlash=True)
		self.jobsRelPath = self.ui.jobsRelPath_lineEdit.text()
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

