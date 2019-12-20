#!/usr/bin/python

# [Icarus] settings.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2019
#
# Modular settings editor dialog.
# Provides a skeleton dialog which can be extended with load-in panels, each
# with their own UI file and helper module (if required).


import os
import sys

from Qt import QtCompat, QtCore, QtWidgets

# Import custom modules
import ui_template as UI

from shared import verbose

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

cfg = {}

# Set window title and object names
cfg['window_title'] = "Settings"
cfg['window_object'] = "settingsUI"

# Set the UI and the stylesheet
cfg['ui_file'] = 'settings.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
cfg['store_window_geometry'] = True

# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class SettingsDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Settings editor dialog class.
	"""
	def __init__(self, parent=None):
		super(SettingsDialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.setWindowIcon(self.iconSet('icon_settings.png', tintNormal=False))

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.categories_listWidget.currentItemChanged.connect(lambda current: self.openProperties(current.text()))
		# self.ui.categories_listWidget.itemActivated.connect(lambda item: self.openProperties(current.text()))

		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.removeOverrides)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveAllAndClose)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)


	def display(self, 
		settings_type="Generic",
		self_name="", 
		category_list=[], 
		start_panel=None, 
		prefs_file=None, 
		inherit=None, 
		autofill=False):
		""" Display the dialog.

			'settings_type' is the name given to the settings dialog.
			'self_name' e.g. the name of the job or shot.
			'category_list' is a list of categories, should correspond to a
			page of properties defined by a .ui file.
			'start_panel' if set will jump straight to the named panel.
			'prefs_file' is the path to the file storing the settings. Can be
			either an XML or a JSON file.
			'inherit' whether to inherit any values. This should be in the
			form of a path just like the 'prefs_file' argument.
			'autofill' when true, attempt to fill some fields automatically.
		"""
		if start_panel:
			verbose.debug("Start Panel: " + start_panel)
			self.currentCategory = start_panel
		else:
			self.currentCategory = ""

		self.settings_type = settings_type
		self.self_name = self_name
		self.category_list = category_list
		self.prefs_file = prefs_file
		self.inherit = inherit
		self.autofill = autofill

		self.reset()

		# Set window title
		if self_name != "":
			self.setWindowTitle(
				"%s %s: %s" % (settings_type, cfg['window_title'], self_name))
		else:
			self.setWindowTitle(
				"%s %s" % (settings_type, cfg['window_title']))

		return self.exec_()


	def reset(self):
		""" Initialise or reset by reloading data.
		"""
		# self.ui.categories_listWidget.blockSignals(True)

		# Instantiate preferences data class(es)
		if self.prefs_file is not None:
			self.prefs = self.createPrefs(self.prefs_file)
			if self.inherit:
				self.prefs_inherited = self.createPrefs(self.inherit)
			else:
				self.prefs_inherited = None

		# Populate categories
		if self.category_list:
			self.ui.categories_listWidget.clear()

			for cat in self.category_list:
				self.ui.categories_listWidget.addItem(cat)

			# Set the maximum size of the list widget
			self.ui.categories_listWidget.setMaximumWidth(self.ui.categories_listWidget.sizeHintForColumn(0)*2)

			# Select the first item & show the appropriate settings panel
			if self.currentCategory == "":
				currentItem = self.ui.categories_listWidget.item(0)
			else:
				currentItem = self.ui.categories_listWidget.findItems(self.currentCategory, QtCore.Qt.MatchExactly)[0]

			currentItem.setSelected(True)
			# self.openProperties(currentItem.text())

			# Hide category list if there's only one item
			if len(self.category_list) <= 1:
				# self.ui.categories_listWidget.hide()  # doesn't work
				self.ui.categories_listWidget.setMaximumWidth(0)

		# self.ui.categories_listWidget.blockSignals(False)


	def openProperties(self, category, storeProperties=True):
		""" Open properties panel for selected settings category. Loads UI
			file and sets up widgets.
		"""
		self.currentCategory = category

		# Show panel & load values into form widgets
		if self.loadPanel(category):
			if (self.inherit is not None) \
			and self.ui.settings_frame.property('inheritable'):
				verbose.print_("Category: %s (values inheritable)" % category)
				self.setupWidgets(
					self.ui.settings_frame, 
					forceCategory=category, 
					inherit=self.prefs_inherited, 
					storeProperties=False)
			else:
				verbose.print_("Category: %s" % category)
				self.setupWidgets(
					self.ui.settings_frame, 
					forceCategory=category, 
					storeProperties=storeProperties)


	def loadPanel(self, category):
		""" Load the panel UI (and helper module if required).
			The exec function is called here to avoid the error: 'unqualified
			exec is not allowed in function because it contains a nested
			function with free variables' with Python 2.x.
		"""
		ui_file = "settings_%s.ui" % category
		helper_module = 'settings_%s' % category
		panel_ui_loaded = False
		helper_module_loaded = False

		# Create new frame to hold properties UI & load into frame
		self.ui.settings_frame.close()
		try:
			uifile = os.path.join(os.environ['IC_FORMSDIR'], ui_file)
			self.ui.settings_frame = QtCompat.loadUi(uifile)
			self.ui.settings_verticalLayout.addWidget(self.ui.settings_frame)
			panel_ui_loaded = True
		except FileNotFoundError:
			message = "Could not open '%s' properties panel UI. " % category
			verbose.error(message)

		# Load helper module
		try:
			exec_str = 'from . import %s as sh; helper = sh.helper(self, self.ui.settings_frame)' % helper_module
			# print(exec_str)
			exec(exec_str)
			helper_module_loaded = True
		except ImportError:
			message = "Could not import '%s' module. " % helper_module
			verbose.debug(message)

		if panel_ui_loaded: # and helper_module_loaded:
			return True
		else:
			return False


	def removeOverrides(self):
		""" Remove stored values and instead inherit defaults for widgets on
			the current panel.
		"""
		for widget in self.ui.settings_frame.findChildren(QtWidgets.QWidget):
			attr = widget.property('xmlTag')
			if attr:
				self.prefs.remove_attr(self.currentCategory, attr)

		self.openProperties(self.currentCategory, storeProperties=False)


	def saveAllAndClose(self):
		""" Save settings and close the dialog.
		"""
		# Store the values from widgets on all pages
		for category in self.category_list:
			self.openProperties(category, storeProperties=True)

		# There's a bug where all property panel widgets become visible if a
		# save fails. As a quick dodgy workaround we exit so we don't see it
		# happen.
		if self.save():
			self.accept()
		else:
			# self.close()
			self.reject()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return \
		or event.key() == QtCore.Qt.Key_Enter:
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
