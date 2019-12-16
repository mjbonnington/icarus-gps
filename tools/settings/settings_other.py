#!/usr/bin/python

# [Icarus] settings_other.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019 Gramercy Park Studios
#
# Other (misc.) settings handler.


import os

from Qt import QtCore

# Import custom modules
from shared import os_wrapper


class helper():

	def __init__(self, parent, frame):
		""" Setup application properties panel.
		"""
		self.frame = frame
		self.parent = parent

		# Set icons
		self.frame.elementsLibBrowse_toolButton.setIcon(parent.iconSet('folder-open.svg'))

		# Connect signals & slots
		self.frame.elementsLibBrowse_toolButton.clicked.connect(lambda: self.browseFolder(self.frame.elementsLib_lineEdit))

		# Populate line edit with user name
		if self.frame.version_lineEdit.text() == "":
			self.frame.version_lineEdit.setText(os.environ['IC_VERSION'])


	def browseFolder(self, lineEdit):
		""" Browse for a folder and put the result into the specified
			lineEdit field.
		"""
		starting_dir = os_wrapper.absolutePath(lineEdit.text())
		result = self.parent.folderDialog(starting_dir)
		if result:
			result = os_wrapper.relativePath(result, 'IC_ASSETLIBRARY')
			result = os_wrapper.relativePath(result, 'IC_FILESYSTEM_ROOT')
			lineEdit.setText(result)
