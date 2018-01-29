#!/usr/bin/python

# [Icarus] prompt_dialog.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# Launches and controls a generic prompt dialog.


import os
import sys

from Qt import QtCore, QtWidgets
import ui_template as UI


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Prompt Dialog"
WINDOW_OBJECT = "promptDialogUI"

# Set the UI and the stylesheet
UI_FILE = "pDialog_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = False


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Prompt dialog class.
	"""
	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | 
		                    QtCore.Qt.WindowTitleHint)
		# if os.environ['IC_RUNNING_OS'] == 'Darwin':
		# 	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
		# 	                    QtCore.Qt.X11BypassWindowManagerHint | 
		# 	                    QtCore.Qt.WindowCloseButtonHint)
		# else:
		# 	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
		# 	                    QtCore.Qt.WindowCloseButtonHint)

		# Set other Qt attributes
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)


	def display(self, message, title=WINDOW_TITLE, conf=False, modal=True):
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

