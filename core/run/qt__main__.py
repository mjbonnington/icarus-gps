#!/usr/bin/python

# [Icarus] source_filename.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2018 Gramercy Park Studios
#
# Description.


# If running as standalone app, initialise Icarus environment and add libs to
# sys path
if __name__ == "__main__":
	import env__init__
	env__init__.setEnv()

import os
import sys

from Qt import QtCompat, QtCore, QtGui, QtWidgets
#import ui_template as UI

# Import custom modules


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Test Dialog"
WINDOW_OBJECT = "testDialogUI"

# Set the UI and the stylesheet
UI_FILE = "edit_root_paths_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog):

	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Load UI
		uifile = os.path.join(os.environ['IC_FORMSDIR'], UI_FILE)
		self.ui = QtCompat.loadUi(uifile, self)

		if STYLESHEET is not None:
			qss = os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
			with open(qss, "r") as fh:
				self.setStyleSheet(fh.read())

		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle(WINDOW_TITLE)

		# Connect signals & slots
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)

		self.exec_()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	myDialog = dialog()  # Replace 'dialog' with the name of your app
	sys.exit(app.exec_())

else:
	myDialog = dialog()  # Replace 'dialog' with the name of your app

