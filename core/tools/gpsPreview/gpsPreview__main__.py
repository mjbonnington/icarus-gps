#!/usr/bin/python

# [GPS Preview] gpsPreview__main__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2017 Gramercy Park Studios
#
# GPS Preview: a generic UI for previewing animations, replaces Maya's
# playblast interface.
# TODO: Add Nuke support for flipbook viewer.


import os
import subprocess

from Qt import QtCompat, QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import appConnect
import djvOps
import osOps
#import userPrefs
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "GPS Preview"
WINDOW_OBJECT = "gpsPreviewUI"

# Set the UI and the stylesheet
UI_FILE = "gpsPreview_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
DOCK_WITH_MAYA_UI = False
DOCK_WITH_NUKE_UI = False


# ----------------------------------------------------------------------------
# Main window class
# ----------------------------------------------------------------------------

class previewUI(UI.TemplateUI):
	""" Launches and controls GPS Preview UI.
	"""
	def __init__(self, parent=None):
		super(previewUI, self).__init__(parent)
		self.parent = parent

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Instantiate XML data classes
		# self.xd = settingsData.settingsData()  # DONE IN TEMPLATE
		xd_load = self.xd.loadXML(os.path.join(os.environ['IC_USERPREFS'], 'userPrefs.xml'))
		self.setupUI(WINDOW_OBJECT, WINDOW_TITLE, UI_FILE, STYLESHEET)

		# Connect signals & slots
		self.ui.preview_pushButton.clicked.connect(self.preview)
		self.ui.reset_toolButton.clicked.connect(self.resetFilename)
		self.ui.resolution_comboBox.currentIndexChanged.connect(self.updateResGrp)
		self.ui.range_comboBox.currentIndexChanged.connect(self.updateRangeGrp)

		self.ui.file_lineEdit.textChanged.connect(self.storeFilename)
		self.ui.x_spinBox.valueChanged.connect(self.storeRes)
		self.ui.y_spinBox.valueChanged.connect(self.storeRes)
		self.ui.start_spinBox.valueChanged.connect(self.storeRangeStart)
		self.ui.end_spinBox.valueChanged.connect(self.storeRangeEnd)

		# Set input validators
		# alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-]+'), self.ui.file_lineEdit)
		alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w]+'), self.ui.file_lineEdit)
		self.ui.file_lineEdit.setValidator(alphanumeric_validator)

		# Populate UI with env vars
		self.display()


	def display(self):
		""" Initialise UI and set options to stored values if possible.
		"""
		self.returnValue = False

		# Read user prefs config file - if it doesn't exist it will be created
		# userPrefs.read()

		self.resetFilename()
		self.storeFilename()

		# # Load values into form widgets (make recursive)
		# for widget in self.ui.options_groupBox.children():

		# 	# Set up handlers for different widget types & apply values
		# 	attr = widget.property('xmlTag')
		# 	if attr:

		# 		# Check box(es)...
		# 		if isinstance(widget, QtWidgets.QCheckBox):
		# 			try:
		# 				value = userPrefs.config.getboolean('gpspreview', attr)
		# 				widget.setChecked(value)
		# 				#print("Set")
		# 			except:
		# 				self.storeValue(attr, self.getCheckBoxValue(widget))
		# 				#print("Store")
		# 			widget.toggled.connect(self.storeCheckBoxValue)

		# 		# # Combo box(es)...
		# 		# elif isinstance(widget, QtWidgets.QComboBox):
		# 		# 	if value is not "":
		# 		# 		widget.setCurrentIndex(widget.findText(value))
		# 		# 	if storeProperties:
		# 		# 		self.storeValue(attr, widget.currentText())
		# 		# 	# widget.currentIndexChanged.connect(lambda index: self.storeComboBoxValue(index))
		# 		# 	widget.currentIndexChanged.connect(self.storeComboBoxValue)

		# try:
		# 	self.ui.resolution_comboBox.setCurrentIndex(userPrefs.config.getint('gpspreview', 'resolutionmode'))
		# except:
		# 	pass

		# try:
		# 	self.ui.range_comboBox.setCurrentIndex(userPrefs.config.getint('gpspreview', 'framerangemode'))
		# except:
		# 	pass

		self.updateResGrp()
		self.updateRangeGrp()

		self.show()
		self.raise_()
		return self.returnValue


	# def getCheckBoxValue(self, checkBox):
	# 	""" Get the value from a checkbox and return a Boolean value.
	# 	"""
	# 	if checkBox.checkState() == QtCore.Qt.Checked:
	# 		return True
	# 	else:
	# 		return False


	def resetFilename(self):
		""" Reset filename field to use scene/script/project filename.
		"""
		filename = osOps.sanitize(appConnect.getScene(), pattern="[^\w]", replace="_")
		self.ui.file_lineEdit.setText(filename)


	def updateResGrp(self):
		""" Update resolution group UI based on combo box selection.
		"""
		# Stop the other widgets from emitting signals
		self.ui.x_spinBox.blockSignals(True)
		self.ui.y_spinBox.blockSignals(True)

		# Store current values
		res = self.ui.x_spinBox.value(), self.ui.y_spinBox.value()
		resMode = self.ui.resolution_comboBox.currentText()

		# Set resolution appropriately
		if resMode == "Custom":
			self.ui.x_spinBox.setEnabled(True) #setReadOnly(False)
			self.ui.y_spinBox.setEnabled(True) #setReadOnly(False)
			# Read values from user settings
			try:
				#res = userPrefs.config.get('gpspreview', 'customresolution').split('x')
				res = self.xd.getValue('gpspreview', 'customresolution').split('x')
				res[0] = int(res[0])
				res[1] = int(res[1])
			except:
				pass
		else:
			self.ui.x_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.y_spinBox.setEnabled(False) #setReadOnly(True)
			if resMode == "Shot default":
				res = int(os.environ['RESOLUTIONX']), int(os.environ['RESOLUTIONY'])
			elif resMode == "Proxy":
				res = int(os.environ['PROXY_RESOLUTIONX']), int(os.environ['PROXY_RESOLUTIONY'])
			elif resMode == "Render settings":
				res = appConnect.getResolution()
			else:
				resOrig = appConnect.getResolution()
				resMult = float(self.ui.resolution_comboBox.currentText().replace('%', '')) / 100.0
				res = int((float(resOrig[0])*resMult)), int((float(resOrig[1])*resMult))

		# Store mode setting in user prefs
		#userPrefs.edit('gpspreview', 'resolutionmode', str(self.ui.resolution_comboBox.currentIndex()))
		#self.storeValue('resolutionmode', self.ui.resolution_comboBox.currentIndex())

		# Update widgets
		self.ui.x_spinBox.setValue(res[0])
		self.ui.y_spinBox.setValue(res[1])

		# Re-enable signals
		self.ui.x_spinBox.blockSignals(False)
		self.ui.y_spinBox.blockSignals(False)


	def updateRangeGrp(self):
		""" Update frame range group UI based on combo box selection.
		"""
		# Stop the other widgets from emitting signals
		self.ui.start_spinBox.blockSignals(True)
		self.ui.end_spinBox.blockSignals(True)

		# Store current values
		frRange = self.ui.start_spinBox.value(), self.ui.end_spinBox.value()
		rangeMode = self.ui.range_comboBox.currentText()

		# Set frame range appropriately
		if rangeMode == "Custom":
			self.ui.start_spinBox.setEnabled(True) #setReadOnly(False)
			self.ui.end_spinBox.setEnabled(True) #setReadOnly(False)
			# Read values from user settings
			try:
				#frRange = userPrefs.config.get('gpspreview', 'customframerange').split('-')
				frRange = self.xd.getValue('gpspreview', 'customframerange').split('-')
				frRange[0] = int(frRange[0])
				frRange[1] = int(frRange[1])
			except:
				pass
		else:
			self.ui.start_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.end_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.start_spinBox.setMaximum(9999)
			self.ui.end_spinBox.setMinimum(0)
			if rangeMode == "Shot default":
				frRange = int(os.environ['STARTFRAME']), int(os.environ['ENDFRAME'])
			elif rangeMode == "Timeline":
				frRange = appConnect.getFrameRange()
			elif rangeMode == "Current frame only":
				frame = appConnect.getCurrentFrame()
				frRange = frame, frame

		# Store mode setting in user prefs
		#userPrefs.edit('gpspreview', 'framerangemode', str(self.ui.range_comboBox.currentIndex()))
		#self.storeValue('framerangemode', self.ui.range_comboBox.currentIndex())

		# Update widgets
		self.ui.start_spinBox.setValue(frRange[0])
		self.ui.end_spinBox.setValue(frRange[1])

		# Re-enable signals
		self.ui.start_spinBox.blockSignals(False)
		self.ui.end_spinBox.blockSignals(False)


	# @QtCore.Slot()
	def storeFilename(self):
		""" Store custom output filename in user prefs.
		"""
		filename = self.ui.file_lineEdit.text()
		if filename:
			# userPrefs.edit('gpspreview', 'customfilename', filename)
			# self.storeValue('customfilename', filename)
			self.ui.preview_pushButton.setEnabled(True)
		else:
			self.ui.preview_pushButton.setEnabled(False)


	# @QtCore.Slot()
	def storeRes(self):
		""" Store custom resolution in user prefs.
		"""
		res = "%dx%d" %(self.ui.x_spinBox.value(), self.ui.y_spinBox.value())
		#userPrefs.edit('gpspreview', 'customresolution', res)
		self.storeValue('gpspreview', 'customresolution', res)


	# @QtCore.Slot()
	def storeRangeStart(self):
		""" Store custom frame range in user prefs.
		"""
		rangeStart = self.ui.start_spinBox.value()
		rangeEnd = self.ui.end_spinBox.value()

		# Stop the other widgets from emitting signals
		self.ui.end_spinBox.blockSignals(True)

		# Update widgets
		self.ui.end_spinBox.setMinimum(rangeStart)
		if rangeStart >= rangeEnd:
			self.ui.end_spinBox.setValue(rangeStart)

		# Re-enable signals
		self.ui.end_spinBox.blockSignals(False)

		frRange = "%d-%d" %(self.ui.start_spinBox.value(), self.ui.end_spinBox.value())
		#userPrefs.edit('gpspreview', 'customframerange', frRange)
		self.storeValue('gpspreview', 'customframerange', frRange)


	# @QtCore.Slot()
	def storeRangeEnd(self):
		""" Store custom frame range in user prefs.
		"""
		rangeStart = self.ui.start_spinBox.value()
		rangeEnd = self.ui.end_spinBox.value()
		frRange = "%d-%d" %(self.ui.start_spinBox.value(), self.ui.end_spinBox.value())
		#userPrefs.edit('gpspreview', 'customframerange', frRange)
		self.storeValue('gpspreview', 'customframerange', frRange)


	# # @QtCore.Slot()
	# def storeCheckBoxValue(self):
	# 	""" Get the value from a Check Box and store in XML data.
	# 	"""
	# 	attr = self.sender().property('xmlTag')
	# 	value = self.getCheckBoxValue(self.sender())
	# 	self.storeValue(attr, value)


	# def storeValue(self, attr, value=""):
	# 	""" Store value in XML data.
	# 	"""
	# 	verbose.print_("%20s %s.%s=%s" %(type(value), 'gpspreview', attr, value), 4)
	# 	userPrefs.edit('gpspreview', attr, value)


	def getOpts(self):
		""" Get UI options before generating playblast.
		"""
		try:
			# Get file name output string
			self.fileInput = self.ui.file_lineEdit.text()

			# Get frame range and resolution
			self.res = self.ui.x_spinBox.value(), self.ui.y_spinBox.value()
			self.frRange = self.ui.start_spinBox.value(), self.ui.end_spinBox.value()

			# Get values from checkboxes
			self.offscreen = self.getCheckBoxValue(self.ui.offscreen_checkBox)
			self.noSelect = self.getCheckBoxValue(self.ui.noSelection_checkBox)
			self.guides = self.getCheckBoxValue(self.ui.guides_checkBox)
			self.slate = self.getCheckBoxValue(self.ui.slate_checkBox)
			self.viewer = self.getCheckBoxValue(self.ui.launchViewer_checkBox)
			self.createQt = self.getCheckBoxValue(self.ui.createQuicktime_checkBox)

			return True

		except:
			return False


	def preview(self):
		""" Get options, pass information to appConnect and save options once
			appConnect is done.
		"""
		self.save()  # Save settings

		self.updateRangeGrp()
		if self.getOpts():
			previewSetup = appConnect.connect(self.fileInput, self.res, self.frRange, self.offscreen, self.noSelect, self.guides, self.slate)
			previewOutput = previewSetup.appPreview()
			if previewOutput:
				self.outputDir, self.outputFile, self.frRange, self.ext = previewOutput
				if self.createQt:
					self.createQuicktime()
				if self.viewer:
					self.launchViewer()
				osOps.setPermissions(self.outputDir)


	def createQuicktime(self):
		""" Creates a QuickTime movie.
		"""
		# Delete qt file if exists in output dir...
		input = os.path.join(self.outputDir, self.outputFile)
		if os.path.isfile('%s.mov' %input):
			osOps.recurseRemove(input)
		output = self.outputDir
		startFrame = str(self.frRange[0]).zfill(4)  # Hard-coded to 4-digit padding
		endFrame = str(self.frRange[1]).zfill(4)  # Hard-coded to 4-digit padding
		inExt = self.ext
		djvOps.prcQt(input, output, startFrame, endFrame, inExt, name=self.outputFile, fps=os.environ['FPS'], resize=None)


	def launchViewer(self):
		""" Launch viewer.
		"""
		import sequence
		inPath = os.path.join(self.outputDir, '%s.#.%s' % (self.outputFile, self.ext))
		djvOps.viewer(sequence.getFirst(inPath))


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings


	# ############################################
	# # Dialog acceptance/cancellation functions #
	# ############################################

	# def update(self):
	# 	""" Dialog accept function.
	# 	"""
	# 	self.ui.accept()

	# def cancel(self):
	# 	""" Dialog cancel function.
	# 	"""
	# 	print("X")
	# 	_maya_delete_ui()
	# 	self.ui.reject()

