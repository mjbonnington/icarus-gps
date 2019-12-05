#!/usr/bin/python

# [scenemanager] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Scene Manager for DCC apps
# - Automatically handle file save locations, naming conventions and versions.
# - Provide a consistent experience across DCC apps.
# - Make it easier to find latest versions regardless of the last user to work
#   on the file.
#
# Current support is for Maya, Nuke and Houdini.
# In theory, adding support for a new app is as simple as writing a new module
# 'scenemanager_<app>.py' wrapping the basic open/save functionality of the
# app, then add the appropriate entry in the create() function here.
# (Assuming the app supports Python & PySide/PyQt of course).
#
# Initialise at app startup with:
# from tools.scenemanager import scenemanager
# session.scnmgr = scenemanager.create(app='<app>')


import os

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
		from . import scenemanager_houdini
		return scenemanager_houdini.SceneManager()

	elif app == "nuke":
		from . import scenemanager_nuke
		return scenemanager_nuke.SceneManager()
