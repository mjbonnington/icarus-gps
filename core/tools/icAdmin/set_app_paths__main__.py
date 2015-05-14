#!/usr/bin/python

# Icarus Admin Tools
# Set App Paths dialog
# v0.2
#
# Michael Bonnington 2015
# Gramercy Park Studios


from PySide import QtCore, QtGui
from set_app_paths_ui import *
import os, sys

# Initialise Icarus environment
sys.path.append(os.environ['ICWORKINGDIR'])
import env__init__
env__init__.setEnv()
env__init__.appendSysPaths()

import appPaths


class setAppPathsDialog(QtGui.QDialog):

	def __init__(self, parent = None):
		#QtGui.QDialog.__init__(self, parent)
		super(setAppPathsDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.init()

		#self.ui.appName_comboBox.setProperty("mandatoryField", True)
		#self.ui.appVer_comboBox.setProperty("mandatoryField", True)

		# Set up keyboard shortcuts
		self.shortcut = QtGui.QShortcut(self)
		self.shortcut.setKey('Ctrl+S')
		self.shortcut.activated.connect(self.saveAppPaths)

		# Connect signals and slots (new style)
		self.ui.appName_comboBox.currentIndexChanged.connect(self.populateAppVersions)
		self.ui.appVer_comboBox.currentIndexChanged.connect(self.populateAppExecPaths)
		self.ui.appNameDel_toolButton.clicked.connect(self.deleteApp)
		self.ui.appVerDel_toolButton.clicked.connect(self.deleteAppVersion)
		self.ui.osxPath_lineEdit.editingFinished.connect(self.storeAppPathOSX)
		self.ui.linuxPath_lineEdit.editingFinished.connect(self.storeAppPathLinux)
		self.ui.winPath_lineEdit.editingFinished.connect(self.storeAppPathWin)
		self.ui.guess_pushButton.clicked.connect(self.guessAppPaths)

		#self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.init)
		#self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.saveAppPaths)
		self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.exit)
		self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)


	def init(self):
		""" Initialise or reset by reloading data
		"""
		# Load data from xml file
		self.ap = appPaths.appPaths()
		ap_load = self.ap.loadXML(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'appPaths.xml'))

		# Populate fields
		self.populateApps()
		self.populateAppVersions()
		self.populateAppExecPaths()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering OK / Cancel buttons
		"""
		pass
#		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
#			return


	def toggleAppVerDelButton(self):
		""" Enable or disable the application version delete button as required
		"""
		if (self.ui.appVer_comboBox.count() == 0) or (self.ui.appVer_comboBox.currentText() == '[template]'):
			self.ui.appVerDel_toolButton.setEnabled(False)
		else:
			self.ui.appVerDel_toolButton.setEnabled(True)


	def populateApps(self):
		""" Populate application name combo box
		"""
		# Clear menu
		self.ui.appName_comboBox.clear()

		# Populate menu with apps
		for app in self.ap.getApps():
			self.ui.appName_comboBox.addItem(app)


	def populateAppVersions(self):
		""" Populate application version combo box
		"""
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
		""" Populate application executable paths for each OS
		"""
		# Enable/disable delete button
		if self.ui.appVer_comboBox.count():
			if self.ui.appVer_comboBox.currentText() == '[template]':
				self.ui.appVerDel_toolButton.setEnabled(False)
				self.ui.guess_pushButton.setEnabled(False)
			else:
				self.ui.appVerDel_toolButton.setEnabled(True)
				self.ui.guess_pushButton.setEnabled(True)
			self.ui.execPaths_groupBox.setEnabled(True)
			self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(True)
		else:
			self.ui.appVerDel_toolButton.setEnabled(False)
			self.ui.execPaths_groupBox.setEnabled(False)
			self.ui.appPaths_buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(False)

		self.ui.osxPath_lineEdit.setText( self.ap.getPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'osx' ) )
		self.ui.linuxPath_lineEdit.setText( self.ap.getPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'linux' ) )
		self.ui.winPath_lineEdit.setText( self.ap.getPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'win' ) )


	def deleteApp(self):
		""" Delete an entry for an application
		"""
		self.ap.deleteApp( self.ui.appName_comboBox.currentText() )
		self.populateApps()
		self.populateAppVersions()


	def deleteAppVersion(self):
		""" Delete an entry for a version of an application
		"""
		self.ap.deleteVersion( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText() )
		self.populateAppVersions()
		self.populateAppExecPaths()


	def storeAppPathOSX(self):
		""" Store Mac OS X executable path when relevant field is updated
		"""
		self.ap.setPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'osx', self.ui.osxPath_lineEdit.text() )
		#print "%s %s - Mac OS X executable path set to %s" %( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), self.ui.osxPath_lineEdit.text() )


	def storeAppPathLinux(self):
		""" Store Linux executable path when relevant field is updated
		"""
		self.ap.setPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'linux', self.ui.linuxPath_lineEdit.text() )
		#print "%s %s - Linux executable path set to %s" %( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), self.ui.linuxPath_lineEdit.text() )


	def storeAppPathWin(self):
		""" Store Windows executable path when relevant field is updated
		"""
		self.ap.setPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'win', self.ui.winPath_lineEdit.text() )
		#print "%s %s - Windows executable path set to %s" %( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), self.ui.winPath_lineEdit.text() )


	def guessAppPaths(self):
		""" Guess the executable paths for each OS based on the [template] entry (if it exists)
		"""
		osxGuess = self.ap.guessPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'osx' )
		if osxGuess:
			self.ui.osxPath_lineEdit.setText(osxGuess)
			self.storeAppPathOSX()

		linuxGuess = self.ap.guessPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'linux' )
		if linuxGuess:
			self.ui.linuxPath_lineEdit.setText(linuxGuess)
			self.storeAppPathLinux()

		winGuess = self.ap.guessPath( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), 'win' )
		if winGuess:
			self.ui.winPath_lineEdit.setText(winGuess)
			self.storeAppPathWin()


	def saveAppPaths(self):
		""" Save the application paths to the data file
		"""
		self.storeAppPathOSX()
		self.storeAppPathLinux()
		self.storeAppPathWin()
		if self.ap.saveXML():
			print "Application paths data file saved."
			return True
		else:
			print "Warning: Application paths data file could not be saved."
			return False


	def saveAndExit(self):
		""" Save data and exit
		"""
		if self.saveAppPaths():
			self.exit()


	def exit(self):
		""" Exit the dialog
		"""
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	setAppPaths = setAppPathsDialog()

	setAppPaths.show()
	sys.exit(setAppPaths.exec_())

