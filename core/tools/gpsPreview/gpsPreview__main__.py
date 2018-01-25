#!/usr/bin/python

# [GPS Preview] gpsPreview__main__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2018 Gramercy Park Studios
#
# GPS Preview: a generic UI for previewing animations, replaces Maya's
# playblast interface.
# TODO: Add Nuke support for flipbook viewer.


import os
import subprocess
import sys

from Qt import QtCore, QtGui, QtWidgets
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
STORE_WINDOW_GEOMETRY = True
DOCK_WITH_MAYA_UI = False
DOCK_WITH_NUKE_UI = False


# ----------------------------------------------------------------------------
# Main window class
# ----------------------------------------------------------------------------

class PreviewUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" GPS Preview UI.
	"""
	def __init__(self, parent=None):
		super(PreviewUI, self).__init__(parent)
		self.parent = parent

		xml_data = os.path.join(os.environ['IC_USERPREFS'], 'gpsPreview.xml')

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             xml_data=xml_data, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.name_lineEdit.textChanged.connect(self.checkFilename)
		#self.ui.nameUpdate_toolButton.clicked.connect(self.updateFilename)
		self.ui.camera_radioButton.toggled.connect(self.updateCameras)
		self.ui.resolution_comboBox.currentIndexChanged.connect(self.updateResGrp)
		self.ui.x_spinBox.valueChanged.connect(self.storeRes)
		self.ui.y_spinBox.valueChanged.connect(self.storeRes)
		self.ui.range_comboBox.currentIndexChanged.connect(self.updateRangeGrp)
		self.ui.start_spinBox.valueChanged.connect(self.storeRangeStart)
		self.ui.end_spinBox.valueChanged.connect(self.storeRangeEnd)
		self.ui.preview_pushButton.clicked.connect(self.preview)

		# Context menus
		self.addContextMenu(self.ui.nameUpdate_toolButton, "Reset to default", self.updateFilename)
		self.addContextMenu(self.ui.nameUpdate_toolButton, "Insert scene name token <Scene>", lambda: self.insertFilenameToken("<Scene>"))
		self.addContextMenu(self.ui.nameUpdate_toolButton, "Insert camera name token <Camera>", lambda: self.insertFilenameToken("<Camera>"))

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w<>]+'), self.ui.name_lineEdit) #r'[\w\.-]+'
		self.ui.name_lineEdit.setValidator(alphanumeric_validator)


	def display(self):
		""" Initialise UI and set options to stored values if possible.
		"""
		self.returnValue = False

		self.initSettings()

		self.show()
		self.raise_()

		return self.returnValue


	def initSettings(self):
		""" Initialise settings.
		"""
		self.activeView = self.xd.getValue('gpspreview', 'activeview')
		# self.ui.activeView_lineEdit.hide()
		self.ui.message_plainTextEdit.hide()

		if not self.ui.name_lineEdit.text():
			self.updateFilename()
		# self.updateCameras()
		self.updateResGrp()
		self.updateRangeGrp()
		self.checkFilename()


	def updateFilename(self):
		""" Update filename field.
		"""
		# Add camera token only if multiple renderable cameras found
		if len(appConnect.getCameras(renderableOnly=True)) > 1:
			filename = "<Scene>_<Camera>"
		else:
			filename = "<Scene>"
		self.ui.name_lineEdit.setText(filename)


	def insertFilenameToken(self, token):
		""" Insert token into filename field.
		"""
		self.ui.name_lineEdit.insert(token)


	def updateCameras(self):
		""" Update active view and camera combo box.
		"""
		activeView = appConnect.getActiveView()
		if activeView:  # Only update active view if it has a camera attached
			self.activeView = activeView
			self.storeValue('gpspreview', 'activeview', self.activeView)
			verbose.print_("Active view set to %s" %self.activeView)
			# self.ui.activeView_lineEdit.setText(activeView)
		else:
			verbose.warning("Using active view %s" %self.activeView)

		self.populateComboBox(self.ui.camera_comboBox, appConnect.getCameras())


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
			self.ui.resSep_label.setEnabled(True)
			# Read values from user settings
			#res = userPrefs.config.get('gpspreview', 'customresolution').split('x')
			value = self.xd.getValue('gpspreview', 'customresolution')
			if value is not "":
				try:
					res = value.split('x')
					res = int(res[0]), int(res[1])
				except:
					pass
		else:
			self.ui.x_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.y_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.resSep_label.setEnabled(False)
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
			self.ui.rangeSep_label.setEnabled(True)
			# Read values from user settings
			#frRange = userPrefs.config.get('gpspreview', 'customframerange').split('-')
			value = self.xd.getValue('gpspreview', 'customframerange')
			if value is not "":
				try:
					frRange = value.split('-')
					frRange = int(frRange[0]), int(frRange[1])
				except:
					pass
		else:
			self.ui.start_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.end_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.rangeSep_label.setEnabled(False)
			self.ui.start_spinBox.setMaximum(9999)
			self.ui.end_spinBox.setMinimum(0)
			if rangeMode == "Shot default":
				frRange = int(os.environ['STARTFRAME']), int(os.environ['ENDFRAME'])
			elif rangeMode == "Timeline":
				frRange = appConnect.getFrameRange()
			elif rangeMode == "Current frame only":
				frame = appConnect.getCurrentFrame()
				frRange = frame, frame

		# Update widgets
		self.ui.start_spinBox.setValue(frRange[0])
		self.ui.end_spinBox.setValue(frRange[1])

		# Re-enable signals
		self.ui.start_spinBox.blockSignals(False)
		self.ui.end_spinBox.blockSignals(False)


	# @QtCore.Slot()
	def checkFilename(self):
		""" Check custom output filename and adjust UI appropriately.
		"""
		filename = self.ui.name_lineEdit.text()
		camera = self.getCurrentCamera()

		# Replace tokens and remove invalid characters...
		filename = filename.replace('<Scene>', osOps.sanitize(appConnect.getScene(), pattern=r"[^\w]", replace="_"))
		filename = filename.replace('<Camera>', camera)

		if filename and filename == osOps.sanitize(filename): # and camera:
			verbose.print_("Filename preview: '%s'" %filename)
			self.ui.message_plainTextEdit.hide()
			self.ui.preview_pushButton.setEnabled(True)
			return filename
		else:
			msg = "Invalid output name."
			verbose.warning(msg)
			self.ui.message_plainTextEdit.setPlainText(msg)
			self.ui.message_plainTextEdit.show()
			self.ui.preview_pushButton.setEnabled(False)
			return False


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


	def getCurrentCamera(self):
		""" Get the current camera to playblast from.
		"""
		self.updateCameras()
		if self.ui.camera_radioButton.isChecked():
			return self.ui.camera_comboBox.currentText()
		else:
			#print(self.activeView)
			return appConnect.getActiveCamera(self.activeView)


	def getOpts(self):
		""" Get UI options before generating playblast.
		"""
		try:
			# Get file name output string
			self.fileInput = self.checkFilename() #self.ui.name_lineEdit.text()

			# Get file format
			self.format = self.ui.format_comboBox.currentText()

			# Get camera
			# self.updateCameras()
			# self.activeView = self.ui.activeView_lineEdit.text()
			self.camera = self.getCurrentCamera()

			# Get frame range and resolution
			self.updateRangeGrp()
			self.res = self.ui.x_spinBox.value(), self.ui.y_spinBox.value()
			self.frRange = self.ui.start_spinBox.value(), self.ui.end_spinBox.value()

			# Get option values from checkboxes
			self.offscreen = self.getCheckBoxValue(self.ui.offscreen_checkBox)
			self.noSelect = self.getCheckBoxValue(self.ui.noSelection_checkBox)
			self.guides = self.getCheckBoxValue(self.ui.guides_checkBox)
			self.slate = self.getCheckBoxValue(self.ui.slate_checkBox)
			self.viewer = self.getCheckBoxValue(self.ui.launchViewer_checkBox)
			self.interruptible = self.getCheckBoxValue(self.ui.interruptible_checkBox)
			# self.createQt = self.getCheckBoxValue(self.ui.createQuickTime_checkBox)

			return True

		except:
			return False


	def preview(self, showUI=True):
		""" Get options, pass information to appConnect and save options once
			appConnect is done.
		"""
		if self.getOpts():
			# Minimise window if rendering offscreen
			if not self.offscreen and showUI:
				self.showMinimized()

			previewSetup = appConnect.AppConnect(fileInput=self.fileInput, 
			                                     format=self.format, 
			                                     activeView=self.activeView, 
			                                     camera=self.camera, 
			                                     res=self.res, 
			                                     frRange=self.frRange, 
			                                     offscreen=self.offscreen, 
			                                     noSelect=self.noSelect, 
			                                     guides=self.guides, 
			                                     slate=self.slate, 
			                                     interruptible=self.interruptible)
			previewOutput = previewSetup.appPreview()
			if previewOutput[0]:
				# print(previewOutput[1])
				outputFilePath = previewOutput[1]
				# if self.createQt:
				# 	self.createQuickTime()
				if self.viewer:
					self.launchViewer(outputFilePath)
				# osOps.setPermissions(self.outputDir)
				self.ui.message_plainTextEdit.hide()
				# print(self.sizeHint())
				# self.setFixedHeight(self.sizeHint().height())
			else:
				self.ui.message_plainTextEdit.setPlainText(previewOutput[1])
				self.ui.message_plainTextEdit.show()
				# print(self.sizeHint())
				# self.setFixedHeight(self.sizeHint().height())

			# Restore window
			if not self.offscreen and showUI:
				self.showNormal()

		self.save()  # Save settings


	# def createQuickTime(self):
	# 	""" Creates a QuickTime movie using djv for encoding.
	# 	"""
	# 	# Delete qt file if exists in output dir...
	# 	input = os.path.join(self.outputDir, self.outputFile)
	# 	if os.path.isfile('%s.mov' %input):
	# 		osOps.recurseRemove(input)
	# 	output = self.outputDir
	# 	startFrame = str(self.frRange[0]).zfill(4)  # Hard-coded to 4-digit padding
	# 	endFrame = str(self.frRange[1]).zfill(4)  # Hard-coded to 4-digit padding
	# 	inExt = self.ext
	# 	djvOps.prcQt(input, output, startFrame, endFrame, inExt, name=self.outputFile, fps=os.environ['FPS'], resize=None)


	def launchViewer(self, outputFilePath):
		""" Launch viewer.
		"""
		import sequence
		if self.format == "JPEG sequence":
			outputFilePath = sequence.getFirst(outputFilePath)
		elif self.format == "QuickTime":
			outputFilePath += ".mov"
		djvOps.viewer(outputFilePath)


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main window class
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Run functions - MOVE TO TEMPLATE MODULE?
# ----------------------------------------------------------------------------

