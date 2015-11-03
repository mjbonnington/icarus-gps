#!/usr/bin/python

# Icarus Admin Tools
# Generic settings editor dialog
# v0.3
#
# Michael Bonnington 2015
# Gramercy Park Studios


from PySide import QtCore, QtGui
from PySide.QtCore import QSignalMapper, Signal
from settings_ui import *
import os, sys, math

# Initialise Icarus environment - only required when standalone
#sys.path.append(os.environ['ICWORKINGDIR'])
#import env__init__
#env__init__.setEnv()
#env__init__.appendSysPaths()

import appPaths, jobSettings, resPresets, units, verbose


class settingsDialog(QtGui.QDialog):

	# Custom signals
	customSignal = Signal(str)

	def __init__(self, parent=None, settingsType="Generic", categoryLs=[], xmlData=None, autoFill=False):
		#QtGui.QDialog.__init__(self, parent)
		super(settingsDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Set window title
		self.setWindowTitle("%s Settings" %settingsType)

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
		self.reset()

		# Set up keyboard shortcuts
		#self.shortcutSave = QtGui.QShortcut(self)
		#self.shortcutSave.setKey('Ctrl+S')
		#self.shortcutSave.activated.connect(self.save)

		self.shortcutLock = QtGui.QShortcut(self)
		self.shortcutLock.setKey('Ctrl+L')
		self.shortcutLock.activated.connect(self.toggleLockUI)

		self.shortcutRemoverOverride = QtGui.QShortcut(self)
		self.shortcutRemoverOverride.setKey('Ctrl+R')
		self.shortcutRemoverOverride.activated.connect(self.removeOverrides)

		# Connect signals and slots
		self.ui.categories_listWidget.currentItemChanged.connect( lambda current: self.openProperties(current.text()) )

		#self.ui.settings_buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.reset)
		self.ui.settings_buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)
		self.ui.settings_buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.exit)


	def reset(self):
		""" Initialise or reset by reloading data
		"""
		# Load data from xml file(s)
		jd_load = self.jd.loadXML(self.xmlData)
		ap_load = self.ap.loadXML(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'appPaths.xml'))
		rp_load = self.rp.loadXML(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'resPresets.xml'))

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
		self.ui.settings_buttonBox.button(QtGui.QDialogButtonBox.Save).setEnabled(self.lockUI) # disable save button


	def importUI(self, ui_file, frame):
		""" Import specified UI file and insert into specified frame
		"""
		try:
			exec('from %s import *' %ui_file)
			#exec('reload(%s)' %ui_file)
			properties_panel = Ui_settings_frame()
			properties_panel.setupUi(frame)
		except ImportError:
			print "Error: The '%s' properties panel could not be loaded." % ui_file


	def openProperties(self, category, storeProperties=True):
		""" Open properties panel for selected settings category
		"""
		#print "[%s]" %category
		inherited = False

		# Store the widget values of the currently open page
		if storeProperties:
			self.storeProperties(self.currentCategory)

		self.currentCategory = category # a bit hacky

		# Create the signal mapper
		signalMapper = QSignalMapper(self)
		signalMapper.mapped.connect(self.customSignal)

		# Create new frame to hold properties UI
		self.ui.settings_frame.close()
		self.ui.settings_frame = QtGui.QFrame(self.ui.settings_scrollAreaWidgetContents)
		self.ui.settings_frame.setObjectName("settings_frame")
		self.ui.verticalLayout_2.addWidget(self.ui.settings_frame)

		# Load approprate UI file into frame
		self.importUI('settings_%s_ui' %category, self.ui.settings_frame)

		# Load values into form widgets
		widgets = self.ui.settings_frame.children()

		# Run special function to autofill the project and job number fields - must happen before we set the widget values for defaults to work correctly
		if category == 'job' and self.autoFill:
			self.jd.autoFill(self.xmlData)

		# Run special function to deal with units panel - must happen before we set the widget values for defaults to work correctly
		if category == 'units':
			self.setupUnits()

		for widget in widgets:
			#attr = widget.objectName().split('_')[0] # use first part of widget object's name
			attr = widget.property('xmlTag') # use widget's dynamic 'xmlTag' 

			if attr is not None:
				signalMapper.setMapping(widget, attr)

				#text = self.jd.getValue(category, attr)
				text, inherited = self.inheritFrom(category, attr)

				if inherited:
					widget.setProperty('xmlTag', None)
					widget.setProperty('inheritedValue', True)
					widget.setToolTip("This value is being inherited. Change the value to override the inherited value.")

					# Apply pop-up menu to remove override - can't get to work here
					#widget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

					#actionRemoveOverride = QtGui.QAction("Remove override", None)
					#actionRemoveOverride.triggered.connect(self.removeOverrides)
					#widget.addAction(actionRemoveOverride)

				# Combo box(es)...
				if isinstance(widget, QtGui.QComboBox):
					if text is not "":
						widget.setCurrentIndex( widget.findText(text) )
					#print "%s: %s" %(attr, widget.currentText())
					widget.currentIndexChanged.connect(signalMapper.map)
					widget.currentIndexChanged.connect( lambda current: self.storeComboBoxValue(current) )

				# Line edit(s)...
				if isinstance(widget, QtGui.QLineEdit):
					if text is not "":
						widget.setText(text)
					#print "%s: %s" %(attr, widget.text())
					widget.textEdited.connect(signalMapper.map)
					widget.textEdited.connect( lambda current: self.storeValue(current) )

				# Spin box(es)...
				if isinstance(widget, QtGui.QSpinBox):
					if text is not "":
						widget.setValue( int(text) )
					#print "%s: %s" %(attr, widget.value())
					widget.valueChanged.connect(signalMapper.map)
					widget.valueChanged.connect( lambda current: self.storeValue(current) )

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

		#print "%s/%s: got value %s, inherited=%s" %(category, attr, text, inherited)
		return text, inherited


	def setupUnits(self):
		""" Setup units properties panel
		"""
		frame = self.ui.settings_frame

		# Populate combo boxes with presets
		for item in units.linear:
			frame.findChildren(QtGui.QComboBox, 'linear_comboBox')[0].addItem(item[0]) # Find a way to display nice names but store short names internally

		for item in units.angular:
			frame.findChildren(QtGui.QComboBox, 'angle_comboBox')[0].addItem(item[0]) # Find a way to display nice names but store short names internally

		for item in units.time:
			frame.findChildren(QtGui.QComboBox, 'time_comboBox')[0].addItem(item[0]) # Find a way to display nice names but store short names internally

		# Set default values - this must happen before values are read from XML data
		frame.findChildren(QtGui.QComboBox, 'linear_comboBox')[0].setCurrentIndex(1) # cm
		frame.findChildren(QtGui.QComboBox, 'angle_comboBox')[0].setCurrentIndex(0) # deg
		frame.findChildren(QtGui.QComboBox, 'time_comboBox')[0].setCurrentIndex(1) # pal

		# Set FPS spin box to correct value based on time combo box selection
		self.setFPS( frame.findChildren(QtGui.QComboBox, 'time_comboBox')[0].currentIndex() )

		# Connect signals and slots
		frame.findChildren(QtGui.QComboBox, 'time_comboBox')[0].currentIndexChanged.connect(lambda current: self.setFPS(current))
		#frame.findChildren(QtGui.QSpinBox, 'fps_spinBox')[0].valueChanged.connect(lambda value: self.setTimeUnit(value))


	def setFPS(self, current=None):
		""" Set FPS spin box value based on time unit combo box
		"""
		frame = self.ui.settings_frame
		frame.findChildren(QtGui.QSpinBox, 'fps_spinBox')[0].setValue(units.time[current][2])


	#def setTimeUnit(self, current=None):
	#	""" Set time unit combo box value based on FPS - currently disabled
	#	"""
	#	frame = self.ui.settings_frame
	#	frame.findChildren(QtGui.QSpinBox, 'time_comboBox')[0].setCurrentIndex(0)


	def setupRes(self):
		""" Setup resolution properties panel
		"""
		frame = self.ui.settings_frame

		# Populate combo box with presets
		presets = self.rp.getPresets()
		comboBox = frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0]

		for item in presets:
			comboBox.addItem(item)
		#comboBox.setCurrentIndex(0)
		width = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		height = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
		comboBox.setCurrentIndex( comboBox.findText( self.rp.getPresetFromRes(width, height) ) )

		self.calcAspectRatio()
		self.checkProxyRes()

		# Connect signals and slots
		frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].currentIndexChanged.connect(self.updateResFromPreset)
		frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].stateChanged.connect(self.calcAspectRatio)
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].valueChanged.connect(self.updateResFullWidth)
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].valueChanged.connect(self.updateResFullHeight)
		frame.findChildren(QtGui.QRadioButton, 'proxyModeScale_radioButton')[0].toggled.connect(self.calcProxyRes)
		frame.findChildren(QtGui.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].valueChanged.connect(self.calcProxyRes)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].valueChanged.connect(self.updateResProxyWidth)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].valueChanged.connect(self.updateResProxyHeight)


	def calcAspectRatio(self):
		""" Calculate aspect ratio
		"""
		frame = self.ui.settings_frame

		fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullHeight = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
		self.aspectRatio = float(fullWidth) / float(fullHeight)

		#print "aspect ratio: %f" %self.aspectRatio


	def updateResFromPreset(self, index = -1):
		""" Update resolution settings when a preset is chosen
		"""
		frame = self.ui.settings_frame

		preset = frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].currentText()
		width = int( self.rp.getValue(preset, 'width') )
		height = int( self.rp.getValue(preset, 'height') )

		# Stop the other widgets from emitting signals
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		# Update widgets
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].setValue(width)
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].setValue(height)

		self.calcAspectRatio()
		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)

		#print index, frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].currentText()


	def updateResFullWidth(self, width = -1):
		""" Update resolution when width is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			height = int(math.ceil(width/self.aspectRatio))
		else:
			height = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()

		#print "full res: [%d]x%d (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Set the preset to 'Custom'
		comboBox = frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0]
		comboBox.setCurrentIndex( comboBox.findText( self.rp.getPresetFromRes(width, height) ) )
		#comboBox.setCurrentIndex( comboBox.findText('Custom') )

		# Update height widget
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].setValue(height)

		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)


	def updateResFullHeight(self, height = -1):
		""" Update resolution when height is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			width = int(math.ceil(height*self.aspectRatio))
		else:
			width = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()

		#print "full res: %dx[%d] (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Set the preset to 'Custom'
		comboBox = frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0]
		comboBox.setCurrentIndex( comboBox.findText( self.rp.getPresetFromRes(width, height) ) )
		#comboBox.setCurrentIndex( comboBox.findText('Custom') )

		# Update width widget
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].setValue(width)

		self.calcProxyRes(fullWidth=width, fullHeight=height)

		# Re-enable signals
		frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)


	def updateResProxyWidth(self, width = -1):
		""" Update proxy resolution when width is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			height = int(math.ceil(width/self.aspectRatio))
		else:
			height = frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].value()

		#print "proxy res: [%d]x%d (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Update height widget
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].setValue(height)

		# Re-enable signals
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].blockSignals(False)


	def updateResProxyHeight(self, height = -1):
		""" Update proxy resolution when height is changed
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(True)

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			width = int(math.ceil(height*self.aspectRatio))
		else:
			width = frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].value()

		#print "proxy res: %dx[%d] (aspect ratio: %f)" %(width, height, self.aspectRatio)

		# Update width widget
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].setValue(width)

		# Re-enable signals
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].blockSignals(False)


	def calcProxyRes(self, proxyScale = -1, fullWidth = -1, fullHeight = -1):
		""" Calculate proxy resolution
		"""
		frame = self.ui.settings_frame

		# If fullWidth or fullHeight not specified, get values from widgets
		if fullWidth < 0:
			fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		if fullHeight < 0:
			fullHeight = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()

		if frame.findChildren(QtGui.QRadioButton, 'proxyModeScale_radioButton')[0].isChecked():
			proxyMode = 'scale'
			proxyScale = frame.findChildren(QtGui.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].value()
			proxyRes = int(fullWidth * proxyScale), int(fullHeight * proxyScale)
		else:
			proxyMode = 'res'
			proxyScale = -1
			proxyRes = frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].value(), frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].value()

		#print "proxy res: %dx%d (%s: %f)" %(proxyRes[0], proxyRes[1], proxyMode, proxyScale)

		# Update widgets
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].setValue(proxyRes[0])
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].setValue(proxyRes[1])


	def checkProxyRes(self):
		""" Check proxy resolution matches full resolution * scale and set appropriate proxy mode
		"""
		frame = self.ui.settings_frame

		fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullHeight = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
		proxyWidth = frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].value()
		proxyHeight = frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].value()
		proxyScale = frame.findChildren(QtGui.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].value()

		if (proxyWidth == fullWidth*proxyScale) and (proxyHeight == fullHeight*proxyScale):
			frame.findChildren(QtGui.QRadioButton, 'proxyModeScale_radioButton')[0].setChecked(True)
			frame.findChildren(QtGui.QRadioButton, 'proxyModeRes_radioButton')[0].setChecked(False)
		else:
			frame.findChildren(QtGui.QRadioButton, 'proxyModeScale_radioButton')[0].setChecked(False)
			frame.findChildren(QtGui.QRadioButton, 'proxyModeRes_radioButton')[0].setChecked(True)


	def setupAppVersions(self, selectCurrent=True):
		""" Setup application version properties panel and populate combo boxes
		"""
		frame = self.ui.settings_frame

		# Create the signal mapper
		signalMapper = QSignalMapper(self)
		signalMapper.mapped.connect(self.customSignal)

		noSelectText = ""
		apps = self.ap.getApps() # get apps and versions
		formLayout = frame.findChildren(QtGui.QFormLayout, 'formLayout')
		appPaths_pushButton = frame.findChildren(QtGui.QPushButton, 'appPaths_pushButton')

		formLayout[0].setWidget(len(apps), QtGui.QFormLayout.FieldRole, appPaths_pushButton[0]) # move edit button to bottom of form
		appPaths_pushButton[0].clicked.connect(self.appPathsEditor)

		for i, app in enumerate(apps):
			label = QtGui.QLabel(frame)
			label.setObjectName("%s_label" %app)
			label.setText("%s:" %app)
			formLayout[0].setWidget(i, QtGui.QFormLayout.LabelRole, label)

			comboBox = QtGui.QComboBox(frame)
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
			formLayout[0].setWidget(i, QtGui.QFormLayout.FieldRole, comboBox)


	def resPresetsEditor(self):
		""" Open the resolution presets editor dialog. TODO: Prevent multiple windows from opening
		"""
		import set_res_presets__main__
		reload(set_res_presets__main__)
		self.setAppPaths = set_res_presets__main__.setResPresetsDialog()
		self.setAppPaths.show()
		self.setAppPaths.exec_()

		# Reload resPresets XML and update comboBox contents after closing dialog
		self.rp.loadXML()
		self.openProperties('resolution')


	def appPathsEditor(self):
		""" Open the application paths editor dialog. TODO: Prevent multiple windows from opening
		"""
		import set_app_paths__main__
		reload(set_app_paths__main__)
		self.setResPresets = set_app_paths__main__.setAppPathsDialog()
		self.setResPresets.show()
		self.setResPresets.exec_()

		# Reload appPaths XML and update comboBox contents after closing dialog
		self.ap.loadXML()
		self.openProperties('apps')


	def storeValue(self, val):
		""" Stores the currently edited attribute value into the XML data
		"""
		self.currentValue = str(val) # value must be a string for XML
		#print '[%s] [%s] : %s' %(self.currentCategory, self.currentAttr, self.currentValue)
		self.jd.setValue(self.currentCategory, self.currentAttr, self.currentValue)


	def storeComboBoxValue(self, index):
		""" Get the value of the currently edited ComboBox. A bit hacky
		"""
		frame = self.ui.settings_frame
		val = frame.findChildren(QtGui.QComboBox, '%s_comboBox' %self.currentAttr)[0].currentText()
		self.storeValue(val)


	def storeProperties(self, category):
		""" Store properties for all relevant widgets on selected settings category panel
		"""
		widgets = self.ui.settings_frame.children()

		for widget in widgets:
			attr = widget.property('xmlTag')

			# Only store values of wigets which have the dynamic property 'xmlTag' set
			if attr is not None:
				self.currentAttr = attr

				# Combo box(es)...
				if isinstance(widget, QtGui.QComboBox):
					#print "%s: %s" %(attr, widget.currentText())
					self.storeValue( widget.currentText() )
					#self.storeComboBoxValue( widget.currentIndex() )

				# Line edit(s)...
				if isinstance(widget, QtGui.QLineEdit):
					#print "%s: %s" %(attr, widget.text())
					self.storeValue( widget.text() )

				# Spin box(es)...
				if isinstance(widget, QtGui.QSpinBox):
					#print "%s: %s" %(attr, widget.value())
					self.storeValue( widget.value() )


	def removeOverrides(self):
		""" Remove overrides and instead inherit values for widgets on the selected panel
		"""
		widgets = self.ui.settings_frame.children()

		for widget in widgets:
			attr = widget.property('xmlTag')

			if attr is not None:
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
			verbose.settingsData_written(self.settingsType)
			#print "%s settings data file saved." %self.settingsType
			return True
		else:
			verbose.settingsData_notWritten(self.settingsType)
			#print "Warning: %s settings data file could not be saved." %self.settingsType
			return False


	def saveAndExit(self):
		""" Save data and exit
		"""
		if self.save():
			self.hide()
			self.returnValue = True
		else:
			self.exit() # There's a bug where all property panel widgets become visible if a save fails. As a quick dodgy workaround we exit so we don't see it happen.


	def exit(self):
		""" Exit the dialog
		"""
		self.hide()
		self.returnValue = False


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	settingsEditor = settingsDialog()

	@settingsEditor.customSignal.connect
	def storeAttr(attr):
		settingsEditor.currentAttr = attr # a bit hacky - need to find a way to add this function to main class
		#print '[%s] :' %attr,
		#print '[%s] : %d' %(attr, value)
	#storeAttr = settingsEditor.customSignal.connect(storeAttr)

	settingsEditor.show()
	sys.exit(settingsEditor.exec_())

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
