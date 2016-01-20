#!/usr/bin/python

# [Icarus] icarus__main__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Launches and controls the Icarus main UI.


from PySide import QtCore, QtGui
from PySide.QtGui import QStyleFactory
from icarusUI import *
import os, sys, env__init__


#initializing icarus environment and adding libs to sysPath
env__init__.setEnv()

#note: publish modules are imported on demand rather than all at once at beggining of file
import launchApps, setJob, userPrefs, verbose, pblChk, pblOptsPrc, openDirs, jobs #, setTerm, listShots
import sequence as seq


class icarusApp(QtGui.QDialog):
	def __init__(self, parent = None):
		super(icarusApp, self).__init__(parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Read user prefs config file file - if it doesn't exist it will be created
		userPrefs.read()

	#	# Define Phonon as preview player if Icarus is standalone
	#	# (only enabled on Mac OS X as haven't yet figured out how to get Phonon video player working properly on Windows or Linux)
	#	if os.environ['ICARUSENVAWARE'] == 'STANDALONE' and os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
	#		from PySide.phonon import Phonon
	#		self.previewPlayer = Phonon.VideoPlayer(parent = self.ui.gatherImgPreview_label)
	#	else:
	#		self.previewPlayer = None

		# Set up keyboard shortcuts
		self.shortcutShotInfo = QtGui.QShortcut(self)
		self.shortcutShotInfo.setKey('Ctrl+I')
		self.shortcutShotInfo.activated.connect(self.printShotInfo)

		# Connect signals & slots
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

		#QtCore.QObject.connect(self.ui.renderPblAdd_pushButton, QtCore.SIGNAL('clicked()'), self.renderTableAdd)
		#QtCore.QObject.connect(self.ui.renderPblRemove_pushButton, QtCore.SIGNAL('clicked()'), self.renderTableRm)
		#QtCore.QObject.connect(self.ui.renderPblSetMain_pushButton, QtCore.SIGNAL('clicked()'), self.setLayerAsMain)
		self.ui.renderPblAdd_pushButton.clicked.connect(self.renderTableAdd)
		self.ui.renderPblRemove_pushButton.clicked.connect(self.renderTableRemove)
		#self.ui.renderPblRevert_pushButton.clicked.connect(self.renderTableClear)
		self.ui.renderPbl_treeWidget.itemDoubleClicked.connect(self.renderPreview)

		QtCore.QObject.connect(self.ui.dailyPblType_comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), self.setDailyType)
		QtCore.QObject.connect(self.ui.dailyPblAdd_pushButton, QtCore.SIGNAL('clicked()'), self.dailyTableAdd)
		QtCore.QObject.connect(self.ui.publish_pushButton, QtCore.SIGNAL('clicked()'), self.initPublish)
		QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL('currentChanged(int)'), self.adjustMainUI)
		QtCore.QObject.connect(self.ui.about_toolButton, QtCore.SIGNAL('clicked()'), self.about)

		self.ui.minimise_checkBox.stateChanged.connect(self.setMinimiseOnAppLaunch)

		# Set minimise on launch checkbox
		self.boolMinimiseOnAppLaunch = userPrefs.config.getboolean('main', 'minimiseonlaunch')
		self.ui.minimise_checkBox.setChecked(self.boolMinimiseOnAppLaunch)

	########################################Adding right click menus to buttons#######################################
	##################################################################################################################
		#Nuke
		self.ui.nuke_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionNuke = QtGui.QAction("Nuke", None)
		self.actionNuke.triggered.connect(self.launchNuke)
		self.ui.nuke_pushButton.addAction(self.actionNuke)
		self.actionNukeX = QtGui.QAction("NukeX", None)
		self.actionNukeX.triggered.connect(self.launchNukeX)
		self.ui.nuke_pushButton.addAction(self.actionNukeX)
	#	self.actionNukeStudio = QtGui.QAction("NukeStudio", None)
	#	self.actionNukeStudio.triggered.connect(self.launchNukeStudio)
	#	self.ui.nuke_pushButton.addAction(self.actionNukeStudio)
		# [removed NukeStudio Launcher until properly supported in Icarus]

		#Review
		self.ui.openReview_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionHieroPlayer = QtGui.QAction("HieroPlayer", None)
		self.actionHieroPlayer.triggered.connect(self.launchHieroPlayer)
		self.ui.openReview_pushButton.addAction(self.actionHieroPlayer)
		self.actionDjv = QtGui.QAction("djv_view", None)
		self.actionDjv.triggered.connect(self.launchDjv)
		self.ui.openReview_pushButton.addAction(self.actionDjv)

		#Browse
		self.ui.browse_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionOpenShot = QtGui.QAction("Shot", None)
		self.actionOpenShot.triggered.connect(openDirs.openShot)
		self.ui.browse_pushButton.addAction(self.actionOpenShot)
		self.actionOpenJob = QtGui.QAction("Job", None)
		self.actionOpenJob.triggered.connect(openDirs.openJob)
		self.ui.browse_pushButton.addAction(self.actionOpenJob)

		#Render
		self.ui.render_pushButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
		self.actionDeadlineMonitor = QtGui.QAction("Deadline Monitor", None)
		self.actionDeadlineMonitor.triggered.connect(self.launchDeadlineMonitor)
		self.ui.render_pushButton.addAction(self.actionDeadlineMonitor)
		self.actionDeadlineSlave = QtGui.QAction("Deadline Slave", None)
		self.actionDeadlineSlave.triggered.connect(self.launchDeadlineSlave)
		self.ui.render_pushButton.addAction(self.actionDeadlineSlave)
		self.actionSubmitLocal = QtGui.QAction("Submit Maya command-line render (local)", None)
		self.actionSubmitLocal.triggered.connect(self.launchSubmitRender)
		self.ui.render_pushButton.addAction(self.actionSubmitLocal)

		# About menu
	#	self.ui.about_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
	#	self.actionAbout = QtGui.QAction("About", None)
	#	self.actionAbout.triggered.connect(self.about)
	#	self.ui.about_toolButton.addAction(self.actionAbout)
	#	self.actionPrefs = QtGui.QAction("User Preferences", None)
	#	self.actionPrefs.triggered.connect(self.userSettings)
	#	self.ui.about_toolButton.addAction(self.actionPrefs)

	##########################################UI adapt environment awareness##########################################
	##################################################################################################################
		self.jobMngTab = self.ui.tabWidget.widget(0)
		self.publishTab = self.ui.tabWidget.widget(1)
		self.gatherTab = self.ui.tabWidget.widget(2)
		self.publishAssetTab = self.ui.publishType_tabWidget.widget(0)
		self.publishRenderTab = self.ui.publishType_tabWidget.widget(1)


		###########STANDALONE ENVIRONMENT#############
		##############################################
		if os.environ['ICARUSENVAWARE'] == 'STANDALONE':
			#hides ui items relating to maya environment
			uiHideLs = ['setNewShot_pushButton', 'shotEnv_toolButton', 'appIcon_label'] # Removed 'shotEnv_label_maya', 
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
					if entryLs[1]:
						shotLs = setJob.listShots(entryLs[0])
						if entryLs[1] in shotLs:
							self.ui.shot_comboBox.setCurrentIndex(self.ui.shot_comboBox.findText(entryLs[1]))

			#deletes all tabs but jobMng
			for i in range(0, self.ui.tabWidget.count()-1):
				self.ui.tabWidget.removeTab(1)
			#deletes Asset, NK Asset publish tabs
			for i in range(0,2):
				self.ui.publishType_tabWidget.removeTab(0)

			# Apply job/shot settings pop-up menu to shotEnv label (only in standalone mode)
			self.ui.shotEnv_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

			self.actionJobSettings = QtGui.QAction("Job Settings...", None)
			self.actionJobSettings.triggered.connect(self.jobSettings)
			self.ui.shotEnv_toolButton.addAction(self.actionJobSettings)

			self.actionShotSettings = QtGui.QAction("Shot Settings...", None)
			self.actionShotSettings.triggered.connect(self.shotSettings)
			self.ui.shotEnv_toolButton.addAction(self.actionShotSettings)

			self.ui.shotEnv_toolButton.setEnabled(True)


		##############MAYA ENVIRONMENT################
		##############################################
		elif os.environ['ICARUSENVAWARE'] == 'MAYA':
			pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_maya.png")
			self.ui.appIcon_label.setPixmap(pixmap)
			uiHideLs = ['assetSubType_listWidget', 'ma_assetTypes_listWidget'] # Removed 'icarusBanner', 
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
			pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_nuke.png")
			self.ui.appIcon_label.setPixmap(pixmap)
			uiHideLs = ['assetSubType_listWidget', 'nk_assetTypes_listWidget'] # Removed 'icarusBanner', 
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

	#	self.ui.dailyPbl_tableWidget.cellDoubleClicked.connect(self.cell_was_clicked)

		#QtCore.QObject.connect(self.ui.assetType_listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.updateAssetNameCol)
		#QtCore.QObject.connect(self.ui.assetName_listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.adjustColumns)
		#QtCore.QObject.connect(self.ui.assetSubType_listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.updateAssetVersionCol)
		#QtCore.QObject.connect(self.ui.assetVersion_listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.updateInfoField)
		#QtCore.QObject.connect(self.ui.assetVersion_listWidget, QtCore.SIGNAL('currentItemChanged(QListWidgetItem *, QListWidgetItem *)'), self.updateImgPreview)

		#self.ui.assetType_listWidget.currentItemChanged.connect(self.updateAssetNameCol)
		#self.ui.assetName_listWidget.currentItemChanged.connect(self.adjustColumns)
		#self.ui.assetSubType_listWidget.currentItemChanged.connect(self.updateAssetVersionCol)
		#self.ui.assetVersion_listWidget.currentItemChanged.connect(self.updateInfoField)
		#self.ui.assetVersion_listWidget.currentItemChanged.connect(self.updateImgPreview)
		
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


	def fileDialog(self, dialogHome):
		""" Opens a dialog from which to select a single file.
			The env check puts the main window in the background so dialog pop up can return properly when running inside certain applications.
			The window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env.
		"""
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


	def folderDialog(self, dialogHome):
		""" Opens a dialog from which to select a folder.
			The env check puts the main window in the background so dialog pop up can return properly when running inside certain applications.
			The window flags bypass a mac bug that made the dialog always appear under the Icarus window. This is ignored in a Linux env.
		"""
		envOverride = ['MAYA', 'NUKE']
		if os.environ['ICARUSENVAWARE'] in envOverride:
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnBottomHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
			dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)
			if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				app.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowCloseButtonHint)
				app.show()
		else:
			dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)

		return dialog


	##############################################Job management tab##############################################
	##############################################################################################################

	def populateShots(self):
		""" Populates shot drop down menu.
		"""
		# Remove all items
		for shot in range(0, self.ui.shot_comboBox.count(), 1):
			self.ui.shot_comboBox.removeItem(0)

		selJob = self.ui.job_comboBox.currentText()
		shotLs = setJob.listShots(selJob)

		# Add shots...
		if shotLs:
			for shot in shotLs:
				self.ui.shot_comboBox.insertItem(0, shot)

			# Try to set current item in combo box to the current shot 
			try:
				index = self.ui.shot_comboBox.findText(self.shot)
			except AttributeError:
				index = 0

			if 0 <= index < len(shotLs):
				self.ui.shot_comboBox.setCurrentIndex(index)
			else:
				self.ui.shot_comboBox.setCurrentIndex(0)

			self.ui.shot_comboBox.setEnabled(True)
			self.ui.setShot_label.setEnabled(True)
			self.ui.setShot_pushButton.setEnabled(True)

		# No shots detected...
		else:
			self.ui.shot_comboBox.insertItem(0, '[None]')
			self.ui.shot_comboBox.setEnabled(False)
			self.ui.setShot_label.setEnabled(False)
			self.ui.setShot_pushButton.setEnabled(False)


	#populates publish shot drop down menu	
	def populatePblShotLs(self):
		self.ui.publishToShot_comboBox.clear()
		shotLs = setJob.listShots(os.environ['JOB'])
		if shotLs:
			for shot in shotLs:
				self.ui.publishToShot_comboBox.insertItem(0, shot)
			self.ui.publishToShot_comboBox.setCurrentIndex(self.ui.publishToShot_comboBox.findText(os.environ['SHOT']))
	
	#populates gather shot drop down menu	
	def populateGatherShotLs(self):
		self.ui.gatherFromShot_comboBox.clear()
		shotLs = setJob.listShots(os.environ['JOB'])
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
		if setJob.setup(self.job, self.shot):
			self.adjustPblTypeUI()
			self.populatePblShotLs()
			self.populateGatherShotLs()
			self.connectNewSignalsSlots()
			self.lockJobUI()
		else:
			verbose.defaultJobSettings()
			#print "Unable to load job settings. Default values have been applied.\nPlease review the settings in the editor and click Save when done."
			if self.openSettings("Job", autoFill=True):
				self.setupJob()


	def lockJobUI(self):
		""" Updates and locks UI job tab.
		"""
		self.updateJobLabel()
		self.ui.shotSetup_groupBox.setEnabled(False)
		self.ui.launchApp_groupBox.setEnabled(True)
		self.ui.launchOptions_groupBox.setEnabled(True)
		self.ui.tabWidget.insertTab(1, self.publishTab, 'Publish')
		self.ui.tabWidget.insertTab(2, self.gatherTab, 'Assets')
		self.ui.gather_pushButton.hide()
		self.ui.setShot_pushButton.hide()
		self.ui.shotEnv_toolButton.show()
		self.ui.setNewShot_pushButton.show()
		verbose.jobSet(self.job, self.shot)


	def unlockJobUI(self):
		""" Unlocks UI if 'Set New Shot' is clicked.
		"""
		# Re-scan for shots
		self.populateShots()

		self.ui.shotSetup_groupBox.setEnabled(True)
		self.ui.launchApp_groupBox.setEnabled(False)
		self.ui.launchOptions_groupBox.setEnabled(False)

		# Remove publish and assets tab
		self.ui.tabWidget.removeTab(1); self.ui.tabWidget.removeTab(1)
	#	for row in range(self.ui.renderPbl_tableWidget.rowCount()):
	#		self.ui.renderPbl_tableWidget.removeRow(0)
	#	self.ui.renderPbl_tableWidget.clearContents()
		self.ui.renderPbl_treeWidget.clear() # clear the render layer tree view widget
		self.ui.dailyPbl_tableWidget.removeRow(0)
		self.ui.dailyPbl_tableWidget.clearContents()
		self.ui.shotEnv_toolButton.setText('')
		self.ui.shotEnv_toolButton.hide()
		self.ui.setNewShot_pushButton.hide()
		self.ui.setShot_pushButton.show()


