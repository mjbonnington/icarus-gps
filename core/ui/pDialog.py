#!/usr/bin/python

# [Icarus] pDialog.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Launches and controls a generic prompt dialog.


import os, sys
from PySide import QtCore, QtGui
from pDialogUI import *


class dialog(QtGui.QDialog):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Apply UI style sheet
		qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
		with open(qss, "r") as fh:
			self.ui.main_frame.setStyleSheet(fh.read())


	def dialogWindow(self, dialogMsg, dialogTitle, conf=False, modal=True):
		self.ui.message_textEdit.setText(dialogMsg)
		self.setWindowTitle(dialogTitle)
		self.pDialogReturn = False

		if conf:
			self.ui.cancel_pushButton.hide()

		QtCore.QObject.connect(self.ui.ok_pushButton, QtCore.SIGNAL("clicked()"), self.ok)
		QtCore.QObject.connect(self.ui.cancel_pushButton, QtCore.SIGNAL("clicked()"), self.cancel)

		# Qt window flags
		if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
		else:
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

		# Centre window
	#	self.move(QtGui.QDesktopWidget().availableGeometry(1).center() - self.frameGeometry().center())

		if modal:
			self.exec_()
			return self.pDialogReturn
		else:
			self.show()


	def ok(self):
		self.pDialogReturn = True
		self.accept()
		return #True


	def cancel(self):
		self.pDialogReturn = False
		self.accept()
		return #False

