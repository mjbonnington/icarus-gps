#!/usr/bin/python

# [Icarus] job_settings__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Generic settings editor dialog
# TODO: inherit the generic settings class, containing the non job-specific
# methods from this class


import math
import os
import sys

from Qt import QtCore, QtGui, QtWidgets, QtCompat
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
STYLESHEET = None  # Set to None to use the parent app's stylesheet


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class settingsDialog(QtWidgets.QDialog):
	""" Main dialog class.
	"""
	# Custom signals
	customSignal = Signal(str)

	def __init__(self, parent=None, settingsType="Generic", categoryLs=[], xmlData=None, autoFill=False):
		super(settingsDialog, self).__init__(parent)

		# Set object name and window title
		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle("%s %s" %(settingsType, WINDOW_TITLE))

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Load UI
		self.ui = QtCompat.load_ui(fname=os.path.join(os.path.dirname(os.path.realpath(__file__)), UI_FILE))
		if STYLESHEET is not None:
			with open(STYLESHEET, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Some global variables to hold the currently edited attribute and its value. A bit hacky
		self.currentCategory = ""
		self.currentAttr = ""
		self.currentValue = ""

		self.settingsType = settingsType
		self.categoryLs = categoryLs
		self.xmlData = xmlData
		self.autoFill = autoFill

		self.lockUI = True

		self.returnValue = False

		# Instantiate XML data classes
		self.jd = jobSettings.jobSettings()
		self.ap = appPaths.appPaths()
		self.rp = resPresets.resPresets()
		self.cp = camPresets.camPresets()
		self.reset()

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
		self.ui.categories_listWidget.currentItemChanged.connect( lambda current: self.openProperties(current.text()) )

		#self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.exit)


	def reset(self):
		""" Initialise or reset by reloading data
		"""
		# Load data from xml file(s)
		jd_load = self.jd.loadXML(self.xmlData)
		ap_load = self.ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'))
		rp_load = self.rp.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'resPresets.xml'))
		cp_load = self.cp.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'camPresets.xml'))

		#if jd_load and ap_load and rp_load:
		#	pass
		#else:
		#	print "Warning: XML data error."

		# Populate categories
		if self.categoryLs is not None:
			self.ui.categories_listWidget.clear()

			for cat in self.categoryLs:
				self.ui.categories_listWidget.addItem(cat)

			# Set the maximum size of the list widget
			self.ui.categories_listWidget.setMaximumWidth( self.ui.categories_listWidget.sizeHintForColumn(0) + 64 )

			# Select the first item & show the appropriate settings panel
			if self.currentCategory == "":
				currentItem = self.ui.categories_listWidget.item(0)
			else:
				currentItem = self.ui.categories_listWidget.findItems(self.currentCategory, QtCore.Qt.MatchExactly)[0]
			currentItem.setSelected(True)
			self.openProperties( currentItem.text() )


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
		#self.ui.settings_scrollArea.setEnabled(self.lockUI) # disable properties panel widgets
		self.ui.settings_buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(self.lockUI) # disable save button


	def importUI(self, ui_file, frame):
		""" Import specified UI file and insert into specified frame
		"""
		try:
			exec('from %s import *' %ui_file)
			#exec('reload(%s)' %ui_file)
			properties_panel = Ui_settings_frame()
			properties_panel.setupUi(frame)

		except ImportError:
			verbose.error("The '%s' properties panel could not be loaded." %ui_file)


	def openProperties(self, category, storeProperties=True):
		""" Open properties panel for selected settings category
		"""
		inherited = False

		# Store the widget values of the currently open page
		if storeProperties:
			self.storeProperties(self.currentCategory)

		# verbose.print_("\n[%s]" %category, 4)
		self.currentCategory = category # a bit hacky

		# Create the signal mapper
		signalMapper = QSignalMapper(self)
		signalMapper.mapped.connect(self.customSignal)  # TEMP DISABLE new-style signal connection not working with PyQt5
		# QtCore.QObject.connect(signalMapper, QtCore.SIGNAL("mapped()"), self.customSignal, SLOT("map()"))

		# Create new frame to hold properties UI
		# self.ui.settings_frame.close()
		# self.ui.settings_frame = QtWidgets.QFrame(self.ui.settings_scrollAreaWidgetContents)
		# self.ui.settings_frame.setObjectName("settings_frame")
		# self.ui.verticalLayout_2.addWidget(self.ui.settings_frame)

		# Load approprate UI file into frame
		# self.importUI('settings_%s_ui' %category, self.ui.settings_frame)

		self.ui.settings_frame.close()
		ui_file = "settings_%s_ui.ui" %category
		self.ui.settings_frame = QtCompat.load_ui(fname=os.path.join(os.path.dirname(os.path.realpath(__file__)), ui_file))
		self.ui.verticalLayout_2.addWidget(self.ui.settings_frame)

		# Load values into form widgets
		widgets = self.ui.settings_frame.children()

		# Run special function to autofill the project and job number fields - must happen before we set the widget values for defaults to work correctly
		if category == 'job' and self.autoFill:
			self.jd.autoFill(self.xmlData)

		# Run special function to deal with units panel - must happen before we set the widget values for defaults to work correctly
		if category == 'units':
			self.setupUnits()

		# Run special function to deal with camera panel - must happen before we set the widget values for defaults to work correctly
		if category == 'camera':
			self.setupCam()

		for widget in widgets:
			#attr = widget.objectName().split('_')[0] # use first part of widget object's name
			attr = widget.property('xmlTag') # use widget's dynamic 'xmlTag'

			if attr:
				signalMapper.setMapping(widget, attr)

				if category == 'camera': # or category == 'time': # nasty hack to avoid camera panel inheriting non-existent values - fix with 'inheritable' attribute to UI file
					text = self.jd.getValue(category, attr)
				else:
					text, inherited = self.inheritFrom(category, attr)

				if inherited:
					widget.setProperty('xmlTag', None)
					widget.setProperty('inheritedValue', True)
					widget.setToolTip("This value is being inherited. Change the value to override the inherited value.")

					# Apply pop-up menu to remove override - can't get to work here
					#widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

					#actionRemoveOverride = QtWidgets.QAction("Remove override", None)
					#actionRemoveOverride.triggered.connect(self.removeOverrides)
					#widget.addAction(actionRemoveOverride)

				# Combo box(es)...
				if isinstance(widget, QtWidgets.QComboBox):
					if text is not "":
						widget.setCurrentIndex( widget.findText(text) )
					#print "%s: %s" %(attr, widget.currentText())
					widget.currentIndexChanged.connect(signalMapper.map)
					widget.currentIndexChanged.connect( lambda current: self.storeComboBoxValue(current) )

				# Line edit(s)...
				if isinstance(widget, QtWidgets.QLineEdit):
					if text is not "":
						widget.setText(text)
					#print "%s: %s" %(attr, widget.text())
					widget.textEdited.connect(signalMapper.map)
					widget.textEdited.connect( lambda current: self.storeValue(current) )

				# Plain text edit(s)...
				if isinstance(widget, QtWidgets.QPlainTextEdit):
					if text is not "":
						widget.setPlainText(text)
					#print "%s: %s" %(attr, widget.text())
					widget.textChanged.connect(signalMapper.map)
					widget.textChanged.connect( lambda: self.storeValue() ) # This seems to give an TypeError when passing 'current', but still works as expected

				# Spin box(es)...
				if isinstance(widget, QtWidgets.QSpinBox):
					if text is not "":
						widget.setValue( int(text) )
					#print "%s: %s" %(attr, widget.value())
					widget.valueChanged.connect(signalMapper.map)
					widget.valueChanged.connect( lambda current: self.storeValue(current) )

				# Double spin box(es)...
				if isinstance(widget, QtWidgets.QDoubleSpinBox):
					if text is not "":
						widget.setValue( float(text) )
					#print "%s: %s" %(attr, widget.value())
					widget.valueChanged.connect(signalMapper.map)
					widget.valueChanged.connect( lambda current: self.storeValue(current) )

		# Run special function to deal with resolution panel
		if category == 'time':
			self.setupTime()

		# Run special function to deal with resolution panel
		if category == 'resolution':
			self.setupRes()

		# Run special function to deal with apps panel
		if category == 'apps':
			self.setupAppVersions()


	def inheritFrom(self, category, attr):
		""" Tries to get a value from the current settings type, and if no value is found tries to inherit the value instead
			Returns two values:
			text - the value of the requested attribute
			inherited - a Boolean value which is true if the value was inherited
		"""
		text = self.jd.getValue(category, attr)
		inherited = False

		if text is not "":
			pass

		elif self.settingsType == 'Shot':
			jd = jobSettings.jobSettings()
			jd.loadXML( os.path.join(os.environ['JOBDATA'], 'jobData.xml') )
			text = jd.getValue(category, attr)
			inherited = True
			verbose.print_('%s.%s = %s (inheriting value from job data)' %(category, attr, text), 4)

		#print "%s/%s: got value %s, inherited=%s" %(category, attr, text, inherited)
		return text, inherited


	def setupUnits(self):
		""" Setup units properties panel
		"""
		frame = self.ui.settings_frame

		# Populate combo boxes with presets
		for item in units.linear:
			frame.findChildren(QtWidgets.QComboBox, 'linear_comboBox')[0].addItem(item[0]) # Find a way to display nice names but store short names internally

		for item in units.angular:
			frame.findChildren(QtWidgets.QComboBox, 'angle_comboBox')[0].addItem(item[0]) # Find a way to display nice names but store short names internally

		for item in units.time:
			frame.findChildren(QtWidgets.QComboBox, 'time_comboBox')[0].addItem(item[0]) # Find a way to display nice names but store short names internally

		# Set default values - this must happen before values are read from XML data
		frame.findChildren(QtWidgets.QComboBox, 'linear_comboBox')[0].setCurrentIndex(1) # cm
		frame.findChildren(QtWidgets.QComboBox, 'angle_comboBox')[0].setCurrentIndex(0) # deg
		frame.findChildren(QtWidgets.QComboBox, 'time_comboBox')[0].setCurrentIndex(1) # pal

		# Set FPS spin box to correct value based on time combo box selection
		self.setFPS( frame.findChildren(QtWidgets.QComboBox, 'time_comboBox')[0].currentIndex() )

		# Connect signals and slots
		frame.findChildren(QtWidgets.QComboBox, 'time_comboBox')[0].currentIndexChanged.connect(lambda current: self.setFPS(current))
		#frame.findChildren(QtWidgets.QSpinBox, 'fps_spinBox')[0].valueChanged.connect(lambda value: self.setTimeUnit(value))


	def setFPS(self, current=None):
		""" Set FPS spin box value based on time unit combo box
		"""
		frame = self.ui.settings_frame
		frame.findChildren(QtWidgets.QSpinBox, 'fps_spinBox')[0].setValue(units.time[current][2])


	#def setTimeUnit(self, current=None):
	#	""" Set time unit combo box value based on FPS - currently disabled
	#	"""
	#	frame = self.ui.settings_frame
	#	frame.findChildren(QtWidgets.QSpinBox, 'time_comboBox')[0].setCurrentIndex(0)


	def setupTime(self):
		""" Setup time properties panel
		"""
		frame = self.ui.settings_frame

		self.calcTimeValues()

		# Connect signals and slots
		frame.findChildren(QtWidgets.QSpinBox, 'rangeStart_spinBox')[0].valueChanged.connect(self.calcTimeValues)
		frame.findChildren(QtWidgets.QSpinBox, 'rangeEnd_spinBox')[0].valueChanged.connect(self.calcTimeValues)


	def calcTimeValues(self):
		""" Calculate time values (frame range, duration, in/out, etc.)
		"""
		frame = self.ui.settings_frame

		rangeStart = frame.findChildren(QtWidgets.QSpinBox, 'rangeStart_spinBox')[0].value()
		rangeEnd = frame.findChildren(QtWidgets.QSpinBox, 'rangeEnd_spinBox')[0].value()

		durationFull = rangeEnd - rangeStart + 1

		# Stop the other widgets from emitting signals
		frame.findChildren(QtWidgets.QSpinBox, 'rangeStart_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'rangeEnd_spinBox')[0].blockSignals(True)

		# Update widgets
		frame.findChildren(QtWidgets.QLabel, 'rangeInfo_label')[0].setText("(duration: %d frames)" %durationFull)

		frame.findChildren(QtWidgets.QSpinBox, 'rangeStart_spinBox')[0].setMaximum(rangeEnd)
		frame.findChildren(QtWidgets.QSpinBox, 'rangeEnd_spinBox')[0].setMinimum(rangeStart)
		frame.findChildren(QtWidgets.QSpinBox, 'posterFrame_spinBox')[0].setMinimum(rangeStart)
		frame.findChildren(QtWidgets.QSpinBox, 'posterFrame_spinBox')[0].setMaximum(rangeEnd)

		# Re-enable signals
		frame.findChildren(QtWidgets.QSpinBox, 'rangeStart_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'rangeEnd_spinBox')[0].blockSignals(False)


	def setupRes(self):
		""" Setup resolution properties panel
		"""
		frame = self.ui.settings_frame

		# Populate combo box with presets
		presets = self.rp.getPresets()
		comboBox = frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0]

		for item in presets:
			comboBox.addItem(item)
		#comboBox.setCurrentIndex(0)
		width = frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].value()
		height = frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].value()
		comboBox.setCurrentIndex( comboBox.findText( self.rp.getPresetFromRes(width, height) ) )

		self.calcAspectRatio()
		self.checkProxyRes()

		# Connect signals and slots
		frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].currentIndexChanged.connect(self.updateResFromPreset)
		frame.findChildren(QtWidgets.QCheckBox, 'preserveAR_checkBox')[0].stateChanged.connect(self.calcAspectRatio)
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].valueChanged.connect(self.updateResFullWidth)
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].valueChanged.connect(self.updateResFullHeight)
		frame.findChildren(QtWidgets.QRadioButton, 'proxyModeScale_radioButton')[0].toggled.connect(self.calcProxyRes)
		frame.findChildren(QtWidgets.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].valueChanged.connect(self.calcProxyRes)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].valueChanged.connect(self.updateResProxyWidth)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].valueChanged.connect(self.updateResProxyHeight)


	def calcAspectRatio(self):
		""" Calculate aspect ratio
		"""
		frame = self.ui.settings_frame

		fullWidth = frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullHeight = frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].value()
		self.aspectRatio = float(fullWidth) / float(fullHeight)

		#print "aspect ratio: %f" %self.aspectRatio


	def updateResFromPreset(self, index = -1):
		""" Update resolution settings when a preset is chosen
		"""
		frame = self.ui.settings_frame

		preset = frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].currentText()
		width = int( self.rp.getValue(preset, 'width') )
		height = int( self.rp.getValue(preset, 'height') )

		# Stop the other widgets from emitting signals
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		# Update widgets
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].setValue(width)
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].setValue(height)

		# Store values (a little bit hacky and nasty but needs to be done manually as signals are blocked)
		self.currentAttr = 'fullWidth'; self.storeValue(width)
		self.currentAttr = 'fullHeight'; self.storeValue(height)

		self.calcAspectRatio()
		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)

		#print index, frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].currentText()


	def updateResFullWidth(self, width = -1):
		""" Update resolution when width is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtWidgets.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			height = int(math.ceil(width/self.aspectRatio))
		else:
			height = frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].value()

		#print "full res: [%d]x%d (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Set the preset to 'Custom'
		comboBox = frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0]
		comboBox.setCurrentIndex( comboBox.findText( self.rp.getPresetFromRes(width, height) ) )
		#comboBox.setCurrentIndex( comboBox.findText('Custom') )

		# Update height widget
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].setValue(height)

		# Store values (a little bit hacky and nasty but needs to be done manually as signals are blocked)
		self.currentAttr = 'fullHeight'; self.storeValue(height)

		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)


	def updateResFullHeight(self, height = -1):
		""" Update resolution when height is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtWidgets.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			width = int(math.ceil(height*self.aspectRatio))
		else:
			width = frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].value()

		#print "full res: %dx[%d] (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Set the preset to 'Custom'
		comboBox = frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0]
		comboBox.setCurrentIndex( comboBox.findText( self.rp.getPresetFromRes(width, height) ) )
		#comboBox.setCurrentIndex( comboBox.findText('Custom') )

		# Update width widget
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].setValue(width)

		# Store values (a little bit hacky and nasty but needs to be done manually as signals are blocked)
		self.currentAttr = 'fullWidth'; self.storeValue(width)

		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		frame.findChildren(QtWidgets.QComboBox, 'resPreset_comboBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)


	def updateResProxyWidth(self, width = -1):
		""" Update proxy resolution when width is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtWidgets.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			height = int(math.ceil(width/self.aspectRatio))
		else:
			height = frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].value()

		#print "proxy res: [%d]x%d (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Update height widget
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].setValue(height)

		# Store values (a little bit hacky and nasty but needs to be done manually as signals are blocked)
		self.currentAttr = 'proxyHeight'; self.storeValue(height)

		# Re-enable signals
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)


	def updateResProxyHeight(self, height = -1):
		""" Update proxy resolution when height is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtWidgets.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			width = int(math.ceil(height*self.aspectRatio))
		else:
			width = frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].value()

		#print "proxy res: %dx[%d] (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Update width widget
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].setValue(width)

		# Store values (a little bit hacky and nasty but needs to be done manually as signals are blocked)
		self.currentAttr = 'proxyWidth'; self.storeValue(width)

		# Re-enable signals
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)


	def calcProxyRes(self, proxyScale = -1, fullWidth = -1, fullHeight = -1):
		""" Calculate proxy resolution
		"""
		frame = self.ui.settings_frame

		# If fullWidth or fullHeight not specified, get values from widgets
		if fullWidth < 0:
			fullWidth = frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].value()
		if fullHeight < 0:
			fullHeight = frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].value()

		if frame.findChildren(QtWidgets.QRadioButton, 'proxyModeScale_radioButton')[0].isChecked():
			proxyMode = 'scale'
			proxyScale = frame.findChildren(QtWidgets.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].value()
			proxyRes = int(fullWidth * proxyScale), int(fullHeight * proxyScale)
		else:
			proxyMode = 'res'
			proxyScale = -1
			proxyRes = frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].value(), frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].value()

		#print "proxy res: %dx%d (%s: %f)" %(proxyRes[0], proxyRes[1], proxyMode, proxyScale)

		# Update widgets
		frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].setValue(proxyRes[0])
		frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].setValue(proxyRes[1])


	def checkProxyRes(self):
		""" Check proxy resolution matches full resolution * scale and set appropriate proxy mode
		"""
		frame = self.ui.settings_frame

		fullWidth = frame.findChildren(QtWidgets.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullHeight = frame.findChildren(QtWidgets.QSpinBox, 'fullHeight_spinBox')[0].value()
		proxyWidth = frame.findChildren(QtWidgets.QSpinBox, 'proxyWidth_spinBox')[0].value()
		proxyHeight = frame.findChildren(QtWidgets.QSpinBox, 'proxyHeight_spinBox')[0].value()
		proxyScale = frame.findChildren(QtWidgets.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].value()

		if (proxyWidth == fullWidth*proxyScale) and (proxyHeight == fullHeight*proxyScale):
			frame.findChildren(QtWidgets.QRadioButton, 'proxyModeScale_radioButton')[0].setChecked(True)
			frame.findChildren(QtWidgets.QRadioButton, 'proxyModeRes_radioButton')[0].setChecked(False)
		else:
			frame.findChildren(QtWidgets.QRadioButton, 'proxyModeScale_radioButton')[0].setChecked(False)
			frame.findChildren(QtWidgets.QRadioButton, 'proxyModeRes_radioButton')[0].setChecked(True)


	def setupCam(self):
		""" Setup camera properties panel
		"""
		frame = self.ui.settings_frame

		# Populate combo box with presets
		camPresets = self.cp.getPresets()
		camera_comboBox = frame.findChildren(QtWidgets.QComboBox, 'camera_comboBox')[0]

		for item in camPresets:
			camera_comboBox.addItem(item)
		#camera_comboBox.setCurrentIndex(0)
		width = frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackWidth_doubleSpinBox')[0].value()
		height = frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackHeight_doubleSpinBox')[0].value()
	#	camera_comboBox.setCurrentIndex( camera_comboBox.findText( self.rp.getPresetFromRes(width, height) ) )

		# Connect signals and slots
		camera_comboBox.currentIndexChanged.connect(self.updateFilmbackFromPreset)
		frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackWidth_doubleSpinBox')[0].valueChanged.connect( lambda: self.resetPresetToCustom('camera_comboBox') )
		frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackHeight_doubleSpinBox')[0].valueChanged.connect( lambda: self.resetPresetToCustom('camera_comboBox') )


	def updateFilmbackFromPreset(self, index = -1):
		""" Update filmback settings when a preset is chosen
		"""
		frame = self.ui.settings_frame

		camera = frame.findChildren(QtWidgets.QComboBox, 'camera_comboBox')[0].currentText()
		if camera != 'Custom':
			sensorWidth, sensorHeight = self.cp.getFilmback(camera)

			# Stop the other widgets from emitting signals
			frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackWidth_doubleSpinBox')[0].blockSignals(True)
			frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackHeight_doubleSpinBox')[0].blockSignals(True)

			# Update widgets
			frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackWidth_doubleSpinBox')[0].setValue(sensorWidth)
			frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackHeight_doubleSpinBox')[0].setValue(sensorHeight)

			# Re-enable signals
			frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackWidth_doubleSpinBox')[0].blockSignals(False)
			frame.findChildren(QtWidgets.QDoubleSpinBox, 'filmbackHeight_doubleSpinBox')[0].blockSignals(False)


	def resetPresetToCustom(self, comboBoxName):
		""" Reset filmback settings preset combo box to 'Custom' when values are changed manually
		"""
		frame = self.ui.settings_frame
		comboBox = frame.findChildren(QtWidgets.QComboBox, comboBoxName)[0]
		comboBox.setCurrentIndex( comboBox.findText('Custom') )


	def setupAppVersions(self, selectCurrent=True):
		""" Setup application version properties panel and populate combo boxes
		"""
		frame = self.ui.settings_frame

		# Create the signal mapper
		signalMapper = QSignalMapper(self)
		signalMapper.mapped.connect(self.customSignal)  # TEMP DISABLE new-style signal connection not working with PyQt5

		noSelectText = ""
		apps = self.ap.getApps() # get apps and versions
		formLayout = frame.findChildren(QtWidgets.QFormLayout, 'formLayout')
		appPaths_pushButton = frame.findChildren(QtWidgets.QPushButton, 'appPaths_pushButton')

		formLayout[0].setWidget(len(apps), QtWidgets.QFormLayout.FieldRole, appPaths_pushButton[0]) # move edit button to bottom of form
		appPaths_pushButton[0].clicked.connect(self.appPathsEditor)

		for i, app in enumerate(apps):
			label = QtWidgets.QLabel(frame)
			label.setObjectName("%s_label" %app)
			label.setText("%s:" %app)
			formLayout[0].setWidget(i, QtWidgets.QFormLayout.LabelRole, label)

			comboBox = QtWidgets.QComboBox(frame)
			comboBox.setObjectName("%s_comboBox" %app)
			comboBox.clear()

			signalMapper.setMapping(comboBox, app)

			versions = self.ap.getVersions(app) # popluate the combo box with available app versions
			availableVersions = []
			for version in versions:
				if version == '[template]':
					pass
					#availableVersions.append(noSelectText)
				else:
					availableVersions.append(version)
			for version in availableVersions:
				comboBox.addItem(version)

			if selectCurrent: # set selection to correct entry
				try:
					text = self.jd.getAppVersion(app)
				except AttributeError:
					text = noSelectText
					#comboBox.insertItem(text, 0)
				#print "%s: %s" %(app, text)
				comboBox.setCurrentIndex( comboBox.findText(text) )

			comboBox.currentIndexChanged.connect(signalMapper.map)
			comboBox.currentIndexChanged.connect( lambda current: self.storeComboBoxValue(current) )
			formLayout[0].setWidget(i, QtWidgets.QFormLayout.FieldRole, comboBox)


	# def resPresetsEditor(self):
	# 	""" Open the resolution presets editor dialog. Not yet implemented.
	# 	"""
	# 	import set_res_presets
	# 	reload(set_res_presets)
	# 	self.editResPresets = set_res_presets__main__.editResPresetsDialog()
	# 	self.editResPresets.show()
	# 	self.editResPresets.exec_()

	# 	# Reload resPresets XML and update comboBox contents after closing dialog
	# 	self.rp.loadXML()
	# 	self.openProperties('resolution')


	def appPathsEditor(self):
		""" Open the application paths editor dialog.
		"""
		import edit_app_paths
		editAppPathsDialog = edit_app_paths.dialog(parent=self)
		if editAppPathsDialog.display():
			self.ap.loadXML()  # Reload XML and update comboBox contents after closing dialog

		self.openProperties('apps')


	def storeValue(self, val=""):
		""" Stores the currently edited attribute value into the XML data
		"""
		self.currentValue = str(val) # value must be a string for XML
		verbose.print_('%s.%s = %s' %(self.currentCategory, self.currentAttr, self.currentValue), 4)
		self.jd.setValue(self.currentCategory, self.currentAttr, self.currentValue)


	def storeComboBoxValue(self, index):
		""" Get the value of the currently edited ComboBox. A bit hacky
		"""
		frame = self.ui.settings_frame
		val = frame.findChildren(QtWidgets.QComboBox, '%s_comboBox' %self.currentAttr)[0].currentText()
		self.storeValue(val)


	def storeProperties(self, category):
		""" Store properties for all relevant widgets on selected settings category panel
		"""
		widgets = self.ui.settings_frame.children()

		for widget in widgets:
			attr = widget.property('xmlTag')

			# Only store values of wigets which have the dynamic property 'xmlTag' set
			if attr:
				self.currentAttr = attr

				# Combo box(es)...
				if isinstance(widget, QtWidgets.QComboBox):
					#verbose.print_("%s: %s" %(attr, widget.currentText()), 4)
					self.storeValue( widget.currentText() )
					#self.storeComboBoxValue( widget.currentIndex() )

				# Line edit(s)...
				if isinstance(widget, QtWidgets.QLineEdit):
					#verbose.print_("%s: %s" %(attr, widget.text()), 4)
					self.storeValue( widget.text() )

				# Plain text edit(s)...
				if isinstance(widget, QtWidgets.QPlainTextEdit):
					#verbose.print_("%s: %s" %(attr, widget.toPlainText()), 4)
					self.storeValue( widget.toPlainText() )

				# Spin box(es)...
				if isinstance(widget, QtWidgets.QSpinBox) or isinstance(widget, QtWidgets.QDoubleSpinBox):
					#verbose.print_("%s: %s" %(attr, widget.value()), 4)
					self.storeValue( widget.value() )


	def removeOverrides(self):
		""" Remove overrides and instead inherit values for widgets on the selected panel
		"""
		widgets = self.ui.settings_frame.children()

		for widget in widgets:
			attr = widget.property('xmlTag')

			if attr:
				self.jd.removeElement(self.currentCategory, attr)

		self.openProperties(self.currentCategory, storeProperties=False)


	def save(self):
		""" Save data
		"""
		# Store the values from widgets on the current page
		#self.storeProperties(self.currentCategory)
		for cat in self.categoryLs:
			self.openProperties(cat)
			#self.storeProperties(cat)

		if self.jd.saveXML():
			verbose.message("%s settings saved." %self.settingsType)
			return True
		else:
			verbose.error("%s settings could not be saved." %self.settingsType)
			return False


	def saveAndExit(self):
		""" Save data and exit
		"""
		if self.save():
			self.ui.hide()
			self.returnValue = True
		else:
			self.exit() # There's a bug where all property panel widgets become visible if a save fails. As a quick dodgy workaround we exit so we don't see it happen.


	def exit(self):
		""" Exit the dialog
		"""
		self.ui.hide()
		self.returnValue = False

# ----------------------------------------------------------------------------
# End of main application class
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Run as standalone app
# ----------------------------------------------------------------------------

# if __name__ == "__main__":
# 	app = QtWidgets.QApplication(sys.argv)

# 	import rsc_rc # TODO: Check why this isn't working from within the UI file

# 	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

# 	qss=os.path.join(os.environ['IC_WORKINGDIR'], "style.qss")
# 	with open(qss, "r") as fh:
# 		app.setStyleSheet(fh.read())

# 	settingsEditor = settingsDialog()

# 	@settingsEditor.customSignal.connect
# 	def storeAttr(attr):
# 		settingsEditor.currentAttr = attr # a bit hacky - need to find a way to add this function to main class
# 		#print '[%s] :' %attr,
# 		#print '[%s] : %d' %(attr, value)
# 	#storeAttr = settingsEditor.customSignal.connect(storeAttr)

# 	settingsEditor.show()
# 	sys.exit(settingsEditor.exec_())

#else:
#	settingsEditor = settingsDialog()
#
#	@settingsEditor.customSignal.connect
#	def storeAttr(attr):
#		settingsEditor.currentAttr = attr # a bit hacky - need to find a way to add this function to main class
#		#print '[%s] :' %attr,
#		#print '[%s] : %d' %(attr, value)
#	#storeAttr = settingsEditor.customSignal.connect(storeAttr)
#
#	settingsEditor.show()