#	#controls phonon preview player
#	def previewPlayerCtrl(self, show=False, hide=False, play=False, loadImg=None):
#		if self.previewPlayer:
#			if show:
#				self.previewPlayer.show()
#			elif hide:
#				self.previewPlayer.hide()
#			elif play:
#				self.previewPlayer.play()
#			elif loadImg:
#				self.previewPlayer.load(loadImg)


	def updateJobLabel(self):
		""" Updates job label tool button with the current job and shot.
		"""
		if os.environ['ICARUSENVAWARE'] != 'STANDALONE':
			self.job = os.environ['JOB']
			self.shot = os.environ['SHOT']
		self.ui.shotEnv_toolButton.setText('%s - %s' % (self.job, self.shot))


	def setMinimiseOnAppLaunch(self, state):
		""" Sets state of minimise on app launch variable.
			Ultimately, this option should form part of a 'User Prefs' dialog, and be removed from the main UI.
		"""
		if state == QtCore.Qt.Checked:
			self.boolMinimiseOnAppLaunch = True
			userPrefs.edit('main', 'minimiseonlaunch', 'True')
			#print "Minimise on launch enabled"
		else:
			self.boolMinimiseOnAppLaunch = False
			userPrefs.edit('main', 'minimiseonlaunch', 'False')
			#print "Minimise on launch disabled"


	def printShotInfo(self):
		""" Print job / shot information stored in enviroment variables - used for debugging
		"""
		try:
			print """
     Job/Shot: %s - %s

  Frame range: %s
      Handles: %s

   Resolution: %s (full)
               %s (proxy)

 Linear units: %s
Angular units: %s
   Time units: %s (%s fps)
""" %(os.environ['JOB'], os.environ['SHOT'],
      os.environ['FRAMERANGE'],
      os.environ['HANDLES'],
      os.environ['RESOLUTION'],
      os.environ['PROXY_RESOLUTION'],
      os.environ['UNIT'],
      os.environ['ANGLE'],
      os.environ['TIMEFORMAT'], os.environ['FPS'])
		except KeyError:
			print "Environment variable(s) not set."


	def about(self):
		""" Show about dialog
		"""
		import PySide.QtCore
		python_ver_str = "%d.%d.%d" %(sys.version_info[0], sys.version_info[1], sys.version_info[2])
		pyside_ver_str = PySide.__version__
		qt_ver_str = PySide.QtCore.qVersion()

		about_msg = """
I   C   A   R   U   S

%s

Python %s / PySide %s / Qt %s / %s
Environment: %s

(c) 2013-2016 Gramercy Park Studios
""" %(os.environ['ICARUSVERSION'], python_ver_str, pyside_ver_str, qt_ver_str, os.environ['ICARUS_RUNNING_OS'], os.environ['ICARUSENVAWARE'])

		import about
		about = about.aboutDialog()
		about.msg(about_msg)


	def openSettings(self, settingsType, autoFill=False):
		""" Open settings dialog
		"""
		if settingsType == "Job":
			categoryLs = ['job', 'time', 'resolution', 'units', 'apps', 'other']
			xmlData = os.path.join(os.environ['JOBDATA'], 'jobData.xml')
		elif settingsType == "Shot":
			categoryLs = ['time', 'resolution', 'units', 'camera']
			xmlData = os.path.join(os.environ['SHOTDATA'], 'shotData.xml')
		elif settingsType == "User":
			categoryLs = ['user', ]
			xmlData = os.path.join(os.environ['ICUSERPREFS'], 'userPrefs.xml')
		import job_settings__main__
		reload(job_settings__main__)
		settingsEditor = job_settings__main__.settingsDialog(settingsType=settingsType, categoryLs=categoryLs, xmlData=xmlData, autoFill=autoFill)
		@settingsEditor.customSignal.connect
		def storeAttr(attr):
			settingsEditor.currentAttr = attr # a bit hacky - need to find a way to add this function to main class
		settingsEditor.show()
		settingsEditor.exec_()
		return settingsEditor.returnValue # return True if user clicked Save, False for Cancel


	def jobSettings(self):
		""" Open job settings dialog wrapper function
		"""
		if self.openSettings("Job"):
			setJob.setup(self.job, self.shot) # Set up environment variables


	def shotSettings(self):
		""" Open shot settings dialog wrapper function
		"""
		if self.openSettings("Shot"):
			setJob.setup(self.job, self.shot) # Set up environment variables


	def userSettings(self):
		""" Open user settings dialog wrapper function
		"""
		if self.openSettings("User"):
			pass


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

	#runs launch nuke studio procedure
	def launchNukeStudio(self):
		launchApps.nuke(nukeType='NukeStudio')
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

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
	#	self.ui.openTerminal_pushButton.setEnabled(False)
	#	self.ui.setNewShot_pushButton.setEnabled(False)
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#Launches HieroPlayer with and tries to load the job Hrox automatically
	def launchHieroPlayer(self):
		launchApps.hieroPlayer()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	# Launches djv_view
	def launchDjv(self):
		launchApps.djv()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	# Preview - opens djv_view to preview movie or image sequence
	def preview(self, path=None):
		import djvOps
		verbose.launchApp('djv_view')
		if path is None:
			djvOps.viewer(self.gatherPath) # this is purely a bodge for asset browser - fix at a later date
		else:
			djvOps.viewer(path)

	#Launches Deadline Monitor
	def launchDeadlineMonitor(self):
		launchApps.deadlineMonitor()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#Launches Deadline Slave
	def launchDeadlineSlave(self):
		launchApps.deadlineSlave()
		if self.boolMinimiseOnAppLaunch:
			self.showMinimized()

	#Launches GPS command-line render script
	def launchSubmitRender(self):
		import submit__main__
		reload(submit__main__)
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
		
