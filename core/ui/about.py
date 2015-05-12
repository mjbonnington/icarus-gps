#!/usr/bin/python

# Icarus About Dialog
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios


from PySide import QtCore, QtGui
from aboutUI import *
import sys


class aboutDialog(QtGui.QDialog):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		#super(aboutDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Connect signals and slots


	def mousePressEvent(self, QMouseEvent):
		""" Close about dialog if mouse is clicked
		"""
		self.hide()


	def msg(self, msg):
		""" Display message in about dialog
		"""
		self.ui.aboutMessage_label.setText(msg)
		self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
		self.show()
		self.exec_()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	about = aboutDialog()

	#about.setWindowFlags(QtCore.Qt.FramelessWindowHint)
	about.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.WindowStaysOnTopHint)
	about.show()
	sys.exit(about.exec_())
