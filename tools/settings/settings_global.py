#!/usr/bin/python

# [Icarus] settings_global.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019 Gramercy Park Studios
#
# Global settings handler.


import os

from Qt import QtCore

# Import custom modules
from . import edit_root_paths
from shared import jobs
from shared import os_wrapper
# from shared import prompt


class helper():

	def __init__(self, parent, frame):
		""" Setup application properties panel.
		"""
		self.frame = frame
		self.parent = parent

		# # Populate line edit with user name
		# self.frame.user_lineEdit.setText(os.getenv('IC_USERNAME', ''))

		# Set icons
		self.frame.configDirBrowse_toolButton.setIcon(parent.iconSet('folder-open.svg'))
		self.frame.assetLibraryBrowse_toolButton.setIcon(parent.iconSet('folder-open.svg'))

		# Connect signals & slots
		self.frame.configDirBrowse_toolButton.clicked.connect(lambda: self.browseFolder(self.frame.configDir_lineEdit))
		self.frame.assetLibraryBrowse_toolButton.clicked.connect(lambda: self.browseFolder(self.frame.assetLibrary_lineEdit))
		self.frame.userPrefsServer_radioButton.toggled.connect(lambda state: self.updateUserPrefsLocation(state, 'server'))
		self.frame.userPrefsHome_radioButton.toggled.connect(lambda state: self.updateUserPrefsLocation(state, 'home'))
		self.frame.editPaths_pushButton.clicked.connect(lambda: self.editPaths())  # Only works with a lambda for some reason

		# Instantiate jobs class and load data
		self.j = jobs.Jobs()


	@QtCore.Slot(bool, str)
	def updateUserPrefsLocation(self, state, value):
		""" Update user prefs location based on the setting above.
		"""
		if state:
			if value == 'server':
				config_dir = self.frame.configDir_lineEdit.text()
				path = os.path.join(config_dir, 'users', os.environ['IC_USERNAME'])
			elif value == 'home':
				metadata = self.frame.metadataDir_lineEdit.text()
				path = os.path.join(os.environ['IC_USERHOME'], metadata)

			path = os_wrapper.absolutePath(path)
			path = os_wrapper.relativePath(path, 'IC_BASEDIR')
			path = os_wrapper.relativePath(path, 'IC_USERHOME')
			path = os_wrapper.relativePath(path, 'IC_USERNAME')
			self.frame.userPrefs_lineEdit.setText(path)


	def browseFolder(self, lineEdit):
		""" Browse for a folder and put the result into the specified
			lineEdit field.
		"""
		starting_dir = os_wrapper.absolutePath(lineEdit.text())
		result = self.parent.folderDialog(starting_dir)
		if result:
			result = os_wrapper.relativePath(result, 'IC_BASEDIR')
			result = os_wrapper.relativePath(result, 'IC_FILESYSTEM_ROOT')
			lineEdit.setText(result)


	def editPaths(self):
		""" Open edit paths dialog.
		"""
		#self.j.loadXML()
		self.j.getRootPaths()

		editPathsDialog = edit_root_paths.dialog(parent=self.parent)
		if editPathsDialog.display(self.j.win_root, self.j.osx_root, self.j.linux_root, self.j.jobs_path):
			self.j.setRootPaths(editPathsDialog.winPath, editPathsDialog.osxPath, editPathsDialog.linuxPath, editPathsDialog.jobsRelPath)
			self.j.getRootPaths()
			self.j.saveXML()
