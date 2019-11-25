#!/usr/bin/python

# [scenemanager] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures.


import os

# Import custom modules
from shared import os_wrapper
from shared import recentFiles


def create(app=None):
	""" Return a new SceneManager object with wrappers for various DCC apps'
		functionality.
	"""
	if app is None:
		pass

	elif app == "maya":
		from . import scenemanager_maya
		return scenemanager_maya.SceneManager()

	elif app == "houdini":
		pass

	elif app == "nuke":
		from . import scenemanager_nuke
		return scenemanager_nuke.SceneManager()


# class SceneManager(object):
# 	""" File Open UI.
# 	"""
# 	def __init__(self):
# 		pass


# 	def file_new(self):
# 		""" Start a new file.
# 		"""
# 		pass


# 	def file_open_dialog(self, starting_dir=None):
# 		""" Display a dialog to select a file to open.
# 		"""
# 		pass


# 	def file_open(self, filepath):
# 		""" Open the specified file.
# 		"""
# 		pass


# 	def file_save_dialog(self, starting_dir=None):
# 		""" Display a dialog for saving a file.
# 		"""
# 		pass


# 	def file_save(self):
# 		""" Save the current file.
# 		"""
# 		pass


# 	def file_save_as(self, filepath):
# 		""" Save the specified file.
# 		"""
# 		pass


# 	def file_save_new_version(self):
# 		""" Convenience function to save a new version of a file.
# 		"""
# 		pass


# 	def file_snapshot(self, dest_dir=None):
# 		""" Save a copy (snapshot) of the current scene to the destination
# 			directory, without changing the current file pointer.
# 		"""
# 		pass


# 	def file_get_name(self):
# 		""" Change the name of the current file.
# 		"""
# 		pass


# 	def file_set_name(self, new_name):
# 		""" Change the name of the current file.
# 		"""
# 		pass


# 	def update_recents_menu(self):
# 		""" Populate the recent files menu or disable it if no recent files
# 			in list.
# 		"""
# 		pass
