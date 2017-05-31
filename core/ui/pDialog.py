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

from Qt import QtCore, QtGui, QtWidgets, QtCompat


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Prompt Dialog"
WINDOW_OBJECT = "promptDialogUI"

# Set the UI and the stylesheet
UI_FILE = "pDialog_ui.ui"
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
		# if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		# 	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
		# else:
		# 	self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

		# Load UI
		self.ui = QtCompat.load_ui(fname=UI_FILE)
		if STYLESHEET is not None:
			with open(STYLESHEET, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.cancel)



	def dialogWindow(self, dialogMsg, dialogTitle, conf=False, modal=True):
		""" Show the dialog.
		"""
		self.ui.message_textEdit.setText(dialogMsg)
		self.ui.setWindowTitle(dialogTitle)
		self.pDialogReturn = False

		if conf:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).hide()

		if modal:
			self.ui.exec_()
			return self.pDialogReturn
		else:
			self.ui.show()


	def ok(self):
		self.pDialogReturn = True
		self.ui.accept()
		return #True


	def cancel(self):
		self.pDialogReturn = False
		self.ui.accept()
		return #False

