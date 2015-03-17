#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsPreview

import os, subprocess
from PySide import QtCore, QtGui
from gpsPreviewUI import *
import djvOps, verbose, appConnect, userPrefs, osOps

#launches and controls GPS Preview UI

class previewUI(QtGui.QDialog):
	
	def __init__(self, parent = None):
		super(previewUI, self).__init__(parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Apply UI style sheet
		qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
		with open(qss, "r") as fh:
			self.ui.main_frame.setStyleSheet(fh.read())

		#connecting signals and slots
		QtCore.QObject.connect(self.ui.preview_pushButton, QtCore.SIGNAL("clicked()"), self.preview)
		QtCore.QObject.connect(self.ui.resolution_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateResGrp)
		QtCore.QObject.connect(self.ui.range_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateRangeGrp)

		self.ui.offscreen_checkBox.stateChanged.connect(self.setOffscreen)
		self.ui.noSelection_checkBox.stateChanged.connect(self.setNoSelection)
		self.ui.guides_checkBox.stateChanged.connect(self.setGuides)
		self.ui.slate_checkBox.stateChanged.connect(self.setSlate)
		self.ui.launchViewer_checkBox.stateChanged.connect(self.setLaunchViewer)
		self.ui.createQuicktime_checkBox.stateChanged.connect(self.setCreateQuicktime)

		# Read values from config file and apply to checkboxes
		userPrefs.read()
		self.ui.offscreen_checkBox.setChecked(userPrefs.config.getboolean('gpspreview', 'offscreen'))
		self.ui.noSelection_checkBox.setChecked(userPrefs.config.getboolean('gpspreview', 'noselection'))
		self.ui.guides_checkBox.setChecked(userPrefs.config.getboolean('gpspreview', 'guides'))
		self.ui.slate_checkBox.setChecked(userPrefs.config.getboolean('gpspreview', 'slate'))
		self.ui.launchViewer_checkBox.setChecked(userPrefs.config.getboolean('gpspreview', 'launchviewer'))
		self.ui.createQuicktime_checkBox.setChecked(userPrefs.config.getboolean('gpspreview', 'createqt'))
	
		#populating UI with env vars
		self.setupUI()

	############################################################## UI ##############################################################
	################################################################################################################################
	
	def setupUI(self):
		self.ui.jobShot_label.setText('%s - %s' % (os.environ['JOB'], os.environ['SHOT']))
		self.ui.x_lineEdit.setText(os.environ['RESOLUTIONX'])
		self.ui.y_lineEdit.setText(os.environ['RESOLUTIONY'])
		try:
			self.ui.file_lineEdit.setText(os.environ['GPSPREVIEW_FILE'])
			self.ui.range_comboBox.setCurrentIndex(int(os.environ['GPSPREVIEW_RANGEINDEX']))
			if int(os.environ['GPSPREVIEW_RANGEINDEX']) is 1:
				self.ui.start_lineEdit.setText('')
				self.ui.end_lineEdit.setText('')
			else:
				self.ui.start_lineEdit.setText(os.environ['GPSPREVIEW_STARTFRAME'])
				self.ui.end_lineEdit.setText(os.environ['GPSPREVIEW_ENDFRAME'])
			self.ui.resolution_comboBox.setCurrentIndex(int(os.environ['GPSPREVIEW_RESINDEX']))
			self.ui.x_lineEdit.setText(os.environ['GPSPREVIEW_HRES'])
			self.ui.y_lineEdit.setText(os.environ['GPSPREVIEW_VRES'])
		except KeyError:
			pass

	#updates resolution group UI based on combo box selection
	def updateResGrp(self):
		resType = self.ui.resolution_comboBox.currentText()
		if resType == 'custom':
			self.ui.x_lineEdit.setEnabled(True)
			self.ui.y_lineEdit.setEnabled(True)
		else:
			self.ui.x_lineEdit.setEnabled(False)
			self.ui.y_lineEdit.setEnabled(False)
		self.getRes()
		self.ui.x_lineEdit.setText(str(self.res[0]))
		self.ui.y_lineEdit.setText(str(self.res[1]))

	#updates range group UI based on combo box selection
	def updateRangeGrp(self):
		rangeType = self.ui.range_comboBox.currentText()
		if rangeType == 'custom':
			self.ui.start_lineEdit.setEnabled(True)
			self.ui.end_lineEdit.setEnabled(True)
		else:
			self.ui.start_lineEdit.setEnabled(False)
			self.ui.end_lineEdit.setEnabled(False)
			
		self.getRange()
		if self.frRange in ('timeline', 'current frame'):
			self.ui.start_lineEdit.setText('')
			self.ui.end_lineEdit.setText('')
		else:
			self.ui.start_lineEdit.setText(str(self.frRange[0]))
			self.ui.end_lineEdit.setText(str(self.frRange[1]))


	def setOffscreen(self, state):
		if state == QtCore.Qt.Checked:
			#self.offscreen = True
			userPrefs.edit('gpspreview', 'offscreen', 'True')
		else:
			#self.offscreen = False
			userPrefs.edit('gpspreview', 'offscreen', 'False')

	def setNoSelection(self, state):
		if state == QtCore.Qt.Checked:
			#self.noSelect = True
			userPrefs.edit('gpspreview', 'noselection', 'True')
		else:
			#self.noSelect = False
			userPrefs.edit('gpspreview', 'noselection', 'False')

	def setGuides(self, state):
		if state == QtCore.Qt.Checked:
			#self.guides = True
			userPrefs.edit('gpspreview', 'guides', 'True')
		else:
			#self.guides = False
			userPrefs.edit('gpspreview', 'guides', 'False')

	def setSlate(self, state):
		if state == QtCore.Qt.Checked:
			#self.slate = True
			userPrefs.edit('gpspreview', 'slate', 'True')
		else:
			#self.slate = False
			userPrefs.edit('gpspreview', 'slate', 'False')

	def setLaunchViewer(self, state):
		if state == QtCore.Qt.Checked:
			#self.viewer = True
			userPrefs.edit('gpspreview', 'launchviewer', 'True')
		else:
			#self.viewer = False
			userPrefs.edit('gpspreview', 'launchviewer', 'False')

	def setCreateQuicktime(self, state):
		if state == QtCore.Qt.Checked:
			#self.createQt = True
			userPrefs.edit('gpspreview', 'createqt', 'True')
		else:
			#self.createQt = False
			userPrefs.edit('gpspreview', 'createqt', 'False')


	#getting UI options
	def getOpts(self):
		self.fileInput = self.ui.file_lineEdit.text()

		self.offscreen, self.noSelect, self.guides, self.slate, self.viewer, self.createQt = False, False, False, False, False, False
		if self.ui.offscreen_checkBox.checkState() == 2:
			self.offscreen = True
		if self.ui.noSelection_checkBox.checkState() == 2:
			self.noSelect = True
		if self.ui.guides_checkBox.checkState() == 2:
			self.guides = True
		if self.ui.slate_checkBox.checkState() == 2:
			self.slate = True
		if self.ui.launchViewer_checkBox.checkState() == 2:
			self.viewer = True
		if self.ui.createQuicktime_checkBox.checkState() == 2:
			self.createQt = True

		#getting frame range and resolution and testing for all inputs and integers
		self.getRes()
		self.getRange()
		#testing fileInput
		if not len(self.fileInput):
			verbose.redFields()
			return
		#testing resolution for integers
		try:
			self.res = (int(self.res[0]), int(self.res[1]))
		except ValueError:
			verbose.integersInput('resolution')
			return
		#testing frame range for integers
		if self.frRange not in ('timeline', 'current frame'):
			try:
				self.frRange = (int(self.frRange[0]), int(self.frRange[1]))
			except ValueError:	
				verbose.integersInput('frame range')
				return
		return 1
	
	#getting resolution
	def getRes(self):
		self.resType = self.ui.resolution_comboBox.currentText()
		shotRes = (os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY'])
		if self.resType == 'shot default':
			self.res = shotRes 
		elif self.resType == 'custom':
			self.res = self.ui.x_lineEdit.text(), self.ui.y_lineEdit.text()
		else:
			resMult = int(self.ui.resolution_comboBox.currentText().replace('%', ''))
			resMult = float(resMult) / 100.0
			shotRes = (int((float(shotRes[0])*resMult)), int((float(shotRes[1])*resMult)))
			self.res = shotRes 
	
	#getting frame range
	def getRange(self):
		self.rangeType = self.ui.range_comboBox.currentText()
		frRange = (os.environ['STARTFRAME'], os.environ['ENDFRAME'])
		if self.rangeType == 'shot default':
			self.frRange = frRange
		elif self.rangeType == 'custom':
			self.frRange = (self.ui.start_lineEdit.text(), self.ui.end_lineEdit.text())
		elif self.rangeType == 'timeline':
			self.frRange = 'timeline'
		elif self.rangeType == 'current frame':
			self.frRange = 'current frame'
	
	#saves UI options during the session
	def saveOpts(self):
		os.environ['GPSPREVIEW_FILE'] = self.ui.file_lineEdit.text()
		os.environ['GPSPREVIEW_RESINDEX'] = str(self.ui.resolution_comboBox.currentIndex())
		os.environ['GPSPREVIEW_HRES'] = str(self.res[0])
		os.environ['GPSPREVIEW_VRES'] = str(self.res[1])
		os.environ['GPSPREVIEW_RANGEINDEX'] = str(self.ui.range_comboBox.currentIndex())
		os.environ['GPSPREVIEW_STARTFRAME'] = str(self.frRange[0])
		os.environ['GPSPREVIEW_ENDFRAME'] = str(self.frRange[1])
		
	############################################################ END UI ############################################################
	################################################################################################################################
	
	#gets options passing information to appConnect and saving options once appConnect is done
	def preview(self):
		if self.getOpts():
			previewSetup = appConnect.connect(self.fileInput, self.res, self.frRange, self.offscreen, self.noSelect, self.guides, self.slate)
			previewOutput = previewSetup.appPreview()
			if previewOutput:
				self.outputDir, self.outputFile, self.frRange, self.ext = previewOutput
				if self.createQt:
					self.createQuicktime()
				if self.viewer:
					self.launchViewer()
			self.saveOpts()
			osOps.setPermissions(self.outputDir)
				
	#creates a quicktime
	def createQuicktime(self):
		#deletes qt file if exists in outputDir
		input = os.path.join(self.outputDir, self.outputFile)
		if os.path.isfile('%s.mov' % input):
			osOps.recurseRemove(input)
		output = self.outputDir
		startFrame = self.frRange[0]
		endFrame = self.frRange[1]
		inExt = self.ext
		djvOps.prcQt(input, output, startFrame, endFrame, inExt, name=self.outputFile, fps=os.environ['FPS'], resize=None)

	#launches viewer
	def launchViewer(self):
		input = os.path.join(self.outputDir, '%s.%s.%s' % (self.outputFile, self.frRange[0], self.ext))
		djvOps.viewer(input)

#launching UI window
if os.environ['ICARUSENVAWARE'] == 'MAYA':
	gpsPreviewApp = previewUI()
	#Qt window flags
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		gpsPreviewApp.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
	else:
		gpsPreviewApp.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)
	#centering window
	gpsPreviewApp.move(QtGui.QDesktopWidget().availableGeometry(1).center() - gpsPreviewApp.frameGeometry().center())

	gpsPreviewApp.show()