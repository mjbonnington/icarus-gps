#!/usr/bin/python

# [scenemanager] file_open.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Scene Manager - Open File Dialog
# A UI for opening files/scenes/scripts.


import datetime
# import fnmatch
# import glob
import os
import re
import sys
# import time
# import traceback

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from . import convention
from shared import os_wrapper
from shared import recentFiles
# from shared import sequence
from shared import verbose

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

VERSION = "0.1.0"

cfg = {}

# Set window title and object names
cfg['window_object'] = "fileOpenUI"
if os.environ['SCNMGR_VENDOR_INITIALS']:
	cfg['window_title'] = "%s Open" % os.environ['SCNMGR_VENDOR_INITIALS']
else:
	cfg['window_title'] = "Open"

# Set the UI and the stylesheet
cfg['ui_file'] = 'file_open.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
cfg['prefs_file'] = os.path.join(
	os.environ['SCNMGR_USER_PREFS_DIR'], 'scenemanager_prefs.json')
cfg['store_window_geometry'] = True

# ----------------------------------------------------------------------------
# Begin main window class
# ----------------------------------------------------------------------------

class FileOpenUI(QtWidgets.QDialog, UI.TemplateUI):
	""" File Open UI.
	"""
	def __init__(self, parent=None, session=None):
		super(FileOpenUI, self).__init__(parent)
		self.parent = parent
		self.session = session

		self.base_dir = os_wrapper.absolutePath('$SCNMGR_SAVE_DIR/..')
		self.file_ext = os.environ['SCNMGR_FILE_EXT'].split(os.pathsep)

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui)

		# Set window icon, flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set icons
		# self.ui.shot_toolButton.setIcon(self.iconSet('configure.svg'))  # causes crash?
		self.ui.refresh_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.nativeDialog_toolButton.setIcon(self.iconSet('folder-open.svg'))

		# Connect signals & slots
		# self.ui.shot_toolButton.clicked.connect(self.setShot)
		# self.ui.shotChange_toolButton.clicked.connect(self.setShot)
		# self.ui.shotReset_toolButton.clicked.connect(self.resetShot)

		# self.ui.shot_lineEdit.textChanged.connect(self.updateFilters)  # disabled as this call should be done explicitly when shot is (re)set
		self.ui.discipline_comboBox.currentIndexChanged.connect(self.updateFilters)
		self.ui.artist_comboBox.currentIndexChanged.connect(self.updateFilters)
		self.ui.versionAll_radioButton.toggled.connect(self.updateView)
		self.ui.versionLatest_radioButton.toggled.connect(self.updateView)

		self.ui.refresh_toolButton.clicked.connect(self.updateView)
		self.ui.nativeDialog_toolButton.clicked.connect(self.nativeDialog)

		self.ui.fileBrowser_treeWidget.itemSelectionChanged.connect(self.updateSelection)

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).clicked.connect(self.openFile)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

		# # Context menus
		# self.addContextMenu(self.ui.shot_toolButton, "Change", self.setShot)
		# self.addContextMenu(self.ui.shot_toolButton, "Reset to current", self.resetShot)

		# Restore widget state
		self.restoreView()

		# Define global variables
		self.time_format_str = "%Y/%m/%d %H:%M:%S"

		# Show initialisation message
		info_ls = []
		for key, value in self.getInfo().items():
			info_ls.append("{} {}".format(key, value))
		info_str = " | ".join(info_ls)
		verbose.message("%s v%s" % (cfg['window_title'], VERSION))
		verbose.print_(info_str)


	def display(self):
		""" Display the window.
		"""
		self.returnValue = False

		self.setWindowTitle("%s - %s" % (cfg['window_title'], os.environ['SCNMGR_JOB']))

		self.ui.shot_lineEdit.setText(os.environ['SCNMGR_SHOT'])
		self.ui.shot_toolButton.setEnabled(False)  # temp until implemented

		# Generate a master list of all files matching the naming convention
		# to compare against
		# self.generateFilter(shot=self.ui.shot_lineEdit.text())
		# self.matches_latest = convention.get_latest(self.matchFiles(self.file_filter))
		self.matches_latest = convention.get_latest(
			convention.match_files(
				self.base_dir, 
				convention.generate_filter(shot=self.ui.shot_lineEdit.text())))
		print self.matches_latest

		# self.base_dir = os_wrapper.absolutePath('$SCNMGR_SAVE_DIR/..')
		# self.file_ext = os.environ['SCNMGR_FILE_EXT'].split(os.pathsep)

		self.populateComboBox(self.ui.artist_comboBox, self.getArtists(), blockSignals=True)
		self.updateFilters()
		self.updateView()
		self.updateSelection()

		self.show()
		self.raise_()

		return self.returnValue


	# @QtCore.Slot()
	def updateSelection(self):
		""" Enable/disable 'Open' button depending on current selection.
		"""
		# No items selected...
		if len(self.ui.fileBrowser_treeWidget.selectedItems()) == 0:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(False)
		# More than one item selected...
		else:
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(True)


	# @QtCore.Slot()
	def updateFilters(self):
		""" Update the search filter arguments when the widgets' values are
			modified.
		"""
		shot = self.ui.shot_lineEdit.text()
		discipline = self.ui.discipline_comboBox.currentText()
		artist = self.ui.artist_comboBox.currentText()

		# self.generateFilter(shot, discipline, artist)
		self.file_filter = convention.generate_filter(
			shot=shot, 
			discipline=discipline, 
			artist=artist)
		self.updateView()


	# def generateFilter(self, shot=os.environ['SCNMGR_SHOT'], discipline=None, artist=None):
	# 	""" Update the search filter to show filenames based on the currently
	# 		selected values, which match the naming convention described in
	# 		the environment variable 'SCNMGR_CONVENTION'.
	# 	"""
	# 	ignore_list = ["[any]", "[please select]", "", None]

	# 	# Current naming convention for reference:
	# 	# <artist>/<shot>.<discipline>.[<description>.]<version>.ext

	# 	# Remove file extension
	# 	self.file_filter = os.path.splitext(os.environ['SCNMGR_CONVENTION'])[0]

	# 	# Replace compulsory tokens
	# 	self.file_filter = self.file_filter.replace("<shot>", shot)

	# 	# Replace known tokens
	# 	if discipline not in ignore_list:
	# 		self.file_filter = self.file_filter.replace("<discipline>", discipline)
	# 	if artist not in ignore_list:
	# 		self.file_filter = self.file_filter.replace("<artist>", artist)

	# 	# Replace unspecified tokens with wildcards
	# 	self.file_filter = self.file_filter.replace("<artist>", "*")
	# 	self.file_filter = self.file_filter.replace("<discipline>", "*")
	# 	self.file_filter = self.file_filter.replace("[<description>.]<version>", "*")

	# 	# print self.file_filter


	# def matchFiles(self, file_filter):
	# 	""" Match files based on the convention given in file_filter and
	# 		return as a list.
	# 	"""
	# 	matches = []
	# 	for filetype in self.file_ext:
	# 		search_pattern = os.path.join(self.base_dir, file_filter+filetype)
	# 		# print search_pattern
	# 		for filepath in glob.glob(search_pattern):
	# 			# Only add files, not directories or symlinks
	# 			if os.path.isfile(filepath) \
	# 			and not os.path.islink(filepath):
	# 				filepath = os_wrapper.absolutePath(filepath)
	# 				matches.append(filepath)

	# 	return matches


	def updateView(self):
		""" Update the file browser.
		"""
		try:
			verbose.debug("updateView called from %s" % self.sender().objectName())
		except:
			verbose.debug("updateView called explicitly")

		show_latest = self.ui.versionLatest_radioButton.isChecked()

		# Clear tree widget
		self.ui.fileBrowser_treeWidget.clear()

		# Get list of files that match filters
		# matches = self.matchFiles(self.file_filter)
		matches = convention.match_files(self.base_dir, self.file_filter)

		# matches_latest = convention.get_latest(matches)

		if show_latest:
			# matches = matches_latest
			matches = convention.get_latest(matches)

		# Add entries to tree widget
		for item in matches:
			fileItem = QtWidgets.QTreeWidgetItem(self.ui.fileBrowser_treeWidget)
			if item in self.matches_latest:
				fileItem.setIcon(0, self.iconSet('starred.svg'))
			else:
				fileItem.setIcon(0, self.iconSet('empty.png'))
				fileItem.setForeground(0, self.col['disabled'])
			fileItem.setText(0, os.path.basename(item))
			fileItem.setText(1, str(os.path.getsize(item)))
			timestamp = os.path.getmtime(item)
			timestr = datetime.datetime.fromtimestamp(timestamp).strftime(self.time_format_str)
			fileItem.setText(2, timestr)
			if self.getArtist(item) != os.environ['SCNMGR_USER']:
				fileItem.setForeground(3, self.col['disabled'])
			fileItem.setText(3, self.getArtist(item))
			fileItem.setText(4, os.path.normpath(item))

			self.ui.fileBrowser_treeWidget.addTopLevelItem(fileItem)

		# Hide last column
		self.ui.fileBrowser_treeWidget.setColumnHidden(4, True)

		# Sort by submit time column - move this somewhere else?
		# self.ui.fileBrowser_treeWidget.sortByColumn(2, QtCore.Qt.DescendingOrder)


	def getArtists(self):
		""" Return a list of artists. Calculate from all the subdirectories
			of base dir plus the current username.
		"""
		artists = ["[any]", os.environ['SCNMGR_USER']]

		subdirs = next(os.walk(self.base_dir))[1]
		if subdirs:
			for subdir in subdirs:
				if not subdir.startswith('.'):  # ignore hidden directories
					if subdir not in artists:
						artists.append(subdir)

		return artists


	def getArtist(self, filepath):
		""" Return the artist name based on the filepath.
		"""
		# dirname = os.path.dirname(filepath)
		# artist = os.path.split(dirname)[-1]
		# return artist
		meta = convention.parse(filepath)
		return meta['<artist>']


	def restoreView(self):
		""" Restore and apply saved state of tree widgets.
		"""
		try:
			# self.ui.splitter.restoreState(self.settings.value("splitterSizes")) #.toByteArray())
			self.ui.fileBrowser_treeWidget.header().restoreState(self.settings.value("fileBrowserView")) #.toByteArray())
		except:
			pass


	# def resetView(self):
	# 	""" Reset state of tree widgets to default.
	# 	"""
	# 	self.settings.remove("fileBrowserView")


	def openFile(self):
		""" Dialog accept function.
		"""
		try:
			for item in self.ui.fileBrowser_treeWidget.selectedItems():
				filename = item.text(4)

		except ValueError:
			verbose.error("Nothing selected.")
			return False

		if self.session.file_open(filename):
			self.returnValue = filename
			self.accept()


	def nativeDialog(self):
		""" Open file using application-native dialog.
		"""
		self.hide()

		if self.session.file_open_native_dialog():
			self.close()
		else:  # Return to custom dialog
			self.show()


	# def keyPressEvent(self, event):
	# 	""" Override function to prevent Enter / Esc keypresses triggering
	# 		OK / Cancel buttons.
	# 	"""
	# 	if event.key() == QtCore.Qt.Key_Return \
	# 	or event.key() == QtCore.Qt.Key_Enter:
	# 		return


	def closeEvent(self, event):
		""" Event handler for when window is closed. Save settings, store
			window gemotry and state of certain widgets
		"""
		self.save()
		self.storeWindow()
		self.settings.setValue(
			"fileBrowserView", 
			self.ui.fileBrowser_treeWidget.header().saveState())

# ----------------------------------------------------------------------------
# End of main window class
# ============================================================================
# Run functions
# ----------------------------------------------------------------------------

def dialog(session, app='standalone'):
	""" Instantiate UI object parented to appropriate app's main window
	"""
	if app == 'standalone':
		pass
	elif app == 'maya':
		parent = UI._maya_main_window()
	elif app == 'houdini':
		parent = UI._houdini_main_window()
	elif app == 'nuke':
		parent = UI._nuke_main_window()

	return FileOpenUI(parent=parent, session=session)
