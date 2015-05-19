#!/usr/bin/python

# Icarus Admin Tools
# Job Settings editor dialog
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios


from PySide import QtCore, QtGui
from job_settings_ui import *
import os, sys, math

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
			print "DATA ERROR"
			self.init()

		# Connect signals and slots
		self.ui.categories_listWidget.currentItemChanged.connect( lambda current: self.openProperties(current.text()) )

##		self.ui.appPaths_pushButton.clicked.connect(self.appPathsEditor)

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
		# Populate categories
		#categories = self.jd.getCategories()
		categories = ['job', 'units', 'time', 'resolution', 'apps', 'other']

		for cat in categories:
			self.ui.categories_listWidget.addItem(cat)

		# Set the maximum size of the list widget
		self.ui.categories_listWidget.setMaximumWidth( self.ui.categories_listWidget.sizeHintForColumn(0) + 64 )

		# Select the first item & show the appropriate settings panel
		self.ui.categories_listWidget.item(0).setSelected(True)
		self.openProperties( self.ui.categories_listWidget.item(0).text() )

##		self.populateAppVersions()


	def noop(self):
		""" Empty function to do nothing (used to connect to a signal)
		"""
		pass


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering OK / Cancel buttons
		"""
		pass
#		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
#			return


	def importUI(self, ui_file, frame):
		""" Import specified UI file and insert into specified frame
		"""
		exec('from %s import *' %ui_file)
		#exec('reload(%s)' %ui_file)
		properties_panel = Ui_settings_frame()
		properties_panel.setupUi(frame)


	def openProperties(self, category):
		""" Open properties panel for selected settings category
		"""
		# Reload job data
		#self.jd.loadXML()

		# Create new frame to hold properties UI
		self.ui.settings_frame.close()
		self.ui.settings_frame = QtGui.QFrame(self.ui.settings_scrollAreaWidgetContents)
		self.ui.settings_frame.setObjectName("settings_frame")
		self.ui.verticalLayout_2.addWidget(self.ui.settings_frame)

		# Load approprate UI file into frame
		self.importUI('settings_%s_ui' %category, self.ui.settings_frame)

		# Load data
		#print "[%s]" %category

		if category == 'apps':
			self.populateAppVersions(self.ui.settings_frame)

		if category == 'resolution':
			self.setupRes()

		widgets = self.ui.settings_frame.children()
		for widget in widgets:
			# TODO: only connect widgets which have a dynamic property attached
			attr = widget.objectName().split('_')[0]

			if isinstance(widget, QtGui.QComboBox):
				#widget.setValue( int(self.jd.getText(category, widget.property('xmlAttr'))) )
				try:
					text = self.jd.getText(category, attr)
					widget.setCurrentIndex( widget.findText(text) )
				except AttributeError:
					pass
					#text = ""
				print "%s: %s" %(attr, widget.currentText())

			if isinstance(widget, QtGui.QLineEdit):
				#widget.setText( self.jd.getText(category, widget.property('xmlAttr')) )
				try:
					text = self.jd.getText(category, attr)
					widget.setText(text)
				except AttributeError:
					pass
					#text = ""
				print "%s: %s" %(attr, widget.text())
				#widget.editingFinished.connect( lambda current: self.jd.setText(category, attr, current.text()) )
			#	widget.s = QtCore.Signal()
			#	widget.s.connect = lambda f: self.connect(widget.s, f)
				#widget.editingFinished.connect( func )

			if isinstance(widget, QtGui.QSpinBox):
				#widget.setValue( int(self.jd.getText(category, widget.property('xmlAttr'))) )
				try:
					value = int( self.jd.getText(category, attr) )
					widget.setValue(value)
				except AttributeError:
					pass
					#value = 0
				print "%s: %s" %(attr, widget.value())


# We monkey-patch signal to tell you when it is being connected to.
#	def connect(self, f):
#		print("Boy just got a new connection")
#		QtCore.Signal.connect(self, f)

	def bollox(self, val='tosser'):
		print val


	def populateAppVersions(self, frame, selectCurrent=True):
		""" Populate application version combo boxes
		"""
		noSelectText = ""
		apps = self.ap.getApps() # Get apps and versions
		formLayout = frame.findChildren(QtGui.QFormLayout, 'formLayout')
		appPaths_pushButton = frame.findChildren(QtGui.QPushButton, 'appPaths_pushButton')

		formLayout[0].setWidget(len(apps), QtGui.QFormLayout.FieldRole, appPaths_pushButton[0]) # Move edit button to bottom of form
		appPaths_pushButton[0].clicked.connect(self.appPathsEditor)

		for i, app in enumerate(apps):
			label = QtGui.QLabel(frame)
			label.setObjectName("%s_label" %app)
			label.setText("%s:" %app)
			formLayout[0].setWidget(i, QtGui.QFormLayout.LabelRole, label)

			comboBox = QtGui.QComboBox(frame)
			comboBox.setObjectName("%s_comboBox" %app)
			comboBox.clear()
			versions = self.ap.getVersions(app) # Popluate the combo box with available app versions
			availableVersions = []
			for version in versions:
				if version == '[template]':
					#pass
					availableVersions.append(noSelectText)
				else:
					availableVersions.append(version)
			for version in availableVersions:
				comboBox.addItem(version)

			if selectCurrent: # Set selection to correct entry
				try:
					text = self.jd.getAppVersion(app)
				except AttributeError:
					text = noSelectText
					#comboBox.insertItem(text, 0)
				print "%s: %s" %(app, text)
				comboBox.setCurrentIndex( comboBox.findText(text) )

			#QtCore.QObject.connect(comboBox, QtCore.SIGNAL('currentIndexChanged(int)'), lambda x: self.storeAppVersion(x) )
			#comboBox.currentIndexChanged.connect( lambda x: self.storeAppVersion(app[0], availableVersions[x]) )
			formLayout[0].setWidget(i, QtGui.QFormLayout.FieldRole, comboBox)


	def setupRes(self):
		""" Setup resolution properties panel
		"""
		frame = self.ui.settings_frame

		#children = frame.children()
		#for child in children:
		#	print child.objectName()

		self.calcAR()

		# Connect signals and slots
		#frame.findChildren(QtGui.QComboBox, 'resPreset_comboBox')[0].currentIndexChanged.connect(self.updateRes)
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].valueChanged.connect(self.updateResFullWidth)
		#frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].valueChanged.connect(self.updateResFullHeight)
		frame.findChildren(QtGui.QRadioButton, 'proxyModeScale_radioButton')[0].toggled.connect(self.calcProxyRes)
		frame.findChildren(QtGui.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].valueChanged.connect(self.calcProxyRes)
		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].valueChanged.connect(self.updateResProxyWidth)
		#frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].valueChanged.connect(self.updateResProxyHeight)
		frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].stateChanged.connect(self.calcAR)


	def calcAR(self, value=0):
		""" Calculate aspect ratio
		"""
		frame = self.ui.settings_frame

		fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullHeight = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
		self.aspectRatio = float(fullWidth) / float(fullHeight)

		print "aspect ratio: %f" %self.aspectRatio


	def updateResFullWidth(self, value=0):
		""" 
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		#frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].valueChanged.connect(self.noop)
		#frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].valueChanged.disconnect(self.updateResFullHeight)

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			height = int(math.ceil(value/self.aspectRatio))
		else:
			height = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
		fullRes = value, height

