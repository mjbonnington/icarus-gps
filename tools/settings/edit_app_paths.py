#!/usr/bin/python

# [Icarus] edit_app_paths.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2019
#
# A UI for managing application versions and paths to executables for all
# operating systems.


import os
import sys

from Qt import QtCore, QtWidgets

# Import custom modules
import ui_template as UI

from shared import appPaths
from shared import verbose

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

cfg = {}

# Set window title and object names
cfg['window_title'] = "Edit Application Paths"
cfg['window_object'] = "editAppPathsUI"

# Set the UI and the stylesheet
cfg['ui_file'] = 'edit_app_paths.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

cfg['store_window_geometry'] = True

# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Edit App Paths dialog class.
	"""
	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)

		self.conformFormLayoutLabels(self.ui)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Set up keyboard shortcuts
		self.shortcut = QtWidgets.QShortcut(self)
		self.shortcut.setKey('Ctrl+S')
		self.shortcut.activated.connect(self.saveAppPaths)

		# Set icons
		self.ui.appNameDel_toolButton.setIcon(self.iconSet('edit-delete.svg'))
		self.ui.appVerDel_toolButton.setIcon(self.iconSet('edit-delete.svg'))
		self.ui.winPathBrowse_toolButton.setIcon(self.iconSet('folder-open.svg'))
		self.ui.osxPathBrowse_toolButton.setIcon(self.iconSet('folder-open.svg'))
		self.ui.linuxPathBrowse_toolButton.setIcon(self.iconSet('folder-open.svg'))

		# Connect signals & slots
		self.ui.appName_comboBox.currentIndexChanged.connect(self.populateAppVersions)
		self.ui.appVer_comboBox.currentIndexChanged.connect(self.populateAppExecPaths)
		self.ui.appNameDel_toolButton.clicked.connect(self.deleteApp)
		self.ui.appVerDel_toolButton.clicked.connect(self.deleteAppVersion)
		self.ui.winPath_lineEdit.editingFinished.connect(self.storeAppPathWin)
		self.ui.osxPath_lineEdit.editingFinished.connect(self.storeAppPathOSX)
		self.ui.linuxPath_lineEdit.editingFinished.connect(self.storeAppPathLinux)
		self.ui.winPathBrowse_toolButton.clicked.connect(lambda: self.browseAppExec(self.ui.winPath_lineEdit))
		self.ui.osxPathBrowse_toolButton.clicked.connect(lambda: self.browseAppExec(self.ui.osxPath_lineEdit))
		self.ui.linuxPathBrowse_toolButton.clicked.connect(lambda: self.browseAppExec(self.ui.linuxPath_lineEdit))
		self.ui.guess_pushButton.clicked.connect(self.guessAppPaths)

		#self.ui.appPaths_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
		#self.ui.appPaths_buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.saveAppPaths)
		self.ui.appPaths_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)
		self.ui.appPaths_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)

		# Enable app exec path browse button for the current OS only
		if os.environ['IC_RUNNING_OS'] == "Windows":
			self.ui.winPathBrowse_toolButton.setEnabled(True)
		elif os.environ['IC_RUNNING_OS'] == "MacOS":
			self.ui.osxPathBrowse_toolButton.setEnabled(True)
		elif os.environ['IC_RUNNING_OS'] == "Linux":
			self.ui.linuxPathBrowse_toolButton.setEnabled(True)

		# Instantiate jobs class and load data
		self.ap = appPaths.AppPaths()


	def display(self):
		""" Initialise or reset by reloading data.
		"""
		# Load data from xml file
		self.ap.loadXML(
			os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), 
			use_template=True)

		# Populate fields
		self.populateApps()
		self.populateAppVersions()
		self.populateAppExecPaths()

		return self.exec_()


	def browseAppExec(self, lineEdit):
		""" Browse for a applivation executable and put the result into the
			specified lineEdit field.
		"""
		starting_dir = os.path.dirname(lineEdit.text())
		result = self.fileDialog(starting_dir)
		if result:
			lineEdit.setText(result)


	def toggleAppVerDelButton(self):
		""" Enable or disable the application version delete button as
			required.
		"""
		if (self.ui.appVer_comboBox.count() == 0) \
		or (self.ui.appVer_comboBox.currentText() == '[template]'):
			self.ui.appVerDel_toolButton.setEnabled(False)
		else:
			self.ui.appVerDel_toolButton.setEnabled(True)


	def populateApps(self):
		""" Populate application name combo box.
		"""
		# Clear menu
		self.ui.appName_comboBox.clear()

		# Populate menu with apps
		for app in self.ap.getAppNames():
			self.ui.appName_comboBox.addItem(app)


	def populateAppVersions(self):
		""" Populate application version combo box.
		"""
		# Clear menu
		self.ui.appVer_comboBox.clear()

		# Populate menu with associated app versions
		for version in self.ap.getVersions(self.ui.appName_comboBox.currentText()):
			self.ui.appVer_comboBox.addItem(version)
			#self.ui.appVer_comboBox.insertItem(0, version)  # Add to start

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
		""" Populate application executable paths for each OS.
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
			self.ui.appPaths_buttonBox.button(
				QtWidgets.QDialogButtonBox.Save).setEnabled(True)
		else:
			self.ui.appVerDel_toolButton.setEnabled(False)
			self.ui.execPaths_groupBox.setEnabled(False)
			self.ui.appPaths_buttonBox.button(
				QtWidgets.QDialogButtonBox.Save).setEnabled(False)

		self.ui.osxPath_lineEdit.setText(
			self.ap.getPath(
				self.ui.appName_comboBox.currentText(), 
				self.ui.appVer_comboBox.currentText(), 'osx' ))
		self.ui.linuxPath_lineEdit.setText(
			self.ap.getPath(
				self.ui.appName_comboBox.currentText(), 
				self.ui.appVer_comboBox.currentText(), 'linux' ))
		self.ui.winPath_lineEdit.setText(
			self.ap.getPath(
				self.ui.appName_comboBox.currentText(), 
				self.ui.appVer_comboBox.currentText(), 'win' ))


	def deleteApp(self):
		""" Delete an entry for an application.
		"""
		self.ap.deleteApp(self.ui.appName_comboBox.currentText())
		self.populateApps()
		self.populateAppVersions()


	def deleteAppVersion(self):
		""" Delete an entry for a version of an application.
		"""
		self.ap.deleteVersion(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText())
		self.populateAppVersions()
		self.populateAppExecPaths()


	def storeAppPathOSX(self):
		""" Store Mac OS X executable path when relevant field is updated.
		"""
		self.ap.setPath(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText(), 
			'osx', 
			self.ui.osxPath_lineEdit.text())
		#print "%s %s - Mac OS X executable path set to %s" %( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), self.ui.osxPath_lineEdit.text() )


	def storeAppPathLinux(self):
		""" Store Linux executable path when relevant field is updated.
		"""
		self.ap.setPath(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText(), 
			'linux', 
			self.ui.linuxPath_lineEdit.text())
		#print "%s %s - Linux executable path set to %s" %( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), self.ui.linuxPath_lineEdit.text() )


	def storeAppPathWin(self):
		""" Store Windows executable path when relevant field is updated.
		"""
		self.ap.setPath(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText(), 
			'win', 
			self.ui.winPath_lineEdit.text().replace("\\", "/"))
		#print "%s %s - Windows executable path set to %s" %( self.ui.appName_comboBox.currentText(), self.ui.appVer_comboBox.currentText(), self.ui.winPath_lineEdit.text() )


	def guessAppPaths(self):
		""" Guess the executable paths for each OS based on the [template]
			entry (if it exists).
		"""
		osxGuess = self.ap.guessPath(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText(), 'osx')
		if osxGuess:
			self.ui.osxPath_lineEdit.setText(osxGuess)
			self.storeAppPathOSX()

		linuxGuess = self.ap.guessPath(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText(), 'linux')
		if linuxGuess:
			self.ui.linuxPath_lineEdit.setText(linuxGuess)
			self.storeAppPathLinux()

		winGuess = self.ap.guessPath(
			self.ui.appName_comboBox.currentText(), 
			self.ui.appVer_comboBox.currentText(), 'win')
		if winGuess:
			self.ui.winPath_lineEdit.setText(winGuess)
			self.storeAppPathWin()


	def saveAppPaths(self):
		""" Save the application paths to the data file.
		"""
		self.storeAppPathOSX()
		self.storeAppPathLinux()
		self.storeAppPathWin()

		if self.ap.save():
			verbose.message("Application paths data file saved.")
			return True
		else:
			verbose.error("Application paths data file could not be saved.")
			return False


	def saveAndExit(self):
		""" Save data and exit.
		"""
		if self.saveAppPaths():
			self.accept()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return \
		or event.key() == QtCore.Qt.Key_Enter:
			return
