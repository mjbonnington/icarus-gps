#!/usr/bin/python

# [Icarus] icarus__main__.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2013-2019 Gramercy Park Studios
#
# The main Icarus UI.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

# Note: publish modules are imported on demand rather than all at once at
# beginning of file.
from publish import pblChk
# from publish import pblOptsPrc

from shared import disciplines
from shared import jobs
from shared import app_launcher  # merge these two?
from shared import launchApps   # merge these two?
from shared import openDirs
from shared import os_wrapper
from shared import prompt
from shared import recent_shots
from shared import sequence
from shared import verbose

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

cfg = {}

NAME = "Icarus"
COPYRIGHT = "(c) 2013-2019"
DEVELOPERS = "Mike Bonnington, Nuno Pereira, Ben Parry, Peter Bartfay"

# Set window title and object names
cfg['window_object'] = "icarusMainUI"
if os.environ['IC_ENV'] == 'STANDALONE':
	cfg['window_title'] = NAME
else:
	cfg['window_title'] = NAME + " - " + os.environ['IC_ENV'].capitalize()

# Set the UI and the stylesheet
cfg['ui_file'] = 'icarus.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
cfg['prefs_file'] = os.path.join(
	os.environ['IC_USERPREFS'], 'icarus_prefs.json')
cfg['store_window_geometry'] = True
# cfg['dock_with_maya_ui'] = False
# cfg['dock_with_nuke_ui'] = False

# ----------------------------------------------------------------------------
# Begin main application class
# ----------------------------------------------------------------------------

