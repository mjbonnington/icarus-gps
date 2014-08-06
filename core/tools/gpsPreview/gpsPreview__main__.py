#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsPreview

import os, subprocess
from PySide import QtCore, QtGui
from gpsPreviewUI import *
import djvOps, verbose, appConnect

class previewUI(QtGui.QDialog):
	
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.pDialog = self
		self.pDialog.ui = Ui_Dialog()
		self.pDialog.ui.setupUi(self)
		#connecting signals and slots
		QtCore.QObject.connect(self.pDialog.ui.preview_pushButton, QtCore.SIGNAL("clicked()"), self.preview)
		QtCore.QObject.connect(self.pDialog.ui.resolution_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateResGrp)
		QtCore.QObject.connect(self.pDialog.ui.range_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.updateRangeGrp)
		
		#populating UI with env vars
		self.setupUI()		
			
		#launching UI window
		self.pDialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
		self.pDialog.show()
			
	############################################################## UI ##############################################################
	################################################################################################################################
	
	def setupUI(self):
		self.pDialog.ui.jobShot_label.setText('%s - %s' % (os.environ['JOB'], os.environ['SHOT']))
		self.pDialog.ui.x_lineEdit.setText(os.environ['RESOLUTIONX'])
		self.pDialog.ui.y_lineEdit.setText(os.environ['RESOLUTIONY'])
		try:
			self.pDialog.ui.file_lineEdit.setText(os.environ['GPSPREVIEW_FILE'])
			self.pDialog.ui.range_comboBox.setCurrentIndex(int(os.environ['GPSPREVIEW_RANGEINDEX']))
			if int(os.environ['GPSPREVIEW_RANGEINDEX']) is 1:
				self.pDialog.ui.start_lineEdit.setText('')
				self.pDialog.ui.end_lineEdit.setText('')
			else:
				self.pDialog.ui.start_lineEdit.setText(os.environ['GPSPREVIEW_STARTFRAME'])
				self.pDialog.ui.end_lineEdit.setText(os.environ['GPSPREVIEW_ENDFRAME'])
			self.pDialog.ui.resolution_comboBox.setCurrentIndex(int(os.environ['GPSPREVIEW_RESINDEX']))
			self.pDialog.ui.x_lineEdit.setText(os.environ['GPSPREVIEW_HRES'])
			self.pDialog.ui.y_lineEdit.setText(os.environ['GPSPREVIEW_VRES'])
		except KeyError:
			pass
	
	#updates resolution group UI based on combo box selection
	def updateResGrp(self):
		resType = self.pDialog.ui.resolution_comboBox.currentText()
		if resType == 'custom':
			self.pDialog.ui.x_lineEdit.setEnabled(True)
			self.pDialog.ui.y_lineEdit.setEnabled(True)
		else:
			self.pDialog.ui.x_lineEdit.setEnabled(False)
			self.pDialog.ui.y_lineEdit.setEnabled(False)
		self.getRes()
		self.pDialog.ui.x_lineEdit.setText(str(self.res[0]))
		self.pDialog.ui.y_lineEdit.setText(str(self.res[1]))

	#updates range group UI based on combo box selection
	def updateRangeGrp(self):
		rangeType = self.pDialog.ui.range_comboBox.currentText()
		if rangeType == 'custom':
			self.pDialog.ui.start_lineEdit.setEnabled(True)
			self.pDialog.ui.end_lineEdit.setEnabled(True)
		else:
			self.pDialog.ui.start_lineEdit.setEnabled(False)
			self.pDialog.ui.end_lineEdit.setEnabled(False)
			
		self.getRange()
		if self.frRange == 'timeline':
			self.pDialog.ui.start_lineEdit.setText('')
			self.pDialog.ui.end_lineEdit.setText('')
		else:
			self.pDialog.ui.start_lineEdit.setText(str(self.frRange[0]))
			self.pDialog.ui.end_lineEdit.setText(str(self.frRange[1]))
			
	#getting UI options
	def getOpts(self):
		self.fileInput = self.pDialog.ui.file_lineEdit.text()
		self.offscreen, self.noSelect, self.guides, self.slate, self.createQt = False, False, False, False, False
		if self.pDialog.ui.offscreen_checkBox.checkState() == 2:
			self.offscreen = True
		if self.pDialog.ui.noSelection_checkBox.checkState() == 2:
			self.noSelect = True
		if self.pDialog.ui.guides_checkBox.checkState() == 2:
			self.guides = True
		if self.pDialog.ui.slate_checkBox.checkState() == 2:
			self.slate = True
		if self.pDialog.ui.createQuicktime_checkBox.checkState() == 2:
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
		if self.frRange is not 'timeline':
			try:
				self.frRange = (int(self.frRange[0]), int(self.frRange[1]))
			except ValueError:	
				verbose.integersInput('frame range')
				return
		return 1
	
	#getting resolution
	def getRes(self):
		self.resType = self.pDialog.ui.resolution_comboBox.currentText()
		shotRes = (os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY'])
		if self.resType == 'shot default':
			self.res = shotRes 
		elif self.resType == 'custom':
			self.res = self.pDialog.ui.x_lineEdit.text(), self.pDialog.ui.y_lineEdit.text()
		else:
			resMult = int(self.pDialog.ui.resolution_comboBox.currentText().replace('%', ''))
			resMult = float(resMult) / 100.0
			shotRes = (int((float(shotRes[0])*resMult)), int((float(shotRes[1])*resMult)))
			self.res = shotRes 
	
	#getting frame range
	def getRange(self):
		self.rangeType = self.pDialog.ui.range_comboBox.currentText()
		frRange = (os.environ['STARTFRAME'], os.environ['ENDFRAME'])
		if self.rangeType == 'shot default':
			self.frRange = frRange
		elif self.rangeType == 'custom':
			self.frRange = (self.pDialog.ui.start_lineEdit.text(), self.pDialog.ui.end_lineEdit.text())
		else:
			self.frRange = 'timeline'
	
	#saves UI options during the session
	def saveOpts(self):
		os.environ['GPSPREVIEW_FILE'] = self.pDialog.ui.file_lineEdit.text()
		os.environ['GPSPREVIEW_RESINDEX'] = str(self.pDialog.ui.resolution_comboBox.currentIndex())
		os.environ['GPSPREVIEW_HRES'] = str(self.res[0])
		os.environ['GPSPREVIEW_VRES'] = str(self.res[1])
		os.environ['GPSPREVIEW_RANGEINDEX'] = str(self.pDialog.ui.range_comboBox.currentIndex())
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
		djvPath = os.environ['FRAMEVIEWER']
		input = '%s/%s.%s.%s' % (self.outputDir, self.outputFile, self.frRange[0], self.ext)
		command = '%s %s' % (djvPath, input)
		subprocess.Popen(command, shell=True)


