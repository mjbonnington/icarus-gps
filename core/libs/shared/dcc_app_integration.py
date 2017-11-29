#!/usr/bin/python

# [Icarus] dcc_app_integration.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# This module provides windowing / UI helper functions for better integration
# of PySide / PyQt UIs in supported DCC applications.
# Currently supports Maya and Nuke.


import os


# Detect environment & import appropriate modules
if os.environ['IC_ENV'] == 'MAYA':
	import maya.cmds as mc
elif os.environ['IC_ENV'] == 'NUKE':
	import nuke
	import nukescripts


# ----------------------------------------------------------------------------
# Maya
# ----------------------------------------------------------------------------

def maya_delete_ui(window_title, window_object):
	""" Delete existing UI in Maya.
	"""
	if mc.window(window_object, query=True, exists=True):
		mc.deleteUI(window_object)  # Delete window
	if mc.dockControl('MayaWindow|' + window_title, query=True, exists=True):
		mc.deleteUI('MayaWindow|' + window_title)  # Delete docked window


def maya_main_window():
	""" Return Maya's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if obj.objectName() == 'MayaWindow':
			return obj
	raise RuntimeError("Could not find MayaWindow instance")


# ----------------------------------------------------------------------------
# Nuke
# ----------------------------------------------------------------------------

def nuke_delete_ui():
	""" Delete existing UI in Nuke.
	"""
	for obj in QtWidgets.QApplication.allWidgets():
		if obj.objectName() == window_object:
			obj.deleteLater()


def nuke_main_window():
	""" Returns Nuke's main window.
	"""
	for obj in QtWidgets.QApplication.topLevelWidgets():
		if (obj.inherits('QMainWindow') and obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
			return obj
	raise RuntimeError("Could not find DockMainWindow instance")


def nuke_set_zero_margins(widget_object):
	""" Remove Nuke margins when docked UI.
		More info:
		https://gist.github.com/maty974/4739917
	"""
	parentApp = QtWidgets.QApplication.allWidgets()
	parentWidgetList = []
	for parent in parentApp:
		for child in parent.children():
			if widget_object.__class__.__name__ == child.__class__.__name__:
				parentWidgetList.append(parent.parentWidget())
				parentWidgetList.append(parent.parentWidget().parentWidget())
				parentWidgetList.append(parent.parentWidget().parentWidget().parentWidget())

				for sub in parentWidgetList:
					for tinychild in sub.children():
						try:
							tinychild.setContentsMargins(0, 0, 0, 0)
						except:
							pass