#	#populates the render publish table
#	def renderTableAdd(self):
#		#processes latest path added to self.renderPaths
#		renderPath = self.renderPblBrowse()
#		renderPath = renderPath.replace(os.environ['SHOTPATH'], '$SHOTPATH')
#		renderDic = {}
#		if renderPath:
#			renderDic = pblOptsPrc.renderPath_prc(renderPath)
#		if renderDic:
#			autoMainLayer = None
#			for layer in renderDic.keys():
#				layerPath = renderDic[layer]
#				layerItem = QtGui.QTableWidgetItem(layer)
#				pathItem = QtGui.QTableWidgetItem(layerPath)
#				mainItem = QtGui.QTableWidgetItem()
#				#check if layers already exist
#				layerChk = True
#				rowCount = self.ui.renderPbl_tableWidget.rowCount()
#				for row in range(0, rowCount):
#					if layer == self.ui.renderPbl_tableWidget.item(row, 0).text():
#						layerChk = False
#						break
#				#adding items and locking table
#				if layerChk:
#					newRow = self.ui.renderPbl_tableWidget.insertRow(0)
#					self.ui.renderPbl_tableWidget.setItem(0, 0, layerItem)
#					layerItem.setFlags(~QtCore.Qt.ItemIsEditable)
#					self.ui.renderPbl_tableWidget.setItem(0, 1, pathItem)
#					pathItem.setFlags(~QtCore.Qt.ItemIsEditable)
#					self.ui.renderPbl_tableWidget.setItem(0, 2, mainItem)
#					mainItem.setFlags(~QtCore.Qt.ItemIsEditable)
#					mainItem.setText('layer')
#					self.ui.renderPbl_tableWidget.resizeColumnsToContents()
#					#making layer main if autoDetected
#					if layer == 'main':
#						autoMainLayer = layerItem
#						self.setLayerAsMain(autoMainLayer)
#					elif layer in ('masterLayer', 'master', 'beauty'):
#						if not autoMainLayer:
#							autoMainLayer = layerItem
#							self.setLayerAsMain(autoMainLayer)

