#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:icarus__main__
#copyright	:Gramercy Park Studios


from PySide import QtCore, QtGui
from PySide.QtGui import QStyleFactory
from icarusUI import *
import os, sys, env__init__


#lauches and controls Icarus main UI

#initializing icarus environment and adding libs to sysPath
env__init__.setEnv()

#note: publish modules are imported on demand rather than all at once at beggining of file
import launchApps, setJob, userPrefs, verbose, pblChk, pblOptsPrc, openDirs, setTerm, jobs, listShots

class icarusApp(QtGui.QDialog):
	def __init__(self, parent = None):
		super(icarusApp, self).__init__(parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Read user prefs config file file - if it doesn't exist it will be created
		userPrefs.read()

		#defining phonon as preview player if icarus is standalone
		if os.environ['ICARUSENVAWARE'] == 'STANDALONE':
			from PySide.phonon import Phonon
			self.previewPlayer = Phonon.VideoPlayer(parent = self.ui.gatherImgPreview_label)
		else:
			self.previewPlayer = None

	##########################################Connecting signals and slots##########################################
	################################################################################################################
		QtCore.QObject.connect(self.ui.job_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.populateShots)
		QtCore.QObject.connect(self.ui.setShot_pushButton, QtCore.SIGNAL('clicked()'), self.setupJob)
		QtCore.QObject.connect(self.ui.setNewShot_pushButton, QtCore.SIGNAL('clicked()'), self.unlockJobUI)
		QtCore.QObject.connect(self.ui.maya_pushButton, QtCore.SIGNAL('clicked()'), self.launchMaya)
		QtCore.QObject.connect(self.ui.mudbox_pushButton, QtCore.SIGNAL('clicked()'), self.launchMudbox)
		QtCore.QObject.connect(self.ui.nuke_pushButton, QtCore.SIGNAL('clicked()'), self.launchNuke)
		QtCore.QObject.connect(self.ui.mari_pushButton, QtCore.SIGNAL('clicked()'), self.launchMari)
		QtCore.QObject.connect(self.ui.realflow_pushButton, QtCore.SIGNAL('clicked()'), self.launchRealflow)
		QtCore.QObject.connect(self.ui.openProdBoard_pushButton, QtCore.SIGNAL('clicked()'), launchApps.prodBoard)
		QtCore.QObject.connect(self.ui.openReview_pushButton, QtCore.SIGNAL('clicked()'), self.launchHieroPlayer)
		QtCore.QObject.connect(self.ui.openTerminal_pushButton, QtCore.SIGNAL('clicked()'), self.launchTerminal)
		QtCore.QObject.connect(self.ui.browse_pushButton, QtCore.SIGNAL('clicked()'), openDirs.openShot)
		QtCore.QObject.connect(self.ui.render_pushButton, QtCore.SIGNAL('clicked()'), self.launchSubmitRender)
		QtCore.QObject.connect(self.ui.renderPblAdd_pushButton, QtCore.SIGNAL('clicked()'), self.renderTableAdd)
		QtCore.QObject.connect(self.ui.renderPblRemove_pushButton, QtCore.SIGNAL('clicked()'), self.renderTableRm)
		QtCore.QObject.connect(self.ui.renderPblSetMain_pushButton, QtCore.SIGNAL('clicked()'), self.setLayerAsMain)
		QtCore.QObject.connect(self.ui.dailyPblType_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.setDailyType)
		QtCore.QObject.connect(self.ui.dailyPblAdd_pushButton, QtCore.SIGNAL('clicked()'), self.dailyTableAdd)
		QtCore.QObject.connect(self.ui.publish_pushButton, QtCore.SIGNAL('clicked()'), self.initPublish)
		QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.adjustMainUI)

		self.ui.minimise_checkBox.stateChanged.connect(self.setMinimiseOnAppLaunch)

		self.boolMinimiseOnAppLaunch = userPrefs.config.getboolean('main', 'minimiseonlaunch')
		self.ui.minimise_checkBox.setChecked(self.boolMinimiseOnAppLaunch)

	########################################Adding right click menus to buttons#######################################
	##################################################################################################################
		#Nuke
		self.ui.nuke_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionNuke = QtGui.QAction("Nuke", None)
		self.actionNuke.triggered.connect(self.launchNuke)
		self.actionNukeX = QtGui.QAction("NukeX", None)
		self.actionNukeX.triggered.connect(self.launchNukeX)
		self.ui.nuke_pushButton.addAction(self.actionNuke)
		self.ui.nuke_pushButton.addAction(self.actionNukeX)
		#Review
		self.ui.openReview_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionHieroPlayer = QtGui.QAction("HieroPlayer", None)
		self.actionHieroPlayer.triggered.connect(self.launchHieroPlayer)
		self.actionDjv = QtGui.QAction("djv_view", None)
		self.actionDjv.triggered.connect(self.launchDjv)
		self.ui.openReview_pushButton.addAction(self.actionHieroPlayer)
		self.ui.openReview_pushButton.addAction(self.actionDjv)
		#Browse
		self.ui.browse_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionOpenShot = QtGui.QAction("Shot", None)
		self.actionOpenShot.triggered.connect(openDirs.openShot)
		self.actionOpenJob = QtGui.QAction("Job", None)
		self.actionOpenJob.triggered.connect(openDirs.openJob)
		self.ui.browse_pushButton.addAction(self.actionOpenShot)
		self.ui.browse_pushButton.addAction(self.actionOpenJob)
		#Render
		self.ui.render_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionDeadlineMonitor = QtGui.QAction("Deadline Monitor", None)
		self.actionDeadlineMonitor.triggered.connect(openDirs.openShot)
		self.actionDeadlineSlave = QtGui.QAction("Deadline Slave", None)
		self.actionDeadlineSlave.triggered.connect(openDirs.openShot)
		self.actionSubmitLocal = QtGui.QAction("Submit Maya command-line render (local)", None)
		self.actionSubmitLocal.triggered.connect(self.launchSubmitRender)
		self.ui.render_pushButton.addAction(self.actionDeadlineMonitor)
		self.ui.render_pushButton.addAction(self.actionDeadlineSlave)
		self.ui.render_pushButton.addAction(self.actionSubmitLocal)

	##########################################UI adapt environment awareness##########################################
	##################################################################################################################
		self.jobMngTab = self.ui.tabWidget.widget(0)
		self.publishTab = self.ui.tabWidget.widget(1)
		self.gatherTab = self.ui.tabWidget.widget(2)
		self.publishAssetTab = self.ui.publishType_tabWidget.widget(0)
		self.publishRenderTab = self.ui.publishType_tabWidget.widget(1)
		self.ui.renderPbl_tableWidget.setColumnWidth(0,120)
		self.ui.renderPbl_tableWidget.setColumnWidth(1,380)
		self.ui.renderPbl_tableWidget.setColumnWidth(2,81)
		self.ui.dailyPbl_tableWidget.setColumnWidth(0,120)
		self.ui.dailyPbl_tableWidget.setColumnWidth(1,380)
		self.ui.dailyPbl_tableWidget.setColumnWidth(2,81)
			
		###########STANDALONE ENVIRONMENT#############
		##############################################
		if os.environ['ICARUSENVAWARE'] == 'STANDALONE':
			#hides ui items relating to maya environment
			uiHideLs = ['setNewShot_pushButton'] # Removed 'shotEnv_label_maya', 
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' % uiItem
				eval(hideProc)
			#populates job and shot drop down menus
			entryLs = userPrefs.config.get('main', 'lastjob').split(',')
			jobLs = jobs.dic.keys()
			jobLs = sorted(jobLs, reverse=True)
			for job in jobLs:
				self.ui.job_comboBox.insertItem(0, job)
			if entryLs:
				if entryLs[0] in jobLs:
					self.ui.job_comboBox.setCurrentIndex(self.ui.job_comboBox.findText(entryLs[0]))
					self.ui.shot_comboBox.setCurrentIndex(self.ui.shot_comboBox.findText(entryLs[1]))			
			#deletes all tabs but jobMng
			for i in range(0, self.ui.tabWidget.count()-1):
				self.ui.tabWidget.removeTab(1)
			#deletes Asset, NK Asset publish tabs
			for i in range(0,2):
				self.ui.publishType_tabWidget.removeTab(0)
				
				
		##############MAYA ENVIRONMENT################
		##############################################
		elif os.environ['ICARUSENVAWARE'] == 'MAYA':
			uiHideLs = ['assetSubType_listWidget'] # Removed 'icarusBanner', 
			#hides UI items 
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' % uiItem
				eval(hideProc)
			self.ui.publishType_tabWidget.removeTab(1)
			#update shot label in maya env
			self.connectNewSignalsSlots()
			self.populatePblShotLs()
			self.populateGatherShotLs()
			self.updateJobLabel()
			self.ui.tabWidget.removeTab(0)
			
			
		##############NUKE ENVIRONMENT################
		##############################################
		elif os.environ['ICARUSENVAWARE'] == 'NUKE':
			uiHideLs = ['assetSubType_listWidget'] # Removed 'icarusBanner', 
			#hides UI 
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' % uiItem
				eval(hideProc)
			#update shot label in maya env
			self.connectNewSignalsSlots()
			self.populatePblShotLs()
			self.populateGatherShotLs()
			self.updateJobLabel()
			self.ui.tabWidget.removeTab(0)
			#deletes Asset publish tabs
			self.ui.publishType_tabWidget.removeTab(0)
			

	##############################################Generic UI procedures############################################
	###############################################################################################################
	#connects new singals and slots after job and shot env is set
	def connectNewSignalsSlots(self):
		QtCore.QObject.connect(self.ui.shotPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.setDropDownToShotEnv)
		QtCore.QObject.connect(self.ui.animPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.setDropDownToShotEnv)
		QtCore.QObject.connect(self.ui.publishType_tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.adjustPblTypeUI)
		QtCore.QObject.connect(self.ui.cameraPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.uncheckSubset)
		QtCore.QObject.connect(self.ui.modelPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.uncheckSubset)
		QtCore.QObject.connect(self.ui.geoCachePbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.uncheckSubset)
		QtCore.QObject.connect(self.ui.geoPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.uncheckSubset)
		QtCore.QObject.connect(self.ui.rigPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.uncheckSubset)
		QtCore.QObject.connect(self.ui.nodePbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.uncheckSubset)
		QtCore.QObject.connect(self.ui.nk_compPbl_radioButton, QtCore.SIGNAL("clicked(bool)"), self.adjustPblTypeUI)
		QtCore.QObject.connect(self.ui.gatherFromShot_radioButton, QtCore.SIGNAL('clicked(bool)'), self.adjustMainUI)
		QtCore.QObject.connect(self.ui.gatherFromShot_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.adjustMainUI)
		QtCore.QObject.connect(self.ui.gatherFromJob_radioButton, QtCore.SIGNAL('clicked(bool)'), self.adjustMainUI)
		QtCore.QObject.connect(self.ui.gather_pushButton, QtCore.SIGNAL('clicked(bool)'), self.initGather)
		QtCore.QObject.connect(self.ui.assetType_listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.updateAssetNameCol)
		QtCore.QObject.connect(self.ui.assetName_listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.adjustColumns)
		QtCore.QObject.connect(self.ui.assetSubType_listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.updateAssetVersionCol)
		QtCore.QObject.connect(self.ui.assetVersion_listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.updateInfoField)
		QtCore.QObject.connect(self.ui.assetVersion_listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem *)'), self.updateImgPreview)
		
	#gets the current main tab
	def getMainTab(self):
		tabIndex = self.ui.tabWidget.currentIndex()
		tabText = self.ui.tabWidget.tabText(tabIndex)
		return tabIndex, tabText
		
	#gets current publish type tab
	def getPblTab(self):
		tabIndex = self.ui.publishType_tabWidget.currentIndex()
		tabText = self.ui.publishType_tabWidget.tabText(tabIndex)
		return tabIndex, tabText
		
	#makes UI adjustments and connections based on what tab is currently selected
	def adjustMainUI(self):
		mainTabName = self.getMainTab()[1]
		if mainTabName == 'Gather' or mainTabName == 'Assets' :
			self.defineColumns()
			self.updateAssetTypeCol()
			
	#makes UI lock adjustments based on what publish type tab is currently selected
	def adjustPblTypeUI(self):
		#tabText = self.ui.publishType_tabWidget.setGeometry(17, 80, 771, 215)
		tabIndex = self.ui.publishType_tabWidget.currentIndex()
		tabText = self.ui.publishType_tabWidget.tabText(tabIndex)
		if tabText == 'ma Asset':
			self.lockPublishTo()
		if tabText == 'nk Asset':
			#tabText = self.ui.publishType_tabWidget.setGeometry(187, 80, 451, 215)
			if self.ui.nk_compPbl_radioButton.isChecked() == True:
				self.setDropDownToShotEnv()
				self.lockPublishTo(lock=True)
			else:
				self.lockPublishTo()
		if tabText == 'Render':
			self.lockPublishTo(lock=True)
			self.setDropDownToShotEnv()
		if tabText == 'Daily':
			self.lockPublishTo(lock=True)
			self.setDropDownToShotEnv()		
			
	#locks Publish To section of UI based on selection		
	def lockPublishTo(self, lock=False):
		if lock:
			self.ui.publishToJob_radioButton.setEnabled(False)
			self.ui.publishToShot_radioButton.setChecked(True)
			self.ui.publishToShot_comboBox.setEnabled(False)
		else:
			self.ui.modelPbl_radioButton.setChecked(True)
			self.ui.publishToJob_radioButton.setEnabled(True)
			self.ui.publishToShot_comboBox.setEnabled(True)
	
	#swicthes the shot drop down menu to the current environment shot		
	def setDropDownToShotEnv(self):
		self.ui.publishToShot_comboBox.setCurrentIndex(self.ui.publishToShot_comboBox.findText(os.environ['SHOT']))
		
	#file dialog
	#the env check puts the main window in the background so dialog pop up can return properly when running inside certain applications
	#the window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env
	def fileDialog(self, dialogHome):
		envOverride = ['MAYA', 'NUKE']
		if os.environ['ICARUSENVAWARE'] in envOverride:
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
			dialog = QtGui.QFileDialog.getOpenFileName(app, self.tr('Files'), dialogHome, 'All files (*.*)')
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
		else:
			dialog = QtGui.QFileDialog.getOpenFileName(app, self.tr('Files'), dialogHome, 'All files (*.*)')
		return dialog[0]
	
	#fodler dialog
	#the env check puts the main window in the background so dialog pop up can return properly when running inside certain applications
	#the window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env
	def folderDialog(self, dialogHome):
		envOverride = ['MAYA', 'NUKE']
		if os.environ['ICARUSENVAWARE'] in envOverride:
			#this window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
			dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
		else:
			dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome,
			QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)
		return dialog
				
	##############################################Job management tab##############################################
	##############################################################################################################
	#populates shot drop down menu
	def populateShots(self):
		for shot in range(0, self.ui.shot_comboBox.count(), 1):
			self.ui.shot_comboBox.removeItem(0)
		selJob = self.ui.job_comboBox.currentText()
		shotLs = listShots.list_(selJob)
		if shotLs:
			for shot in shotLs:
				self.ui.shot_comboBox.insertItem(0, shot)
			self.ui.shot_comboBox.setCurrentIndex(0)
			self.ui.shot_comboBox.setEnabled(True)
			self.ui.setShot_label.setEnabled(True)
			self.ui.setShot_pushButton.setEnabled(True)
		else:
			self.ui.shot_comboBox.insertItem(0, '[None]')
			self.ui.shot_comboBox.setEnabled(False)
			self.ui.setShot_label.setEnabled(False)
			self.ui.setShot_pushButton.setEnabled(False)

	#populates publish shot drop down menu	
	def populatePblShotLs(self):
		self.ui.publishToShot_comboBox.clear()
		shotLs = listShots.list_(os.environ['JOB'])
		if shotLs:
			for shot in shotLs:
				self.ui.publishToShot_comboBox.insertItem(0, shot)
			self.ui.publishToShot_comboBox.setCurrentIndex(self.ui.publishToShot_comboBox.findText(os.environ['SHOT']))
	
	#populates gather shot drop down menu	
	def populateGatherShotLs(self):
		self.ui.gatherFromShot_comboBox.clear()
		shotLs = listShots.list_(os.environ['JOB'])
		if shotLs:
			for shot in shotLs:
				self.ui.gatherFromShot_comboBox.insertItem(0, shot)
			self.ui.gatherFromShot_comboBox.setCurrentIndex(self.ui.gatherFromShot_comboBox.findText(os.environ['SHOT']))

	#updates job tab ui with shot selection
	def updateJobUI(self):
		self.ui.setShot_pushButton.setEnabled(True)

	#sets up shot environment, creates user directories and updates user job log
	def setupJob(self):
		self.job = self.ui.job_comboBox.currentText()
		self.shot = self.ui.shot_comboBox.currentText()
		setJob.setup(self.job, self.shot)
		self.adjustPblTypeUI()
		self.populatePblShotLs()
		self.populateGatherShotLs()
		self.connectNewSignalsSlots()
		self.lockJobUI()

	#updates and locks UI job tab
	def lockJobUI(self):
		self.updateJobLabel()
		self.ui.shotSetup_groupBox.setEnabled(False)
		self.ui.launchApp_groupBox.setEnabled(True)
		self.ui.launchOptions_groupBox.setEnabled(True)
		self.ui.tabWidget.insertTab(1, self.publishTab, 'Publish')
		self.ui.tabWidget.insertTab(2, self.gatherTab, 'Assets')
		self.ui.gather_pushButton.hide()
		self.ui.setShot_pushButton.hide()
		self.ui.setNewShot_pushButton.show()
		verbose.jobSet(self.job, self.shot)
	
	#unlocks UI if set new shot is clicked
	def unlockJobUI(self):
		self.ui.shotSetup_groupBox.setEnabled(True)
		self.ui.launchApp_groupBox.setEnabled(False)
		self.ui.launchOptions_groupBox.setEnabled(False)
		#removing publish and assets tab
		self.ui.tabWidget.removeTab(1); self.ui.tabWidget.removeTab(1)
		for row in range(self.ui.renderPbl_tableWidget.rowCount()):
			self.ui.renderPbl_tableWidget.removeRow(0)
		self.ui.renderPbl_tableWidget.clearContents()
		self.ui.dailyPbl_tableWidget.removeRow(0)
		self.ui.dailyPbl_tableWidget.clearContents()
		self.ui.shotEnv_label.setText('')
		self.ui.setNewShot_pushButton.hide()
		self.ui.setShot_pushButton.show()
		
	#controls phonon preview player
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

	#updates job label
	def updateJobLabel(self):
		if os.environ['ICARUSENVAWARE'] != 'STANDALONE':
			self.job = os.environ['JOB']
			self.shot = os.environ['SHOT']
		self.ui.shotEnv_label.setText('%s - %s' % (self.job, self.shot))
		#self.ui.shotEnv_label_maya.setText('%s - %s' % (self.job, self.shot)) # This is now redundant as the current shot is always shown in the header.

	# Sets state of minimise on app launch variable
	def setMinimiseOnAppLaunch(self, state):
		if state == QtCore.Qt.Checked:
			self.boolMinimiseOnAppLaunch = True
			userPrefs.edit('main', 'minimiseonlaunch', 'True')
			#print "Minimise on launch enabled"
		else:
			self.boolMinimiseOnAppLaunch = False
			userPrefs.edit('main', 'minimiseonlaunch', 'False')
			#print "Minimise on launch disabled"

	#runs launch maya procedure
	def launchMaya(self):
		launchApps.maya()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#runs launch mudbox procedure
	def launchMudbox(self):
		launchApps.mudbox()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#runs launch nuke procedure
	def launchNuke(self):
		launchApps.nuke(nukeType='Nuke')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#runs launch nukex procedure
	def launchNukeX(self):
		launchApps.nuke(nukeType='NukeX')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()
		#launchApps.nuke()
		#self.showMinimized()

	#runs launch mari procedure
	def launchMari(self):
		launchApps.mari()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#runs launch realflow procedure
	def launchRealflow(self):
		launchApps.realflow()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#launches terminal locks button
	def launchTerminal(self):
		launchApps.terminal()
		self.ui.openTerminal_pushButton.setEnabled(False)
		self.ui.setNewShot_pushButton.setEnabled(False)
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#Launches HieroPlayer with and tries to load the job Hrox automatically
	def launchHieroPlayer(self):
		launchApps.hieroPlayer()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#Launches DJV
	def launchDjv(self):
		launchApps.djv()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#Launches GPS command-line render script
	def launchSubmitRender(self):
		import submit__main__; reload(submit__main__)
		#gpsSubmitRenderApp = submit__main__.gpsSubmitRender(parent=app)
		#gpsSubmitRenderApp.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinMaxButtonsHint )
		#gpsSubmitRenderApp.show()

	##################################################Publish tab###################################################
	################################################################################################################
	###################adjusting ui####################				
	#unchecking subset checkbox based on asset type
	def uncheckSubset(self):
		self.ui.subSet_checkBox.setChecked(False)
		self.ui.subSetName_lineEdit.setEnabled(False)
		self.ui.subSetWarning_textEdit.setEnabled(False)
		
	#populates the render publish table
	def renderTableAdd(self):
		#processes latest path added to self.renderPaths
		renderPath = self.renderPblBrowse()
		renderPath = renderPath.replace(os.environ['SHOTPATH'], '$SHOTPATH')
		renderDic = {}
		if renderPath:
			renderDic = pblOptsPrc.renderPath_prc(renderPath)
		if renderDic:
			autoMainLayer = None
			for layer in renderDic.keys():
				layerPath = renderDic[layer]
				layerItem = QtGui.QTableWidgetItem(layer)
				pathItem = QtGui.QTableWidgetItem(layerPath)
				mainItem = QtGui.QTableWidgetItem()
				#check if layers already exist
				layerChk = True
				rowCount = self.ui.renderPbl_tableWidget.rowCount()
				for row in range(0, rowCount):
					if layer == self.ui.renderPbl_tableWidget.item(row, 0).text():
						layerChk = False
						break
				#adding items and locking table
				if layerChk:
					newRow = self.ui.renderPbl_tableWidget.insertRow(0)
					self.ui.renderPbl_tableWidget.setItem(0, 0, layerItem)
					layerItem.setFlags(~QtCore.Qt.ItemIsEditable)
					self.ui.renderPbl_tableWidget.setItem(0, 1, pathItem)
					pathItem.setFlags(~QtCore.Qt.ItemIsEditable)
					self.ui.renderPbl_tableWidget.setItem(0, 2, mainItem)
					mainItem.setFlags(~QtCore.Qt.ItemIsEditable)
					mainItem.setText('layer')
					#making layer main if autoDetected
					if layer == 'main':
						autoMainLayer = layerItem
						self.setLayerAsMain(autoMainLayer)
					elif layer in ('masterLayer', 'master', 'beauty'):
						if not autoMainLayer:
							autoMainLayer = layerItem
							self.setLayerAsMain(autoMainLayer)				

	#removes items from the render table
	def renderTableRm(self):
		rmRowLs = []
		for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
			selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
			selRow = self.ui.renderPbl_tableWidget.row(selItem)
			if selRow not in rmRowLs:
				rmRowLs.append(selRow)
		rmRowLs = sorted(rmRowLs, reverse=True)
		for rmRow in rmRowLs:
			self.ui.renderPbl_tableWidget.removeRow(rmRow)
	
	#sets the selected render layer as the main layer
	def setLayerAsMain(self, autoMainLayer=None):
		for rowItem in range(0, self.ui.renderPbl_tableWidget.rowCount()):
			mainItem = self.ui.renderPbl_tableWidget.item(rowItem, 2)
			mainItem.setText('layer')
			mainItem.setBackground(QtGui.QColor(34,34,34))
			rowItem1 = self.ui.renderPbl_tableWidget.item(rowItem, 1)
			rowItem1.setBackground(QtGui.QColor(34,34,34))
			rowItem0 = self.ui.renderPbl_tableWidget.item(rowItem, 0)
			rowItem0.setBackground(QtGui.QColor(34,34,34))
		rowLs = []
		if autoMainLayer:
			selRow = self.ui.renderPbl_tableWidget.row(autoMainLayer)
			rowLs.append(selRow)
		else:
			for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
				selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
				selRow = self.ui.renderPbl_tableWidget.row(selItem)
				if selRow not in rowLs and selRow != -1:
					rowLs.append(selRow)
		if len(rowLs) == 1:
			mainItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 2)
			mainItem.setText('main')
			mainItem.setBackground(QtGui.QColor(60,75,40))
			passItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 1)
			passName = passItem.text()
			passItem.setBackground(QtGui.QColor(60,75,40))
			layerItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 0)
			layerName = passItem.text()
			layerItem.setBackground(QtGui.QColor(60,75,40))
		#app hide and show forces thw window to update
		app.hide()
		app.show()
		
	#populates the daily publish table
	def dailyTableAdd(self):
		#processes latest path added to self.renderPaths
		dailyPath = self.dailyPblBrowse()
		dailyDic = {}
		if dailyPath:
			dailyDic = pblOptsPrc.dailyPath_prc(dailyPath)
			seqPath = dailyPath.replace(os.environ['SHOTPATH'], '$SHOTPATH')
			seqPath = os.path.split(seqPath)[0]
			if dailyDic:
				seq = dailyDic.keys()[0]
				seqItem = QtGui.QTableWidgetItem(seq)
				pathItem = QtGui.QTableWidgetItem(seqPath)
				mainItem = QtGui.QTableWidgetItem()
				#deleting existent sequence
				self.ui.dailyPbl_tableWidget.removeRow(0)
				#adding items and locking table
				newRow = self.ui.dailyPbl_tableWidget.insertRow(0)
				self.ui.dailyPbl_tableWidget.setItem(0, 0, seqItem)
				seqItem.setFlags(~QtCore.Qt.ItemIsEditable)
				self.ui.dailyPbl_tableWidget.setItem(0, 1, pathItem)
				pathItem.setFlags(~QtCore.Qt.ItemIsEditable)
				self.ui.dailyPbl_tableWidget.setItem(0, 2, mainItem)
				mainItem.setFlags(~QtCore.Qt.ItemIsEditable)
				mainItem.setText(self.dailyType)
			else:
				verbose.noSeq(seqPath)
			
	#sets the daily type and locks/unlocks the add and remove button accordingly
	def setDailyType(self):
		self.dailyType = self.ui.dailyPblType_comboBox.currentText()
		if not self.dailyType:
			self.ui.dailyPblAdd_pushButton.setEnabled(False)
		else:
			self.ui.dailyPblAdd_pushButton.setEnabled(True)

	################browse dialogs###############	
	#asset browse
	def assetPblBrowse(self):
		dialogHome = os.environ['JOBPATH']
		self.ui.pathToAsset_lineEdit.setText(self.fileDialog(dialogHome))
	
	#render master browse	
	def renderPblBrowse(self):
		return self.folderDialog(os.environ['MAYARENDERSDIR'])
	
	#render master browse	
	def dailyPblBrowse(self):
		if self.dailyType in ('modeling', 'texturing', 'animation', 'anim', 'fx', 'previs', 'tracking', 'rigging'):
			return self.fileDialog(os.environ['MAYAPLAYBLASTSDIR'])
		elif self.dailyType in ('lighting', 'shading'):
			return self.fileDialog(os.environ['MAYARENDERSDIR'])
		elif self.dailyType == 'comp':
			return self.fileDialog(os.environ['NUKERENDERSDIR'])
		else:
			return self.fileDialog(os.environ['SHOTPATH'])

	#################getting ui options################
	#gets main publish options
	def getMainPblOpts(self):
		self.approved, self.mail = '', ''
		self.pblNotes = self.ui.notes_textEdit.text() #.toPlainText() # Edited line as notes box is now line edit widget, not text edit
		self.pblType = self.getPblTab()[1]
		self.slShot = self.ui.publishToShot_comboBox.currentText()
		#gets path to publish to. if selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.publishToShot_radioButton.isChecked() == 1:
			if self.slShot == os.environ['SHOT']:
				self.pblTo = os.environ['SHOTPUBLISHDIR']
			else:
				self.pblTo = os.path.join(os.environ['JOBPATH'], self.slShot, os.environ["PUBLISHRELATIVEDIR"])
		else:
			self.pblTo = os.environ["JOBPUBLISHDIR"]
		if self.ui.approved_checkBox.checkState() == 2:
			self.approved = True
		if self.ui.mail_checkBox.checkState() == 2:
			self.mail = True

	#gets asset publish options
	def get_maya_assetPblOpts(self, genericAsset=False):
		self.textures, self.subsetName, self.sceneName = '', '', ''
		self.chkLs = [self.pblNotes]
		if self.ui.textures_checkBox.checkState() == 2:
			self.textures = True
		if self.ui.subSet_checkBox.checkState() == 2:
			self.subsetName = '%s_sbs' % self.ui.subSetName_lineEdit.text()
			self.chkLs.append(self.subsetName)
		if self.ui.scenePbl_radioButton.isChecked() == True:
			self.sceneName = self.ui.scenePblName_lineEdit.text()
			self.chkLs.append(self.sceneName)
			
	#gets nuke asset publish options
	def get_nuke_assetPblOpts(self, name=True):
		self.chkLs = [self.pblNotes]
		if name:
			self.pblName = self.ui.nk_PblName_lineEdit.text()
			self.chkLs.append(self.pblName)

	#gets daily publish options
	def getDailyPblOpts(self):
		self.dailyDic = {}
		rowCount = self.ui.dailyPbl_tableWidget.rowCount()
		if rowCount:
			self.dailySeq = self.ui.dailyPbl_tableWidget.item(0, 0).text()
			self.dailyPath = self.ui.dailyPbl_tableWidget.item(0, 1).text()
			self.dailyType = self.ui.dailyPbl_tableWidget.item(0, 2).text()
		else:
			rowCount = None
		self.chkLs = [self.pblNotes, rowCount]
		
	#gets render publish options
	def getRenderPblOpts(self):
		self.renderDic = {}
		self.streamPbl, self.mainLayer = '', ''
		if self.ui.streamPbl_checkBox.checkState() == 2:
			self.streamPbl = True
		rowCount = self.ui.renderPbl_tableWidget.rowCount()
		for row in range(0, rowCount):
			layerName = self.ui.renderPbl_tableWidget.item(row, 0).text()
			filePath = self.ui.renderPbl_tableWidget.item(row, 1).text()
			self.renderDic[layerName] = filePath
			if self.ui.renderPbl_tableWidget.item(row, 2).text() == 'main':
				self.mainLayer = layerName
		if not rowCount:
			rowCount = None
		self.chkLs = [self.pblNotes, rowCount]

	##############intializes publish###################
	def initPublish(self):
		self.getMainPblOpts()
		
		##########MAYA ASSETS PUBLISH############
		#########################################
		if self.pblType == 'ma Asset':

			self.get_maya_assetPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return

			#camera publish
			if self.ui.cameraPbl_radioButton.isChecked() == True:
				import ma_camPbl
				self.camType = self.ui.cameraPbl_comboBox.currentText()
				ma_camPbl.publish(self.pblTo, self.slShot, self.camType, self.pblNotes, self.mail, self.approved)
			#rig publish
			elif self.ui.rigPbl_radioButton.isChecked() == True:
				import ma_rigPbl
				self.rigType = self.ui.rigPbl_comboBox.currentText()
				ma_rigPbl.publish(self.pblTo, self.slShot, self.rigType, self.textures, self.pblNotes, self.mail, self.approved)
			#anim publish
			elif self.ui.animPbl_radioButton.isChecked() == True:
				import ma_animPbl
				ma_animPbl.publish(self.pblTo, self.slShot, self.pblNotes, self.mail, self.approved)
			#fx publish
			elif self.ui.fxPbl_radioButton.isChecked() == True:
				import ma_fxPbl
				ma_fxPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes, self.mail, self.approved)
			#pointCloud publish
			elif self.ui.pointCloudPbl_radioButton.isChecked() == True:
				import ma_pointCloudPbl
				ma_pointCloudPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes, self.mail, self.approved)
			#geoCache publish
			elif self.ui.geoCachePbl_radioButton.isChecked() == True:
				import ma_geoChPbl
				self.geoChType = self.ui.geoCachePbl_comboBox.currentText()
				ma_geoChPbl.publish(self.pblTo, self.slShot, self.geoChType, self.pblNotes, self.mail, self.approved)
			#geo publish
			elif self.ui.geoPbl_radioButton.isChecked() == True:
				import ma_geoPbl
				self.geoType = self.ui.geoPbl_comboBox.currentText()
				ma_geoPbl.publish(self.pblTo, self.slShot, self.geoType, self.textures, self.pblNotes, self.mail, self.approved)
			#model publish
			elif self.ui.modelPbl_radioButton.isChecked() == True:
				import ma_mdlPbl
				self.mdlType = self.ui.modelPbl_comboBox.currentText()
				ma_mdlPbl.publish(self.pblTo, self.slShot, self.mdlType, self.textures, self.pblNotes, self.mail, self.approved)
			#shader publish
			elif self.ui.shaderPbl_radioButton.isChecked() == True:
				import ma_shdPbl
				ma_shdPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes, self.mail, self.approved)
			#node publish
			elif self.ui.nodePbl_radioButton.isChecked() == True:
				import ma_nodePbl
				self.nodeType = self.ui.nodePbl_comboBox.currentText()
				ma_nodePbl.publish(self.pblTo, self.slShot, self.nodeType, self.subsetName, self.textures, self.pblNotes, self.mail, self.approved)
			#scene publish
			elif self.ui.scenePbl_radioButton.isChecked() == True:
				import ma_scnPbl
				ma_scnPbl.publish(self.pblTo, self.slShot, self.sceneName, self.subsetName, self.textures, self.pblNotes, self.mail, self.approved)
			#shot publish
			elif self.ui.shotPbl_radioButton.isChecked() == True:
				import ma_shotPbl
				ma_shotPbl.publish(self.pblTo, self.pblNotes, self.mail, self.approved)
					
			
		##########NUKE ASSETS PUBLISH############
		#########################################		
		if self.pblType == 'nk Asset':

			if self.ui.nk_cardPbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts()
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_setupPbl
				self.pblType = 'card'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes, self.mail, self.approved)

			elif self.ui.nk_pointCloudPbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts()
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_setupPbl
				self.pblType = 'pointCloud'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes, self.mail, self.approved)

			elif self.ui.nk_nodePbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts()
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_setupPbl
				self.pblType = 'node'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes, self.mail, self.approved)

			elif self.ui.nk_compPbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts(name=False)
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_compPbl
				self.pblType = 'comp'
				nk_compPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblNotes, self.mail, self.approved)

			elif self.ui.nk_preCompPbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts()
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_setupPbl
				self.pblType = 'preComp'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes, self.mail, self.approved)

			elif self.ui.nk_setupPbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts()
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_setupPbl
				self.pblType = 'setup'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes, self.mail, self.approved)	
				
						
		#############DAILY PUBLISH##############
		#########################################
		elif self.pblType == 'Daily':
			import ic_dailyPbl;
			self.getDailyPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return
			ic_dailyPbl.publish(self.dailySeq, self.dailyPath, self.dailyType, self.pblTo, self.pblNotes, self.mail)
			
		#############RENDER PUBLISH##############
		#########################################
		elif self.pblType == 'Render':
			import ic_renderPbl
			self.getRenderPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return
			ic_renderPbl.publish(self.renderDic, self.pblTo, self.mainLayer, self.streamPbl, self.pblNotes, self.mail, self.approved)


	##################################################Gather tab####################################################
	################################################################################################################
	#ui adjustments
	def adjustGatherTab(self, showGatherButton = False):
		self.ui.gather_pushButton.setEnabled(False)
		if showGatherButton:
			self.ui.gather_pushButton.setEnabled(True)

	#gets gather from
	def getGatherFrom(self):
		slShot = self.ui.gatherFromShot_comboBox.currentText()
		#gets path to gather from. if selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.gatherFromShot_radioButton.isChecked() == 1:
			if slShot == os.environ['SHOT']:
				self.gatherFrom = os.environ['SHOTPUBLISHDIR']
			else:
				self.gatherFrom = os.path.join(os.environ['JOBPATH'], slShot, os.environ["PUBLISHRELATIVEDIR"])
		else:
			self.gatherFrom = os.environ['JOBPUBLISHDIR']
			
	###################columns system, info and preview img update##################
	#defines columns to shorten name
	def defineColumns(self):
		self.aTypeCol = self.ui.assetType_listWidget
		self.aNameCol = self.ui.assetName_listWidget
		self.aSubTypeCol = self.ui.assetSubType_listWidget
		self.aVersionCol = self.ui.assetVersion_listWidget

	#clears columns
	def clearColumn(self, column):
		for i in range(0, column.count()):
			column.takeItem(0)
	
	#returns a list of items to display in gather based on running environment
	def getAssetEnvPrefix(self):
		if os.environ['ICARUSENVAWARE'] == 'MAYA':
			return ('ma', 'ic')
		elif os.environ['ICARUSENVAWARE'] == 'NUKE':
			return ('nk', 'ic', 'render')
		else:
			return ('ma', 'nk', 'ic', 'render', 'daily')
		
	#populates columns
	def fillColumn(self, column, searchPath):
		envPrefix = self.getAssetEnvPrefix()
		itemLs = os.listdir(searchPath); itemLs.sort()
		#making in progress publishes not visible
		if column == self.aVersionCol:
			for item in itemLs:
				if os.path.isdir(os.path.join(searchPath, item)):
					if 'in_progress.tmp' in os.listdir(os.path.join(searchPath, item)):
						itemLs.remove(item)
			#reversing order to facilitate user gather
			itemLs.reverse()
		if column == self.aTypeCol:
			for item in itemLs:
				if item[:2] in envPrefix or item in envPrefix:
					column.addItem(item)
		else:
			for item in itemLs:
				if not item.startswith('.'):
					column.addItem(item)
	
	#adjust UI columns to accodmodate assetSubType column
	def adjustColumns(self):
		#checks for versioned items inside assetName folder. If not found displays subset column
		self.getGatherFrom()
		self.assetName = self.aNameCol.currentItem().text()
		vItemsPath = os.path.join(self.gatherFrom, self.assetType, self.assetName)
		if not pblChk.versionedItems(vItemsPath, vb=False):
			self.subType = True
			self.ui.assetSubType_listWidget.show()
			self.updateAssetSubTypeCol()
		else:
			self.subType = None
			self.ui.assetSubType_listWidget.hide()
			self.updateAssetVersionCol()

	#updates assetType column
	def updateAssetTypeCol(self):
		self.getGatherFrom()
		self.adjustGatherTab()
		self.clearColumn(self.aTypeCol)
		self.clearColumn(self.aNameCol)
		self.clearColumn(self.aSubTypeCol)
		self.clearColumn(self.aVersionCol)
		self.ui.gatherInfo_textEdit.setText('')
		self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		self.fillColumn(self.aTypeCol, self.gatherFrom)
	
	#updates assetName column
	def updateAssetNameCol(self):
		self.adjustGatherTab()
		self.assetType = self.aTypeCol.currentItem().text()
		self.clearColumn(self.aNameCol)
		self.clearColumn(self.aSubTypeCol)
		self.clearColumn(self.aVersionCol)
		self.ui.gatherInfo_textEdit.setText('')
		self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType)
		self.fillColumn(self.aNameCol, searchPath)

	#updates assetSubType column
	def updateAssetSubTypeCol(self):
		self.adjustGatherTab()
		self.clearColumn(self.aSubTypeCol)
		self.clearColumn(self.aVersionCol)
		self.ui.gatherInfo_textEdit.setText('')
		self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType, self.assetName)
		self.fillColumn(self.aSubTypeCol, searchPath)

	#updates assetVersion column
	def updateAssetVersionCol(self):
		self.adjustGatherTab()
		self.clearColumn(self.aVersionCol)
		if self.subType:
			self.assetSubType = self.aSubTypeCol.currentItem().text()
		else:
			self.assetSubType = ''
		self.ui.gatherInfo_textEdit.setText('')
		self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType)
		self.fillColumn(self.aVersionCol, searchPath)

	#updates infoField with notes 
	def updateInfoField(self):
		self.adjustGatherTab(showGatherButton = True)
		self.assetVersion = self.aVersionCol.currentItem().text()
		self.gatherPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType, self.assetVersion)
		sys.path.append(self.gatherPath)
		import icData; reload(icData)
		sys.path.remove(self.gatherPath)
		self.ui.gatherInfo_textEdit.setText(icData.notes)

	#updates image preview field with snapshot 
	def updateImgPreview(self):
		import previewImg
		imgPath = ''
		self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		if self.previewPlayer:
			imgPath = previewImg.getImg(self.gatherPath, forceExt='mov')
			if imgPath:
					self.previewPlayerCtrl(hide=True)
					pixmap = QtGui.QPixmap(None)
					self.ui.gatherImgPreview_label.setPixmap(pixmap)
					self.previewPlayerCtrl(loadImg=imgPath)
					self.previewPlayerCtrl(show=True)
					self.previewPlayerCtrl(play=True)
		if not imgPath or not self.previewPlayer:
			imgPath = previewImg.getImg(self.gatherPath, forceExt='jpg')
			if imgPath:
				self.previewPlayerCtrl(hide=True)
				pixmap = QtGui.QPixmap(None)
				self.ui.gatherImgPreview_label.setPixmap(pixmap)
				pixmap = QtGui.QPixmap(imgPath)
				self.ui.gatherImgPreview_label.setScaledContents(True)
				self.ui.gatherImgPreview_label.setPixmap(pixmap)		

	##################intializes gather################
	def initGather(self):
		if os.environ['ICARUSENVAWARE'] == 'MAYA':
			if self.assetType == 'ma_anim':
				import ma_animGather
				ma_animGather.gather(self.gatherPath)
			else:
				import ma_assetGather
				ma_assetGather.gather(self.gatherPath)
		elif os.environ['ICARUSENVAWARE'] == 'NUKE':
			if self.assetType in ('ic_geo', 'ic_pointCloud') :
				import nk_geoGather
				nk_geoGather.gather(self.gatherPath)
			elif self.assetType == 'render':
				import nk_renderGather
				app.hide()
				nk_renderGather.gather(self.gatherPath)
				app.show()
			else:
				import nk_assetGather
				nk_assetGather.gather(self.gatherPath)


