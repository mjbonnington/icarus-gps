#!/usr/bin/python

# envvarbrowser.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2018-2020
#
# Environment Variables Browser
# A tool for viewing and editing environment variables.
# Note that it's not possible change the system environment.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
from . import edit_envvar


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Environment Variables"
WINDOW_OBJECT = "EnvVarsUI"

# Set the UI and the stylesheet
UI_FILE = 'envvar_browser.ui'
STYLESHEET = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Begin main dialog class
# ----------------------------------------------------------------------------

class EnvVarsDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Environment Variables Browser dialog class.
	"""
	def __init__(self, parent=None):
		super(EnvVarsDialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(
			window_object=WINDOW_OBJECT,
			window_title=WINDOW_TITLE,
			ui_file=UI_FILE,
			stylesheet=STYLESHEET,
			store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Set icons
		self.ui.reload_toolButton.setIcon(self.iconSet('refresh.svg'))
		self.ui.add_toolButton.setIcon(self.iconSet('add.svg'))
		self.ui.remove_toolButton.setIcon(self.iconSet('remove.svg'))
		self.ui.edit_toolButton.setIcon(self.iconSet('edit.svg'))
		self.ui.searchFilterClear_toolButton.setIcon(self.iconSet('clear.svg'))

		# Connect signals & slots
		self.accepted.connect(self.save)  # Save settings if dialog accepted

		self.ui.reload_toolButton.clicked.connect(self.reloadEnvVars)
		self.ui.add_toolButton.clicked.connect(lambda: self.addEnvVar())
		self.ui.remove_toolButton.clicked.connect(self.removeEnvVars)
		self.ui.edit_toolButton.clicked.connect(self.editEnvVar)

		#self.ui.searchFilter_lineEdit.textChanged.connect(lambda text: self.populateEnvVarList(searchFilter=text))
		self.ui.searchFilter_lineEdit.textChanged.connect(lambda: self.populateEnvVarList())
		self.ui.searchFilterClear_toolButton.clicked.connect(self.clearFilter)
		self.ui.searchKeys_checkBox.toggled.connect(lambda: self.populateEnvVarList())
		self.ui.searchValues_checkBox.toggled.connect(lambda: self.populateEnvVarList())

		self.ui.envVars_treeWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		self.ui.envVars_treeWidget.itemDoubleClicked.connect(self.editEnvVar)

		self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.accept)
		self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)

		# Sort by key column
		self.ui.envVars_treeWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)

		self.reloadEnvVars()
		#self.updateToolbarUI()


	def updateToolbarUI(self):
		""" Update the toolbar UI based on the current selection.
		"""
		# No items selected...
		if len(self.ui.envVars_treeWidget.selectedItems()) == 0:
			self.ui.remove_toolButton.setEnabled(False)
			self.ui.edit_toolButton.setEnabled(False)
		# One item selected...
		elif len(self.ui.envVars_treeWidget.selectedItems()) == 1:
			self.ui.remove_toolButton.setEnabled(True)
			self.ui.edit_toolButton.setEnabled(True)
		# More than one item selected...
		else:
			self.ui.remove_toolButton.setEnabled(True)
			self.ui.edit_toolButton.setEnabled(False)


	def reloadEnvVars(self):
		""" Reload environment variables by making a copy of the os.environ
			dictionary.
		"""
		self.environ = dict(os.environ)
		self.populateEnvVarList()


	def populateEnvVarList(self, selectItem=None): #, searchFilter=""):
		""" Populate the environment variables list view.

			'selectItem' specifies an item by name that will be selected
			automatically.
			'searchFilter' is a search string to filter the list.
		"""
		searchFilter = self.ui.searchFilter_lineEdit.text()

		# Stop the widget from emitting signals
		self.ui.envVars_treeWidget.blockSignals(True)

		# Clear tree widget
		self.ui.envVars_treeWidget.clear()

		for key in self.environ.keys():
			value = self.environ[key]

			# Populate list view, using filter
			if searchFilter is not "":
				searchScope = ""
				if self.getCheckBoxValue(self.ui.searchKeys_checkBox):
					searchScope += key.lower()
				if self.getCheckBoxValue(self.ui.searchValues_checkBox):
					searchScope += value.lower()
				if searchFilter.lower() in searchScope:  # Case-insensitive
					item = self.envVarEntry(key, value)
				self.ui.searchFilterClear_toolButton.setEnabled(True)

			else:
				item = self.envVarEntry(key, value)
				self.ui.searchFilterClear_toolButton.setEnabled(False)

			if selectItem == key:
				selectedItem = item

		self.updateToolbarUI()

		# Resize column zero (Keys)
		self.ui.envVars_treeWidget.resizeColumnToContents(0)

		# Re-enable signals
		self.ui.envVars_treeWidget.blockSignals(False)

		# Set selection - view will also scroll to show selection
		if selectItem is not None:
			self.ui.envVars_treeWidget.setCurrentItem(selectedItem)


	def envVarEntry(self, key, value):
		""" Return a new entry in the environment variables list view.
		"""
		item = QtWidgets.QTreeWidgetItem(self.ui.envVars_treeWidget)
		item.setText(0, key)
		item.setText(1, value)

		return item


	def addEnvVar(self, value=""):
		""" Open the edit environment variable dialog to add a new environment
			variable.
			TODO: on Windows, when checking if the env var already exists,
			the check should be case-insensitive.
		"""
		editEnvVarDialog = edit_envvar.Dialog(parent=self)
		if editEnvVarDialog.display("", value):
			if editEnvVarDialog.key not in self.environ:
				self.environ[editEnvVarDialog.key] = editEnvVarDialog.value
				self.populateEnvVarList(selectItem=editEnvVarDialog.key)
			else:
				errorMsg = "The environment variable '%s' already exists." %editEnvVarDialog.key
				dialogMsg = errorMsg + "\nWould you like to create an environment variable with a different name?"
				print(errorMsg)

				# Show user prompt dialog
				dialogTitle = "Environment variable not created"
				if self.promptDialog(dialogMsg, dialogTitle):
					# Re-open the edit dialog and pass in the previous value
					self.addEnvVar(editEnvVarDialog.value)


	def editEnvVar(self):
		""" Open edit environment variable dialog.
		"""
		item = self.ui.envVars_treeWidget.selectedItems()[0]
		key = item.text(0)
		value = item.text(1)

		editEnvVarDialog = edit_envvar.Dialog(parent=self)
		if editEnvVarDialog.display(key, value):
			self.environ[editEnvVarDialog.key] = editEnvVarDialog.value
			self.populateEnvVarList(selectItem=editEnvVarDialog.key)


	def removeEnvVars(self):
		""" Remove the selected environment variable(s).
		"""
		for item in self.ui.envVars_treeWidget.selectedItems():
			self.environ.pop(item.text(0), None)
			index = self.ui.envVars_treeWidget.indexOfTopLevelItem(item)
			self.ui.envVars_treeWidget.takeTopLevelItem(index)


	def clearFilter(self):
		""" Clear the search filter field.
		"""
		self.ui.searchFilter_lineEdit.clear()


	def save(self):
		""" Save data by writing to the os.environ dictionary.
			Existing environment variables will be cleared first.
		"""
		# os.environ = dict(self.environ) # this doesn't actually set the env vars
		os.environ.clear()
		for key in self.environ.keys():
			os.environ[key] = self.environ[key]


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

# ----------------------------------------------------------------------------
# End main dialog class
# ============================================================================
# Run as standalone app
# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	myApp = EnvVarsDialog()
	myApp.show()
	sys.exit(app.exec_())
