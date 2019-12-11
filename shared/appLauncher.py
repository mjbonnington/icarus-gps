#!/usr/bin/python

# [Icarus] appLauncher.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2017-2019
#
# Handles software application launching from Icarus, auto-generates UI,
# creates folder structures, etc.


import math
import os
# import subprocess
# import sys

from Qt import QtCore, QtGui, QtWidgets
#import rsc_rc  # Import resource file as generated by pyside-rcc

# Import custom modules
from . import appPaths
from . import dirStructure
from . import launchApps  # temp?
from . import json_metadata as metadata
from . import os_wrapper
# from . import recentFiles  # for sorting by most used
from . import userPrefs
from . import verbose


class AppLauncher(QtWidgets.QDialog):
	""" App launcher UI panel main class.
	"""
	def __init__(self, parent, frame):
		super(AppLauncher, self).__init__(parent)

		self.frame = frame
		self.parent = parent

		# Instantiate data classes
		self.jd = metadata.Metadata()  # Job settings
		self.ap = appPaths.AppPaths()
		self.ds = dirStructure.DirStructure()

		# Set OS identifier strings to get correct app executable paths
		if os.environ['IC_RUNNING_OS'] == "Windows":
			self.currentOS = "win"
		elif os.environ['IC_RUNNING_OS'] == "MacOS":
			self.currentOS = "osx"
		elif os.environ['IC_RUNNING_OS'] == "Linux":
			self.currentOS = "linux"

		# self.setupIconGrid()


	def setAppEnvVars(self):
		""" Dynamically generate application environment variables.
		"""
		for app in self.ap.getApps():
			displayName = app.get('name')
			shortName = app.get('id')
			appVersion = self.jd.getAppVersion(shortName)
			if app.get('projectFolders') == "True":
				projectFolders = True
			else:
				projectFolders = False

			if appVersion:  # Only apps that have a version set in the job settings
				appExecutable = self.ap.getPath(displayName, appVersion, self.currentOS)

				# Set app exec and version environment variables
				os.environ['IC_%s_EXECUTABLE' % shortName.upper()] = appExecutable
				os.environ['IC_%s_VERSION' % shortName.upper()] = appVersion

				# Set environment variables for project folder structure
				if projectFolders:
					folder_xml = os_wrapper.absolutePath("$IC_BASEDIR/rsc/%s/templates/projectDir.xml" % shortName)
					self.ds.createDirStructure(
						datafile=folder_xml, 
						createDirs=False, 
						createFiles=False, 
						createEnvVars=True)

				# Source individual app's custom environment
				try:
					exec_str = 'from rsc.%s import %s__env__ as app_env; app_env.set_env()' % (shortName.lower(), shortName.lower())
					# verbose.debug(exec_str)
					exec(exec_str)

				except ImportError:
					message = "Could not import '%s' environment variables." % shortName.lower()
					verbose.print_(message)

				except (AttributeError, KeyError, TypeError):
					message = "Unable to set %s environment variables." % displayName
					verbose.warning(message)


	def setupIconGrid(self, job=None, sort_by=None):
		""" Dynamically generate grid of tool button icons.
		"""
		if sort_by:
			verbose.print_("Populating app launcher icons sorted by %s..." %sort_by.lower(), 4)
		else:
			verbose.print_("Populating app launcher icons...", 4)

		if job is not None:
			# self.jd.loadXML(os.path.join(os.environ['IC_JOBDATA'], 'jobData.xml'), use_template=False)
			if not self.jd.load(
				os.path.join(os.environ['IC_JOBDATA'], 'job_settings.json')):
				self.jd.clear()
			self.ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'), use_template=True)

		parentLayout = self.frame.findChildren(QtWidgets.QVBoxLayout, 'launchApp_verticalLayout')[0]

		# Delete any existing layouts
		for layout in parentLayout.findChildren(QtWidgets.QGridLayout):
			if "apps_gridLayout" in layout.objectName():
				for i in reversed(range(layout.count())): 
					layout.itemAt(i).widget().deleteLater()
				layout.deleteLater()

		# Get apps
		item_index = 0
		app_ls = []
		if job is not None:
			all_apps = self.ap.getApps(visible_only=True, sort_by=sort_by)
			for app in all_apps:
				if self.jd.getAppVersion(app.get('id')):  # app.get('name') for backwards-compatibility
					app_ls.append(app)

		# Create icons
		num_items = len(app_ls)
		if num_items:
			rows = self.getRows(num_items)
			for row, num_row_items in enumerate(rows):
				# Create grid layout
				icon_size = self.getIconSize(num_row_items)
				row_gridLayout = QtWidgets.QGridLayout()
				row_gridLayout.setObjectName("apps_gridLayout%d" % row)
				parentLayout.insertLayout(row, row_gridLayout)
				for col in range(num_row_items):
					self.createIcon(app_ls[item_index], icon_size, row_gridLayout, col)
					item_index += 1

			# Hide 'No Apps' placeholder button
			self.parent.ui.appPlaceholder_toolButton.hide()

		else:
			# Show 'No Apps' placeholder button
			self.parent.ui.appPlaceholder_toolButton.show()


	def getIcon(self, element, appName=None):
		""" Get icon.
		"""
		if appName is None:
			appName = element.get('id')
		appIcon = element.findtext('icon')
		if appIcon is None:
			appIcon = ""

		icon = QtGui.QIcon()

		iconPath = ":/icons/icons/icon_editor"
		searchPaths = [os_wrapper.absolutePath(os.path.splitext(appIcon)[0]), 
		               os_wrapper.absolutePath("$IC_BASEDIR/rsc/%s/icons/app_icon_%s" % (appName, appName)), 
		               os_wrapper.absolutePath("$IC_FORMSDIR/icons/app_icon_%s" % appName), 
		              ]

		for searchPath in searchPaths:
			if os.path.isfile(searchPath + ".png"):
				iconPath = searchPath
				break

		icon.addPixmap(QtGui.QPixmap(iconPath + ".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		icon.addPixmap(QtGui.QPixmap(iconPath + "_disabled.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)

		return icon


	def createIcon(self, app, iconSize, layout, column):
		""" Create tool button icon.
		"""
		shortName = app.get('id')
		displayName = app.get('name')
		if app.get('projectFolders') == "True":
			projectFolders = True
		else:
			projectFolders = False
		appVersion = self.jd.getAppVersion(shortName)
		appExecutable = self.ap.getPath(displayName, appVersion, self.currentOS)
		flags = app.findtext('flags')
		# tooltip = ""
		# if self.showToolTips:
		tooltip = "Launch %s %s" % (displayName, appVersion)
		# print(layout.objectName(), column, shortName)

		toolButton = QtWidgets.QToolButton(self.frame)

		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(toolButton.sizePolicy().hasHeightForWidth())
		toolButton.setSizePolicy(sizePolicy)
		toolButton.setIcon(self.getIcon(app))
		toolButton.setIconSize(QtCore.QSize(iconSize[0], iconSize[1]))  # Vary according to number of items in row - QSize won't accept tuple
		toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
		toolButton.setText(displayName)
		toolButton.setObjectName("%s_toolButton" % shortName)
		toolButton.setProperty('shortName', shortName)
		toolButton.setProperty('displayName', displayName)
		toolButton.setProperty('projectFolders', projectFolders)
		toolButton.setProperty('version', appVersion)
		toolButton.setProperty('executable', appExecutable)
		toolButton.setProperty('flags', flags)

		if not os.path.isfile(appExecutable):
			toolButton.setEnabled(False)
			# if self.showToolTips:
			tooltip = "%s %s executable not found" % (displayName, appVersion)

		toolButton.setToolTip(tooltip)
		toolButton.setStatusTip(tooltip)

		# Connect signals & slots
		toolButton.clicked.connect(self.launchApp)

		# Add context menus
		submenus = self.ap.getSubMenus(shortName)
		if submenus:
			# self.createSubmenus(submenus, toolButton)
			toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
			for entry in submenus:
				menuName = entry.get('name')
				flags = entry.findtext('flags')
				actionName = "action%s" % menuName.replace(" ", "")

				action = QtWidgets.QAction(menuName, None)
				action.setIcon(self.getIcon(entry, shortName))
				action.setObjectName(actionName)
				action.setProperty('shortName', shortName)
				action.setProperty('displayName', displayName)
				action.setProperty('version', appVersion)
				action.setProperty('executable', appExecutable)
				action.setProperty('flags', flags)
				# if self.showToolTips:
				tooltip = "Launch %s %s" % (menuName, appVersion)
				action.setToolTip(tooltip)    # Does nothing?
				action.setStatusTip(tooltip)  # Does nothing?
				action.triggered.connect(self.launchApp)
				toolButton.addAction(action)

				# Make a class-scope reference to this object
				# (won't work without it for some reason)
				exec_str = "self.%s = action" % actionName
				exec(exec_str)

		layout.addWidget(toolButton, 0, column)


	def getRows(self, num_items):
		""" Calculate icon grid arrangement.
			Returns an integer list with each item representing the number of
			icons in each row.
			N.B. Weird syntax here is to maintain compatibility due to the
			different ways Python 2.x and 3.x handle division between integers
			and floats.
		"""
		# Specify some thresholds at which we cascade on to another row. In
		# this instance it's hardcoded that we increase the number of rows
		# after 4, 10, and thereafter every additional 5 items. There will
		# never be more than 5 items in a row.
		if num_items <= 4:
			num_rows = 1
		elif num_items <= 10:
			num_rows = 2
		else:
			num_rows = int(math.ceil(num_items/5.0))

		max_items_per_row = int(math.ceil(num_items/(num_rows*1.0)))

		# Create list of rows each holding an integer value representing the
		# number of items in each row.
		rows = []
		for i in range(num_rows):
			rows.append(max_items_per_row)

		# Progressively reduce items per row until we have the correct total
		# number of items.
		i = 0
		while sum(rows) > num_items:
			rows[i] -= 1
			i += 1

		# Sort the rows so that the rows with the fewest items appear first,
		# then return the list.
		rows.sort()
		return rows


	def getIconSize(self, num_items):
		""" Return icon size in pixels as a tuple, based on the number of
			icons in the row.
		"""
		if num_items == 5:
			icon_size = 40, 40
		elif num_items == 4:
			icon_size = 48, 48
		elif num_items == 3:
			icon_size = 56, 56
		elif num_items == 2:
			icon_size = 64, 64
		elif num_items == 1:
			icon_size = 80, 80
		else:
			icon_size = 48, 48

		return icon_size


	# @QtCore.Slot()
	def launchApp(self):
		""" Launches an application.
		"""
		shortName = self.sender().property('shortName')
		displayName = self.sender().property('displayName')
		version = self.sender().property('version')
		executable = self.sender().property('executable')
		flags = self.sender().property('flags')
		projectFolders = self.sender().property('projectFolders')
		# print(self.sender().objectName(), displayName, version, executable, flags)

		# Create project folder structure & set environment variables
		if projectFolders:
			folder_xml = os_wrapper.absolutePath("$IC_BASEDIR/rsc/%s/templates/projectDir.xml" % shortName)
			self.ds.createDirStructure(datafile=folder_xml)

		# Run the executable
		launchApps.launch(displayName, executable, flags)

		# Increase launch counter
		userPrefs.read()  # Reload user prefs file
		count = userPrefs.query('launchcounter', shortName, datatype='int', default=0)
		count += 1
		userPrefs.edit('launchcounter', shortName, count)

		# Minimise the UI if the option is set
		if self.parent.minimiseOnAppLaunch:
			self.parent.showMinimized()
