#!/usr/bin/python

# Icarus Admin Tools
# Job Settings editor dialog
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios


from PySide import QtCore, QtGui
from job_settings_ui import *
import os, sys

# Initialise Icarus environment
sys.path.append(os.environ['ICWORKINGDIR'])
import env__init__
env__init__.setEnv()
env__init__.appendSysPaths()

import jobSettings, appPaths


class jobSettingsDialog(QtGui.QDialog):

	def __init__(self, parent = None):
		#QtGui.QDialog.__init__(self, parent)
		super(jobSettingsDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Load data from xml file
		self.jd = jobSettings.jobSettings()
		jd_load = self.jd.loadXML(os.path.join(os.environ['JOBDATA'], 'jobData.xml'))
		self.ap = appPaths.appPaths()
		ap_load = self.ap.loadXML(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'appPaths.xml'))

		if jd_load and ap_load:
			self.init()
		else:
			print "ERROR"

		# Connect signals and slots
		self.ui.appPaths_pushButton.clicked.connect(self.appPathsEditor)
		# Work out a way to do this procedurally
#		self.ui.Maya_comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion('Maya', x) )
#		self.ui.Mudbox_comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion('Mudbox', x) )
#		self.ui.Nuke_comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion('Nuke', x) )
#		self.ui.Mari_comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion('Mari', x) )
#		self.ui.RealFlow_comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion('RealFlow', x) )
#		self.ui.HieroPlayer_comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion('HieroPlayer', x) )

		self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.init)
		#self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.ap.saveXML)
		self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Close).clicked.connect(self.exit)


	def init(self):
		""" Initialise or reset by reloading data
		"""
		# Populate fields
#		self.populateJobSettings()
#		self.populateTimeSettings()
#		self.populateResSettings()
#		self.populateAppSettings()
#		self.populateOtherSettings()

		self.ui.projNum_spinBox.setValue( int(self.jd.getText("./job/proj-num")) )
		self.ui.jobNum_spinBox.setValue( int(self.jd.getText("./job/job-num")) )
		self.ui.client_lineEdit.setText( self.jd.getText("./job/client") )
		self.ui.brand_lineEdit.setText( self.jd.getText("./job/brand") )
		self.ui.title_lineEdit.setText( self.jd.getText("./job/title") )
		self.ui.deliverable_lineEdit.setText( self.jd.getText("./job/deliverable") )

		self.ui.fps_spinBox.setValue( int(self.jd.getText("./time/fps")) )
		self.ui.rangeStart_spinBox.setValue( int(self.jd.getAttr("./time/range", "start")) )
		self.ui.rangeEnd_spinBox.setValue( int(self.jd.getAttr("./time/range", "end")) )
		self.ui.handles_spinBox.setValue( int(self.jd.getText("./time/handles")) )

		self.ui.resX_spinBox.setValue( int(self.jd.getAttr("./res/full", "x")) )
		self.ui.resY_spinBox.setValue( int(self.jd.getAttr("./res/full", "y")) )
		self.ui.proxyResX_spinBox.setValue( int(self.jd.getAttr("./res/proxy", "x")) )
		self.ui.proxyResY_spinBox.setValue( int(self.jd.getAttr("./res/proxy", "y")) )

		self.populateAppVersions()

		self.ui.board_lineEdit.setText( self.jd.getText("./other/production-board") )


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering OK / Cancel buttons
		"""
		pass
#		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
#			return


	def populateAppVersions(self, selectCurrent=True):
		""" Populate application version combo boxes
		"""
		apps = self.jd.getApps() # Get apps and versions
		pass # Append apps from appPaths
		self.ui.apps_formLayout.setWidget(len(apps), QtGui.QFormLayout.FieldRole, self.ui.appPaths_pushButton) # Move edit button to bottom of form

		for i, app in enumerate(apps):
			label = QtGui.QLabel(self.ui.apps_groupBox)
			label.setObjectName("%s_label" %app[0])
			label.setText("%s:" %app[0])
			self.ui.apps_formLayout.setWidget(i, QtGui.QFormLayout.LabelRole, label)

			comboBox = QtGui.QComboBox(self.ui.apps_groupBox)
			comboBox.setObjectName("%s_comboBox" %app[0])
			comboBox.clear()
			versions = self.ap.getVersions(app[0]) # Popluate the combo box with available app versions
			availableVersions = []
			for version in versions:
				if version == '[template]':
					pass
				else:
					availableVersions.append(version)
			for version in availableVersions:
				comboBox.addItem(version)
			if selectCurrent: # Set selection to correct entry
				comboBox.setCurrentIndex( comboBox.findText(app[1]) )
			#QtCore.QObject.connect(comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), lambda x: self.storeAppVersion(x) )
			#comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion(app[0], availableVersions[x]) )
			self.ui.apps_formLayout.setWidget(i, QtGui.QFormLayout.FieldRole, comboBox)


	def storeAppVersion(self, app, ver):
		""" Store Application version
		"""
		#self.jd.setAppVersion(app, version)
		print app, ver


	def appPathsEditor(self):
		""" Open the application paths editor dialog
		"""
		import set_app_paths__main__
		reload(set_app_paths__main__)
		setAppPaths = set_app_paths__main__.setAppPathsDialog()
		setAppPaths.show()
		#sys.exit(setAppPaths.exec_())
		setAppPaths.exec_()

		# Update comboBox contents after closing application paths dialog
		self.populateAppVersions(selectCurrent=False)


	def exit(self):
		""" Exit the dialog
		"""
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	jobSettingsEditor = jobSettingsDialog()

	jobSettingsEditor.show()
	sys.exit(jobSettingsEditor.exec_())
