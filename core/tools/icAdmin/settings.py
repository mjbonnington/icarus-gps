#!/usr/bin/python

# [Icarus] settings.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Modular settings editor dialog.
# Provides a skeleton dialog which can be extended with load-in panels, each
# with their own UI file and helper module (if required).


import math
import os
import sys

from Qt import QtCompat, QtCore, QtWidgets
import ui_template as UI

# Import custom modules
#import settingsData
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Settings"
WINDOW_OBJECT = "settingsUI"

# Set the UI and the stylesheet
UI_FILE = "settings_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class SettingsDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Settings editor dialog class.
	"""
	def __init__(self, parent=None):
		super(SettingsDialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Set up keyboard shortcuts
		self.shortcutLock = QtWidgets.QShortcut(self)
		self.shortcutLock.setKey('Ctrl+L')
		self.shortcutLock.activated.connect(self.toggleLockUI)

		# self.shortcutSave = QtWidgets.QShortcut(self)
		# self.shortcutSave.setKey('Ctrl+S')
		# self.shortcutSave.activated.connect(self.saveAll)

		# self.shortcutRemoveOverride = QtWidgets.QShortcut(self)
		# self.shortcutRemoveOverride.setKey('Ctrl+R')
		# self.shortcutRemoveOverride.activated.connect(self.removeOverrides)

		# Context menus
		# self.addContextMenu(self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset), "Reset all settings", self.reset)
		# self.addContextMenu(self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset), "Reset this page only", self.reset)

		# Connect signals & slots
		self.ui.categories_listWidget.currentItemChanged.connect(lambda current: self.openProperties(current.text()))
		# self.ui.categories_listWidget.itemActivated.connect(lambda item: self.openProperties(current.text()))

		#self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveAllAndClose)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)


	def display(self, settingsType="Generic", categoryLs=[], startPanel=None, 
	            xmlData=None, inherit=None, autoFill=False):
		""" Display the dialog.
			'settingsType' is the name given to the settings dialog.
			'categoryLs' is a list of categories, should correspond to a page
			of properties defined by a .ui file.
			'startPanel' if set will jump straight to the named panel.
			'xmlData' is the path to the XML file storing the settings.
			'inherit' whether to inherit any values.
			'autoFill' when true, attempt to fill some fields automatically.
		"""
		if startPanel:
			print("Start Panel: " + startPanel)
			self.currentCategory = startPanel
		else:
			self.currentCategory = ""

		self.settingsType = settingsType
		self.categoryLs = categoryLs
		self.xmlData = xmlData
		self.inherit = inherit
		self.autoFill = autoFill

		self.lockUI = True

		self.reset()
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setEnabled(False)  # temporarily disable the reset button

		# Set window title
		if settingsType == "Job":
			title_suffix = ": " + os.environ['JOB']
		elif settingsType == "Shot":
			title_suffix = ": " + os.environ['SHOT']
		else:
			title_suffix = ""
		self.setWindowTitle("%s %s%s" %(settingsType, WINDOW_TITLE, title_suffix))

		return self.exec_()


	def reset(self):
		""" Initialise or reset by reloading data.
		"""
		# self.ui.categories_listWidget.blockSignals(True)

		# Load data from xml file(s)
		xd_load = self.xd.loadXML(self.xmlData)

		# Populate categories
		if self.categoryLs:
			self.ui.categories_listWidget.clear()

			for cat in self.categoryLs:
				self.ui.categories_listWidget.addItem(cat)

			# Set the maximum size of the list widget
			self.ui.categories_listWidget.setMaximumWidth(self.ui.categories_listWidget.sizeHintForColumn(0) * 2)

			# Select the first item & show the appropriate settings panel
			if self.currentCategory == "":
				currentItem = self.ui.categories_listWidget.item(0)
			else:
				currentItem = self.ui.categories_listWidget.findItems(self.currentCategory, QtCore.Qt.MatchExactly)[0]

			currentItem.setSelected(True)
			# self.openProperties(currentItem.text())

		# self.ui.categories_listWidget.blockSignals(False)


	def toggleLockUI(self):
		""" Lock/unlock UI for editing.
		"""
		self.lockUI = not self.lockUI
		self.ui.settings_scrollArea.setEnabled(self.lockUI)  # Disable properties panel widgets
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.lockUI)  # Disable save button


	def loadPanel(self, category):
		""" Load the panel UI (and helper module if required).
			The exec function is called here to avoid the error:
			'unqualified exec is not allowed in function because it contains a
			nested function with free variables' with Python 2.x.
		"""
		ui_file = "settings_%s_ui.ui" %category
		helper_module = 'settings_%s' %category
		panel_ui_loaded = False
		# helper_module_loaded = False

		# Create new frame to hold properties UI & load into frame
		self.ui.settings_frame.close()
		try:
			uifile = os.path.join(os.environ['IC_FORMSDIR'], ui_file)
			#self.ui.settings_frame = QtCompat.load_ui(fname=uifile)
			self.ui.settings_frame = QtCompat.loadUi(uifile)
			self.ui.settings_verticalLayout.addWidget(self.ui.settings_frame)
			panel_ui_loaded = True
		except FileNotFoundError:
			message = "Could not open '%s' properties panel." %category
			verbose.error(message)

		# Load helper module
		try:
			exec_str = 'import %s as sh; helper = sh.helper(self, self.ui.settings_frame)' %helper_module
			# print(exec_str)
			exec(exec_str)
			# helper_module_loaded = True
		except ImportError:
			pass

		return panel_ui_loaded


	def openProperties(self, category, storeProperties=True):
		""" Open properties panel for selected settings category. Loads UI
			file and sets up widgets.
		"""
		self.currentCategory = category
		verbose.print_("Category: " + self.currentCategory, 4)

		if self.loadPanel(category):
			inherited = False
			inheritable = False
			if (self.inherit is not None) and self.ui.settings_frame.property('inheritable'):
				verbose.print_("(values inheritable from %s)" %self.inherit, 4)
				inheritable = True

			# Load values into form widgets
			self.setupWidgets(self.ui.settings_frame, 
			                  forceCategory=category, 
			                  storeProperties=storeProperties)

			# widgets = self.ui.settings_frame.children()

			# for widget in widgets:

			# 	# Set up handler for push button(s)...
			# 	if widget.property('exec'):
			# 		if isinstance(widget, QtWidgets.QPushButton):
			# 			widget.clicked.connect(self.execPushButton)

			# 	# Set up handlers for different widget types & apply values
			# 	attr = widget.property('xmlTag')
			# 	if attr:
			# 		value = self.xd.getValue(category, attr)
			# 		# if inheritable:
			# 		# 	value = self.xd.getValue(category, attr)
			# 		# else:
			# 		# 	value, inherited = self.inheritFrom(category, attr)

			# 		# if inherited:
			# 		# 	widget.setProperty('xmlTag', None)
			# 		# 	widget.setProperty('inheritedValue', True)
			# 		# 	widget.setToolTip("This value is being inherited. Change the value to override the inherited value.")

			# 		# 	# Apply pop-up menu to remove override - can't get to work here
			# 		# 	#widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

			# 		# 	#actionRemoveOverride = QtWidgets.QAction("Remove override", None)
			# 		# 	#actionRemoveOverride.triggered.connect(self.removeOverrides)
			# 		# 	#widget.addAction(actionRemoveOverride)



	# def inheritFrom(self, category, attr):
	# 	""" Tries to get a value from the current settings type, and if no
	# 		value is found tries to inherit the value instead.
	# 		Returns two values:
	# 		'text' - the value of the requested attribute.
	# 		'inherited' - a Boolean value which is true if the value was
	# 		inherited.
	# 	"""
	# 	text = self.xd.getValue(category, attr)
	# 	inherited = False

	# 	if text is not "":
	# 		pass

	# 	# elif self.settingsType == 'Shot':
	# 	elif self.inherit == 'Job':
	# 		jd = settingsData.settingsData()
	# 		jd.loadXML(os.path.join(os.environ['JOBDATA'], 'jobData.xml'))
	# 		text = jd.getValue(category, attr)
	# 		inherited = True
	# 		verbose.print_('%s.%s = %s (inheriting value from job data)' %(category, attr, text), 4)

	# 	# print("%s/%s: got value %s, inherited=%s" %(category, attr, text, inherited))
	# 	return text, inherited


	# def removeOverrides(self):
	# 	""" Remove overrides and instead inherit values for widgets on the
	# 		current panel.
	# 	"""
	# 	widgets = self.ui.settings_frame.children()

	# 	for widget in widgets:
	# 		attr = widget.property('xmlTag')
	# 		if attr:
	# 			self.xd.removeElement(self.currentCategory, attr)

	# 	self.openProperties(self.currentCategory, storeProperties=False)


	def saveAllAndClose(self):
		""" Save data.
		"""
		# Store the values from widgets on all pages
		for category in self.categoryLs:
			self.openProperties(category, storeProperties=True)

		# There's a bug where all property panel widgets become visible if a
		# save fails. As a quick dodgy workaround we exit so we don't see it
		# happen.
		if self.save():
			self.accept()
		else:
			self.close()


	# def saveAll(self):
	# 	""" Save data.
	# 	"""
	# 	# Store the values from widgets on all pages
	# 	for category in self.categoryLs:
	# 		self.openProperties(category, storeProperties=True)

	# 	# There's a bug where all property panel widgets become visible if a
	# 	# save fails. As a quick dodgy workaround we exit so we don't see it
	# 	# happen.
	# 	if self.save():
	# 		self.accept()
	# 	else:
	# 		self.close()


	# def saveAndExit(self):
	# 	""" Save data and exit dialog.
	# 	"""
	# 	if self.save():
	# 		# self.ui.hide()
	# 		self.returnValue = True
	# 		self.ui.accept()
	# 	else:
	# 		self.exit()  # There's a bug where all property panel widgets become visible if a save fails. As a quick dodgy workaround we exit so we don't see it happen.


	# def exit(self):
	# 	""" Exit the dialog.
	# 	"""
	# 	# self.ui.hide()
	# 	self.returnValue = False
	# 	self.ui.reject()


	# def closeEvent(self, event):
	# 	""" Event handler for when window is closed.
	# 	"""
	# 	QtWidgets.QMainWindow.closeEvent(self, event)


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			return


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.storeWindow()  # Store window geometry


	# def closeEvent(self, event):
	# 	""" Event handler for when window is closed.
	# 	"""
	# 	#self.save()  # Save settings
	# 	#self.storeWindow()  # Store window geometry