#	#removes items from the render table
#	def renderTableRm(self):
#		rmRowLs = []
#		for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
#			selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
#			selRow = self.ui.renderPbl_tableWidget.row(selItem)
#			if selRow not in rmRowLs:
#				rmRowLs.append(selRow)
#		rmRowLs = sorted(rmRowLs, reverse=True)
#		for rmRow in rmRowLs:
#			self.ui.renderPbl_tableWidget.removeRow(rmRow)
	
#	#sets the selected render layer as the main layer
#	def setLayerAsMain(self, autoMainLayer=None):
#		font = QtGui.QFont()
#		for rowItem in range(0, self.ui.renderPbl_tableWidget.rowCount()):
#			font.setBold(False)
#			mainItem = self.ui.renderPbl_tableWidget.item(rowItem, 2)
#			mainItem.setText('layer')
#			mainItem.setFont(font)
#			#mainItem.setBackground(QtGui.QColor(34,34,34))
#			rowItem1 = self.ui.renderPbl_tableWidget.item(rowItem, 1)
#			rowItem1.setFont(font)
#			#rowItem1.setBackground(QtGui.QColor(34,34,34))
#			rowItem0 = self.ui.renderPbl_tableWidget.item(rowItem, 0)
#			rowItem0.setFont(font)
#			#rowItem0.setBackground(QtGui.QColor(34,34,34))
#		rowLs = []
#		if autoMainLayer:
#			selRow = self.ui.renderPbl_tableWidget.row(autoMainLayer)
#			rowLs.append(selRow)
#		else:
#			for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
#				selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
#				selRow = self.ui.renderPbl_tableWidget.row(selItem)
#				if selRow not in rowLs and selRow != -1:
#					rowLs.append(selRow)
#		if len(rowLs) == 1:
#			font.setBold(True)
#			mainItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 2)
#			mainItem.setText('main')
#			mainItem.setFont(font)
#			#mainItem.setBackground(QtGui.QColor(60,75,40))
#			passItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 1)
#			passName = passItem.text()
#			passItem.setFont(font)
#			#passItem.setBackground(QtGui.QColor(60,75,40))
#			layerItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 0)
#			layerName = passItem.text()
#			layerItem.setFont(font)
#			#layerItem.setBackground(QtGui.QColor(60,75,40))
#		#app hide and show forces thw window to update
#	#	app.hide()
#	#	app.show() # This was causing an issue with the UI closing so I've commented it out fot the time being. The widget still seems to auto update.


	def renderPreview(self, item, column):
		""" Launches sequence viewer when entry is double-clicked.
		"""
		#print item.text(column), column
		path = seq.getFirst( item.text(3) )
		#path = seq.getFirst( self.absolutePath(item.text(3)) )
		#print path
		#djvOps.viewer(path)
		self.preview(path)


