#!/usr/bin/python

# Icarus Admin Tools
# Settings editor dialog (generic)
# v0.2
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# A generic settings dialog class. Job, shot and user settings should inherit this base class.


from PySide import QtCore, QtGui
from settings_ui import *
import os, sys

# Initialise Icarus environment
sys.path.append(os.environ['IC_WORKINGDIR'])
import env__init__
env__init__.setEnv()
env__init__.appendSysPaths()

#import jobSettings, appPaths


class settingsDialog(QtGui.QDialog):

	def __init__(self, parent = None, categoryList = None):
		#QtGui.QDialog.__init__(self, parent)
		super(settingsDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		# Populate categories - hard coding this for now so XML can be generated from this list. Perhaps could be auto-generated from existing ui files?
		#	categoryList = ['job', 'units', 'time', 'resolution', 'apps', 'other']
		if categoryList is not None:
			for cat in categoryList:
				self.ui.categories_listWidget.addItem(cat)

			# Set the maximum size of the list widget
			self.ui.categories_listWidget.setMaximumWidth( self.ui.categories_listWidget.sizeHintForColumn(0) + 64 )

			# Select the first item & show the appropriate settings panel
			self.ui.categories_listWidget.item(0).setSelected(True)
			self.openProperties( self.ui.categories_listWidget.item(0).text() )

		# Set up keyboard shortcuts
		self.shortcut = QtGui.QShortcut(self)
		self.shortcut.setKey('Ctrl+S')
		self.shortcut.activated.connect(self.save)

		# Connect signals and slots for categories list widget and main buttons
		self.ui.categories_listWidget.currentItemChanged.connect( lambda current: self.openProperties(current.text()) )

		#self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.init)
		#self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.ap.saveXML)
		self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.exit)
		self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering OK / Cancel buttons
		"""
		pass
		#if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
		#	return


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

			if isinstance(widget, QtGui.QSpinBox):
				#widget.setValue( int(self.jd.getText(category, widget.property('xmlAttr'))) )
				try:
					value = int( self.jd.getText(category, attr) )
					widget.setValue(value)
				except AttributeError:
					pass
					#value = 0
				print "%s: %s" %(attr, widget.value())

		# Run these functions if specific properties panels are opened
		if category == 'apps':
			self.populateAppVersions(self.ui.settings_frame)

		if category == 'resolution':
			self.setupRes()


	def save(self):
		""" Save the settings to the data file
		"""
		# Store values to the ET

		#if self.ap.saveXML():
		#	print "Settings saved."
		#	return True
		#else:
		#	print "Warning: Settings could not be saved."
		#	return False


	def saveAndExit(self):
		""" Save data and exit
		"""
		if self.save():
			self.hide()


	def exit(self):
		""" Exit the dialog
		"""
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	#app.setStyle('plastique') # Set UI style - you can also use a flag e.g. '-style plastique'

	qss=os.path.join(os.environ['IC_WORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	jobSettingsEditor = settingsDialog()
	jobSettingsEditor.show()
	sys.exit(jobSettingsEditor.exec_())

#else:
#	jobSettingsEditor = settingsDialog()
#	jobSettingsEditor.show()
