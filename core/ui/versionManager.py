#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@hogarthww.com
#title     	:versionManger

import os, sys
from PySide import QtCore, QtGui
from versionManagerUI import *

#laucnhes and controls the Version Manager UI

class dialog(QtGui.QDialog):
	
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		# Apply UI style sheet
		qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
		with open(qss, "r") as fh:
			self.ui.main_frame.setStyleSheet(fh.read())

		#defining phonon as preview player. Excepting import as Nuke does not include phonon its pySide compile
		try:
			from PySide.phonon import Phonon
			self.previewPlayer = Phonon.VideoPlayer(parent = self.ui.gatherImgPreview_label)
		except ImportError:
			self.previewPlayer = None
		
	def dialogWindow(self, assetRootDir, version, modal=True):
		#connecting signals and slots and setting window flags
		QtCore.QObject.connect(self.ui.update_pushButton, QtCore.SIGNAL("clicked()"), self.update)
		QtCore.QObject.connect(self.ui.cancel_pushButton, QtCore.SIGNAL("clicked()"), self.cancel)
		QtCore.QObject.connect(self.ui.assetVersion_listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.reloadVersionDetails)
		#Qt window flags
		if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
		else:
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)
		#centering window
		self.move(QtGui.QDesktopWidget().availableGeometry(1).center() - self.frameGeometry().center())
		
		
		#loading ICData for current asset verion
		assetRootDir = os.path.expandvars(assetRootDir)
		assetDir = os.path.join(assetRootDir, version) #.replace('\\', '\\\\') # backslashes in Windows paths need escaping
		sys.path.append(assetDir)
		#print assetDir
		import icData;	reload(icData)
		sys.path.remove(assetDir)
		
		#Setting asset label text
		self.ui.asset_label.setText(icData.assetPblName)
		
		self.updateVersion = ''
		self.assetRootDir = os.path.expandvars(icData.assetRootDir)
		self.updateAssetVersionCol(icData, setCurrentVersion=True)
		self.reloadVersionDetails()
		
		#running dialog based on modality flag
		if modal:
			self.exec_()
			return self.updateVersion
		else:
			self.show()
			
			
			
	##########################################################Phonon player flag handler##############################################
	##################################################################################################################################	
	def previewPlayerCtrl(self, show=False, hide=False, play=False, loadImg=None):
		if self.previewPlayer:
			if show:
				self.previewPlayer.show()
			elif hide:
				self.previewPlayer.hide()
			elif play:
				self.previewPlayer.play()
			elif loadImg:
				self.previewPlayer.load(loadImg)
			
			
			
	########################################################Content load/refresg functions############################################
	##################################################################################################################################
	
	#reloads all details related to selected version
	def reloadVersionDetails(self):
		#loading icData file for selected version
		selVersion = self.vColumn.currentItem().text()
		assetDir = os.path.join(self.assetRootDir, selVersion)
		sys.path.append(assetDir)
		import icData;	reload(icData)
		sys.path.remove(assetDir)
		#updating info field
		self.updateInfoField(icData.notes)
		#updating preview
		self.updateImgPreview(assetDir)
		
	#updates assetVersion column
	def updateAssetVersionCol(self, icData, setCurrentVersion=False):
		#gets list of all asset versions
		self.vColumn = self.ui.assetVersion_listWidget
		versionLs = os.listdir(self.assetRootDir)
		versionLs = sorted(versionLs, reverse=True)
		#clears version column
		for i in range(0, self.vColumn.count()):
			self.vColumn.takeItem(0)
		for item in versionLs:
			if not item.startswith('.'):
				self.vColumn.addItem(item)
		#setting the current version as selected
		if setCurrentVersion:
			selVersionItem = self.vColumn.findItems(icData.version, QtCore.Qt.MatchRegExp)
			self.vColumn.setCurrentItem(selVersionItem[0])
		
	#updates infoField with notes 
	def updateInfoField(self, notes):
		self.ui.gatherInfo_textEdit.setText('')
		vColumn = self.ui.assetVersion_listWidget
		self.ui.gatherInfo_textEdit.setText(notes)

	#updates image preview field with snapshot 
	def updateImgPreview(self, assetDir):
		import previewImg
		imgPath = ''
		self.previewPlayerCtrl(hide=True)
		self.ui.gatherImgPreview_label.setPixmap(None)
		if self.previewPlayer:
			imgPath = previewImg.getImg(assetDir, forceExt='mov')
			if imgPath:
					self.previewPlayerCtrl(hide=True)
					self.ui.gatherImgPreview_label.setPixmap(None)
					self.previewPlayerCtrl(loadImg=imgPath)
					self.previewPlayerCtrl(show=True)
					self.previewPlayerCtrl(play=True)
		if not imgPath or not self.previewPlayer:
			imgPath = previewImg.getImg(assetDir, forceExt='jpg')
			if imgPath:
				self.previewPlayerCtrl(hide=True)
				self.ui.gatherImgPreview_label.setPixmap(None)
				self.ui.gatherImgPreview_label.setScaledContents(True)
				self.ui.gatherImgPreview_label.setPixmap(imgPath)
						

					
	###################################################Dialog acceptance/cancelation functions########################################
	##################################################################################################################################				
					
	#dialog acceptance function		
	def update(self):
		self.updateVersion = self.vColumn.currentItem().text()
		self.accept()
		return 

	#dialog cancel function
	def cancel(self):
		self.accept()
		return