#	def cell_was_clicked(self, row, column):
#		""" TEMPORARY FUNCTION - catches double-click signal on dailies table and launches sequence in viewer
#		"""
#		item = self.ui.dailyPbl_tableWidget.itemAt(row, column)
#		print("Row %d and column %d was clicked: %s" % (row, column, item.text()))
#		#self.ID = item.text()
#		self.preview(self.previewPath)


	def renderTableUpdate(self):
		""" Populates the render layer tree view widget with entries.
		"""
		renderPath = self.renderPath
		if renderPath:
			renderLayerDirs = next(os.walk(renderPath))[1] # get subdirectories
			if renderLayerDirs:
				renderLayerDirs.sort()
			else: # use parent dir
				renderLayerDirs = [os.path.basename(renderPath)]
				renderPath = os.path.dirname(renderPath)
			#print renderPath, renderLayerDirs

			# Add render layers
			for renderLayerDir in renderLayerDirs:
				renderPasses = seq.getBases(os.path.join(renderPath, renderLayerDir))

				if renderPasses: # only continue if render pass sequences exist in this directory
					renderLayerItem = QtGui.QTreeWidgetItem(self.ui.renderPbl_treeWidget)
					renderLayerItem.setText(0, '%s (%d)' % (renderLayerDir, len(renderPasses)))
					renderLayerItem.setText(2, 'layer')
					renderLayerItem.setText(3, os.path.join(renderPath, renderLayerDir))
					#renderLayerItem.setText(3, self.relativePath(os.path.join(renderPath, renderLayerDir)))
					self.ui.renderPbl_treeWidget.addTopLevelItem(renderLayerItem)
					renderLayerItem.setExpanded(True)

					# Add render passes
					for renderPass in renderPasses:
						renderPassItem = QtGui.QTreeWidgetItem(renderLayerItem)
						path, prefix, fr_range, ext, num_frames = seq.getSequence( os.path.join(renderPath, renderLayerDir), renderPass )
						renderPassItem.setText(0, prefix)
						renderPassItem.setText(1, fr_range)
						if not fr_range == os.environ['FRAMERANGE']: # set red text for sequence mismatch
							renderPassItem.setForeground(1, QtGui.QBrush(QtGui.QColor("#c33")))
						renderPassItem.setText(2, ext.split('.', 1)[1])
						#renderPassItem.setText(3, path)
						renderPassItem.setText(3, os.path.join(renderPath, renderLayerDir, renderPass))
						#renderPassItem.setText(3, self.relativePath(os.path.join(renderPath, renderLayerDir, renderPass)))
						self.ui.renderPbl_treeWidget.addTopLevelItem(renderPassItem)

			# Resize columns
			self.ui.renderPbl_treeWidget.resizeColumnToContents(0)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(1)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(2)


	def renderTableAdd(self):
		""" Adds entries to the render layer tree view widget.
		"""
		self.renderPath = self.folderDialog(os.environ['MAYARENDERSDIR'])
		self.renderTableUpdate()


	def renderTableRemove(self):
		""" Removes the selected entry from the render layer tree view widget.
			TODO: allow passes to be removed as well as layers.
		"""
		for item in self.ui.renderPbl_treeWidget.selectedItems():
			self.ui.renderPbl_treeWidget.takeTopLevelItem( self.ui.renderPbl_treeWidget.indexOfTopLevelItem(item) )


	def dailyTableAdd(self):
		""" Populates the dailies publish table.
		"""
		# Parse the file path
		dailyPath = self.dailyPblBrowse() # dailyPath is a full path to a file
	#	dailyDic = {}
		if dailyPath:
			dailyPath = dailyPath.replace('\\', '/') # Ensure backslashes from Windows paths are changed to forward slashes
			self.previewPath = dailyPath
			seqDir = dailyPath.replace(os.environ['SHOTPATH'].replace('\\', '/'), '$SHOTPATH') # Change to relative path
			seqDir = os.path.dirname(seqDir)
			#dailyDic = pblOptsPrc.dailyPath_prc(dailyPath)
			seqName, seqRange = seq.detectSeq(dailyPath)
			#if dailyDic:
			if seqName:
				#seqName = dailyDic.keys()[0]
				#seqName = os.path.basename(dailyPath)

				nameItem = QtGui.QTableWidgetItem(seqName)
				rangeItem = QtGui.QTableWidgetItem(seqRange)
				typeItem = QtGui.QTableWidgetItem(self.dailyType)
				pathItem = QtGui.QTableWidgetItem(seqDir)
				# Delete existing entry
				self.ui.dailyPbl_tableWidget.removeRow(0)
				# Add new entries and lock table
				newRow = self.ui.dailyPbl_tableWidget.insertRow(0)
				self.ui.dailyPbl_tableWidget.setItem(0, 0, nameItem)
				nameItem.setFlags(~QtCore.Qt.ItemIsEditable)
				self.ui.dailyPbl_tableWidget.setItem(0, 1, rangeItem)
				rangeItem.setFlags(~QtCore.Qt.ItemIsEditable)
				self.ui.dailyPbl_tableWidget.setItem(0, 2, typeItem)
				typeItem.setFlags(~QtCore.Qt.ItemIsEditable)
				self.ui.dailyPbl_tableWidget.setItem(0, 3, pathItem)
				pathItem.setFlags(~QtCore.Qt.ItemIsEditable)
				#pathItem.setText(self.dailyType)
				self.ui.dailyPbl_tableWidget.resizeColumnsToContents()

			else:
				verbose.noSeq(os.path.basename(dailyPath))
				self.ui.dailyPbl_tableWidget.removeRow(0)


	def setDailyType(self):
		""" Sets the dailies type and locks/unlocks the add and remove button accordingly.
		"""
		self.dailyType = self.ui.dailyPblType_comboBox.currentText()

		if self.dailyType:
			self.ui.dailyPblAdd_pushButton.setEnabled(True)
		else:
			self.ui.dailyPblAdd_pushButton.setEnabled(False)


	################browse dialogs###############	
	# Browse for assets to publish
	def assetPblBrowse(self):
		dialogHome = os.environ['JOBPATH']
		self.ui.pathToAsset_lineEdit.setText(self.fileDialog(dialogHome))

