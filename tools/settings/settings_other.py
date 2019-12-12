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
from shared import prompt


class helper():

	def __init__(self, parent, frame):
		""" Setup application properties panel.
		"""
		self.frame = frame

		# Populate line edit with user name
		if self.frame.version_lineEdit.text() == "":
			self.frame.version_lineEdit.setText(os.environ['IC_VERSION'])
