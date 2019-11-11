#!/usr/bin/python

# [Icarus] versionManager.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# Launches and controls the Icarus Version Manager UI.
# TODO: If XML metadata not found, fall back to legacy python icData.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
from shared import settingsData


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Version Manager"
WINDOW_OBJECT = "versionManagerUI"

# Set the UI and the stylesheet
UI_FILE = "version_manager_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Version Manager dialog class.
	"""
	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.update_pushButton.clicked.connect(self.update)
		self.ui.cancel_pushButton.clicked.connect(self.reject)
		self.ui.assetVersion_listWidget.currentItemChanged.connect(self.reloadVersionDetails)
		#self.ui.assetVersion_listWidget.itemClicked.connect(self.reloadVersionDetails)


	def display(self, assetRootDir, version, modal=True):
		""" Display the dialog.
		"""
		self.assetRootDir = os.path.expandvars(assetRootDir)

		# Instantiate XML data classes
		self.assetData = settingsData.SettingsData()
		self.assetData.loadXML(os.path.join(self.assetRootDir, version, 'assetData.xml'), use_template=False, quiet=False)

		# Set asset label text
		self.ui.asset_label.setText( self.assetData.getValue('asset', 'assetPblName') )

		self.updateVersion = ''
		self.updateAssetVersionCol( self.assetData.getValue('asset', 'version'), setCurrentVersion=True )
		self.reloadVersionDetails()

		if modal:
			self.exec_()
			return self.updateVersion
		else:
			self.show()


	##################################
	# Content load/refresh functions #
	##################################

	def reloadVersionDetails(self):
		""" Reloads all details related to selected version.
		"""
		selVersion = self.ui.assetVersion_listWidget.currentItem().text()
		assetDir = os.path.join(self.assetRootDir, selVersion)

		assetDataLoaded = self.assetData.loadXML(os.path.join(assetDir, 'assetData.xml'), use_template=False, quiet=False)

		# --------------------------------------------------------------------
		# If XML files don't exist, create defaults, and attempt to convert
		# data from Python data files.
		# This code may be removed in the future.
		if not assetDataLoaded:
			from shared import legacySettings

			# Try to convert from icData.py to XML (legacy assets)
			if legacySettings.convertAssetData(assetDir, self.assetData):
				self.assetData.loadXML()
			else:
				return False
		# --------------------------------------------------------------------

		# Update image preview and info field
		self.updateImgPreview(assetDir)
		self.updateInfoField()


	def updateAssetVersionCol(self, version, setCurrentVersion=False):
		""" Update asset version list widget.
		"""
		# Get list of all asset versions
		versionLs = os.listdir(self.assetRootDir)
		versionLs = sorted(versionLs, reverse=True)

		# Clear and re-populate version list widget
		self.ui.assetVersion_listWidget.clear()
		for item in versionLs:
			if not item.startswith('.'):
				self.ui.assetVersion_listWidget.addItem(item)

		# Select the current version
		if setCurrentVersion:
			selVersionItem = self.ui.assetVersion_listWidget.findItems(version, QtCore.Qt.MatchRegExp)
			self.ui.assetVersion_listWidget.setCurrentItem(selVersionItem[0])


	def updateImgPreview(self, assetDir):
		""" Update image preview field with snapshot.
		"""
		from publish import previewImg
		imgPath = previewImg.getImg(assetDir, forceExt='jpg')
		pixmap = QtGui.QPixmap(imgPath)
		self.ui.gatherImgPreview_label.setScaledContents(True)
		self.ui.gatherImgPreview_label.setPixmap(pixmap)


	def updateInfoField(self):
		""" Update info field with notes and other relevant data.
		"""
		infoText = ""
		notes = self.assetData.getValue('asset', 'notes')
		if notes:
			infoText += "%s\n\n" % notes
		infoText += "Published by %s\n%s" % (self.assetData.getValue('asset', 'user'), self.assetData.getValue('asset', 'timestamp'))
		source = self.assetData.getValue('asset', 'assetSource')
		if source:
			infoText += "\nFrom '%s'" % source #os.path.basename(source)

		self.ui.gatherInfo_textEdit.setText(infoText)


	def update(self):
		""" Dialog accept function.
		"""
		self.updateVersion = self.ui.assetVersion_listWidget.currentItem().text()
		self.accept()

