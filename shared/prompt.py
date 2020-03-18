#!/usr/bin/python

# [Icarus] prompt.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Launches and controls a generic prompt dialog.


import os
import sys

from Qt import QtCore, QtWidgets

# Import custom modules
import ui_template as UI


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

cfg = {}

# Set window title and object names
cfg['window_title'] = "Prompt Dialog"
cfg['window_object'] = "promptDialogUI"

# Set the UI and the stylesheet
cfg['ui_file'] = 'prompt.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
cfg['store_window_geometry'] = False

# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class Dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Prompt dialog class.
	"""
	def __init__(self, parent=None):
		super(Dialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)

		# Set other Qt attributes
		# self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)


	def display(
		self, 
		message, 
		title=cfg['window_title'], 
		conf=False, 
		modal=True):
		""" Display the dialog with the specified message.

			'title' - sets the title of the dialog window.
			'conf' - a confirmation dialog with only an OK button.
			'modal' - a modal dialog (default)
		"""
		self.ui.message_textEdit.setText(message)
		self.setWindowTitle(title)

		if conf:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).hide()

		if modal:
			return self.exec_()
		else:
			self.show()
