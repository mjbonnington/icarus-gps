#!/usr/bin/python

# [Icarus] settings.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Generic settings editor dialog.


import math
import os
import sys

from Qt import QtCore, QtWidgets, QtCompat

# Import custom modules
import settingsData
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


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class SettingsDialog(QtWidgets.QDialog):
	""" Main dialog class.
	"""
	def __init__(self, parent=None):
		super(SettingsDialog, self).__init__(parent)

		# Set object name and window title
		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle(WINDOW_TITLE)

		# Load UI & stylesheet
		self.ui = QtCompat.load_ui(fname=os.path.join(os.environ['IC_FORMSDIR'], UI_FILE))
		if STYLESHEET is not None:
			qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
			with open(qss, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set up keyboard shortcuts
		#self.shortcutSave = QtWidgets.QShortcut(self)
		#self.shortcutSave.setKey('Ctrl+S')
		#self.shortcutSave.activated.connect(self.save)

		self.shortcutLock = QtWidgets.QShortcut(self)
		self.shortcutLock.setKey('Ctrl+L')
		self.shortcutLock.activated.connect(self.toggleLockUI)

		# self.shortcutRemoveOverride = QtWidgets.QShortcut(self)
		# self.shortcutRemoveOverride.setKey('Ctrl+R')
		# self.shortcutRemoveOverride.activated.connect(self.removeOverrides)

		# Connect signals & slots
		self.ui.categories_listWidget.currentItemChanged.connect(lambda current: self.openProperties(current.text()))

		# self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.exit)


	def display(self, 
		        settingsType="Generic", 
		        categoryLs=[], 
		        xmlData=None, 
		        inherit=None, 
		        autoFill=False):
		""" Display the dialog.
			'settingsType' is the name given to the settings dialog.
			'categoryLs' is a list of categories, should correspond to a page
			of properties defined by a .ui file.
			'xmlData' is the path to the XML file storing the settings.
			'inherit' whether to inherit any values.
			'autoFill' when true, attempt to fill some fields automatically.
		"""
		self.returnValue = False

		# Declare some global variables
		self.currentCategory = ""

		self.settingsType = settingsType
		self.categoryLs = categoryLs
		self.xmlData = xmlData
		self.inherit = inherit
		self.autoFill = autoFill

		self.lockUI = True

		# Instantiate XML data classes
		self.xd = settingsData.settingsData()

		self.reset()

		self.ui.setWindowTitle("%s %s" %(settingsType, WINDOW_TITLE))

		self.ui.exec_()
		return self.returnValue


	def reset(self):
		""" Initialise or reset by reloading data.
		"""
		# Load data from xml file(s)
		xd_load = self.xd.loadXML(self.xmlData)

		# Populate categories
		if self.categoryLs is not None:
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


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		pass
		#if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
		#	return


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

		# Create new frame to hold properties UI & load into frame
		self.ui.settings_frame.close()
		self.ui.settings_frame = QtCompat.load_ui(fname=os.path.join(os.environ['IC_FORMSDIR'], ui_file))
		self.ui.settings_verticalLayout.addWidget(self.ui.settings_frame)

		# Load helper module
		try:
			exec_str = 'import %s as sh; helper = sh.helper(self, self.ui.settings_frame)' %helper_module
			# print(exec_str)
			exec(exec_str)
		except ImportError:
			pass


	def openProperties(self, category, storeProperties=True):
		""" Open properties panel for selected settings category.
		"""
		self.currentCategory = category
		verbose.print_(self.currentCategory, 4)

		self.loadPanel(category)

		inherited = False
		inheritable = False
		if (self.inherit is not None) and self.ui.settings_frame.property('inheritable'):
			verbose.print_("(values inheritable from %s)" %self.inherit, 4)
			inheritable = True

		# Load values into form widgets
		widgets = self.ui.settings_frame.children()

		# # Run special function to autofill the project and job number fields - must happen before we set the widget values for defaults to work correctly
		# if category == 'job' and self.autoFill:
		# 	self.xd.autoFill(self.xmlData)

		for widget in widgets:

			# Set up handler for push button(s)...
			if widget.property('exec'):
				if isinstance(widget, QtWidgets.QPushButton):
					widget.clicked.connect(self.execPushButton)

			# Set up handlers for different widget types & apply values
			attr = widget.property('xmlTag')
			if attr:
				value = self.xd.getValue(category, attr)
				# if inheritable:
				# 	value = self.xd.getValue(category, attr)
				# else:
				# 	value, inherited = self.inheritFrom(category, attr)

				# if inherited:
				# 	widget.setProperty('xmlTag', None)
				# 	widget.setProperty('inheritedValue', True)
				# 	widget.setToolTip("This value is being inherited. Change the value to override the inherited value.")

				# 	# Apply pop-up menu to remove override - can't get to work here
				# 	#widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

				# 	#actionRemoveOverride = QtWidgets.QAction("Remove override", None)
				# 	#actionRemoveOverride.triggered.connect(self.removeOverrides)
				# 	#widget.addAction(actionRemoveOverride)

				# Spin box(es)...
				if isinstance(widget, QtWidgets.QSpinBox):
					if value is not "":
						widget.setValue(int(value))
					if storeProperties:
						self.storeValue(attr, widget.value())
					# widget.valueChanged.connect(lambda value: self.storeWidgetValue(value))
					widget.valueChanged.connect(self.storeSpinBoxValue)

				# Double spin box(es)...
				elif isinstance(widget, QtWidgets.QDoubleSpinBox):
					if value is not "":
						widget.setValue(float(value))
					if storeProperties:
						self.storeValue(attr, widget.value())
					# widget.valueChanged.connect(lambda value: self.storeWidgetValue(value))
					widget.valueChanged.connect(self.storeSpinBoxValue)

				# Line edit(s)...
				elif isinstance(widget, QtWidgets.QLineEdit):
					if value is not "":
						widget.setText(value)
					if storeProperties:
						self.storeValue(attr, widget.text())
					# widget.textEdited.connect(lambda text: self.storeWidgetValue(text))
					widget.textEdited.connect(self.storeLineEditValue)

				# Plain text edit(s)...
				elif isinstance(widget, QtWidgets.QPlainTextEdit):
					if value is not "":
						widget.setPlainText(value)
					if storeProperties:
						self.storeValue(attr, widget.toPlainText())
					widget.textChanged.connect(self.storeTextEditValue)

				# Check box(es)...
				elif isinstance(widget, QtWidgets.QCheckBox):
					if value is not "":
						if value == "True":
							widget.setCheckState(QtCore.Qt.Checked)
						elif value == "False":
							widget.setCheckState(QtCore.Qt.Unchecked)
					if storeProperties:
						self.storeValue(attr, self.getCheckBoxValue(widget))
					# widget.toggled.connect(lambda checked: self.storeCheckBoxValue(checked))
					widget.toggled.connect(self.storeCheckBoxValue)

				# Radio button(s)...
				elif isinstance(widget, QtWidgets.QRadioButton):
					if value is not "":
						widget.setAutoExclusive(False)
						if value == widget.text():
							widget.setChecked(True)
						else:
							widget.setChecked(False)
						widget.setAutoExclusive(True)
					if storeProperties:
						if widget.isChecked():
							self.storeValue(attr, widget.text())
					# widget.toggled.connect(lambda checked: self.storeRadioButtonValue(checked))
					widget.toggled.connect(self.storeRadioButtonValue)

				# Combo box(es)...
				elif isinstance(widget, QtWidgets.QComboBox):
					if value is not "":
						widget.setCurrentIndex(widget.findText(value))
					if storeProperties:
						self.storeValue(attr, widget.currentText())
					# widget.currentIndexChanged.connect(lambda index: self.storeComboBoxValue(index))
					widget.currentIndexChanged.connect(self.storeComboBoxValue)


	def inheritFrom(self, category, attr):
		""" Tries to get a value from the current settings type, and if no
			value is found tries to inherit the value instead.
			Returns two values:
			'text' - the value of the requested attribute.
			'inherited' - a Boolean value which is true if the value was
			inherited.
		"""
		text = self.xd.getValue(category, attr)
		inherited = False

		if text is not "":
			pass

		# elif self.settingsType == 'Shot':
		elif self.inherit == 'Job':
			jd = settingsData.settingsData()
			jd.loadXML(os.path.join(os.environ['JOBDATA'], 'jobData.xml'))
			text = jd.getValue(category, attr)
			inherited = True
			verbose.print_('%s.%s = %s (inheriting value from job data)' %(category, attr, text), 4)

		# print("%s/%s: got value %s, inherited=%s" %(category, attr, text, inherited))
		return text, inherited


# --- Snipped out custom functions ---


	# @QtCore.Slot()
	def execPushButton(self):
		""" Execute the function associated with a button.
		"""
		verbose.print_("%s %s" %(self.sender().objectName(), self.sender().property('exec')), 4)


	# @QtCore.Slot()
	def storeSpinBoxValue(self):
		""" Get the value from a Spin Box and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		value = self.sender().value()
		self.storeValue(attr, value)


	# @QtCore.Slot()
	def storeLineEditValue(self):
		""" Get the value from a Line Edit and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		value = self.sender().text()
		self.storeValue(attr, value)


	# @QtCore.Slot()
	def storeTextEditValue(self):
		""" Get the value from a Plain Text Edit and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		value = self.sender().toPlainText()
		self.storeValue(attr, value)


	# @QtCore.Slot()
	def storeCheckBoxValue(self):
		""" Get the value from a Check Box and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		value = self.getCheckBoxValue(self.sender())
		self.storeValue(attr, value)


	# @QtCore.Slot()
	def storeRadioButtonValue(self):
		""" Get the value from a Radio Button group and store in XML data.
		"""
		if self.sender().isChecked():
			attr = self.sender().property('xmlTag')
			value = self.sender().text()
			self.storeValue(attr, value)


	# @QtCore.Slot()
	def storeComboBoxValue(self):
		""" Get the value from a Combo Box and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		value = self.sender().currentText()
		self.storeValue(attr, value)


	def storeValue(self, attr, value=""):
		""" Store value in XML data.
		"""
		verbose.print_("%20s %s.%s=%s" %(type(value), self.currentCategory, attr, value), 4)
		self.xd.setValue(self.currentCategory, attr, str(value))


	def getCheckBoxValue(self, checkBox):
		""" Get the value from a checkbox and return a Boolean value.
		"""
		if checkBox.checkState() == QtCore.Qt.Checked:
			return True
		else:
			return False


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


	def save(self):
		""" Save data.
		"""
		# Store the values from widgets on all pages
		for category in self.categoryLs:
			self.openProperties(category, storeProperties=True)

		# Save XML file
		if self.xd.saveXML():
			verbose.message("%s settings saved." %self.settingsType)
			return True
		else:
			verbose.error("%s settings could not be saved." %self.settingsType)
			return False


	def saveAndExit(self):
		""" Save data and exit dialog.
		"""
		if self.save():
			# self.ui.hide()
			self.returnValue = True
			self.ui.accept()
		else:
			self.exit()  # There's a bug where all property panel widgets become visible if a save fails. As a quick dodgy workaround we exit so we don't see it happen.


	def exit(self):
		""" Exit the dialog.
		"""
		# self.ui.hide()
		self.returnValue = False
		self.ui.reject()

