#!/usr/bin/python

# [Icarus] edit_root_paths.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# A dialog for editing filesystem root paths.
# This provides a mechanism for OS portability.


from PySide import QtCore, QtGui
from edit_root_paths_ui import *
import os, sys

# Import custom modules
import osOps

class dialog(QtGui.QDialog):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Connect signals & slots
		self.ui.jobRootPathWin_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathOSX_lineEdit.textChanged.connect(self.updateUI)
		self.ui.jobRootPathLinux_lineEdit.textChanged.connect(self.updateUI)
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.cancel)


	def dialogWindow(self, winPath, osxPath, linuxPath):
		self.dialogReturn = False
		if winPath is not None:
			self.ui.jobRootPathWin_lineEdit.setText(winPath)
		if osxPath is not None:
			self.ui.jobRootPathOSX_lineEdit.setText(osxPath)
		if linuxPath is not None:
			self.ui.jobRootPathLinux_lineEdit.setText(linuxPath)

		self.exec_()


	def updateUI(self):
		""" Disables the OK button if any of the text fields are empty.
		"""
		if self.ui.jobRootPathWin_lineEdit.text() == "" or self.ui.jobRootPathOSX_lineEdit.text() == "" or self.ui.jobRootPathLinux_lineEdit.text() == "":
			self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
		else:
			self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)


	def ok(self):
		self.dialogReturn = True
		# Normalise paths and strip trailing slash
		self.winPath = osOps.absolutePath(self.ui.jobRootPathWin_lineEdit.text()).rstrip('/')
		self.osxPath = osOps.absolutePath(self.ui.jobRootPathOSX_lineEdit.text()).rstrip('/')
		self.linuxPath = osOps.absolutePath(self.ui.jobRootPathLinux_lineEdit.text()).rstrip('/')
		self.accept()
		return #True


	def cancel(self):
		self.dialogReturn = False
		self.accept()
		return #False