#	# Browse for renders to publish
#	def renderPblBrowse(self):
#		return self.folderDialog(os.environ['MAYARENDERSDIR'])

	# Browse for dailies to publish
	def dailyPblBrowse(self):
		if self.dailyType in ('modeling', 'texturing', 'animation', 'anim', 'fx', 'previs', 'tracking', 'rigging'):
			return self.fileDialog(os.environ['MAYAPLAYBLASTSDIR'])
		elif self.dailyType in ('lighting', 'shading', 'lookdev'):
			return self.fileDialog(os.environ['MAYARENDERSDIR'])
		elif self.dailyType == 'comp':
			return self.fileDialog(os.environ['NUKERENDERSDIR'])
		else:
			return self.fileDialog(os.environ['SHOTPATH'])

	#################getting ui options################
	#gets main publish options
	def getMainPblOpts(self):
	#	self.approved, self.mail = '', ''
		self.pblNotes = self.ui.notes_textEdit.text() #.toPlainText() # Edited line as notes box is now line edit widget, not text edit
		self.pblType = self.getPblTab()[1]
		self.slShot = self.ui.publishToShot_comboBox.currentText()
		# Get path to publish to. If selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.publishToShot_radioButton.isChecked() == 1:
			if self.slShot == os.environ['SHOT']:
				self.pblTo = os.environ['SHOTPUBLISHDIR']
			else:
				self.pblTo = os.path.join(os.environ['JOBPATH'], self.slShot, os.environ["PUBLISHRELATIVEDIR"])
		else:
			self.pblTo = os.environ["JOBPUBLISHDIR"]
	#	if self.ui.approved_checkBox.checkState() == 2:
	#		self.approved = True
	#	if self.ui.mail_checkBox.checkState() == 2:
	#		self.mail = True

	#gets asset publish options
	def get_maya_assetPblOpts(self, genericAsset=False):
		self.textures, self.subsetName, self.sceneName = '', '', ''
		self.chkLs = [] #self.chkLs = [self.pblNotes]
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
			self.dailyType = self.ui.dailyPbl_tableWidget.item(0, 2).text()
			self.dailyPath = self.ui.dailyPbl_tableWidget.item(0, 3).text()
		else:
			rowCount = None
		self.chkLs = [self.pblNotes, rowCount]
		
	#gets render publish options - THIS NEEDS RE-CODING
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


	def initPublish(self):
		""" Initialises publish.
			Ultimately this whole system should be rewritten.
		"""
		self.getMainPblOpts()

		###############
		# MAYA ASSETS #
		###############
		if self.pblType == 'ma Asset':

			self.get_maya_assetPblOpts()
			#print self.chkLs
			if not pblChk.chkOpts(self.chkLs):
				return

			# Camera
			if self.ui.cameraPbl_radioButton.isChecked() == True:
				import ma_camPbl
				self.camType = self.ui.cameraPbl_comboBox.currentText()
				ma_camPbl.publish(self.pblTo, self.slShot, self.camType, self.pblNotes)

			# Rig
			elif self.ui.rigPbl_radioButton.isChecked() == True:
				import ma_rigPbl
				self.rigType = self.ui.rigPbl_comboBox.currentText()
				ma_rigPbl.publish(self.pblTo, self.slShot, self.rigType, self.textures, self.pblNotes)

			# Animation
			elif self.ui.animPbl_radioButton.isChecked() == True:
				import ma_animPbl
				ma_animPbl.publish(self.pblTo, self.slShot, self.pblNotes)

			# FX
			elif self.ui.fxPbl_radioButton.isChecked() == True:
				import ma_fxPbl
				ma_fxPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes)

			# Point cloud
			elif self.ui.pointCloudPbl_radioButton.isChecked() == True:
				import ma_pointCloudPbl
				ma_pointCloudPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes)

			# Geo cache
			elif self.ui.geoCachePbl_radioButton.isChecked() == True:
				import ma_geoChPbl
				self.geoChType = self.ui.geoCachePbl_comboBox.currentText()
				ma_geoChPbl.publish(self.pblTo, self.slShot, self.geoChType, self.pblNotes)

			# Geo
			elif self.ui.geoPbl_radioButton.isChecked() == True:
				import ma_geoPbl
				self.geoType = self.ui.geoPbl_comboBox.currentText()
				ma_geoPbl.publish(self.pblTo, self.slShot, self.geoType, self.textures, self.pblNotes)

			# Model
			elif self.ui.modelPbl_radioButton.isChecked() == True:
				import ma_mdlPbl
				self.mdlType = self.ui.modelPbl_comboBox.currentText()
				ma_mdlPbl.publish(self.pblTo, self.slShot, self.mdlType, self.textures, self.pblNotes)

			# Shader
			elif self.ui.shaderPbl_radioButton.isChecked() == True:
				import ma_shdPbl
				ma_shdPbl.publish(self.pblTo, self.slShot, self.subsetName, self.textures, self.pblNotes)

			# Node
			elif self.ui.nodePbl_radioButton.isChecked() == True:
				import ma_nodePbl
				self.nodeType = self.ui.nodePbl_comboBox.currentText()
				ma_nodePbl.publish(self.pblTo, self.slShot, self.nodeType, self.subsetName, self.textures, self.pblNotes)

			# Scene
			elif self.ui.scenePbl_radioButton.isChecked() == True:
				import ma_scnPbl
				ma_scnPbl.publish(self.pblTo, self.slShot, self.sceneName, self.subsetName, self.textures, self.pblNotes)

			# Shot
			elif self.ui.shotPbl_radioButton.isChecked() == True:
				import ma_shotPbl
				ma_shotPbl.publish(self.pblTo, self.pblNotes)

		###############
		# NUKE ASSETS #
		###############
		if self.pblType == 'nk Asset':

			self.get_nuke_assetPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return

			# Card
			if self.ui.nk_cardPbl_radioButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'card'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Point cloud
			elif self.ui.nk_pointCloudPbl_radioButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'pointCloud'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Node
			elif self.ui.nk_nodePbl_radioButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'node'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Comp
			elif self.ui.nk_compPbl_radioButton.isChecked() == True:
				self.get_nuke_assetPblOpts(name=False)
				if not pblChk.chkOpts(self.chkLs):
					return
				import nk_compPbl
				self.pblType = 'comp'
				nk_compPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblNotes)

			# Pre-comp
			elif self.ui.nk_preCompPbl_radioButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'preComp'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)

			# Setup
			elif self.ui.nk_setupPbl_radioButton.isChecked() == True:
				import nk_setupPbl
				self.pblType = 'setup'
				nk_setupPbl.publish(self.pblTo, self.slShot, self.pblType, self.pblName, self.pblNotes)	

		###########
		# DAILIES #
		###########
		elif self.pblType == 'Daily':
			import ic_dailyPbl;
			self.getDailyPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return
			ic_dailyPbl.publish(self.dailySeq, self.dailyPath, self.dailyType, self.pblTo, self.pblNotes)

		###########
		# RENDERS #
		###########
		elif self.pblType == 'Render':
			import ic_renderPbl
			self.getRenderPblOpts()
			if not pblChk.chkOpts(self.chkLs):
				return
			ic_renderPbl.publish(self.renderDic, self.pblTo, self.mainLayer, self.streamPbl, self.pblNotes)


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
		#column.item(0).setSelected(True) # select the first item automatically
		#self.updateInfoField()
		#self.updateImgPreview()
	
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
	#	self.previewPlayerCtrl(hide=True)
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
	#	self.previewPlayerCtrl(hide=True)
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
	#	self.previewPlayerCtrl(hide=True)
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
	#	self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		searchPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType)
		self.fillColumn(self.aVersionCol, searchPath)


	def updateInfoField(self):
		""" Update info field with notes and other relevant data.
		"""
		self.adjustGatherTab(showGatherButton = True)
		self.assetVersion = self.aVersionCol.currentItem().text()
		self.gatherPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType, self.assetVersion)

	#	sys.path.append(self.gatherPath)
	#	import icData; reload(icData)
	#	sys.path.remove(self.gatherPath)
	#	self.ui.gatherInfo_textEdit.setText(icData.notes)

		import jobSettings
		# Instantiate XML data classes
		assetData = jobSettings.jobSettings()
		assetDataLoaded = assetData.loadXML(os.path.join(self.gatherPath, 'assetData.xml'))

		# If XML files don't exist, create defaults, and attempt to convert data from Python data files
		if not assetDataLoaded:
			import legacySettings

			# Try to convert from icData.py to XML (legacy assets)
			if legacySettings.convertAssetData(self.gatherPath, assetData):
				assetData.loadXML()
			else:
				return False

		# Print info to text field
		infoText = ""
		notes = assetData.getValue('asset', 'notes')
		if notes:
			infoText += "%s\n\n" % notes
		infoText += "Published by %s\n%s" % (assetData.getValue('asset', 'user'), assetData.getValue('asset', 'timestamp'))
		source = assetData.getValue('asset', 'assetSource')
		if source:
			infoText += "\nFrom '%s'" % source #os.path.basename(source)

		self.ui.gatherInfo_textEdit.setText(infoText)


	def updateImgPreview(self):
		""" Update image preview field with snapshot or preview clip.
		"""
		# Apply context menu to open viewer - DO THIS SOMEWHERE ELSE
	#	self.ui.gatherImgPreview_label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
	#	self.actionPreview = QtGui.QAction("Preview...", None)
	#	self.actionPreview.triggered.connect(self.preview)
	#	self.ui.gatherImgPreview_label.addAction(self.actionPreview)

		import previewImg
		imgPath = previewImg.getImg(self.gatherPath, forceExt='jpg')
	#	self.previewPlayerCtrl(hide=True)
		pixmap = QtGui.QPixmap(None)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)
		pixmap = QtGui.QPixmap(imgPath)
		self.ui.gatherImgPreview_label.setScaledContents(True)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)

#		if self.previewPlayer:
#			imgPath = previewImg.getImg(self.gatherPath, forceExt='mov')
#			if imgPath:
#				self.previewPlayerCtrl(hide=True)
#				pixmap = QtGui.QPixmap(None)
#				self.ui.gatherImgPreview_label.setPixmap(pixmap)
#				self.previewPlayerCtrl(loadImg=imgPath)
#				self.previewPlayerCtrl(show=True)
#				self.previewPlayerCtrl(play=True)
#
#				# Add preview context menu
#				self.ui.gatherImgPreview_label.addAction(self.actionPreview)
#
#		if not imgPath or not self.previewPlayer:
#			imgPath = previewImg.getImg(self.gatherPath, forceExt='jpg')
#			if imgPath:
#				self.previewPlayerCtrl(hide=True)
#				pixmap = QtGui.QPixmap(None)
#				self.ui.gatherImgPreview_label.setPixmap(pixmap)
#				pixmap = QtGui.QPixmap(imgPath)
#				self.ui.gatherImgPreview_label.setScaledContents(True)
#				self.ui.gatherImgPreview_label.setPixmap(pixmap)
#
#				# Remove preview context menu
#				self.ui.gatherImgPreview_label.removeAction(self.actionPreview)


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