# ----------------------------------------------------------------------------
# End of main window class
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# DCC application helper functions - MOVE TO MODULE
# ----------------------------------------------------------------------------

# def _maya_delete_ui():
# 	""" Delete existing UI in Maya.
# 	"""
# 	if mc.window(WINDOW_OBJECT, q=True, exists=True):
# 		mc.deleteUI(WINDOW_OBJECT)  # Delete window
# 	if mc.dockControl('MayaWindow|' + WINDOW_TITLE, q=True, exists=True):
# 		mc.deleteUI('MayaWindow|' + WINDOW_TITLE)  # Delete docked window


# def _nuke_delete_ui():
# 	""" Delete existing UI in Nuke.
# 	"""
# 	for obj in QtWidgets.QApplication.allWidgets():
# 		if obj.objectName() == WINDOW_OBJECT:
# 			obj.deleteLater()


# def _maya_main_window():
# 	""" Return Maya's main window.
# 	"""
# #	for obj in QtWidgets.qApp.topLevelWidgets():
# 	for obj in QtWidgets.QApplication.topLevelWidgets():
# 		if obj.objectName() == 'MayaWindow':
# 			return obj
# 	raise RuntimeError("Could not find MayaWindow instance")


# def _nuke_main_window():
# 	""" Returns Nuke's main window.
# 	"""
# #	for obj in QtWidgets.qApp.topLevelWidgets():
# 	for obj in QtWidgets.QApplication.topLevelWidgets():
# 		if (obj.inherits('QMainWindow') and obj.metaObject().className() == 'Foundry::UI::DockMainWindow'):
# 			return obj
# 	raise RuntimeError("Could not find DockMainWindow instance")