#		fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
#		fullHeight = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
#		aspectRatio = float(fullWidth) / float(fullHeight)

#		if preserveAR:
#			#fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
#			fullRes = fullWidth, float(fullWidth / 2)
#		else:
#			fullRes = fullWidth, fullHeight

#		#fullRes = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value(), frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
#		#aspectRatio = float(fullRes[0]) / float(fullRes[1])

		self.calcProxyRes()
		frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].setValue(height)

		print fullRes, self.aspectRatio


	def updateResFullHeight(self, value=0):
		""" 
		"""
		frame = self.ui.settings_frame

		# Stop the other widgets from emitting signals
		#frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].valueChanged.connect(self.noop)
		#frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].valueChanged.disconnect(self.updateResFullWidth)

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			width = int(math.ceil(value*self.aspectRatio))
		else:
			width = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullRes = width, value

		self.calcProxyRes()
		frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].setValue(width)

		print fullRes, self.aspectRatio


	def calcProxyRes(self): #, fullWidth, fullHeight):
		""" Calculate proxy resolution
		"""
		frame = self.ui.settings_frame

		fullWidth = frame.findChildren(QtGui.QSpinBox, 'fullWidth_spinBox')[0].value()
		fullHeight = frame.findChildren(QtGui.QSpinBox, 'fullHeight_spinBox')[0].value()
		fullRes = fullWidth, fullHeight

		if frame.findChildren(QtGui.QRadioButton, 'proxyModeScale_radioButton')[0].isChecked():
			proxyMode = 'scale'
			proxyScale = frame.findChildren(QtGui.QDoubleSpinBox, 'proxyScale_doubleSpinBox')[0].value()
			proxyRes = int(fullRes[0] * proxyScale), int(fullRes[1] * proxyScale)
		else:
			proxyMode = 'res'
			proxyRes = frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].value(), frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].value()
			proxyScale = 0

		frame.findChildren(QtGui.QSpinBox, 'proxyWidth_spinBox')[0].setValue(proxyRes[0])
		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].setValue(proxyRes[1])

		print "proxy res: %dx%d" %(proxyRes[0], proxyRes[1])


	def updateResProxyWidth(self, value=0):
		""" 
		"""
		frame = self.ui.settings_frame

		preserveAR = frame.findChildren(QtGui.QCheckBox, 'preserveAR_checkBox')[0].isChecked()
		if preserveAR:
			height = int(math.ceil(value/self.aspectRatio))
		else:
			height = frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].value()
		proxyRes = value, height

		frame.findChildren(QtGui.QSpinBox, 'proxyHeight_spinBox')[0].setValue(height)

		print proxyRes, self.aspectRatio


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
