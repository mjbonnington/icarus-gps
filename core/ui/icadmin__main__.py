#!/usr/bin/python

# icadmin__main__.py
# support	: Michael Bonnington - mike.bonnington@gps-ldn.com
# copyright	: Gramercy Park Studios


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

		#jobLs = j.joblist.keys()
		#jobLs = sorted(jobLs)
		for i in range(len(j.joblist)):
			#self.ui.jobs_listWidget.addItem(job)
			item = QtGui.QTreeWidgetItem(self.ui.jobs_treeWidget)
			item.setText(0, j.joblist.keys()[i]) # populate name column
			item.setText(1, j.joblist.values()[i][0]) # populate path column
			#item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
			if j.joblist.values()[i][1] == 'True':
				item.setCheckState(0, QtCore.Qt.Checked)
			else:
				item.setCheckState(0, QtCore.Qt.Unchecked)


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myApp = icadminApp()

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	myApp.show()
	sys.exit(app.exec_())
