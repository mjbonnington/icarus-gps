#!/usr/bin/python

# [Icarus] pDialog.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Launches and controls a generic prompt dialog.


import os
import sys

from Qt import QtCompat, QtCore, QtWidgets


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Prompt Dialog"
WINDOW_OBJECT = "promptDialogUI"

# Set the UI and the stylesheet
UI_FILE = "pDialog_ui.ui"
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
		# self.setWindowFlags(QtCore.Qt.Dialog)
		self.ui.setWindowFlags(QtCore.Qt.CustomizeWindowHint | 
			                   QtCore.Qt.WindowTitleHint)
		# if os.environ['IC_RUNNING_OS'] == 'Darwin':
		# 	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
		# 	                    QtCore.Qt.X11BypassWindowManagerHint | 
		# 	                    QtCore.Qt.WindowCloseButtonHint)
		# else:
		# 	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | 
		# 		                QtCore.Qt.WindowCloseButtonHint)

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)


	def display(self, message, title=WINDOW_TITLE, conf=False, modal=True):
		""" Display the dialog with the specified message.
			'title' - sets the title of the dialog window.
			'conf' - a confirmation dialog with only an OK button.
			'modal' - a modal dialog (default)
		"""
		self.ui.message_textEdit.setText(message)
		self.ui.setWindowTitle(title)
		self.returnValue = False

		if conf:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).hide()

		if modal:
			self.ui.exec_()
			return self.returnValue
		else:
			self.ui.show()


	def ok(self):
		""" Dialog accept function.
		"""
		self.returnValue = True
		self.ui.accept()


	def cancel(self):
		""" Dialog cancel function.
		"""
		self.returnValue = False
		self.ui.reject()

