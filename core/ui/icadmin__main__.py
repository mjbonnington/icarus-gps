#!/usr/bin/python

# icadmin__main__.py
# support	:Michael Bonnington - mike.bonnington@gps-ldn.com
# copyright	:Gramercy Park Studios


import os, sys
from PySide import QtCore, QtGui
from icadminUI import *

import env__init__

# initialise icarus environment
env__init__.setEnv()
env__init__.appendSysPaths()

import jobs


class icadminApp(QtGui.QMainWindow):

	def __init__(self, parent = None):
		super(icadminApp, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# create instance of jobs class; load from xml file
		j = jobs.jobs(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'jobs.xml'))

		jobLs = j.joblist.keys()
		jobLs = sorted(jobLs)
		for job in jobLs:
			#self.ui.listWidget_jobs.addItem(job)
			item = QtGui.QListWidgetItem(self.ui.listWidget_jobs)
			item.setText(job)
			item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
			item.setCheckState(QtCore.Qt.Checked)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myApp = icadminApp()

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	myApp.show()
	sys.exit(app.exec_())
