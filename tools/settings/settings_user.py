#!/usr/bin/python

# [Icarus] settings_user.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019 Gramercy Park Studios
#
# User settings handler.


import os

from Qt import QtCore

# Import custom modules
from shared import os_wrapper
from shared import prompt


class helper():

	def __init__(self, parent, frame):
		""" Setup application properties panel.
		"""
		self.frame = frame
		self.verbosity_level = [
			"No output", 
			"Errors and messages requiring user action", 
			"Errors and warning messages", 
			"Info and progress messages (default)", 
			"Detailed info messages"]

		# Populate line edit with user name
		self.frame.user_lineEdit.setText(os.getenv('IC_USERNAME', ''))

		# Connect signals & slots
		self.frame.verbosity_spinBox.valueChanged.connect(lambda index: self.updateVerbosityInfo(index))
		self.frame.clearRecentFiles_pushButton.clicked.connect(lambda: self.clearRecentFiles())  # Only works with a lambda for some reason

		self.frame.clearRecentFiles_pushButton.setEnabled(False)  # Temporarily disabling as it can case problems


	@QtCore.Slot(int)
	def updateVerbosityInfo(self, index):
		""" Update info label with the verbosity level.
		"""
		self.frame.verbosityInfo_label.setText(self.verbosity_level[index])


	def clearRecentFiles(self):
		""" Clear all recent files.
		"""
		dialog = prompt.Dialog()
		message = "About to delete all recent files information. Are you sure?"
		if dialog.display(message, "Confirm"):
			success, msg = os_wrapper.remove(os.environ['IC_RECENTFILESDIR'])
			if not success:
				dialog.display(msg, "Error", conf=True)
