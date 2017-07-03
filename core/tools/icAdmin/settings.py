#!/usr/bin/python

# [Icarus] settings.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Generic settings editor dialog


import math
import os
import sys

from Qt import __binding__, QtCore, QtGui, QtWidgets, QtCompat
from Qt.QtCore import QSignalMapper, Signal

# Import custom modules
import appPaths
import camPresets
import jobSettings
import resPresets
import units
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

class dialog(QtWidgets.QDialog):
	""" Main dialog class.
	"""
	# customSignal = Signal(str)

	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)

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

		self.shortcutRemoverOverride = QtWidgets.QShortcut(self)
		self.shortcutRemoverOverride.setKey('Ctrl+R')
		self.shortcutRemoverOverride.activated.connect(self.removeOverrides)

		# Connect signals & slots
		self.ui.categories_listWidget.currentItemChanged.connect(lambda current: self.openProperties(current.text()))

		# self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.exit)


	def display(self, settingsType="Generic", categoryLs=[], xmlData=None, autoFill=False):
		""" Display the dialog.
		"""
		self.returnValue = False

		# Some global variables to hold the currently edited attribute and its value. A bit hacky
		self.currentCategory = ""
		self.currentAttr = ""
		self.currentValue = ""

		self.settingsType = settingsType
		self.categoryLs = categoryLs
		self.xmlData = xmlData
		self.autoFill = autoFill

		self.lockUI = True

		# Instantiate XML data classes
		self.xd = jobSettings.jobSettings()
		# self.ap = appPaths.appPaths()
		# self.rp = resPresets.resPresets()
		# self.cp = camPresets.camPresets()
		self.reset()

		self.ui.setWindowTitle("%s %s" %(settingsType, WINDOW_TITLE))

		self.ui.exec_()
		return self.returnValue


	def reset(self):
		""" Initialise or reset by reloading data
		"""
		# Load data from xml file(s)
		xd_load = self.xd.loadXML(self.xmlData)
		# ap_load = self.ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'))
		# rp_load = self.rp.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'resPresets.xml'))
		# cp_load = self.cp.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'camPresets.xml'))

		#if xd_load and ap_load and rp_load:
		#	pass
		#else:
		#	print "Warning: XML data error."

		# Populate categories
		if self.categoryLs is not None:
			self.ui.categories_listWidget.clear()

			for cat in self.categoryLs:
				self.ui.categories_listWidget.addItem(cat)

			# Set the maximum size of the list widget
			self.ui.categories_listWidget.setMaximumWidth(self.ui.categories_listWidget.sizeHintForColumn(0) * 3)

			# Select the first item & show the appropriate settings panel
			if self.currentCategory == "":
				currentItem = self.ui.categories_listWidget.item(0)
			else:
				currentItem = self.ui.categories_listWidget.findItems(self.currentCategory, QtCore.Qt.MatchExactly)[0]
			currentItem.setSelected(True)
			self.openProperties(currentItem.text())


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering OK / Cancel buttons
		"""
		pass
		#if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
		#	return


	def toggleLockUI(self):
		""" Lock/unlock UI for editing
		"""
		self.lockUI = not self.lockUI
		self.ui.settings_scrollArea.setEnabled(self.lockUI)  # Disable properties panel widgets
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.lockUI)  # Disable save button


	def openProperties(self, category, storeProperties=True):
		""" Open properties panel for selected settings category
		"""
		inherited = False

		# Store the widget values of the currently open page
		# if storeProperties:
		# 	self.storeProperties(self.currentCategory)

		# verbose.print_("\n[%s]" %category, 4)
		self.currentCategory = category  # a bit hacky

		# Create the signal mapper
		# signalMapper = QSignalMapper(self)
		# if __binding__ in ('PySide'):
		# 	signalMapper.mapped.connect(self.customSignal)  # not working with PyQt5
		# else:
		# 	print("Using %s, custom signal mapper not working" %__binding__)
		# # QtCore.QObject.connect(signalMapper, QtCore.SIGNAL("mapped()"), self.customSignal, SLOT("map()"))

		# Create new frame to hold properties UI & load into frame
		self.ui.settings_frame.close()
		ui_file = "settings_%s_ui.ui" %category
		self.ui.settings_frame = QtCompat.load_ui(fname=os.path.join(os.environ['IC_FORMSDIR'], ui_file))
		self.ui.settings_verticalLayout.addWidget(self.ui.settings_frame)

		# Load values into form widgets
		widgets = self.ui.settings_frame.children()

		# # Run special function to autofill the project and job number fields - must happen before we set the widget values for defaults to work correctly
		# if category == 'job' and self.autoFill:
		# 	self.xd.autoFill(self.xmlData)

		# # Run special function to deal with units panel - must happen before we set the widget values for defaults to work correctly
		# if category == 'units':
		# 	self.setupUnits()

		# # Run special function to deal with camera panel - must happen before we set the widget values for defaults to work correctly
		# if category == 'camera':
		# 	self.setupCam()

		for widget in widgets:
			#attr = widget.objectName().split('_')[0] # use first part of widget object's name
			attr = widget.property('xmlTag')  # Use widget's dynamic 'xmlTag'

			if attr:
				# signalMapper.setMapping(widget, attr)

				value = self.xd.getValue(category, attr)
				# if category == 'camera': # or category == 'time': # nasty hack to avoid camera panel inheriting non-existent values - fix with 'inheritable' attribute to UI file
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

				# Set up handlers for different widget types & apply values...

				# Spin box(es)...
				if isinstance(widget, QtWidgets.QSpinBox):
					# widget.valueChanged.connect(signalMapper.map)
					widget.valueChanged.connect(lambda value: self.storeValue(value))
					if value is not "":
						widget.setValue(int(value))
					if storeProperties:
						self.storeValueX(attr, widget.value())

				# Double spin box(es)...
				elif isinstance(widget, QtWidgets.QDoubleSpinBox):
					# widget.valueChanged.connect(signalMapper.map)
					widget.valueChanged.connect(lambda value: self.storeValue(value))
					if value is not "":
						widget.setValue(float(value))
					if storeProperties:
						self.storeValueX(attr, widget.value())

				# Line edit(s)...
				elif isinstance(widget, QtWidgets.QLineEdit):
					# widget.textEdited.connect(signalMapper.map)
					widget.textEdited.connect(lambda text: self.storeValue(text))
					if value is not "":
						widget.setText(value)
					if storeProperties:
						self.storeValueX(attr, widget.text())

				# Plain text edit(s)...
				elif isinstance(widget, QtWidgets.QPlainTextEdit):
					# widget.textChanged.connect(signalMapper.map)
					widget.textChanged.connect(self.storeTextEditValue)
					# widget.textChanged.connect(lambda: self.storeValue(widget.plainText()))
					if value is not "":
						widget.setPlainText(value)
					if storeProperties:
						self.storeValueX(attr, widget.toPlainText())

				# Check box(es)...
				elif isinstance(widget, QtWidgets.QCheckBox):
					# widget.toggled.connect(signalMapper.map)
					widget.toggled.connect(lambda checked: self.storeCheckBoxValue(checked))
					if value is not "":
						if value == "True":
							widget.setCheckState(QtCore.Qt.Checked)
						elif value == "False":
							widget.setCheckState(QtCore.Qt.Unchecked)

				# Radio button(s)...
				elif isinstance(widget, QtWidgets.QRadioButton):
					# widget.toggled.connect(signalMapper.map)
					widget.toggled.connect(lambda checked: self.storeRadioButtonValue(checked))
					if value is not "":
						if value == widget.text():
							# widget.setAutoExclusive(False)
							widget.setChecked(QtCore.Qt.Checked)
							# widget.setAutoExclusive(True)
						# else:
						# 	widget.setAutoExclusive(False)
						# 	widget.setChecked(QtCore.Qt.Unchecked)
						# 	widget.setAutoExclusive(True)

				# Combo box(es)...
				elif isinstance(widget, QtWidgets.QComboBox):
					# widget.currentIndexChanged.connect(signalMapper.map)
					widget.currentIndexChanged.connect(lambda index: self.storeComboBoxValue(index))
					if value is not "":
						widget.setCurrentIndex(widget.findText(value))

		# Push button(s)...
		if widget.property('exec'):
			if isinstance(widget, QtWidgets.QPushButton):
				# widget.clicked.connect(signalMapper.map)
				widget.clicked.connect(self.execPushButton)

		# # Run special function to deal with time panel
		# if category == 'time':
		# 	self.setupTime()

		# # Run special function to deal with resolution panel
		# if category == 'resolution':
		# 	self.setupRes()

		# # Run special function to deal with apps panel
		# if category == 'apps':
		# 	self.setupAppVersions()


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

	# 	elif self.settingsType == 'Shot':
	# 		jd = jobSettings.jobSettings()
	# 		jd.loadXML(os.path.join(os.environ['JOBDATA'], 'jobData.xml'))
	# 		text = jd.getValue(category, attr)
	# 		inherited = True
	# 		verbose.print_('%s.%s = %s (inheriting value from job data)' %(category, attr, text), 4)

	# 	# print("%s/%s: got value %s, inherited=%s" %(category, attr, text, inherited))
	# 	return text, inherited


# --- Snipped out custom functions ---


	# def appPathsEditor(self):
	# 	""" Open the application paths editor dialog.
	# 	"""
	# 	import edit_app_paths
	# 	editAppPathsDialog = edit_app_paths.dialog(parent=self)
	# 	if editAppPathsDialog.display():
	# 		self.ap.loadXML()  # Reload XML and update comboBox contents after closing dialog

	# 	self.openProperties('apps')


	def storeValueX(self, attr, value=""):
		""" Store value in XML data.
		"""
		verbose.print_("%s.%s=%s (%s)" %(self.currentCategory, attr, value, type(value)), 4)
		self.xd.setValue(self.currentCategory, attr, str(value))


	def storeValue(self, value=""):
		""" Get the value from a Spin Box, Double Spin Box or Line Edit and
			store in XML data.
		"""
		# self.currentValue = str(val) # value must be a string for XML
		# verbose.print_('%s.%s = %s' %(self.currentCategory, self.currentAttr, self.currentValue), 4)
		# self.xd.setValue(self.currentCategory, self.currentAttr, self.currentValue)
		attr = self.sender().property('xmlTag')
		self.storeValueX(attr, value)


	def storeTextEditValue(self):
		""" Get the value from a Plain Text Edit and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		value = self.sender().toPlainText()
		self.storeValueX(attr, value)


	def storeCheckBoxValue(self, value):
		""" Get the value from a Check Box and store in XML data.
		"""
		attr = self.sender().property('xmlTag')
		self.storeValueX(attr, value)


	def storeRadioButtonValue(self, checked):
		""" Get the value from a Radio Button group and store in XML data.
		"""
		if checked:
			# attr, value = self.sender().property('xmlTag').split("_")
			attr = self.sender().property('xmlTag')
			value = self.sender().text()
			self.storeValueX(attr, value)


	def storeComboBoxValue(self, index):
		""" Get the value from a Combo Box and store in XML data.
		"""
		# frame = self.ui.settings_frame
		# print(self.currentAttr)
		# #val = frame.findChildren(QtWidgets.QComboBox, '%s_comboBox' %self.currentAttr)[0].currentText()
		# #self.storeValue(val)
		attr = self.sender().property('xmlTag')
		value = self.sender().currentText()
		self.storeValueX(attr, value)


	def execPushButton(self):
		""" Execute the function associated with a button.
		"""
		print(self.sender().objectName(), self.sender().property('exec'))


	# def storeProperties(self, category):
	# 	""" Store attribute values for all relevant widgets on selected
	# 		settings category panel.
	# 	"""
	# 	widgets = self.ui.settings_frame.children()

	# 	for widget in widgets:
	# 		attr = widget.property('xmlTag')

	# 		# Only store values of widgets which have the dynamic property
	# 		# 'xmlTag' set...
	# 		if attr:
	# 			# self.currentAttr = attr

	# 			# # Spin box(es)...
	# 			# if isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
	# 			# 	#verbose.print_("%s: %s" %(attr, widget.value()), 4)
	# 			# 	self.storeValue(widget.value())
	# 			# 	# widget.emit()

	# 			# # Combo box(es)...
	# 			# if isinstance(widget, QtWidgets.QComboBox):
	# 			# 	#verbose.print_("%s: %s" %(attr, widget.currentText()), 4)
	# 			# 	self.storeValue( widget.currentText() )
	# 			# 	#self.storeComboBoxValue( widget.currentIndex() )

	# 			# # Line edit(s)...
	# 			# if isinstance(widget, QtWidgets.QLineEdit):
	# 			# 	#verbose.print_("%s: %s" %(attr, widget.text()), 4)
	# 			# 	self.storeValue( widget.text() )

	# 			# # Plain text edit(s)...
	# 			# if isinstance(widget, QtWidgets.QPlainTextEdit):
	# 			# 	#verbose.print_("%s: %s" %(attr, widget.toPlainText()), 4)
	# 			# 	self.storeValue( widget.toPlainText() )


	def removeOverrides(self):
		""" Remove overrides and instead inherit values for widgets on the selected panel
		"""
		widgets = self.ui.settings_frame.children()

		for widget in widgets:
			attr = widget.property('xmlTag')

			if attr:
				self.xd.removeElement(self.currentCategory, attr)

		self.openProperties(self.currentCategory, storeProperties=False)


	def save(self):
		""" Save data.
		"""
		# Store the values from widgets on the current page
		#self.storeProperties(self.currentCategory)
		for cat in self.categoryLs:
			self.openProperties(cat)
			#self.storeProperties(cat)

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
			self.ui.hide()
			self.returnValue = True
		else:
			self.exit() # There's a bug where all property panel widgets become visible if a save fails. As a quick dodgy workaround we exit so we don't see it happen.


	def exit(self):
		""" Exit the dialog.
		"""
		self.ui.hide()
		self.returnValue = False