class IcarusApp(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Main application class.
	"""
	def __init__(self, parent=None, **kwargs):
		super(IcarusApp, self).__init__(parent)
		self.parent = parent

		# Print launch initialisation message
		info_ls = []
		for key, value in self.getInfo().items():
			info_ls.append("{} {}".format(key, value))
		info_str = " | ".join(info_ls)
		verbose.icarusLaunch(
			name=NAME.upper(), 
			version=os.environ['IC_VERSION'], 
			vendor="%s %s" % (COPYRIGHT, os.environ['IC_VENDOR']), 
			location=os.environ['IC_BASEDIR'], 
			extra=info_str)

		self.setupUI(**cfg)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Window)

		# Set other Qt attributes
		# self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Automatically set main tab to 'Launcher' - removes the requirement
		# for the UI file to be saved with this as the current tab.
		self.ui.main_tabWidget.setCurrentIndex(0)

		# Set verbosity - TODO: ideally this should be loaded before
		# instantiating the UI class. However, this would require splitting
		# JSON handler out to its own module
		if 'IC_VERBOSITY' not in os.environ:
			os.environ['IC_VERBOSITY'] = str(self.prefs.get_attr('user', 'verbosity', default=3))
		os.environ['IC_NUMRECENTFILES'] = str(self.prefs.get_attr('user', 'numrecentfiles', default=10))

		# If running for the first time, make sure globals are set
		if 'IC_FIRSTRUN' in os.environ:
			self.globalSettings()

		# Instantiate jobs class
		self.j = jobs.Jobs()

		# Hide main menu bar
		if os.environ['IC_EXPERT_MODE'] == 'True':  #kwargs['expert']:
			self.toggleExpertMode()
		else:
			self.expertMode = False
			self.toggleExpertWidgets(False, self.ui)

		# self.ui.user_toolButton.hide()  # TEMPORARY - until user prefs UI works
		self.ui.user_toolButton.setText(os.environ['IC_USERNAME'])

		# Set up keyboard shortcuts
		self.shortcutExpertMode = QtWidgets.QShortcut(self)
		self.shortcutExpertMode.setKey('Ctrl+Shift+E')
		self.shortcutExpertMode.activated.connect(self.toggleExpertMode)

		self.shortcutEnvVars = QtWidgets.QShortcut(self)
		self.shortcutEnvVars.setKey('Ctrl+E')
		self.shortcutEnvVars.activated.connect(self.openEnvVarEditor)

		# Set icons
		self.ui.shotEnv_toolButton.setIcon(self.iconSet('filmgrain.svg'))
		self.ui.user_toolButton.setIcon(self.iconSet('im-user.svg'))
		self.ui.toolMenu_toolButton.setIcon(self.iconSet('icon_editor.png'))
		self.ui.about_toolButton.setIcon(self.iconSet('icon_info.png'))

		self.ui.actionJobManagement.setIcon(self.iconSet('filmgrain.svg'))
		self.ui.actionShotManagement.setIcon(self.iconSet('filmgrain.svg'))
		self.ui.actionEditAppPaths.setIcon(self.iconSet('edit.svg'))
		self.ui.actionBatchRename.setIcon(self.iconSet('icon_rename.png'))
		self.ui.actionRenderQueue.setIcon(self.iconSet('icon_render.png'))
		self.ui.actionRenderSubmitter.setIcon(self.iconSet('icon_render.png'))
		self.ui.actionAboutIcarus.setIcon(self.iconSet('icon_info.png'))

		# --------------------------------------------------------------------
		# Connect signals & slots
		# --------------------------------------------------------------------

		self.ui.main_tabWidget.currentChanged.connect(self.adjustMainUI)
		self.ui.assetRefresh_toolButton.clicked.connect(self.assetRefresh)

		# Shot menu
		self.ui.menuRecentShots.aboutToShow.connect(self.updateRecentShotsMenu)
		self.ui.actionJobSettings.triggered.connect(self.jobSettings)
		self.ui.actionShotSettings.triggered.connect(self.shotSettings)

		# Tools menu
		self.ui.actionJobManagement.triggered.connect(self.openJobManagement)
		self.ui.actionShotManagement.triggered.connect(self.openShotManagement)
		self.ui.actionEnvironmentVariables.triggered.connect(self.openEnvVarEditor)
		self.ui.actionEditAppPaths.triggered.connect(self.openAppPathsEditor)
		self.ui.actionBatchRename.triggered.connect(self.openBatchRename)
		self.ui.actionRenderQueue.triggered.connect(self.openRenderQueue)
		self.ui.actionRenderSubmitter.triggered.connect(self.openRenderSubmitter)

		self.ui.toolMenu_toolButton.setMenu(self.ui.menuTools)  # Add tools menu to tool button in UI

		# Options menu
		self.ui.actionUserSettings.triggered.connect(self.userSettings)
		self.ui.actionGlobalSettings.triggered.connect(self.globalSettings)

		# Help menu
		self.ui.actionAboutIcarus.triggered.connect(self.about)

		# Header toolbar
		self.ui.about_toolButton.clicked.connect(self.about)

		# Publishing UI
		# self.ui.renderPblAdd_pushButton.clicked.connect(self.renderTableAdd)
		# self.ui.renderPblRemove_pushButton.clicked.connect(self.renderTableRm)
		self.ui.renderPblSetMain_pushButton.clicked.connect(self.setLayerAsMain) # remove when render publishing works properly
		self.ui.renderPblAdd_pushButton.clicked.connect(self.renderTableAdd)
		self.ui.renderPblRemove_pushButton.clicked.connect(self.renderTableRemove)
		# self.ui.renderPblRevert_pushButton.clicked.connect(self.renderTableClear)
		self.ui.renderPbl_treeWidget.currentItemChanged.connect(self.updateRenderPublishUI)
		self.ui.renderPbl_treeWidget.itemDoubleClicked.connect(self.renderPreview)
		self.ui.dailyPbl_treeWidget.itemDoubleClicked.connect(self.dailyPreview)
		self.ui.dailyPblType_comboBox.currentIndexChanged.connect(self.setDailyType)
		self.ui.dailyPblAdd_pushButton.clicked.connect(self.dailyTableAdd)
		self.ui.publish_pushButton.clicked.connect(self.initPublish)

		self.populateComboBox(
			self.ui.dailyPblType_comboBox, 
			disciplines.disciplines, 
			replace=False, 
			blockSignals=True)

		######################################
		# Adapt UI for environment awareness #
		######################################

		self.launchTab = self.ui.main_tabWidget.widget(0)
		self.publishTab = self.ui.main_tabWidget.widget(1)
		self.gatherTab = self.ui.main_tabWidget.widget(2)
		self.publishAssetTab = self.ui.publishType_tabWidget.widget(0)
		self.publishRenderTab = self.ui.publishType_tabWidget.widget(1)


		##########################
		# Standalone environment #
		##########################

		if os.environ['IC_ENV'] == 'STANDALONE':

			# Register status bar with the verbose module in order to print
			# messages to it...
			verbose.registerStatusBar(self.ui.statusbar)

			# Hide UI items relating to app environment(s)
			uiHideLs = ['shotEnv_toolButton', 'appIcon_label']
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' %uiItem
				eval(hideProc)

			# Populate 'Job' and 'Shot' drop down menus
			self.populateJobs(setLast=True, reloadJobs=False)
			self.unlockJobUI(refreshShots=False)  # Currently used to make sure UI state (whether widgets are enabled/visible) is correct when opened, without relying on the UI file

			# Delete all tabs except 'Launcher'
			for i in range(0, self.ui.main_tabWidget.count()-1):
				self.ui.main_tabWidget.removeTab(1)

			# Delete 'ma_asset', 'nk_asset', 'Publish' tabs
			for i in range(0, 2):
				self.ui.publishType_tabWidget.removeTab(0)

			# Initialise app launch icons
			self.al = app_launcher.AppLauncher(
				self, self.ui.launchApp_scrollAreaWidgetContents)

			# ----------------------------------------------------------------
			# Connect signals & slots
			# ----------------------------------------------------------------

			# Set shot UI
			self.ui.refreshJobs_toolButton.clicked.connect(self.populateJobs)
			self.ui.job_comboBox.currentIndexChanged.connect(self.populateShots)
			# self.ui.shot_comboBox.view().pressed.connect(self.populateShots)  # Auto-populate combo box when clicked - cannot get to work
			self.ui.setShot_toolButton.toggled.connect(lambda checked: self.setShot(checked))

			# Utility launch buttons (bottom row)
			self.ui.render_toolButton.clicked.connect(self.openRenderSubmitter)  # self.openRenderQueue
			self.ui.openReview_toolButton.clicked.connect(launchApps.djv)
			self.ui.openProdBoard_toolButton.clicked.connect(launchApps.prodBoard)
			self.ui.openTerminal_toolButton.clicked.connect(launchApps.terminal)
			self.ui.browse_toolButton.clicked.connect(openDirs.openShot)

			# self.ui.appPlaceholder_toolButton.clicked.connect(lambda: self.jobSettings(startPanel='apps'))
			self.ui.appPlaceholder_toolButton.clicked.connect(self.appSettings)

			# # Launch options menu -- DELETED
			# self.ui.launchOptions_toolButton.setMenu(self.ui.menuLauncher)

			# Set 'Minimise on launch' checkbox from user prefs
			self.minimiseOnAppLaunch = self.prefs.get_attr('user', 'minimiseonlaunch', default=True)
			# self.ui.actionMinimise_on_Launch.setChecked(self.minimiseOnAppLaunch)
			# self.ui.actionMinimise_on_Launch.toggled.connect(self.setMinimiseOnAppLaunch)

			# # Add 'Sort by' separator label -- DELETED
			# label = QtWidgets.QLabel("Sort by:")
			# sortBy_separator = QtWidgets.QWidgetAction(self)
			# sortBy_separator.setDefaultWidget(label)
			# self.ui.menuLauncher.insertAction(self.ui.actionName, sortBy_separator)

			# # Make 'Sort by' actions mutually exclusive
			# alignmentGroup = QtWidgets.QActionGroup(self)
			# alignmentGroup.addAction(self.ui.actionName)
			# alignmentGroup.addAction(self.ui.actionCategory)
			# alignmentGroup.addAction(self.ui.actionVendor)
			# alignmentGroup.addAction(self.ui.actionMostUsed)

			# Set 'Sort by' menu from user prefs
			self.sortAppsBy = self.prefs.get_attr('user', 'sortappsby', default="Most used")
			# if self.sortAppsBy == "Name":
			# 	self.ui.actionName.setChecked(True)
			# elif self.sortAppsBy == "Category":
			# 	self.ui.actionCategory.setChecked(True)
			# elif self.sortAppsBy == "Vendor":
			# 	self.ui.actionVendor.setChecked(True)
			# elif self.sortAppsBy == "Most used":
			# 	self.ui.actionMostUsed.setChecked(True)

			# self.ui.actionName.triggered.connect(lambda: self.setSortAppsBy("Name"))
			# self.ui.actionCategory.triggered.connect(lambda: self.setSortAppsBy("Category"))
			# self.ui.actionVendor.triggered.connect(lambda: self.setSortAppsBy("Vendor"))
			# self.ui.actionMostUsed.triggered.connect(lambda: self.setSortAppsBy("Most used"))

			# ----------------------------------------------------------------
			# Add context menus to buttons
			# ----------------------------------------------------------------

			# # Render
			# self.ui.render_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
			# self.ui.render_toolButton.addAction(self.ui.actionRenderQueue)
			# self.ui.render_toolButton.addAction(self.ui.actionRenderSubmitter)

			# Review
			self.addContextMenu(self.ui.openReview_toolButton, 
				"djv_view", 
				launchApps.djv, 
				'app_icon_djv.png', tintNormal=False)
			self.addContextMenu(self.ui.openReview_toolButton, 
				"HieroPlayer", 
				lambda: launchApps.launch('HieroPlayer'), 
				'app_icon_hieroplayer.png', tintNormal=False)
			self.addContextMenu(self.ui.openReview_toolButton, 
				"Bridge", 
				lambda: launchApps.launch('Bridge'), 
				'app_icon_bridge.png', tintNormal=False)

			# Browse
			self.addContextMenu(self.ui.browse_toolButton, 
				"Shot", 
				openDirs.openShot, 
				'icon_folder.png', tintNormal=False)
			self.addContextMenu(self.ui.browse_toolButton, 
				"Job", 
				openDirs.openJob, 
				'icon_folder.png', tintNormal=False)

			# Apply job/shot settings pop-up menu to shotEnv label (only in standalone mode)
			self.ui.shotEnv_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
			self.ui.shotEnv_toolButton.addAction(self.ui.actionJobSettings)
			self.ui.shotEnv_toolButton.addAction(self.ui.actionShotSettings)
			self.ui.shotEnv_toolButton.setEnabled(True)

			# Apply user settings pop-up menu to user label (only in standalone mode)
			self.ui.user_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
			self.ui.user_toolButton.addAction(self.ui.actionUserSettings)
			# self.ui.user_toolButton.setText(os.environ['IC_USERNAME'])
			self.ui.user_toolButton.setEnabled(True)

			# Setup app launch icons
			self.al.setupIconGrid(sort_by=self.sortAppsBy)

			# Store env vars
			self.environ = dict(os.environ)

			# Set shot automatically if command-line args are set
			if kwargs['job'] and kwargs['shot']:
				self.setupJob(kwargs['job'], kwargs['shot'])


		####################
		# Maya environment #
		####################

		elif os.environ['IC_ENV'] == 'MAYA':
			# pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_maya_disabled.png")
			# self.ui.appIcon_label.setPixmap(pixmap)

			# Hide certain UI items
			uiHideLs = ['assetSubType_listWidget', 'toolMenu_toolButton']
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' %uiItem
				eval(hideProc)

			self.connectNewSignalsSlots()
			self.populateShotLs(self.ui.publishToShot_comboBox)
			self.populateShotLs(self.ui.gatherFromShot_comboBox)
			self.updateJobLabel()
			self.ui.main_tabWidget.removeTab(0) # Remove 'Launcher' tab
			self.ui.publishType_tabWidget.removeTab(1) # Remove 'Nuke Asset' tab

			# Attempt to set the publish asset type button to remember the
			# last selection - 'self.connectNewSignalsSlots()' must be called
			# already.
			try:
				assetType = self.prefs.get_attr('maya', 'lastpublishtype')
				for toolButton in self.ui.ma_assetType_frame.children():
					if isinstance(toolButton, QtWidgets.QToolButton):
						if toolButton.text() == assetType:
							toolButton.setChecked(True)
			except:
				verbose.print_("Could not select %s asset type." %assetType)


		#######################
		# Houdini environment #
		#######################

		elif os.environ['IC_ENV'] == 'HOUDINI':
			# pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_houdini_disabled.png")
			# self.ui.appIcon_label.setPixmap(pixmap)

			# Hide certain UI items
			uiHideLs = ['assetSubType_listWidget', 'toolMenu_toolButton']
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' %uiItem
				eval(hideProc)

			self.connectNewSignalsSlots()
			self.populateShotLs(self.ui.publishToShot_comboBox)
			self.populateShotLs(self.ui.gatherFromShot_comboBox)
			self.updateJobLabel()
			self.ui.main_tabWidget.removeTab(0) # Remove 'Launcher' tab
			self.ui.publishType_tabWidget.removeTab(1) # Remove 'Nuke Asset' tab
			self.ui.publishType_tabWidget.removeTab(0) # Remove 'Maya Asset' tab

			# # Attempt to set the publish asset type button to remember the
			# # last selection - 'self.connectNewSignalsSlots()' must be called
			# # already.
			# try:
			# 	assetType = self.prefs.get_attr('houdini', 'lastpublishtype')
			# 	for toolButton in self.ui.ma_assetType_frame.children():
			# 		if isinstance(toolButton, QtWidgets.QToolButton):
			# 			if toolButton.text() == assetType:
			# 				toolButton.setChecked(True)
			# except:
			# 	verbose.print_("Could not select %s asset type." %assetType)


		####################
		# Nuke environment #
		####################

		elif os.environ['IC_ENV'] == 'NUKE':
			# pixmap = QtGui.QPixmap(":/rsc/rsc/app_icon_nuke_disabled.png")
			# self.ui.appIcon_label.setPixmap(pixmap)

			# Hide certain UI items
			uiHideLs = ['assetSubType_listWidget', 'toolMenu_toolButton']
			for uiItem in uiHideLs:
				hideProc = 'self.ui.%s.hide()' %uiItem
				eval(hideProc)

			self.connectNewSignalsSlots()
			self.populateShotLs(self.ui.publishToShot_comboBox)
			self.populateShotLs(self.ui.gatherFromShot_comboBox)
			self.updateJobLabel()
			self.ui.main_tabWidget.removeTab(0) # Remove 'Launcher' tab
			self.ui.publishType_tabWidget.removeTab(0) # Remove 'Maya Asset' tab

			# Attempt to set the publish asset type button to remember the
			# last selection - 'self.connectNewSignalsSlots()' must be called
			# already.
			try:
				assetType = self.prefs.get_attr('nuke', 'lastpublishtype')
				for toolButton in self.ui.nk_assetType_frame.children():
					if isinstance(toolButton, QtWidgets.QToolButton):
						if toolButton.text() == assetType:
							toolButton.setChecked(True)
			except:
				verbose.print_("Could not select %s asset type." %assetType)

	# End of function __init__


	#########################
	# Generic UI procedures #
	#########################

	def connectNewSignalsSlots(self):
		""" Connects new signals and slots after job and shot env is set.
		"""
		self.ui.publishType_tabWidget.currentChanged.connect(self.adjustPblTypeUI)

		for toolButton in self.ui.ma_assetType_frame.children():
			if isinstance(toolButton, QtWidgets.QToolButton):
				toolButton.toggled.connect(self.adjustPublishOptsMayaUI)
		for toolButton in self.ui.nk_assetType_frame.children():
			if isinstance(toolButton, QtWidgets.QToolButton):
				toolButton.toggled.connect(self.adjustPublishOptsNukeUI)

		# self.ui.animation_toolButton.clicked.connect(self.setDropDownToShotEnv)
		# self.ui.shot_toolButton.clicked.connect(self.setDropDownToShotEnv)
		# self.ui.comp_toolButton.clicked.connect(self.setDropDownToShotEnv) #self.adjustPblTypeUI

		self.ui.gatherFromShot_radioButton.clicked.connect(self.assetRefresh)
		self.ui.gatherFromShot_comboBox.currentIndexChanged.connect(self.assetRefresh)
		self.ui.gatherFromJob_radioButton.clicked.connect(self.assetRefresh)
		self.ui.gather_pushButton.clicked.connect(self.initGather)

		self.ui.assetType_listWidget.itemClicked.connect(self.updateAssetNameCol) # currentItemChanged?
		self.ui.assetName_listWidget.itemClicked.connect(self.adjustColumns)
		self.ui.assetSubType_listWidget.itemClicked.connect(self.updateAssetVersionCol)
		self.ui.assetVersion_listWidget.itemClicked.connect(self.updateInfoField)
		self.ui.assetVersion_listWidget.itemClicked.connect(self.updateImgPreview)


	def toggleExpertMode(self):
		""" Toggle expert mode where additional UI items are visible, and
			enable debug-level verbosity for output messages.
		"""
		try:
			self.expertMode = not self.expertMode
		except AttributeError:
			self.expertMode = True

		if self.expertMode:
			os.environ['IC_VERBOSITY'] = '4'
		else:
			os.environ['IC_VERBOSITY'] = str(self.prefs.get_attr('user', 'verbosity', default=3))

		os.environ['IC_EXPERT_MODE'] = str(self.expertMode)
		verbose.message("Expert mode: %s" %self.expertMode)
		self.toggleExpertWidgets(self.expertMode, self.ui)
		# self.populateJobs()


	def getCurrentTab(self, tabWidget):
		""" Returns the index and name of the current tab of tabWidget.
		"""
		tabIndex = tabWidget.currentIndex()
		tabText = tabWidget.tabText(tabIndex)
		return tabIndex, tabText


	def adjustMainUI(self):
		""" Makes UI adjustments and connections based on which tab is
			currently selected. TODO: improve!
		"""
		mainTabName = self.getCurrentTab(self.ui.main_tabWidget)[1]
		if mainTabName == 'Gather' or mainTabName == 'Assets':
			self.defineColumns()
			#self.updateAssetTypeCol()


	def assetRefresh(self):
		""" Allows state of asset browser to be preserved even if the current
			tab changes. TODO: improve!
		"""
		self.defineColumns()
		self.updateAssetTypeCol()


	def adjustPublishOptsMayaUI(self):
		""" Makes UI adjustments based on which asset publish type is
			currently selected.
		"""
		assetType = self.sender().text()

		self.ui.ma_publishOptions_groupBox.setTitle("Publish options: %s" %assetType)

		self.ui.assetSubType_comboBox.clear()
		self.ui.textures_checkBox.setEnabled(True)
		self.ui.assetName_label.setEnabled(False)
		self.ui.assetName_lineEdit.setEnabled(False)

		if assetType == 'model':
			self.ui.assetSubType_comboBox.addItem('base')
			self.ui.assetSubType_comboBox.addItem('anim')
		elif assetType == 'rig':
			self.ui.assetSubType_comboBox.addItem('anim')
			self.ui.assetSubType_comboBox.addItem('light')
			self.ui.assetSubType_comboBox.addItem('fx')
		elif assetType == 'camera':
			self.ui.assetSubType_comboBox.addItem('render')
			self.ui.assetSubType_comboBox.addItem('mm')
			self.ui.assetSubType_comboBox.addItem('previs')
			self.ui.textures_checkBox.setEnabled(False)
			self.ui.textures_checkBox.setChecked(False)
			# self.lockPublishTo(lock=True)
		elif assetType == 'geo':
			self.ui.assetSubType_comboBox.addItem('abc')
			self.ui.assetSubType_comboBox.addItem('obj')
			self.ui.assetSubType_comboBox.addItem('fbx')
		elif assetType == 'geoCache':
			self.ui.assetSubType_comboBox.addItem('anim')
			self.ui.assetSubType_comboBox.addItem('cloth')
			self.ui.assetSubType_comboBox.addItem('rigidBody')
			self.ui.assetSubType_comboBox.addItem('vrmesh')
			self.ui.assetSubType_comboBox.addItem('realflow')
			self.ui.textures_checkBox.setEnabled(False)
			self.ui.textures_checkBox.setChecked(False)
		elif assetType == 'animation':
			self.ui.textures_checkBox.setEnabled(False)
			self.ui.textures_checkBox.setChecked(False)
		elif assetType == 'scene':
			self.ui.assetName_label.setEnabled(True)
			self.ui.assetName_lineEdit.setEnabled(True)
		elif assetType == 'node':
			self.ui.assetSubType_comboBox.addItem('ma')
			self.ui.assetSubType_comboBox.addItem('ic')
		# elif assetType == 'shot':
		# 	self.lockPublishTo(lock=True)

		if self.ui.assetSubType_comboBox.count():
			self.ui.assetSubType_label.setEnabled(True)
			self.ui.assetSubType_comboBox.setEnabled(True)
			self.ui.subSet_checkBox.setEnabled(False)
			self.ui.subSet_checkBox.setChecked(False)
		else:
			self.ui.assetSubType_label.setEnabled(False)
			self.ui.assetSubType_comboBox.setEnabled(False)
			self.ui.subSet_checkBox.setEnabled(True)

		# Remember last selection with entry in user prefs
		self.prefs.set_attr('maya', 'lastpublishtype', assetType)


	def adjustPublishOptsNukeUI(self):
		""" Makes UI adjustments based on which asset publish type is
			currently selected.
		"""
		assetType = self.sender().text()

		self.ui.nk_publishOptions_groupBox.setTitle("Publish options: %s" %assetType)

		self.ui.nk_PblName_label.setEnabled(True)
		self.ui.nk_PblName_lineEdit.setEnabled(True)

		if assetType == 'comp':
			self.ui.nk_PblName_label.setEnabled(False)
			self.ui.nk_PblName_lineEdit.setEnabled(False)
			# self.lockPublishTo(lock=True)

		# Remember last selection with entry in user prefs
		self.prefs.set_attr('nuke', 'lastpublishtype', assetType)


	def adjustPblTypeUI(self):
		""" Makes UI lock adjustments based on which publish type tab is
			currently selected.
		"""
		tabIndex = self.ui.publishType_tabWidget.currentIndex()
		tabText = self.ui.publishType_tabWidget.tabText(tabIndex)

		if tabText == 'Maya Asset':
			self.lockPublishTo(lock=False)

		elif tabText == 'Nuke Asset':
			self.lockPublishTo(lock=False)
			# if self.ui.comp_toolButton.isChecked() == True:
			# 	self.lockPublishTo(lock=True)
			# 	#self.setDropDownToShotEnv()
			# else:
			# 	self.lockPublishTo(lock=False)

		elif tabText == 'Dailies':
			self.lockPublishTo(lock=True)
			#self.setDropDownToShotEnv()

		elif tabText == 'Render':
			self.lockPublishTo(lock=True)
			#self.setDropDownToShotEnv()


	def lockPublishTo(self, lock=False):
		""" Locks 'Publish To' section of UI based on selection.
		"""
		if lock:
			self.ui.publishToJob_radioButton.setEnabled(False)
			self.ui.publishToShot_radioButton.setChecked(True)
			self.ui.publishToShot_comboBox.setEnabled(False)
			self.setDropDownToShotEnv()
		else:
			self.ui.publishToJob_radioButton.setEnabled(True)
			if self.ui.publishToShot_radioButton.isChecked() == 1:
				self.ui.publishToShot_comboBox.setEnabled(True)
			#self.ui.model_toolButton.setChecked(True)


	def setDropDownToShotEnv(self):
		""" Switches the shot drop down menu to the current environment shot.
			Disables publishing to alternative shot.
		"""
		self.ui.publishToShot_comboBox.setCurrentIndex(self.ui.publishToShot_comboBox.findText(os.environ['IC_SHOT']))


	################
	# Launcher tab #
	################

	def populateJobs(self, setLast=False, reloadJobs=True):
		""" Populates job drop down menu.
		"""
		verbose.print_("Populating jobs combo box...", 4)

		# Block signals to prevent call to populateShots() each time a new item is added
		self.ui.job_comboBox.blockSignals(True)

		# Store last set or current item
		if setLast:
			try:
				last_job = recent_shots.recents.get(last=True)[0]
			except:
				last_job = None
		else:
			last_job = self.ui.job_comboBox.currentText()

		# Remove all items
		self.ui.job_comboBox.clear()

		# Reload jobs database
		if reloadJobs:
			self.j.reload()

		# Populate combo box with list of jobs
		if self.expertMode:
			jobLs = sorted(self.j.getAllJobs())
		else:
			jobLs = sorted(self.j.getActiveJobs())

		if jobLs:
			self.ui.job_comboBox.insertItems(0, jobLs)

			# Attempt to set the combo box to remember the last item.
			if self.setComboBox(self.ui.job_comboBox, last_job):
				self.populateShots(setLast=setLast)
			else:
				self.populateShots()

			self.ui.shotSetup_groupBox.setEnabled(True)
			self.ui.shotSetupButtons_groupBox.setEnabled(True)

			# Re-enable signals so that shot list gets repopulated
			self.ui.job_comboBox.blockSignals(False)

			# Setup app launch icons
			# self.al.setupIconGrid(job=last_job, sort_by=self.sortAppsBy)

		# If no jobs found, disable all launcher / shot setup UI controls
		else:
			msg = "No active jobs found"
			verbose.warning(msg+".")
			self.ui.job_comboBox.insertItem(0, '[%s]' %msg)
			self.ui.shot_comboBox.clear()
			self.ui.shot_comboBox.insertItem(0, '[None]')
			self.ui.shotSetup_groupBox.setEnabled(False)
			self.ui.shotSetupButtons_groupBox.setEnabled(False)

			# Warning dialog
			dialogTitle = "No Jobs Found"
			dialogMsg = "No active jobs were found. Would you like to set up some jobs now?"
			dialog = prompt.dialog()
			if dialog.display(dialogMsg, dialogTitle):
				self.openJobManagement()
			else:
				self.unlockJobUI(refreshShots=False)


	def populateShots(self, setLast=False):
		""" Populates shot drop down menu.
		"""
		verbose.print_("Populating shots combo box...", 4)

		# Store last set or current item
		if setLast:
			try:
				last_shot = recent_shots.recents.get(last=True)[1]
			except:
				last_shot = None
		else:
			last_shot = self.ui.shot_comboBox.currentText()

		# Remove all items
		self.ui.shot_comboBox.clear()

		# Populate combo box with list of shots
		selJob = self.ui.job_comboBox.currentText()
		shotLs = self.j.listShots(selJob)
		if shotLs:
			self.ui.shot_comboBox.insertItems(0, shotLs)

			# Attempt to set the combo box to remember the last item.
			self.setComboBox(self.ui.shot_comboBox, last_shot)

			self.ui.shot_comboBox.setEnabled(True)
			self.ui.setShot_label.setEnabled(True)

			return True

		# No shots detected...
		else:
			self.ui.shot_comboBox.insertItem(0, '[None]')
			self.ui.shot_comboBox.setEnabled(False)
			self.ui.setShot_label.setEnabled(False)

			# Warning dialog
			dialogTitle = "No Shots Found"
			dialogMsg = "No shots were found for the job '%s'. Would you like to create some shots now?" %selJob
			dialog = prompt.dialog()
			if dialog.display(dialogMsg, dialogTitle):
				self.openShotManagement()
			else:
				pass

			return False


	def populateShotLs(self, comboBox):
		""" Populate specified combo box with shot list.
		"""
		comboBox.clear()
		shotLs = self.j.listShots(os.environ['IC_JOB'])
		if shotLs:
			comboBox.insertItems(0, shotLs)
			comboBox.setCurrentIndex(comboBox.findText(os.environ['IC_SHOT']))


	def setComboBox(self, comboBox, text):
		""" Update job tab UI with shot selection.
		"""
		index = comboBox.findText(text)

		if index != -1:
			comboBox.setCurrentIndex(index)
			return True
		else:
			verbose.print_("Unable to set %s to %s" %(comboBox.objectName(), text), 4)
			comboBox.setCurrentIndex(0)
			return False


	def setupJob(self, job=None, shot=None):
		""" Sets up shot environment, creates user directories and updates
			user job log.
		"""
		if job is None:
			job = self.ui.job_comboBox.currentText()
		else:
			self.setComboBox(self.ui.job_comboBox, job)

		if shot is None:
			shot = self.ui.shot_comboBox.currentText()
		else:
			self.setComboBox(self.ui.shot_comboBox, shot)

		self.job = job
		self.shot = shot

		if self.j.checkShotExists(self.job, self.shot):

			if self.j.setup(self.job, self.shot):  # Set shot environment
				self.adjustPblTypeUI()
				self.populateShotLs(self.ui.publishToShot_comboBox)
				self.populateShotLs(self.ui.gatherFromShot_comboBox)
				self.connectNewSignalsSlots()
				self.assetRefresh()
				self.al.setupIconGrid(job=self.job, sort_by=self.sortAppsBy)
				self.al.setAppEnvVars()
				self.lockJobUI()

				return True

			else:
				dialogMsg = "Unable to load job settings. Default values have been applied.\nPlease review the values in the Job Settings dialog and click Save when done.\n"
				verbose.warning(dialogMsg)

				# Confirmation dialog
				dialogTitle = "Job settings not found"
				dialog = prompt.dialog()
				dialog.display(dialogMsg, dialogTitle, conf=True)

				if self.openSettings("Job", autofill=True):
					self.setupJob()

				return False

		else:
			verbose.warning("Shot '%s' doesn't exist." %self.shot)
			return False


	@QtCore.Slot(bool)
	def setShot(self, checked):
		""" Wrapper function to set/unset shot from the tool button.
		"""
		if checked:
			if not self.setupJob():
				# If job setup failed, reset check state of button to off
				self.ui.setShot_toolButton.setChecked(False)

		else:
			self.unlockJobUI(refreshShots=True)

			# Restore env vars
			os.environ.clear()
			for key in self.environ.keys():
				os.environ[key] = self.environ[key]


	# @QtCore.Slot()
	def setupRecentJob(self):
		""" Wrapper function to set up shot from the recent shots menu.
		"""
		job = self.sender().property('job')
		shot = self.sender().property('shot')

		self.setupJob(job, shot)


	# @QtCore.Slot()
	def updateRecentShotsMenu(self):
		""" Updates the recent shots menu.
		"""
		verbose.print_("Populating recent shots menu...", 4)
		self.ui.menuRecentShots.clear()

		recent_shots.recents.reload()
		recentShots = recent_shots.recents.get()
		if recentShots:
			self.ui.menuRecentShots.setEnabled(True)
			self.ui.setShot_toolButton.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
			for i, entry in enumerate(recentShots):
				job, shot = entry
				menuName = "%s - %s" %(job, shot)
				actionName = "action%s" %i
				action = QtWidgets.QAction(menuName, None)
				action.setObjectName(actionName)
				action.setText(menuName)
				action.setProperty('job', job)
				action.setProperty('shot', shot)
				tooltip = "Set shot to %s - %s" %(job, shot)
				action.setToolTip(tooltip)
				action.setStatusTip(tooltip)
				action.triggered.connect(self.setupRecentJob)
				self.ui.menuRecentShots.addAction(action)
				self.ui.setShot_toolButton.addAction(action)

				# Make a class-scope reference to this object
				# (won't work without it for some reason)
				exec_str = "self.%s = action" %actionName
				exec(exec_str)

		else:
			self.ui.menuRecentShots.setEnabled(False)


	def lockJobUI(self):
		""" Updates and locks UI job tab.
		"""
		self.updateJobLabel()
		self.updateRecentShotsMenu()

		self.ui.shotSetup_groupBox.setEnabled(False)
		self.ui.refreshJobs_toolButton.setEnabled(False)

		self.ui.launchApp_frame.setEnabled(True)
		# self.ui.launchApp_frame.show()
		# self.ui.launchTab_verticalLayout.removeItem(self.ui.launchTab_verticalSpacer)
		# self.ui.launchTab_verticalSpacer = None
		# # self.ui.launchTab_verticalSpacer.hide()

		self.ui.main_tabWidget.insertTab(1, self.publishTab, 'Publish')
		self.ui.main_tabWidget.insertTab(2, self.gatherTab, 'Assets')
		self.ui.gather_frame.hide()
		self.ui.setShot_toolButton.setChecked(True)
		self.ui.shotEnv_toolButton.show()
		self.ui.actionJobSettings.setEnabled(True)
		self.ui.actionShotSettings.setEnabled(True)
		self.ui.actionJobManagement.setEnabled(False)
		self.ui.actionShotManagement.setEnabled(False)
		self.ui.actionRenderSubmitter.setEnabled(True)

		verbose.message("Shot set: Now working on %s - %s" % (self.job, self.shot))


	def unlockJobUI(self, refreshShots=True):
		""" Unlocks UI if 'Set New Shot' is clicked.
		"""
		# Re-scan for shots
		if refreshShots:
			self.populateShots()
		self.updateRecentShotsMenu()

		self.ui.shotSetup_groupBox.setEnabled(True)
		self.ui.refreshJobs_toolButton.setEnabled(True)

		self.ui.launchApp_frame.setEnabled(False)
		# self.ui.launchApp_frame.hide()
		# self.ui.launchTab_verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
		# self.ui.launchTab_verticalLayout.addItem(self.ui.launchTab_verticalSpacer)
		# # self.ui.launchTab_verticalSpacer.show()

		self.ui.main_tabWidget.removeTab(1)  # Remove publish & assets tab
		self.ui.main_tabWidget.removeTab(1)  # Remove publish & assets tab
		self.ui.renderPbl_treeWidget.clear()  # Clear the render layer tree view widget
		self.ui.dailyPbl_treeWidget.clear()  # Clear the dailies tree view widget
		self.ui.shotEnv_toolButton.setText('')
		self.ui.shotEnv_toolButton.hide()
		self.ui.actionJobSettings.setEnabled(False)
		self.ui.actionShotSettings.setEnabled(False)
		self.ui.actionJobManagement.setEnabled(True)
		self.ui.actionShotManagement.setEnabled(True)
		self.ui.actionRenderSubmitter.setEnabled(False)

		verbose.print_("Shot unset: reverting to clean environment.")


	def updateJobLabel(self):
		""" Updates job label tool button with the current job and shot.
		"""
		if os.environ['IC_ENV'] != 'STANDALONE':
			self.job = os.environ['IC_JOB']
			self.shot = os.environ['IC_SHOT']

		self.ui.shotEnv_toolButton.setText('%s - %s' %(self.job, self.shot))


	def about(self):
		""" Show about dialog.
		"""
		from shared import about

		info_ls1 = []
		info_ls2 = []
		sep = " | "
		for key, value in self.getInfo().items():
			if key in ['Environment', 'OS']:
				info_ls1.append("{}: {}".format(key, value))
			else:
				info_ls2.append("{} {}".format(key, value))
		info_str1 = sep.join(info_ls1)
		info_str2 = sep.join(info_ls2)

		about_msg = \
"""
%s

%s

Developers: %s
%s %s

%s
%s
""" % ("   ".join(NAME.upper()), os.environ['IC_VERSION'], 
DEVELOPERS, COPYRIGHT, os.environ['IC_VENDOR'], 
info_str1, info_str2)

		aboutDialog = about.AboutDialog(parent=self)
		aboutDialog.display(
			bg_image=os_wrapper.absolutePath('$IC_FORMSDIR/icons/icarus_splash.jpg'), 
			# bg_color=QtGui.QColor('#5b6368'), 
			# icon_pixmap=self.iconTint('icarus.png'), 
			message=about_msg)


	def openSettings(self, settingsType, startPanel=None, autofill=False):
		""" Open settings dialog.
			# categoryLs = ['user', 'launcher', 'global', 'test', 'job', 'time', 'resolution', 'units', 'apps', 'other', 'camera']
		"""
		if settingsType == "Job":
			selfName = os.environ['IC_JOB']
			categoryLs = ['job', 'apps', 'units', 'time', 'resolution', 'other']
			settingsFile = os.environ['IC_JOBDATA']
			inherit = None
		elif settingsType == "Shot":
			selfName = os.environ['IC_SHOT']
			categoryLs = ['shot', 'units', 'time', 'resolution', 'camera']
			settingsFile = os.environ['IC_SHOTDATA']
			inherit = os.environ['IC_JOBDATA']
		elif settingsType == "User":
			selfName = os.environ['IC_USERNAME']
			categoryLs = ['user', ]
			settingsFile = cfg['prefs_file']  # Use Icarus UI prefs - os.path.join(os.environ['IC_USERPREFS'], 'icarus_prefs.json')
			inherit = None
		elif settingsType == "Global":
			selfName = ""
			categoryLs = ['global', ]
			settingsFile = os.path.join(os.environ['IC_CONFIGDIR'], 'icarus_globals.json')
			inherit = None
		elif settingsType == "App":  # Workaround for apps only dialog
			selfName = os.environ['IC_JOB']
			categoryLs = ['apps', ]
			settingsFile = os.environ['IC_JOBDATA']
			inherit = None

		if startPanel not in categoryLs:
			startPanel = None

		from tools.settings import settings
		self.settingsEditor = settings.SettingsDialog(parent=self)
		result = self.settingsEditor.display(
			settings_type=settingsType, 
			self_name=selfName, 
			category_list=categoryLs, 
			start_panel=startPanel, 
			prefs_file=settingsFile, 
			inherit=inherit, 
			autofill=autofill)

		return result


	def jobSettings(self, startPanel=None):
		""" Open job settings dialog wrapper function.
		"""
		if self.openSettings("Job", startPanel=startPanel):
			self.setupJob()


	def shotSettings(self):
		""" Open shot settings dialog wrapper function.
		"""
		if self.openSettings("Shot"):
			self.setupJob()


	def userSettings(self):
		""" Open user settings dialog wrapper function.
		"""
		if self.openSettings("User"):
			self.prefs.reload()
			self.minimiseOnAppLaunch = self.prefs.get_attr('user', 'minimiseonlaunch')
			self.sortAppsBy = self.prefs.get_attr('user', 'sortappsby')
			os.environ['IC_VERBOSITY'] = str(self.prefs.get_attr('user', 'verbosity'))
			os.environ['IC_NUMRECENTFILES'] = str(self.prefs.get_attr('user', 'numrecentfiles'))
			try:
				self.al.setupIconGrid(job=self.job, sort_by=self.sortAppsBy)
			except (AttributeError, KeyError):
				pass


	def globalSettings(self):
		""" Open Icarus global settings dialog wrapper function.
		"""
		if self.openSettings("Global"):
			from . import icarus__env__
			icarus__env__.set_env()
			try:
				os.environ.pop('IC_FIRSTRUN')
			except KeyError:
				pass
			# Add dialog prompt to restart Icarus for changes to take effect?
		else:
			if 'IC_FIRSTRUN' in os.environ:
				sys.exit()


	def appSettings(self):
		""" Open job settings dialog wrapper function.
			Only with apps (temporary bodge)
		"""
		if self.openSettings("App"):
			self.setupJob()


	def preview(self, path=None):
		""" Preview - opens djv_view to preview movie or image sequence.
		"""
		from shared import djvOps
		verbose.launchApp('djv_view')
		if path is None:
			djvOps.viewer(self.gatherPath)  # This is purely a bodge for asset browser - fix at a later date
		else:
			djvOps.viewer(path)


	def openJobManagement(self):
		""" Open Job Management window.
		"""
		from tools.settings import job_management__main__
		jobManagementDialog = job_management__main__.JobManagementDialog(parent=self)
		if jobManagementDialog.display():  # Return True if user clicked Save, False for Cancel
			self.populateJobs()


	def openShotManagement(self):
		""" Open Shot Management window.
			THIS IS THE NEW (WIP) SHOT MANAGEMENT EDITOR...
		"""
		from tools.settings import shot_management__main__
		shotManagementDialog = shot_management__main__.ShotManagementDialog(parent=self)
		shotManagementDialog.display(job=self.ui.job_comboBox.currentText())
		self.populateJobs()


	def openAppPathsEditor(self):
		""" Open the application paths editor dialog.
		"""
		from tools.settings import edit_app_paths
		editAppPathsDialog = edit_app_paths.dialog(parent=self)
		if editAppPathsDialog.display():
			self.setupJob()


	def openEnvVarEditor(self, allvars=False):
		""" Open environment variables editor.
		"""
		from tools.envvarbrowser import envvarbrowser
		self.envVarsDialog = envvar_browser.EnvVarsDialog(parent=self)
		self.envVarsDialog.show()


	def openBatchRename(self):
		""" Open Batch Rename tool.
		"""
		from tools.sequencerename import sequencerename
		try:
			self.batchRenameApp.show()
			self.batchRenameApp.raise_()
		except AttributeError:
			self.batchRenameApp = sequencerename.SequenceRenameApp() #parent=self
			self.batchRenameApp.show()


	def openRenderQueue(self):
		""" Open Render Queue Manager window.
		"""
		from tools.renderqueue import renderqueue
		try:
			self.renderQueueApp.show()
			self.renderQueueApp.raise_()
		except AttributeError:
			self.renderQueueApp = renderqueue.RenderQueueApp()
			self.renderQueueApp.show()


	def openRenderSubmitter(self):
		""" Open Render Submitter dialog window.
		"""
		from tools.renderqueue import submit
		try:
			self.renderSubmitUI.display()
		except AttributeError:
			self.renderSubmitUI = submit.RenderSubmitUI(parent=self)
			self.renderSubmitUI.display()
		except KeyError:
			from tools.renderqueue import rq__env__
			rq__env__.set_env()
			self.renderSubmitUI.display()


	# def openRenderBrowser(self):
	# 	""" Open Render Browser window.
	# 	"""
	# 	import rb__main__
	# 	# reload(rb__main__)  # Python 3 doesn't like this


	# def launchGenericDialog(self, module_name, class_name, modal=True):
	# 	""" Launch generic dialog.
	# 	"""
	# 	importProc = "import %s" %module_name
	# 	instProc = "self.%s = %s.%s(parent=self)" %(class_name, module_name, class_name)
	# 	if modal:
	# 		showProc = "self.%s.ui.exec_()" %class_name
	# 	else:
	# 		showProc = "self.%s.ui.show()" %class_name

	# 	eval(importProc)
	# 	try:
	# 		eval(showProc)
	# 	except AttributeError:
	# 		eval(instProc)
	# 		eval(showProc)


	###############
	# Publish tab #
	###############

	###################adjusting ui####################				


#	#populates the render publish table
#	def renderTableAdd(self):
#		#processes latest path added to self.renderPaths
#		renderPath = self.renderPblBrowse()
#		renderPath = renderPath.replace(os.environ['IC_SHOTPATH'], '$IC_SHOTPATH')
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


	# #sets the selected render layer as the main layer
	# def setLayerAsMain(self, autoMainLayer=None):
	# 	font = QtGui.QFont()
	# 	for rowItem in range(0, self.ui.renderPbl_tableWidget.rowCount()):
	# 		font.setBold(False)
	# 		mainItem = self.ui.renderPbl_tableWidget.item(rowItem, 2)
	# 		mainItem.setText('layer')
	# 		mainItem.setFont(font)
	# 		#mainItem.setBackground(QtGui.QColor(34,34,34))
	# 		rowItem1 = self.ui.renderPbl_tableWidget.item(rowItem, 1)
	# 		rowItem1.setFont(font)
	# 		#rowItem1.setBackground(QtGui.QColor(34,34,34))
	# 		rowItem0 = self.ui.renderPbl_tableWidget.item(rowItem, 0)
	# 		rowItem0.setFont(font)
	# 		#rowItem0.setBackground(QtGui.QColor(34,34,34))
	# 	rowLs = []
	# 	if autoMainLayer:
	# 		selRow = self.ui.renderPbl_tableWidget.row(autoMainLayer)
	# 		rowLs.append(selRow)
	# 	else:
	# 		for selIndex in self.ui.renderPbl_tableWidget.selectedIndexes():
	# 			selItem = self.ui.renderPbl_tableWidget.itemFromIndex(selIndex)
	# 			selRow = self.ui.renderPbl_tableWidget.row(selItem)
	# 			if selRow not in rowLs and selRow != -1:
	# 				rowLs.append(selRow)
	# 	if len(rowLs) == 1:
	# 		font.setBold(True)
	# 		mainItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 2)
	# 		mainItem.setText('main')
	# 		mainItem.setFont(font)
	# 		#mainItem.setBackground(QtGui.QColor(60,75,40))
	# 		passItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 1)
	# 		passName = passItem.text()
	# 		passItem.setFont(font)
	# 		#passItem.setBackground(QtGui.QColor(60,75,40))
	# 		layerItem = self.ui.renderPbl_tableWidget.item(rowLs[0], 0)
	# 		layerName = passItem.text()
	# 		layerItem.setFont(font)
	# 		#layerItem.setBackground(QtGui.QColor(60,75,40))
	# 	#app hide and show forces thw window to update
	# #	app.hide()
	# #	app.show() # This was causing an issue with the UI closing so I've commented it out fot the time being. The widget still seems to auto update.


	def updateRenderPublishUI(self, current, previous):
		""" Update the render publish UI based on the current selection.
		"""
		pass
		# print self.sender()
		# print current, previous


	def renderPreview(self, item, column):
		""" Launches sequence viewer when entry is double-clicked.
		"""
		path = os_wrapper.absolutePath(item.text(3))
		self.preview(sequence.getFirst(path))


	def dailyPreview(self, item, column):
		""" Launches sequence viewer when entry is double-clicked.
		"""
		path = os_wrapper.absolutePath(os.path.join(item.text(3), item.text(0)))
		self.preview(sequence.getFirst(path))


	def setLayerAsMain(self):
		""" Sets the selected render layer as the main layer.
		"""
		rowCount = self.ui.renderPbl_treeWidget.topLevelItemCount()
		for row in range(0, rowCount):
			item = self.ui.renderPbl_treeWidget.topLevelItem(row)
			item.setText(2, 'layer')

		for item in self.ui.renderPbl_treeWidget.selectedItems():
			# item.setText(2, 'main')
			try:
				selectedItem = self.ui.renderPbl_treeWidget.topLevelItem( self.ui.renderPbl_treeWidget.indexOfTopLevelItem(item) )
				selectedItem.setText(2, 'main')
			except AttributeError:
				verbose.warning("Only render layers (not render passes / AOVs) can be set as the main layer.")

		self.ui.renderPbl_treeWidget.resizeColumnToContents(2)


	def renderTableAdd(self):
		""" Adds entries to the render layer tree view widget.
		"""
		shot_dir = os.environ['IC_SHOTPATH']
		start_dir = os.environ.get('IC_MAYA_RENDERS_DIR', shot_dir)
		self.renderPath = self.folderDialog(start_dir)
		self.renderTableUpdate()


	def renderTableRemove(self):
		""" Removes the selected entry from the render layer tree view widget.
		"""
		root = self.ui.renderPbl_treeWidget.invisibleRootItem()
		for item in self.ui.renderPbl_treeWidget.selectedItems():
			(item.parent() or root).removeChild(item)
		# for item in self.ui.renderPbl_treeWidget.selectedItems():
		# 	print self.ui.renderPbl_treeWidget.indexFromItem(item)
		# 	print type(item)
		# 	#self.ui.renderPbl_treeWidget.takeTopLevelItem( self.ui.renderPbl_treeWidget.indexOfTopLevelItem(item) )


	def renderTableUpdate(self):
		""" Populates the render layer tree view widget with entries.
		"""
		renderPath = self.renderPath
		if renderPath:
			renderLayerDirs = []

			# Get subdirectories
			subdirs = next(os.walk(renderPath))[1]
			if subdirs:
				for subdir in subdirs:
					if not subdir.startswith('.'): # ignore directories that start with a dot
						renderLayerDirs.append(subdir)
			if renderLayerDirs:
				renderLayerDirs.sort()
			else: # use parent dir
				renderLayerDirs = [os.path.basename(renderPath)]
				renderPath = os.path.dirname(renderPath)

			# self.ui.renderPbl_treeWidget.setIconSize(QtCore.QSize(128, 72))

			# Add render layers
			for renderLayerDir in renderLayerDirs:
				renderPasses = sequence.getBases(os.path.join(renderPath, renderLayerDir))

				if renderPasses: # only continue if render pass sequences exist in this directory
					renderLayerItem = QtWidgets.QTreeWidgetItem(self.ui.renderPbl_treeWidget)
					# renderLayerItem.setText(0, '%s (%d)' % (renderLayerDir, len(renderPasses)))
					renderLayerItem.setText(0, renderLayerDir)
					renderLayerItem.setText(2, 'layer')
					renderLayerItem.setText(3, os_wrapper.relativePath(os.path.join(renderPath, renderLayerDir), 'IC_SHOTPATH'))

					self.ui.renderPbl_treeWidget.addTopLevelItem(renderLayerItem)
					renderLayerItem.setExpanded(True)

					# Add render passes
					for renderPass in renderPasses:
						renderPassItem = QtWidgets.QTreeWidgetItem(renderLayerItem)
						path, prefix, fr_range, ext, num_frames = sequence.getSequence( os.path.join(renderPath, renderLayerDir), renderPass )

						renderPassItem.setText(0, prefix)
						renderPassItem.setText(1, fr_range)
						if not sequence.check(fr_range):  # Set red text for sequence mismatch
							renderPassItem.setForeground(1, QtGui.QBrush(QtGui.QColor("#f92672")))
						renderPassItem.setText(2, ext.split('.', 1)[1])
						renderPassItem.setText(3, os_wrapper.relativePath(os.path.join(renderPath, renderLayerDir, renderPass), 'IC_SHOTPATH'))

						self.ui.renderPbl_treeWidget.addTopLevelItem(renderPassItem)

			# Resize columns
			self.ui.renderPbl_treeWidget.resizeColumnToContents(0)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(1)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(2)


	def dailyTableAdd(self):
		""" Populates the dailies publish table.
		"""
		# Parse the file path
		dailyPath = self.dailyPblBrowse() # dailyPath is a full path to a file

		if dailyPath:
			self.ui.dailyPbl_treeWidget.clear()

			path, prefix, fr_range, ext, num_frames = sequence.detectSeq(dailyPath, contiguous=True, ignorePadding=False)
			padding = '.'
			if num_frames == 1:
				paddingInt = int(len(fr_range))
			else:
				paddingInt = int((len(fr_range)-1)/2)
			padding += '#' * paddingInt

			if prefix:
				dailyItem = QtWidgets.QTreeWidgetItem(self.ui.dailyPbl_treeWidget)
				dailyItem.setText(0, '%s%s%s' % (prefix, padding, ext)) # dailyItem.setText(0, '%s.[%s]%s' % (prefix, fr_range, ext))
				dailyItem.setText(1, fr_range)
				if not sequence.check(fr_range):  # Set red text for sequence mismatch
					dailyItem.setForeground(1, QtGui.QBrush(QtGui.QColor("#f92672")))
				dailyItem.setText(2, self.dailyType)
				dailyItem.setText(3, os_wrapper.relativePath(path, 'IC_SHOTPATH'))
				self.ui.dailyPbl_treeWidget.addTopLevelItem(dailyItem)
				#dailyItem.setExpanded(True)

			else:
				verbose.noSeq(os.path.basename(dailyPath))

		# Resize columns
		self.ui.dailyPbl_treeWidget.resizeColumnToContents(0)
		self.ui.dailyPbl_treeWidget.resizeColumnToContents(1)
		self.ui.dailyPbl_treeWidget.resizeColumnToContents(2)


	def setDailyType(self):
		""" Sets the dailies type and locks/unlocks the add and remove button
			accordingly.
		"""
		self.dailyType = self.ui.dailyPblType_comboBox.currentText()

		if self.dailyType:
			self.ui.dailyPblAdd_pushButton.setEnabled(True)
		else:
			self.ui.dailyPblAdd_pushButton.setEnabled(False)


	# ################browse dialogs###############	
	# # Browse for assets to publish
	# def assetPblBrowse(self):
	# 	dialogHome = os.environ['IC_JOBPATH']
	# 	self.ui.pathToAsset_lineEdit.setText(self.fileDialog(dialogHome))

	# # Browse for renders to publish
	# def renderPblBrowse(self):
	# 	return self.folderDialog(os.environ['IC_MAYA_RENDERS_DIR'])


	def dailyPblBrowse(self):
		""" Browse for dailies to publish.
			TODO: improve discipline filtering
		"""
		shot_dir = os.environ['IC_SHOTPATH']
		if self.dailyType in ('previs', 'postvis', 'techvis', 'model', 'texturing', 'animation', 'anim', 'fx', 'previs', 'matchmove', 'tracking', 'rigging'):
			start_dir = os.environ.get('IC_MAYA_PLAYBLASTS_DIR', shot_dir)
		elif self.dailyType in ('lighting', 'shading', 'lookdev'):
			start_dir = os.environ.get('IC_MAYA_RENDERS_DIR', shot_dir)
		elif self.dailyType in ('roto', 'prep', 'precomp', 'comp'):
			start_dir = os.environ.get('IC_NUKE_RENDERS_DIR', shot_dir)
		else:
			start_dir = shot_dir

		#print(start_dir)
		if not os.path.isdir(start_dir):
			start_dir = shot_dir

		return self.fileDialog(start_dir)


	#################getting ui options################

	def getMainPblOpts(self):
		""" Get basic publish options before publishing.
		"""
	#	self.approved, self.mail = '', ''
		self.pblNotes = self.ui.notes_textEdit.text() #.toPlainText() # Edited line as notes box is now line edit widget, not text edit
		self.pblType = self.getCurrentTab(self.ui.publishType_tabWidget)[1]
		self.slShot = self.ui.publishToShot_comboBox.currentText()

		# Get path to publish to. If selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.publishToShot_radioButton.isChecked() == 1:
			if self.slShot == os.environ['IC_SHOT']: # publish to current shot
				self.pblTo = os.environ['IC_SHOTPUBLISHDIR']
			else: # publish to user-specified shot
				# self.pblTo = os.path.join(os.environ['IC_JOBPATH'], self.slShot, os.environ['IC_ASSETDIR'])
				self.pblTo = os_wrapper.absolutePath('$IC_JOBPATH/%s/$IC_ASSETDIR' % self.slShot)
		elif self.ui.publishToJob_radioButton.isChecked() == 1: # publish to job
			self.pblTo = os.environ['IC_JOBPUBLISHDIR']
		elif self.ui.publishToLibrary_radioButton.isChecked() == 1: # publish to library
			self.pblTo = os.environ['GLOBALPUBLISHDIR']

	#	if self.ui.approved_checkBox.checkState() == 2:
	#		self.approved = True
	#	if self.ui.mail_checkBox.checkState() == 2:
	#		self.mail = True


	def get_maya_assetPblOpts(self, genericAsset=False):
		""" Get Maya asset publish options.
		"""
		self.textures, self.subsetName, self.sceneName = '', '', ''
		self.chkLs = [] #self.chkLs = [self.pblNotes]
		if self.ui.textures_checkBox.checkState() == 2:
			self.textures = True
		if self.ui.subSet_checkBox.checkState() == 2:
			self.subsetName = '%s_sbs' % self.ui.subSetName_lineEdit.text()
			self.chkLs.append(self.subsetName)
		if self.ui.scene_toolButton.isChecked() == True:
			self.sceneName = self.ui.assetName_lineEdit.text()
			self.chkLs.append(self.sceneName)


	def get_nuke_assetPblOpts(self, name=True):
		""" Get Nuke asset publish options.
		"""
		self.chkLs = [] #self.chkLs = [self.pblNotes]
		if name:
			self.pblName = self.ui.nk_PblName_lineEdit.text()
			self.chkLs.append(self.pblName)


	def getDailyPblOpts(self):
		""" Get information about dailies before publishing.
		"""
		rowCount = self.ui.dailyPbl_treeWidget.topLevelItemCount()

		if rowCount == 1: # only allow one sequence to be published at a time
			dailyItem = self.ui.dailyPbl_treeWidget.topLevelItem(0)
			dailyPblOpts = (dailyItem.text(0), dailyItem.text(1), dailyItem.text(2), dailyItem.text(3))

		else:
			rowCount = None
			dailyPblOpts = None

		#self.chkLs = [self.pblNotes, rowCount]
		self.chkLs = [rowCount]
		return dailyPblOpts


	def getRenderPblOpts(self):
		""" Get information about renders before publishing. - THIS NEEDS RE-CODING
		"""
		self.renderDic = {}
		self.streamPbl, self.mainLayer = '', ''
		if self.ui.streamPbl_checkBox.checkState() == 2:
			self.streamPbl = True

		rowCount = self.ui.renderPbl_treeWidget.topLevelItemCount()
		for row in range(0, rowCount):
			renderLayerItem = self.ui.renderPbl_treeWidget.topLevelItem(row)

			layerName = renderLayerItem.text(0)
			filePath = renderLayerItem.text(3)
			self.renderDic[layerName] = filePath

			if renderLayerItem.text(2) == 'main':
				self.mainLayer = layerName

		if not rowCount:
			rowCount = None

		#self.chkLs = [self.pblNotes, rowCount]
		self.chkLs = [rowCount]
		# print self.renderDic, self.streamPbl, self.mainLayer


	def initPublish(self):
		""" Initialises publish.
			Ultimately this whole system should be rewritten.
		"""
		self.getMainPblOpts()
		# print(self.pblTo, self.pblNotes, self.pblType, self.slShot)

		###############
		# MAYA ASSETS #
		###############
		if self.pblType == 'Maya Asset':

			self.get_maya_assetPblOpts()
			#print(self.chkLs)
			if not pblChk.chkOpts(self.chkLs):
				return

			# Model
			elif self.ui.model_toolButton.isChecked() == True:
				from publish import ma_mdlPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_mdlPbl.publish(self.pblTo, self.slShot.replace('/', '_'), subtype, self.textures, self.pblNotes)
				#assetPublish.publish(genericOpts, 'ma_model', assetTypeOpts)

			# Rig
			elif self.ui.rig_toolButton.isChecked() == True:
				from publish import ma_rigPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_rigPbl.publish(self.pblTo, self.slShot.replace('/', '_'), subtype, self.textures, self.pblNotes)

			# Camera
			if self.ui.camera_toolButton.isChecked() == True:
				from publish import ma_camPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_camPbl.publish(self.pblTo, self.slShot.replace('/', '_'), subtype, self.pblNotes)

			# Geo
			elif self.ui.geo_toolButton.isChecked() == True:
				from publish import ma_geoPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_geoPbl.publish(self.pblTo, self.slShot.replace('/', '_'), subtype, self.textures, self.pblNotes)

			# Geo cache
			elif self.ui.geoCache_toolButton.isChecked() == True:
				from publish import ma_geoChPbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_geoChPbl.publish(self.pblTo, self.slShot.replace('/', '_'), subtype, self.pblNotes)

			# Animation
			elif self.ui.animation_toolButton.isChecked() == True:
				from publish import ma_animPbl
				ma_animPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblNotes)

			# Shader
			elif self.ui.shader_toolButton.isChecked() == True:
				from publish import ma_shdPbl
				ma_shdPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.subsetName, self.textures, self.pblNotes)

			# FX
			elif self.ui.fx_toolButton.isChecked() == True:
				from publish import ma_fxPbl
				ma_fxPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.subsetName, self.textures, self.pblNotes)

			# Point cloud
			elif self.ui.ma_pointCloud_toolButton.isChecked() == True:
				from publish import ma_pointCloudPbl
				ma_pointCloudPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.subsetName, self.textures, self.pblNotes)

			# Shot
			elif self.ui.shot_toolButton.isChecked() == True:
				from publish import ma_shotPbl
				ma_shotPbl.publish(self.pblTo, self.pblNotes) # self.subsetName, self.textures ?

			# Scene
			elif self.ui.scene_toolButton.isChecked() == True:
				from publish import ma_scnPbl
				ma_scnPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.sceneName, self.subsetName, self.textures, self.pblNotes)

			# Node
			elif self.ui.ma_node_toolButton.isChecked() == True:
				from publish import ma_nodePbl
				subtype = self.ui.assetSubType_comboBox.currentText()
				ma_nodePbl.publish(self.pblTo, self.slShot.replace('/', '_'), subtype, self.textures, self.pblNotes)

		###############
		# NUKE ASSETS #
		###############
		if self.pblType == 'Nuke Asset':

			self.get_nuke_assetPblOpts()
			# if not pblChk.chkOpts(self.chkLs):
			# 	return

			# Card
			if self.ui.card_toolButton.isChecked() == True:
				from publish import nk_setupPbl
				self.pblType = 'card'
				nk_setupPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblType, self.pblName, self.pblNotes)

			# Point cloud
			elif self.ui.nk_pointCloud_toolButton.isChecked() == True:
				from publish import nk_setupPbl
				self.pblType = 'pointCloud'
				nk_setupPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblType, self.pblName, self.pblNotes)

			# Node
			elif self.ui.nk_node_toolButton.isChecked() == True:
				from publish import nk_setupPbl
				self.pblType = 'node'
				nk_setupPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblType, self.pblName, self.pblNotes)

			# Comp
			elif self.ui.comp_toolButton.isChecked() == True:
				self.get_nuke_assetPblOpts(name=False)
				# if not pblChk.chkOpts(self.chkLs):  # Check for entries in mandatory fields
				# 	return
				from publish import nk_compPbl
				self.pblType = 'comp'
				nk_compPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblType, self.pblNotes)

			# Pre-comp
			elif self.ui.precomp_toolButton.isChecked() == True:
				from publish import nk_setupPbl
				self.pblType = 'preComp'
				nk_setupPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblType, self.pblName, self.pblNotes)

			# Setup
			elif self.ui.setup_toolButton.isChecked() == True:
				from publish import nk_setupPbl
				self.pblType = 'setup'
				nk_setupPbl.publish(self.pblTo, self.slShot.replace('/', '_'), self.pblType, self.pblName, self.pblNotes)	

		###########
		# DAILIES #
		###########
		elif self.pblType == 'Dailies':
			from publish import ic_dailyPbl
			self.getDailyPblOpts() # required just to get self.checkLs
			if not pblChk.chkOpts(self.chkLs):  # Check for entries in mandatory fields
				return
			ic_dailyPbl.publish(self.getDailyPblOpts(), self.pblTo, self.pblNotes)

		###########
		# RENDERS #
		###########
		elif self.pblType == 'Render':
			from publish import ic_renderPbl
			self.getRenderPblOpts()
			# if not pblChk.chkOpts(self.chkLs):  # Check for entries in mandatory fields
			# 	return
			ic_renderPbl.publish(self.renderDic, self.pblTo, self.mainLayer, self.streamPbl, self.pblNotes)


	##############
	# Gather tab #
	##############

	def adjustGatherTab(self, showGatherButton=False):
		""" UI adjustments.
		"""
		self.ui.gather_pushButton.setEnabled(False)
		if showGatherButton:
			self.ui.gather_pushButton.setEnabled(True)


	def getGatherFrom(self):
		""" Get location from which to gather assets.
		"""
		slShot = self.ui.gatherFromShot_comboBox.currentText()

		# Get path to gather from. If selected shot doesn't match shot the correct publish path is assigned based on the selected shot
		if self.ui.gatherFromShot_radioButton.isChecked() == 1:
			if slShot == os.environ['IC_SHOT']: # gather from current shot
				self.gatherFrom = os.environ['IC_SHOTPUBLISHDIR']
			else: # gather from user-specified shot
				self.gatherFrom = os.path.join(os.environ['IC_JOBPATH'], slShot, os.environ['IC_ASSETDIR'])
		elif self.ui.gatherFromJob_radioButton.isChecked() == 1: # gather from job
			self.gatherFrom = os.environ['IC_JOBPUBLISHDIR']
		elif self.ui.gatherFromLibrary_radioButton.isChecked() == 1: # gather from library
			self.gatherFrom = os.environ['GLOBALPUBLISHDIR']


	###################columns system, info and preview img update##################

	def defineColumns(self):
		""" Define short names for asset browser columns.
		"""
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
		if os.environ['IC_ENV'] == 'MAYA':
			return ('ma', 'ic')
		elif os.environ['IC_ENV'] == 'NUKE':
			return ('nk', 'ic', 'render')
		else:
			return ('ma', 'nk', 'ic', 'render', 'daily', 'dailies') # daily -> dailies

	#populates columns
	def fillColumn(self, column, searchPath):
		envPrefix = self.getAssetEnvPrefix()
		try:
			itemLs = os.listdir(searchPath)
			itemLs.sort()
		except:
			itemLs = []
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
					if item == 'scripts' or item == 'icons' or item == 'ma_shelves':  # bodge
						pass
					else:
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


	def updateImgPreview(self):
		""" Update image preview field with snapshot.
		"""
		# Apply context menu to open viewer - DO THIS SOMEWHERE ELSE
	#	self.ui.gatherImgPreview_label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
	#	self.actionPreview = QtWidgets.QAction("Preview...", None)
	#	self.actionPreview.triggered.connect(self.preview)
	#	self.ui.gatherImgPreview_label.addAction(self.actionPreview)

		from publish import previewImg
		imgPath = previewImg.getImg(self.gatherPath, forceExt='jpg')
		pixmap = QtGui.QPixmap(imgPath)
		self.ui.gatherImgPreview_label.setScaledContents(True)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)


	def updateInfoField(self):
		""" Update info field with notes and other relevant data.
		"""
		self.adjustGatherTab(showGatherButton = True)
		self.assetVersion = self.aVersionCol.currentItem().text()
		self.gatherPath = os.path.join(self.gatherFrom, self.assetType, self.assetName, self.assetSubType, self.assetVersion)

		from shared import json_metadata as metadata
		# Instantiate JSON data classes
		assetData = metadata.Metadata(
			os.path.join(self.gatherPath, 'asset_data.json'))

		# from shared import xml_metadata as metadata
		# # Instantiate XML data classes
		# assetData = metadata.Metadata()
		# assetDataLoaded = assetData.load(
		# 	datafile=os.path.join(self.gatherPath, 'assetData.xml'))

		# # --------------------------------------------------------------------
		# # If XML files don't exist, create defaults, and attempt to convert
		# # data from Python data files.
		# # This code may be removed in the future.
		# if not assetDataLoaded:
		# 	from shared import legacy_metadata

		# 	# Try to convert from icData.py to XML (legacy assets)
		# 	if legacy_metadata.convertAssetData(self.gatherPath, assetData):
		# 		assetData.reload()
		# 	else:
		# 		return False
		# # --------------------------------------------------------------------

		# Print info to text field
		infoText = ""
		notes = assetData.get_attr('asset', 'notes')
		if notes:
			infoText += "%s\n\n" % notes
		infoText += "Published by %s\n%s" % (assetData.get_attr('asset', 'user'), assetData.get_attr('asset', 'timestamp'))
		source = assetData.get_attr('asset', 'assetSource')
		if source:
			infoText += "\nFrom '%s'" % source #os.path.basename(source)

		self.ui.gatherInfo_textEdit.setText(infoText)


	def initGather(self):
		""" Initialise gather.
		"""
		if os.environ['IC_ENV'] == 'MAYA':
			if self.assetType == 'ma_anim':
				from publish import ma_animGather
				ma_animGather.gather(self.gatherPath)
			else:
				from publish import ma_assetGather
				if ma_assetGather.gather(self.gatherPath):
					verbose.message("Successfully gathered asset.")

		elif os.environ['IC_ENV'] == 'NUKE':
			if self.assetType in ('ic_geo', 'ic_pointCloud'):
				from publish import nk_geoGather
				nk_geoGather.gather(self.gatherPath)
			elif self.assetType == 'render':
				from publish import nk_renderGather
				self.hide()
				nk_renderGather.gather(self.gatherPath)
				self.show()
			else:
				from publish import nk_assetGather
				nk_assetGather.gather(self.gatherPath)


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main application class
# ============================================================================
# Run functions
# ----------------------------------------------------------------------------