def run_maya(showUI=True):
	""" Run in Maya.
	"""
	UI._maya_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any already existing UI
	previewApp = PreviewUI(parent=UI._maya_main_window())

	if showUI:  # Show the UI
		previewApp.display()
	else:  # Run playblast without displaying the UI
		previewApp.initSettings()
		previewApp.preview(showUI=showUI)
		# previewApp.hide()

	# if not DOCK_WITH_MAYA_UI:
	# 	previewApp.display(**kwargs)  # Show the UI
	# elif DOCK_WITH_MAYA_UI:
	# 	allowed_areas = ['right', 'left']
	# 	mc.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left', 
	# 	               content=WINDOW_OBJECT, allowedArea=allowed_areas)


# def run_nuke(**kwargs):
# 	""" Run in Nuke. NOT YET IMPLEMENTED

# 		Note:
# 			If you want the UI to always stay on top, replace:
# 			`previewApp.ui.setWindowFlags(QtCore.Qt.Tool)`
# 			with:
# 			`previewApp.ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)`

# 			If you want the UI to be modal:
# 			`previewApp.ui.setWindowModality(QtCore.Qt.WindowModal)`
# 	"""
# 	UI._nuke_delete_ui(WINDOW_OBJECT, WINDOW_TITLE)  # Delete any already existing UI