# def _nuke_set_zero_margins(widget_object):
# 	""" Remove Nuke margins when docked UI.
# 		More info:
# 		https://gist.github.com/maty974/4739917
# 	"""
# 	parentApp = QtWidgets.QApplication.allWidgets()
# 	parentWidgetList = []
# 	for parent in parentApp:
# 		for child in parent.children():
# 			if widget_object.__class__.__name__ == child.__class__.__name__:
# 				parentWidgetList.append(parent.parentWidget())
# 				parentWidgetList.append(parent.parentWidget().parentWidget())
# 				parentWidgetList.append(parent.parentWidget().parentWidget().parentWidget())

# 				for sub in parentWidgetList:
# 					for tinychild in sub.children():
# 						try:
# 							tinychild.setContentsMargins(0, 0, 0, 0)
# 						except:
# 							pass


# ----------------------------------------------------------------------------
# Run functions - MOVE TO TEMPLATE MODULE?
# ----------------------------------------------------------------------------

def run_maya(**kwargs):
	""" Run in Maya.
	"""
	UI._maya_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any already existing UI
	previewApp = previewUI(parent=UI._maya_main_window())

	if not DOCK_WITH_MAYA_UI:
		previewApp.display(**kwargs)  # Show the UI
	elif DOCK_WITH_MAYA_UI:
		allowed_areas = ['right', 'left']
		mc.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left', 
					   content=WINDOW_OBJECT, allowedArea=allowed_areas)