def main_application():
	""" Return main Qt Application object.
	"""
	return QtWidgets.QApplication(sys.argv)


def get_style():
	""" Return recommended Qt application style.
		On Windows best results are obtained when this is disabled.
		On Mac, best option is unclear due to inconsistent results.
		Linux has not been tested.
	"""
	if os.environ['IC_RUNNING_OS'] == "MacOS":
		styles = QtWidgets.QStyleFactory.keys()
		if 'Fusion' in styles:
			return 'Fusion'  # Qt5
		elif 'Plastique' in styles:
			return 'Plastique'  # Qt4
	return None


def get_window(app='standalone', parent=None, **kwargs):
	""" Return main Icarus window - 'parent' will be ignored unless 'app' is
		'standalone'.
	"""
	if app == 'standalone':
		pass
	elif app == 'maya':
		parent = UI._maya_main_window()
	elif app == 'houdini':
		parent = UI._houdini_main_window()
	elif app == 'nuke':
		parent = UI._nuke_main_window()

	# Instantiate main application class
	ic_app = IcarusApp(parent, **kwargs)

	# Set window title, flags and application icon
	if app == 'standalone':
		ic_app.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
		ic_app.setWindowIcon(QtGui.QIcon(os.path.join(os.environ['IC_FORMSDIR'], 'icons', 'icarus.png')))

		# Workaround for Windows to use correct icon on the taskbar...
		try:
			import ctypes
			myappid = u'mycompany.myproduct.subproduct.version'  # arbitrary string
			ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
		except:
			pass

	return ic_app


##############
# RUN ICARUS #
##############

# Python version check
try:
	assert sys.version_info >= (2,7)
except AssertionError:
	sys.exit("ERROR: %s requires Python version 2.7 or above." % NAME)

# Enable high DPI scaling - TODO: move this to ui_template?
try:
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
except AttributeError:
	verbose.debug("High DPI scaling not available in Qt %s. User Interface elements may not display correctly on high DPI display devices." %QtCore.qVersion())

if __name__ == '__main__':
	main_app = main_application()
	icarus = get_window()
	icarus.show()
	sys.exit(main_app.exec_())
