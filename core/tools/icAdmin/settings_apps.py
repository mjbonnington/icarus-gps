#!/usr/bin/python

# [Icarus] settings_apps.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Applications settings handler.


import os

from Qt import QtWidgets

# Import custom modules
import appPaths


class helper():

	def __init__(self, parent, frame):
		""" Setup application properties panel.
		"""
		self.frame = frame
		self.parent = parent

		self.jd = parent.xd
		self.ap = appPaths.appPaths()
		ap_load = self.ap.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'appPaths.xml'))

		self.setupAppVersions()


	def setupAppVersions(self, selectCurrent=True):
		""" Setup application version properties panel and populate combo
			boxes.
		"""
		noSelectText = ""
		apps = self.ap.getApps()  # Get apps and versions
		formLayout = self.frame.findChildren(QtWidgets.QFormLayout, 'formLayout')[0]
		appPaths_pushButton = self.frame.appPaths_pushButton

		formLayout.setWidget(len(apps), QtWidgets.QFormLayout.FieldRole, appPaths_pushButton)  # Move edit button to bottom of form
		appPaths_pushButton.clicked.connect(lambda: self.appPathsEditor())

		for i, app in enumerate(apps):
			label = QtWidgets.QLabel(self.frame)
			label.setObjectName("%s_label" %app)
			label.setText("%s:" %app)
			formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, label)

			comboBox = QtWidgets.QComboBox(self.frame)
			comboBox.setObjectName("%s_comboBox" %app)
			comboBox.setProperty('xmlTag', app)
			# print(comboBox.property('xmlTag'))
			comboBox.clear()

			versions = self.ap.getVersions(app)  # Populate the combo box with available app versions
			availableVersions = [noSelectText, ]  # Leave a blank entry in case we want to leave version undefined
			for version in versions:
				if version == '[template]':
					pass
				else:
					availableVersions.append(version)
			for version in availableVersions:
				comboBox.addItem(version)

			if selectCurrent:  # Set selection to correct entry
				try:
					text = self.jd.getAppVersion(app)
				except AttributeError:
					text = noSelectText
					# comboBox.insertItem(text, 0)
				#print("%s: %s" %(app, text))
				comboBox.setCurrentIndex(comboBox.findText(text))

			# comboBox.currentIndexChanged.connect(lambda index: self.parent.storeComboBoxValue(index))
			formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, comboBox)


	def appPathsEditor(self):
		""" Open the application paths editor dialog.
		"""
		import edit_app_paths
		editAppPathsDialog = edit_app_paths.dialog(parent=self.parent)
		if editAppPathsDialog.display():
			self.ap.loadXML()  # Reload XML and update comboBox contents after closing dialog
			self.parent.openProperties('apps')
