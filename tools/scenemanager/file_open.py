#!/usr/bin/python

# [scenemanager] file_open.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Scene Manager - Open File Dialog
# A UI for opening files/scenes/scripts.
# - Automatically handle file save locations, naming conventions and versions.
# - Provide a consistent experience across DCC apps.
# - Make it easier to find latest versions regardless of the last user to work
#   on the file.
# Current support is for Maya, Nuke and Houdini.


import datetime
import fnmatch
import os
import sys
# import time
# import traceback

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from shared import os_wrapper
from shared import recentFiles
from shared import sequence

try:
	import maya.cmds as mc
except ImportError:
	pass

try:
	import hou
except ImportError:
	pass

try:
	import nuke
	import nukescripts
except ImportError:
	pass


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
#class FileOpenUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" File Open UI.
	"""
	def __init__(self, parent=None):
		super(FileOpenUI, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui)

		# Set window icon, flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set icons
		# self.ui.shot_toolButton.setIcon(self.iconSet('configure.svg'))  # Make more appropriate icon

		# Connect signals & slots
		# self.ui.shot_toolButton.clicked.connect(self.setShot)

		# self.ui.discipline_comboBox.currentIndexChanged.connect(self.disciplineChanged)
		self.ui.artist_comboBox.currentIndexChanged.connect(self.artistChanged)

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).clicked.connect(self.openFile)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

		# # Context menus
		# self.addContextMenu(self.ui.shot_toolButton, "Change", self.setShot)
		# self.addContextMenu(self.ui.shot_toolButton, "Reset to current", self.setShot)

		# # Set input validators
		# desc_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w_]+'), self.ui.description_lineEdit)
		# self.ui.description_lineEdit.setValidator(desc_validator)

		# Restore widget state
		self.restoreView()

		# Define global variables
		self.time_format_str = "%Y/%m/%d %H:%M:%S"

		# Show initialisation message
		info_ls = []
		for key, value in self.getInfo().items():
			info_ls.append("{} {}".format(key, value))
		info_str = " | ".join(info_ls)
		print("%s v%s\n%s" % (cfg['window_title'], VERSION, info_str))


	def display(self):
		""" Display the window.
		"""
		self.returnValue = False

		self.setWindowTitle("%s - %s" % (cfg['window_title'], os.environ['SCNMGR_JOB']))
		self.ui.shot_lineEdit.setText(os.environ['SCNMGR_SHOT'])

		self.base_dir = os_wrapper.absolutePath('$SCNMGR_SAVE_DIR/..')
		self.file_filter = os.environ['SCNMGR_FILE_EXT'].split(os.pathsep)

		# # Set job type from pipeline environment when possible
		# if os.environ['IC_ENV'] == "STANDALONE":
		# 	pass

		# elif os.environ['IC_ENV'] == "MAYA":
		# 	self.setWindowTitle(
		# 		"%s Open Scene - %s" % (
		# 			os.environ['IC_VENDOR_INITIALS'], os.environ['IC_JOB']))
		# 	self.base_dir = os_wrapper.absolutePath('$MAYASCENESDIR/..')
		# 	# self.file_filter = '*.ma' # r'^\*\.m[a|b]$'
		# 	self.file_filter = ['*.ma', '*.mb'] # r'^\*\.m[a|b]$'

		# elif os.environ['IC_ENV'] == "HOUDINI":
		# 	self.setWindowTitle(
		# 		"%s Open Scene - %s" % (
		# 			os.environ['IC_VENDOR_INITIALS'], os.environ['IC_JOB']))
		# 	self.base_dir = os_wrapper.absolutePath('$HIP')  # needs thought
		# 	self.file_filter = ['*.hip', ]

		# elif os.environ['IC_ENV'] == "NUKE":
		# 	self.setWindowTitle(
		# 		"%s Open Script - %s" % (
		# 			os.environ['IC_VENDOR_INITIALS'], os.environ['IC_JOB']))
		# 	self.base_dir = os_wrapper.absolutePath('$NUKESCRIPTSDIR/..')
		# 	self.file_filter = ['*.nk', '*.nknc']

		self.populateComboBox(self.ui.artist_comboBox, self.getArtists())
		self.updateView(self.base_dir)

		self.show()
		self.raise_()
		# self.exec_()

		return self.returnValue


	def updateView(self, base_dir):
		""" Update the file browser.
			'base_dir' is the directory to look in.
		"""
		# Clear tree widget
		self.ui.fileBrowser_treeWidget.clear()

		# Populate tree widget
		matches = []
		for root, dirnames, filenames in os.walk(base_dir):
			for filetype in self.file_filter:
				for filename in fnmatch.filter(filenames, "*" + filetype):
					matches.append(os.path.join(root, filename))
		# delimiter='.v'
		# for base in sequence.getBases(base_dir, delimiter=delimiter):
		# 	path, prefix, v_range, ext, num_versions = sequence.getSequence(
		# 		base_dir, base, delimiter=delimiter, ignorePadding=False)
		# 	latest = max(sequence.numList(v_range))
		# 	v_str = 'v' + str(latest).zfill(3)
		# 	filename = 'prefix.%s.%s' % (v_str, ext)
		# 	matches.append(os.path.join(path, filename))

		# print(matches)
		for item in matches:
			fileItem = QtWidgets.QTreeWidgetItem(self.ui.fileBrowser_treeWidget)
			fileItem.setText(0, os.path.basename(item))
			fileItem.setText(1, str(os.path.getsize(item)))

			timestamp = os.path.getmtime(item)
			timestr = datetime.datetime.fromtimestamp(timestamp).strftime(self.time_format_str)
			fileItem.setText(2, timestr)
			fileItem.setText(3, self.getArtist(item))
			fileItem.setText(4, os.path.normpath(item))

			self.ui.fileBrowser_treeWidget.addTopLevelItem(fileItem)
		# self.ui.fileBrowser_treeWidget()

		# Resize all columns to fit content
		# for i in range(0, self.ui.fileBrowser_treeWidget.columnCount()):
		# 	self.ui.fileBrowser_treeWidget.resizeColumnToContents(i)

		# Hide last column
		self.ui.fileBrowser_treeWidget.setColumnHidden(4, True)

		# Sort by submit time column - move this somewhere else?
		# self.ui.fileBrowser_treeWidget.sortByColumn(2, QtCore.Qt.DescendingOrder)


	def artistChanged(self):
		""" Update the base dir for the specified artist.
		"""
		artist = self.ui.artist_comboBox.currentText()
		if artist == "[any]" \
		or artist == "" \
		or artist == None:
			self.updateView(self.base_dir)
		else:
			self.updateView(os.path.join(self.base_dir, artist))


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
		dirname = os.path.dirname(filepath)
		artist = os.path.split(dirname)[-1]
		return artist


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
			pass

		# print("Open %s" % filename)

		if os.environ['SCNMGR_APP'] == "STANDALONE":
			pass

		elif os.environ['SCNMGR_APP'] == "MAYA":
			recentFiles.updateLs(
				mc.file(filename, open=True, force=True, ignoreVersion=True))

		elif os.environ['SCNMGR_APP'] == "HOUDINI":
			pass

		elif os.environ['SCNMGR_APP'] == "NUKE":
			nuke.scriptOpen(filename)
			recentFiles.updateLs(filename)

		self.returnValue = filename
		self.accept()


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

def run_maya(session, **kwargs):
	""" Run in Maya.
	"""
	try:  # Show the UI
		session.fileOpenUI.display(**kwargs)
	except:  # Create the UI
		UI._maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.fileOpenUI = FileOpenUI(parent=UI._maya_main_window())
		session.fileOpenUI.display(**kwargs)


# def run_houdini(session, **kwargs):
# 	""" Run in Houdini.
# 	"""
# 	try:  # Show the UI
# 		session.fileOpenUI.display(**kwargs)
# 	except:  # Create the UI
# 		#UI._houdini_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
# 		#session = UI._houdini_get_session()
# 		session.fileOpenUI = FileOpenUI(parent=UI._houdini_main_window())
# 		session.fileOpenUI.display(**kwargs)


def run_nuke(session, **kwargs):
	""" Run in Nuke.
	"""
	try:  # Show the UI
		session.fileOpenUI.display(**kwargs)
	except:  # Create the UI
		UI._nuke_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.fileOpenUI = FileOpenUI(parent=UI._nuke_main_window())
		session.fileOpenUI.display(**kwargs)
