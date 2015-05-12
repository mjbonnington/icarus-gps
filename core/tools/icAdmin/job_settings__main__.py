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

#import jobs, appPaths


class jobSettingsDialog(QtGui.QDialog):

	def __init__(self, parent = None):
		#QtGui.QDialog.__init__(self, parent)
		super(jobSettingsDialog, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.init()

		# Connect signals and slots
		QtCore.QObject.connect(self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Reset), QtCore.SIGNAL('clicked()'), self.init)
		#QtCore.QObject.connect(self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Save), QtCore.SIGNAL('clicked()'), self.ap.saveXML)
		QtCore.QObject.connect(self.ui.jobSettings_buttonBox.button(QtGui.QDialogButtonBox.Close), QtCore.SIGNAL('clicked()'), self.exit)


	def init(self):
		# Load data from xml file
		#self.ap = appPaths.appPaths(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'appPaths.xml'))
		pass


	def exit(self):
		# TODO: Add confirmation dialog if data has changed
		sys.exit()


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
