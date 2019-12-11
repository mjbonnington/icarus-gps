#!/usr/bin/python

# preview.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2014-2019
#
# A streamlined tool for previewing animations, designed to replace Maya's
# playblast interface.
# TODO: Add Nuke/Houdini support.


import os
import re
import subprocess
import sys

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from . import appConnect
from shared import djvOps  # TODO: Change to viewer-agnostic wrapper
# from shared import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

VERSION = "0.2.4"

cfg = {}

# Set window title and object names
cfg['window_title'] = "GPS Preview"
cfg['window_object'] = "previewUI"

# Set the UI and the stylesheet
cfg['ui_file'] = "preview.ui"
cfg['stylesheet'] = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
cfg['prefs_file'] = os.path.join(os.environ['PREVIEW_USER_PREFS_PATH'], 'preview_prefs.json')
cfg['store_window_geometry'] = True

# DOCK_WITH_MAYA_UI = False
# DOCK_WITH_NUKE_UI = False


# ----------------------------------------------------------------------------
# Begin main window class
# ----------------------------------------------------------------------------

class PreviewUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Preview UI.
	"""
	def __init__(self, parent=None):
		super(PreviewUI, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui.centralwidget)

		# Set window icon, flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Tool)
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Set icons
		# self.ui.nameUpdate_toolButton.setIcon(self.iconSet('configure.svg'))

		# Connect signals & slots
		self.ui.name_lineEdit.textChanged.connect(self.checkFilename)
		#self.ui.nameUpdate_toolButton.clicked.connect(self.updateFilename)
		self.ui.format_comboBox.currentIndexChanged.connect(self.setCreateDaily)
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

		# Show initialisation message
		info_ls = []
		for key, value in self.getInfo().items():
			info_ls.append("{} {}".format(key, value))
		info_str = " | ".join(info_ls)
		print("%s v%s\n%s" % (cfg['window_title'], VERSION, info_str))


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
		self.activeView = self.prefs.get_attr('preview', 'activeview') #None
		# self.ui.activeView_lineEdit.hide()
		self.ui.message_plainTextEdit.hide()
		#self.setFixedHeight(self.minimumSizeHint().height())

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


	def setCreateDaily(self):
		""" Disable dailies creation if format is set to QuickTime movie.
		"""
		if self.sender().currentText() == "QuickTime":
			#self.createDailyTemp = self.createDaily
			self.ui.createDaily_checkBox.setCheckState(QtCore.Qt.Unchecked)
			self.ui.createDaily_checkBox.setEnabled(False)
		else:
			self.ui.createDaily_checkBox.setEnabled(True)


	def updateCameras(self):
		""" Update active view and camera combo box.
		"""
		activeView = appConnect.getActiveView()
		if activeView:  # Only update active view if it has a camera attached
			self.activeView = activeView
			self.storeValue('preview', 'activeview', self.activeView)
			#verbose.print_("Active view set to %s" %self.activeView)
			print("Active view set to %s" %self.activeView)
			# self.ui.activeView_lineEdit.setText(activeView)
		else:
			#verbose.warning("Using active view %s" %self.activeView)
			print("Using active view %s" %self.activeView)

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
			self.ui.x_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
			self.ui.y_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
			self.ui.x_spinBox.setEnabled(True) #setReadOnly(False)
			self.ui.y_spinBox.setEnabled(True) #setReadOnly(False)
			self.ui.resSep_label.setEnabled(True)

			# Read values from user settings
			value = self.prefs.get_attr('preview', 'customresolution')
			if value is not None:
				try:
					res = value.split('x')
					res = int(res[0]), int(res[1])
				except:
					res = value
		else:
			self.ui.x_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
			self.ui.y_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
			self.ui.x_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.y_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.resSep_label.setEnabled(False)

			if resMode == "Shot default":
				res = int(os.environ['PREVIEW_RESOLUTION_X']), int(os.environ['PREVIEW_RESOLUTION_Y'])
			elif resMode == "Proxy":
				try:
					proxy_scale = float(os.environ['PREVIEW_PROXY_SCALE'])
				except:
					proxy_scale = 0.5
				resX = float(os.environ['PREVIEW_RESOLUTION_X']) * proxy_scale
				resY = float(os.environ['PREVIEW_RESOLUTION_Y']) * proxy_scale
				res = int(resX), int(resY)
				#res = int(os.environ['IC_PROXY_RESOLUTION_X']), int(os.environ['IC_PROXY_RESOLUTION_Y'])
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
			self.ui.start_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
			self.ui.end_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
			self.ui.start_spinBox.setEnabled(True) #setReadOnly(False)
			self.ui.end_spinBox.setEnabled(True) #setReadOnly(False)
			self.ui.rangeSep_label.setEnabled(True)

			# Read values from user settings
			value = self.prefs.get_attr('preview', 'customframerange')
			if value is not None:
				try:
					frRange = value.split('-')
					frRange = int(frRange[0]), int(frRange[1])
				except:
					frRange = value
		else:
			self.ui.start_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
			self.ui.end_spinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
			self.ui.start_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.end_spinBox.setEnabled(False) #setReadOnly(True)
			self.ui.rangeSep_label.setEnabled(False)
			self.ui.start_spinBox.setMaximum(9999)
			self.ui.end_spinBox.setMinimum(0)

			if rangeMode == "Shot default":
				frRange = int(os.environ['PREVIEW_STARTFRAME']), int(os.environ['PREVIEW_ENDFRAME'])
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
		#filename = filename.replace('<Scene>', self.sanitize(appConnect.getScene(), pattern=r"[^\w]", replace="_"))
		filename = filename.replace('<Scene>', appConnect.getScene())
		filename = filename.replace('<Camera>', camera)

		#if filename and filename == self.sanitize(filename): # and camera:
		if filename:
			#verbose.print_("Filename preview: '%s'" %filename)
			print("Filename preview: '%s'" %filename)
			self.ui.preview_pushButton.setEnabled(True)
			self.ui.message_plainTextEdit.hide()
			#self.setFixedHeight(self.minimumSizeHint().height())
			return filename
		else:
			msg = "Invalid output name."
			#verbose.warning(msg)
			self.ui.preview_pushButton.setEnabled(False)
			self.ui.message_plainTextEdit.setPlainText(msg)
			self.ui.message_plainTextEdit.show()
			#self.setFixedHeight(self.minimumSizeHint().height())
			return False


	# @QtCore.Slot()
	def storeRes(self):
		""" Store custom resolution in user prefs.
		"""
		#res = "%dx%d" %(self.ui.x_spinBox.value(), self.ui.y_spinBox.value())
		res = [self.ui.x_spinBox.value(), self.ui.y_spinBox.value()]
		self.storeValue('preview', 'customresolution', res)


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

		#frRange = "%d-%d" %(self.ui.start_spinBox.value(), self.ui.end_spinBox.value())
		frRange = [self.ui.start_spinBox.value(), self.ui.end_spinBox.value()]
		self.storeValue('preview', 'customframerange', frRange)


	# @QtCore.Slot()
	def storeRangeEnd(self):
		""" Store custom frame range in user prefs.
		"""
		rangeStart = self.ui.start_spinBox.value()
		rangeEnd = self.ui.end_spinBox.value()
		#frRange = "%d-%d" %(self.ui.start_spinBox.value(), self.ui.end_spinBox.value())
		frRange = [self.ui.start_spinBox.value(), self.ui.end_spinBox.value()]
		self.storeValue('preview', 'customframerange', frRange)


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
			self.outputFormat = self.ui.format_comboBox.currentText()

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
			self.burnin = self.getCheckBoxValue(self.ui.burnin_checkBox)
			self.viewer = self.getCheckBoxValue(self.ui.launchViewer_checkBox)
			self.createDaily = self.getCheckBoxValue(self.ui.createDaily_checkBox)
			self.interruptible = True
			# self.interruptible = self.getCheckBoxValue(self.ui.interruptible_checkBox)

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
			                                     format=self.outputFormat, 
			                                     activeView=self.activeView, 
			                                     camera=self.camera, 
			                                     res=self.res, 
			                                     frRange=self.frRange, 
			                                     offscreen=self.offscreen, 
			                                     noSelect=self.noSelect, 
			                                     guides=self.guides, 
			                                     burnin=self.burnin, 
			                                     interruptible=self.interruptible)
			previewOutput = previewSetup.appPreview()
			if previewOutput[0] == "Completed":  # Playblast completed without interruption
				# print(previewOutput[1])
				outputFilePath = previewOutput[1]
				if self.viewer:
					self.launchViewer(outputFilePath)
				if self.createDaily:
					self.makeDaily(outputFilePath)
				self.ui.message_plainTextEdit.hide()
				#self.setFixedHeight(self.minimumSizeHint().height())
			elif previewOutput[0] == "Interrupted":  # Playblast interrupted
				# print(previewOutput[1])
				outputFilePath = previewOutput[1]
				if self.viewer:
					self.launchViewer(outputFilePath)
				self.ui.message_plainTextEdit.hide()
				#self.setFixedHeight(self.minimumSizeHint().height())
			else:  # Playblast failed
				self.ui.message_plainTextEdit.setPlainText(previewOutput[1])
				self.ui.message_plainTextEdit.show()
				#self.setFixedHeight(self.minimumSizeHint().height())

			# Restore window
			if not self.offscreen and showUI:
				self.showNormal()

		self.save()  # Save settings


	def launchViewer(self, outputFilePath):
		""" Launch viewer.
		"""
		if self.outputFormat == "QuickTime":
			outputFilePath += ".mov"
		else:
			# Quick hack to replace frame number padding with first frame
			outputFilePath = outputFilePath.replace(
				"####", 
				os.environ['PREVIEW_STARTFRAME'])

		print outputFilePath
		djvOps.viewer(outputFilePath)


	def makeDaily(self, outputFilePath):
		""" Create daily from playblast.
		"""
		if self.outputFormat == "QuickTime":
			print("Warning: Cannot create dailies from QuickTime movies.")
			return False
		else:
			# Quick hack to replace frame number padding with first frame
			# outputFilePath = outputFilePath.replace(
			# 	"####", 
			# 	os.environ['PREVIEW_STARTFRAME'])
			# dailyFromApp.makeDaily(
			# 	app=os.environ['IC_ENV'], 
			# 	outputFile=outputFilePath, 
			# 	sourceFile=appConnect.getScene(fullPath=True))
			from publish import ic_dailyPbl
			dailyPblOpts = [
				os.path.basename(outputFilePath), 
				'%d-%d' % (self.frRange), 
				'anim', 
				os.path.dirname(outputFilePath)
			]
			ic_dailyPbl.publish(dailyPblOpts, os.environ['IC_SHOTPUBLISHDIR'], "Published from %s" % cfg['window_title'])
			
			return True


	def sanitize(instr, pattern=r'\W', replace=''):
		""" Sanitizes characters in string. Default removes all non-
			alphanumeric characters.
		"""
		return re.sub(pattern, replace, instr)


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main window class
# ============================================================================
# Run functions - MOVE TO TEMPLATE MODULE?
# ----------------------------------------------------------------------------

def run_maya(session, showUI=True, **kwargs):
	""" Run in Maya.
	"""
	os.environ['PREVIEW_APPCONNECT'] = 'maya'  # Temporary fudge

	try:
		if showUI:  # Open the Preview UI before playblasting
			session.previewUI.display()

		else:  # Run playblast without displaying the UI
			session.previewUI.initSettings()
			session.previewUI.preview(showUI=showUI)
			# session.previewUI.hide()

	except:  # Always display the UI on first run per session
		UI._maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.previewUI = PreviewUI(parent=UI._maya_main_window())
		session.previewUI.display(**kwargs)