def run_nuke(**kwargs):
	""" Run in Nuke.

		Note:
			If you want the UI to always stay on top, replace:
			`previewApp.ui.setWindowFlags(QtCore.Qt.Tool)`
			with:
			`previewApp.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)`

			If you want the UI to be modal:
			`previewApp.ui.setWindowModality(QtCore.Qt.WindowModal)`
	"""
	UI._nuke_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any already existing UI

	if not DOCK_WITH_NUKE_UI:
		previewApp = previewUI(parent=UI._nuke_main_window())
		previewApp.setWindowFlags(QtCore.Qt.Tool)
		previewApp.display(**kwargs)  # Show the UI
	elif DOCK_WITH_NUKE_UI:
		prefix = ''
		basename = os.path.basename(__file__)
		module_name = basename[: basename.rfind('.')]
		if __name__ == module_name:
			prefix = module_name + '.'
		panel = nukescripts.panels.registerWidgetAsPanel(
			widget=prefix + WINDOW_TITLE,  # module_name.Class_name
			name=WINDOW_TITLE,
			id='uk.co.thefoundry.' + WINDOW_TITLE,
			create=True)
		pane = nuke.getPaneFor('Properties.1')
		panel.addToPane(pane)
		previewApp = panel.customKnob.getObject().widget
		UI._nuke_set_zero_margins(previewApp)


# Detect environment and run application
if os.environ['IC_ENV'] == 'STANDALONE':
	verbose.print_("[GPS] %s" %WINDOW_TITLE)
elif os.environ['IC_ENV'] == 'MAYA':
	import maya.cmds as mc
	verbose.print_("[GPS] %s for Maya" %WINDOW_TITLE)
	run_maya()
elif os.environ['IC_ENV'] == 'NUKE':
	import nuke
	import nukescripts
	verbose.print_("[GPS] %s for Nuke" %WINDOW_TITLE)
	run_nuke()
# elif __name__ == '__main__':
# 	run_standalone()