##############################RUNS ICARUS WITH ENVIRONMENT AWARENESS##############################
##################################################################################################
#version verbosity
verbose.icarusLaunch(os.environ['ICARUSVERSION'], os.environ['ICWORKINGDIR']) #os.environ['PIPELINE'])

#detecting environment and runnig application
if os.environ['ICARUSENVAWARE'] == 'MAYA' or os.environ['ICARUSENVAWARE'] == 'NUKE':
	app = icarusApp()

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	#setting qt windows flags based on running OS
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
	else:
		app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

	#centering window
	app.move(QtGui.QDesktopWidget().availableGeometry(1).center() - app.frameGeometry().center())
	app.show()

#CLARISSE ENV - Waiting until clarisse purchase
#elif os.environ['ICARUSENVAWARE'] == 'CLARISSE':
#	import clarisse_icarusEventLoop
#	try:
#	    mainApp = QtGui.QApplication('Icarus')
#	except RuntimeError:
#	    mainApp = QtCore.QCoreApplication.instance()
#	app = icarusApp()
#	app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint)
#	app.show()
#	icarus_clarisseWrap.exec_(mainApp)
	
else:
	if __name__ == '__main__':
		mainApp = QtGui.QApplication(sys.argv)
		mainApp.setApplicationName('Icarus')

		# Apply UI style sheet
		qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
		with open(qss, "r") as fh:
			mainApp.setStyleSheet(fh.read())

		app = icarusApp()

		#passing window flags
		app.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

		#centering window
		app.move(QtGui.QDesktopWidget().availableGeometry(1).center() - app.frameGeometry().center())

		app.show()
		sys.exit(app.exec_())