# 	if not DOCK_WITH_NUKE_UI:
# 		previewApp = PreviewUI(parent=UI._nuke_main_window())
# 		previewApp.setWindowFlags(QtCore.Qt.Tool)
# 		previewApp.display(**kwargs)  # Show the UI
# 	elif DOCK_WITH_NUKE_UI:
# 		prefix = ''
# 		basename = os.path.basename(__file__)
# 		module_name = basename[: basename.rfind('.')]
# 		if __name__ == module_name:
# 			prefix = module_name + '.'
# 		panel = nukescripts.panels.registerWidgetAsPanel(
# 			widget=prefix + WINDOW_TITLE,  # module_name.Class_name
# 			name=WINDOW_TITLE,
# 			id='uk.co.thefoundry.' + WINDOW_TITLE,
# 			create=True)
# 		pane = nuke.getPaneFor('Properties.1')
# 		panel.addToPane(pane)
# 		previewApp = panel.customKnob.getObject().widget
# 		UI._nuke_set_zero_margins(previewApp)


# Detect environment and run application
if os.environ['IC_ENV'] == 'STANDALONE':
	verbose.print_("[GPS] %s" %WINDOW_TITLE)
elif os.environ['IC_ENV'] == 'MAYA':
	import maya.cmds as mc
	verbose.print_("[GPS] %s for Maya" %WINDOW_TITLE)
	# run_maya()
elif os.environ['IC_ENV'] == 'NUKE':
	import nuke
	import nukescripts
	verbose.print_("[GPS] %s for Nuke" %WINDOW_TITLE)
	# run_nuke()
# elif __name__ == '__main__':
# 	run_standalone()

