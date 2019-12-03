#!/usr/bin/python

# [houdini] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures for Houdini.


import os
import hou

# Import custom modules
from . import file_open
from . import file_save
# from shared import os_wrapper
from shared import recentFiles


class SceneManager(object):
	""" Interface to wrap Houdini's file open/save functionality.
	"""
	def __init__(self):
		self.app = 'houdini'
		self.file_open_ui = file_open.dialog(self, app=self.app)
		self.file_save_ui = file_save.dialog(self, app=self.app)


	def file_new(self):
		""" Start a new file with some default settings.
		"""
		# new scene command
		self.set_defaults()


	def file_open_dialog(self, **kwargs):
		""" Display a custom dialog to select a file to open.
		"""
		return self.file_open_ui.display(**kwargs)


	def file_open_native_dialog(self, starting_dir=None):
		""" Display a native dialog to select a file to open.
		"""
		# open scene dialog command
		return True


	def file_open(self, filepath):
		""" Open the specified file.
		"""
		if self.confirm():
			# open scene command (filepath)
			recentFiles.updateLs(filepath)
			return filepath

		else:
			return False


	def file_save_dialog(self, **kwargs):
		""" Display a custom dialog for saving a file.
		"""
		return self.file_save_ui.display(**kwargs)


	def file_save_native_dialog(self, starting_dir=None):
		""" Display a native dialog for saving a file.
		"""
		# save scene dialog command
		return True


	def file_save(self):
		""" Save the current file.
			If saving for first time take over and show custom dialog.
		"""
		pass
		# if # Is this scene empty?
		# 	self.file_save_dialog()

		# else:
		# 	hou.hipFile.save()


	def file_save_as(self, filepath):
		""" Save the specified file.
		"""
		# save file as command
		recentFiles.updateLs(filepath)
		return True


	def file_save_new_version(self):
		""" Increment the version number and save a new version of a file.
		"""
		pass


	def file_snapshot(self, dest_dir=None):
		""" Save a copy (snapshot) of the current scene to the destination
			directory, without changing the current file pointer.
		"""
		pass


	def get_current_name(self):
		""" Get the name of the current file.
		"""
		pass


	def set_current_name(self, new_name):
		""" Change the name of the current file.
		"""
		pass


	def confirm(self):
		""" Obtain confirmation to proceed with operation if the current file
			is not saved.
		"""
		pass
		# if mc.file(query=True, sceneName=True) \
		# and mc.file(query=True, modified=True):
		# 	if 'Yes' == mc.confirmDialog(
		# 		title='Unsaved Changes', 
		# 		message='The current scene has been modified. Do you want to continue?', 
		# 		button=['Yes', 'No'], 
		# 		defaultButton='Yes', 
		# 		cancelButton='No'):
		# 		return True
		# 	else:
		# 		return False
		# else:
		# 	return True


	def update_recents_menu(self):
		""" Populate the recent files menu or disable it if no recent files
			in list.
		"""
		pass


	def set_defaults(self):
		""" Automatically set some defaults from the shot settings for a new
			scene.
		"""
		pass
