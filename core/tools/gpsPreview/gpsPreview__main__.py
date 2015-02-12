#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsPreview

import os, subprocess
from PySide import QtCore, QtGui
from gpsPreviewUI import *
import djvOps, verbose, appConnect

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
			
	#getting UI options
	def getOpts(self):
		self.fileInput = self.ui.file_lineEdit.text()
		self.offscreen, self.noSelect, self.guides, self.slate, self.createQt = False, False, False, False, False
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
				
	#creates a quicktime
	def createQuicktime(self):
		#deletes qt file if exists in outputDir
		input = '%s/%s' % (self.outputDir, self.outputFile)
		if os.path.isfile('%s.mov' % input):
			os.system('rm -f %s.mov' % input)
		output = self.outputDir
		startFrame = self.frRange[0]
		endFrame = self.frRange[1]
		inExt = self.ext
		djvOps.prcQt(input, output, startFrame, endFrame, inExt, name=self.outputFile, fps=os.environ['FPS'], resize=None)

	#launches viewer
	def launchViewer(self):
		djvPath = os.environ['DJV_PLAY']
		#exporting correct path for djv Libraries based on icarus running OS
		if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
			djvLib = 'export DYLD_FALLBACK_LIBRARY_PATH=%s' % os.environ['DJV_LIB']
		else:
			djvLib = 'export LD_LIBRARY_PATH=%s' % os.environ['DJV_LIB']
		input = '%s/%s.%s.%s' % (self.outputDir, self.outputFile, self.frRange[0], self.ext)
		command = '%s; %s %s' % (djvLib, djvPath, input)
		subprocess.Popen(command, shell=True)


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