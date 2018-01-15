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

class PreviewUI(UI.TemplateUI):
	""" GPS Preview UI.
	"""
	def __init__(self, parent=None):
		super(PreviewUI, self).__init__(parent)
		self.parent = parent

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Load XML data
		xd_load = self.xd.loadXML(os.path.join(os.environ['IC_USERPREFS'], 'userPrefs.xml'))
		self.setupUI(WINDOW_OBJECT, WINDOW_TITLE, UI_FILE, STYLESHEET)

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
		self.ui.nameUpdate_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		self.actionNameOption1 = QtWidgets.QAction("Reset to default", None)
		self.actionNameOption1.triggered.connect(self.updateFilename)
		self.ui.nameUpdate_toolButton.addAction(self.actionNameOption1)

		self.actionNameOption2 = QtWidgets.QAction("Insert scene name token <Scene>", None)
		self.actionNameOption2.triggered.connect(lambda: self.insertFilenameToken("<Scene>"))
		self.ui.nameUpdate_toolButton.addAction(self.actionNameOption2)

		self.actionNameOption3 = QtWidgets.QAction("Insert camera name token <Camera>", None)
		self.actionNameOption3.triggered.connect(lambda: self.insertFilenameToken("<Camera>"))
		self.ui.nameUpdate_toolButton.addAction(self.actionNameOption3)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w<>]+'), self.ui.name_lineEdit) #r'[\w\.-]+'
		self.ui.name_lineEdit.setValidator(alphanumeric_validator)


	def display(self):
		""" Initialise UI and set options to stored values if possible.
		"""
		self.returnValue = False

		self.initSettings()

		# self.ui.activeView_lineEdit.hide()

		self.show()
		self.raise_()

		return self.returnValue


	def initSettings(self):
		""" Initialise settings.
		"""
		if not self.ui.name_lineEdit.text():
			self.updateFilename()
		self.updateCameras()
		self.updateResGrp()
		self.updateRangeGrp()
		self.checkFilename()


	def updateFilename(self):
		""" Reset filename field to use scene/script/project filename.
		"""
		# filename = osOps.sanitize(appConnect.getScene(), pattern=r"[^\w]", replace="_")
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
		if activeView:
			self.activeView = activeView
			# self.ui.activeView_lineEdit.setText(appConnect.getActiveView())
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

		# Replace tokens and sanitize...
		filename = filename.replace('<Scene>', osOps.sanitize(appConnect.getScene(), pattern=r"[^\w]", replace="_"))
		filename = filename.replace('<Camera>', self.getCurrentCamera())

		if filename and filename == osOps.sanitize(filename):
			# userPrefs.edit('gpspreview', 'customfilename', filename)
			# self.storeValue('customfilename', filename)
			self.ui.preview_pushButton.setEnabled(True)
			verbose.print_("Filename preview: '%s'" %filename)
			return filename
		else:
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
		if self.ui.camera_radioButton.isChecked():
			return self.ui.camera_comboBox.currentText()
		else:
			return appConnect.getActiveCamera(panel=self.activeView)


	def getOpts(self):
		""" Get UI options before generating playblast.
		"""
		try:
			# Get file name output string
			self.fileInput = self.checkFilename() #self.ui.name_lineEdit.text()

			# Get file format
			self.format = self.ui.format_comboBox.currentText()

			# Get camera
			self.updateCameras()
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
			self.createQt = self.getCheckBoxValue(self.ui.createQuickTime_checkBox)

			return True

		except:
			return False


	def preview(self):
		""" Get options, pass information to appConnect and save options once
			appConnect is done.
		"""
		if self.getOpts():
			if not self.offscreen:
				self.showMinimized()

			# previewSetup = appConnect.AppConnect(self.fileInput, self.res, self.frRange, self.offscreen, self.noSelect, self.guides, self.slate)
			previewSetup = appConnect.AppConnect(fileInput=self.fileInput, 
			                                     format=self.format, 
			                                     activeView=self.activeView, 
			                                     camera=self.camera, 
			                                     res=self.res, 
			                                     frRange=self.frRange, 
			                                     offscreen=self.offscreen, 
			                                     noSelect=self.noSelect, 
			                                     guides=self.guides, 
			                                     slate=self.slate)
			previewOutput = previewSetup.appPreview()
			if previewOutput:
				# self.outputDir, self.outputFile, self.frRange, self.ext = previewOutput
				self.outputFilePath = previewOutput
				# if self.createQt:
				# 	self.createQuickTime()
				if self.viewer:
					self.launchViewer()
				#osOps.setPermissions(self.outputDir)

			if not self.offscreen:
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


	def launchViewer(self):
		""" Launch viewer.
		"""
		import sequence
		if self.format == "JPEG sequence":
			self.outputFilePath = sequence.getFirst(self.outputFilePath)
		elif self.format == "QuickTime":
			self.outputFilePath += ".mov"
		# inPath = os.path.join(self.outputDir, '%s.#.%s' % (self.outputFile, self.ext))
		# djvOps.viewer(sequence.getFirst(inPath))
		djvOps.viewer(sequence.getFirst(self.outputFilePath))


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings

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
		previewApp.preview()

	# if not DOCK_WITH_MAYA_UI:
	# 	previewApp.display(**kwargs)  # Show the UI
	# elif DOCK_WITH_MAYA_UI:
	# 	allowed_areas = ['right', 'left']
	# 	mc.dockControl(WINDOW_TITLE, label=WINDOW_TITLE, area='left', 
	# 	               content=WINDOW_OBJECT, allowedArea=allowed_areas)


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
		previewApp = PreviewUI(parent=UI._nuke_main_window())
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
	# run_maya()
elif os.environ['IC_ENV'] == 'NUKE':
	import nuke
	import nukescripts
	verbose.print_("[GPS] %s for Nuke" %WINDOW_TITLE)
	# run_nuke()
# elif __name__ == '__main__':
# 	run_standalone()

