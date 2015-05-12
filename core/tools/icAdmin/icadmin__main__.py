#!/usr/bin/python

# icadmin__main__.py
# support	: Michael Bonnington - mike.bonnington@gps-ldn.com
# copyright	: Gramercy Park Studios

# Icarus Admin Tool.


import os, sys
from PySide import QtCore, QtGui
from icadminUI import *

# Initialise icarus environment
sys.path.append(os.environ['ICWORKINGDIR'])
import env__init__
env__init__.setEnv()
env__init__.appendSysPaths()

import jobs, appPaths


class icadminApp(QtGui.QMainWindow):

	def __init__(self, parent = None):
		super(icadminApp, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.init()

		# Connect signals and slots
		#QtCore.QObject.connect(self.ui.jobs_treeWidget, QtCore.SIGNAL('itemClicked(QTreeWidgetItem *, int)'), self.populateShotAttr)
		#QtCore.QObject.connect(self.ui.jobs_treeWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.populateShotAttr)
		QtCore.QObject.connect(self.ui.jobs_listWidget, QtCore.SIGNAL('itemSelectionChanged()'), self.populateJobAttr)

		QtCore.QObject.connect(self.ui.jobAdd_toolButton, QtCore.SIGNAL('clicked()'), self.addJob)
		QtCore.QObject.connect(self.ui.jobDelete_toolButton, QtCore.SIGNAL('clicked()'), self.deleteJob)

		QtCore.QObject.connect(self.ui.appName_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.populateAppVersions)
		QtCore.QObject.connect(self.ui.appVer_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.populateAppExecPaths)
		QtCore.QObject.connect(self.ui.appNameDel_toolButton, QtCore.SIGNAL('clicked()'), self.deleteApp)
		QtCore.QObject.connect(self.ui.appVerDel_toolButton, QtCore.SIGNAL('clicked()'), self.deleteAppVersion)
		QtCore.QObject.connect(self.ui.osxPath_lineEdit, QtCore.SIGNAL('editingFinished()'), self.saveAppPathOSX)
		QtCore.QObject.connect(self.ui.linuxPath_lineEdit, QtCore.SIGNAL('editingFinished()'), self.saveAppPathLinux)
		QtCore.QObject.connect(self.ui.winPath_lineEdit, QtCore.SIGNAL('editingFinished()'), self.saveAppPathWin)
		QtCore.QObject.connect(self.ui.guess_pushButton, QtCore.SIGNAL('clicked()'), self.guessAppPaths)

		QtCore.QObject.connect(self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Reset), QtCore.SIGNAL('clicked()'), self.init)
		QtCore.QObject.connect(self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Save), QtCore.SIGNAL('clicked()'), self.ap.saveXML)

		QtCore.QObject.connect(self.ui.main_buttonBox.button(QtGui.QDialogButtonBox.Close), QtCore.SIGNAL('clicked()'), self.exit)


	def init(self):
		# Load data from xml file
		self.jd = jobs.jobs(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'jobs.xml'))
		self.ap = appPaths.appPaths(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'appPaths.xml'))

		# Initialisation
		#jobLs = j.joblist.keys()
		#jobLs = sorted(jobLs)
		self.jd.readjobs()
		for i in range(len(self.jd.joblist)):
			#self.ui.jobs_listWidget.addItem(job)
			item = QtGui.QListWidgetItem(self.ui.jobs_listWidget)
			item.setText(self.jd.joblist.keys()[i])
			#item.setText(self.jd.joblist.keys()[i].replace( '_', ' ' )) # populate name column
			#item.setText(1, j.joblist.values()[i][0]) # populate path column
			#item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
			if self.jd.joblist.values()[i][1] == 'True':
				item.setCheckState(QtCore.Qt.Checked)
			else:
				item.setCheckState(QtCore.Qt.Unchecked)
				#item.setForeground(0, QtGui.QColor(102,102,102))

		# Clear app menu and populate with apps
		self.ui.appName_comboBox.clear()
		for app in self.ap.getApps():
			self.ui.appName_comboBox.addItem(app)

		self.populateAppVersions()
		self.populateAppExecPaths()


	def populateJobAttr(self):
		if (self.ui.jobs_listWidget.count() <= 1) or (self.ui.jobs_listWidget.currentItem().text() == '[defaults]'):
			self.ui.jobDelete_toolButton.setEnabled(False)
		else:
			self.ui.jobDelete_toolButton.setEnabled(True)

		for item in self.ui.jobs_listWidget.selectedItems():
			self.ui.jobPath_lineEdit.text = "/path/to/..." # if multi select display if values are identical

		#self.ui.jobActive_checkBox.setCheckState(QtCore.Qt.Checked)



	def addJob(self):
		#self.ui.jobs_listWidget.addItem('000000_New_Job')
		item = QtGui.QListWidgetItem(self.ui.jobs_listWidget)
		item.setText('000000_New_Job')
		item.setCheckState(QtCore.Qt.Checked)
		item.setSelected(True)


	def deleteJob(self):
		for item in self.ui.jobs_listWidget.selectedItems():
			if item.text() == '[defaults]':
				print "Warning: job defaults cannot be deleted."
			else:
				self.jd.rm( item.text() )
				self.ui.jobs_listWidget.takeItem( self.ui.jobs_listWidget.row(item) )


	def toggleAppVerDelButton(self):
		if (self.ui.appVer_comboBox.count() == 0) or (self.ui.appVer_comboBox.currentText() == '[template]'):
			self.ui.appVerDel_toolButton.setEnabled(False)
		else:
			self.ui.appVerDel_toolButton.setEnabled(True)


	def populateAppVersions(self):
		# Clear menu
		self.ui.appVer_comboBox.clear()

		# Populate menu with associated app versions
		for version in self.ap.getVersions( self.ui.appName_comboBox.currentText() ):
			self.ui.appVer_comboBox.addItem(version)
			#self.ui.appVer_comboBox.insertItem(0, version) # Add to start

		# Select last item
		self.ui.appVer_comboBox.setCurrentIndex(self.ui.appVer_comboBox.count()-1)

		# Enable/disable delete button
		if self.ui.appName_comboBox.count():
			self.ui.appNameDel_toolButton.setEnabled(True)
			self.ui.appVer_comboBox.setEnabled(True)
		else:
			self.ui.appNameDel_toolButton.setEnabled(False)
			self.ui.appVer_comboBox.setEnabled(False)


	def populateAppExecPaths(self):
		# Enable/disable delete button
		if self.ui.appVer_comboBox.count():
			if self.ui.appVer_comboBox.currentText() == '[template]':
				self.ui.appVerDel_toolButton.setEnabled(False)
				self.ui.guess_pushButton.setEnabled(False)
			else:
				self.ui.appVerDel_toolButton.setEnabled(True)
				self.ui.guess_pushButton.setEnabled(True)
			self.ui.execPaths_groupBox.setEnabled(True)
		else:
			self.ui.appVerDel_toolButton.setEnabled(False)
			self.ui.execPaths_groupBox.setEnabled(False)

		self.ui.osxPath_lineEdit.setText( self.ap.getPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'osx' ) )
		self.ui.linuxPath_lineEdit.setText( self.ap.getPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'linux' ) )
		self.ui.winPath_lineEdit.setText( self.ap.getPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'win' ) )


	def deleteApp(self):
		self.ap.deleteApp( self.ui.appName_comboBox.currentText() )
		self.ui.appName_comboBox.removeItem( self.ui.appName_comboBox.currentIndex() )
		#self.populateAppVersions()


	def deleteAppVersion(self):
		self.ap.deleteVersion( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText() )
		self.ui.appVer_comboBox.removeItem( self.ui.appVer_comboBox.currentIndex() )
		#self.populateAppExecPaths()


	def saveAppPathOSX(self):
		self.ap.setPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'osx', self.ui.osxPath_lineEdit.text() )


	def saveAppPathLinux(self):
		self.ap.setPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'linux', self.ui.linuxPath_lineEdit.text() )


	def saveAppPathWin(self):
		self.ap.setPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'win', self.ui.winPath_lineEdit.text() )


	def guessAppPaths(self):
		osxGuess = self.ap.guessPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'osx' )
		if osxGuess:
			self.ui.osxPath_lineEdit.setText(osxGuess)
			self.saveAppPathOSX()

		linuxGuess = self.ap.guessPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'linux' )
		if linuxGuess:
			self.ui.linuxPath_lineEdit.setText(linuxGuess)
			self.saveAppPathLinux()

		winGuess = self.ap.guessPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'win' )
		if winGuess:
			self.ui.winPath_lineEdit.setText(winGuess)
			self.saveAppPathWin()


	def exit(self):
		# Add confirmation dialog if data has changed
		sys.exit()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myApp = icadminApp()

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	myApp.show()
	sys.exit(app.exec_())
