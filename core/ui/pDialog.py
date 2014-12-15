#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:icarus__main__

#laucnhes and controls a generic prompt dialog 

import os, sys
from PySide import QtCore, QtGui
from pDialogUI import *

class dialog(QtGui.QDialog):
	
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.pDialog = self
		self.pDialog.ui = Ui_Dialog()
		self.pDialog.ui.setupUi(self)

		# Apply UI style sheet
		qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
		with open(qss, "r") as fh:
			self.ui.main_frame.setStyleSheet(fh.read())

	def dialogWindow(self, dialogMsg, dialogTitle, conf = False, modal=True):
		self.pDialog.ui.message_textEdit.setText(dialogMsg)
		self.pDialog.setWindowTitle(dialogTitle)
		self.pDialogReturn = False
		if conf:
			self.pDialog.ui.cancel_pushButton.hide()
		QtCore.QObject.connect(self.pDialog.ui.ok_pushButton, QtCore.SIGNAL("clicked()"), self.ok)
		QtCore.QObject.connect(self.pDialog.ui.cancel_pushButton, QtCore.SIGNAL("clicked()"), self.cancel)
		self.pDialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
		if modal:
			self.pDialog.exec_()
			return self.pDialogReturn
		else:
			self.pDialog.show()

	def ok(self):
		self.pDialogReturn = True
		self.pDialog.accept()
		return

	def cancel(self):
		self.pDialogReturn = False
		self.pDialog.accept()
		return
