#!/usr/bin/python

# [Icarus] shot_creator__main__.py
# v0.1
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# A UI for creating shots.


from PySide import QtCore, QtGui
from shot_creator_ui import *
import os, sys

# Import custom modules
import jobs, osOps, verbose


class shotCreatorApp(QtGui.QDialog):

	def __init__(self, job=None, parent=None):
		super(shotCreatorApp, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.job = job

		# Instantiate render queue class and load data
		self.j = jobs.jobs()

		# Connect signals & slots
		self.ui.prefix_comboBox.currentIndexChanged.connect(self.updateShotsPreview)
		self.ui.createSeq_checkBox.stateChanged.connect(self.updateShotsPreview)
		self.ui.start_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.shotCount_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.increment_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.suffix_lineEdit.textChanged.connect(self.updateShotsPreview)

		self.ui.shotCreator_buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.createShots)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\w]+'), self.ui.suffix_lineEdit)
		self.ui.suffix_lineEdit.setValidator(alphanumeric_validator)

		self.populateJobs(reloadDatabase=False)
		self.updateShotsPreview()


	def updateShotsPreview(self):
		""" Update the preview field showing the shot directories to be created.
		"""
		self.shotLs = []
		previewStr = ""
		index = self.ui.start_spinBox.value()
		if self.ui.createSeq_checkBox.checkState() == QtCore.Qt.Checked:
			count = self.ui.shotCount_spinBox.value()
			step = self.ui.increment_spinBox.value()
			for shot in range(count):
				shotName = self.ui.prefix_comboBox.currentText() + str(index).zfill(3) + self.ui.suffix_lineEdit.text()
				self.shotLs.append(shotName)
				previewStr += shotName + " "
				index += step

		else:
			if self.ui.suffix_lineEdit.text():
				shotName = self.ui.prefix_comboBox.currentText() + self.ui.suffix_lineEdit.text()
			else:
				shotName = self.ui.prefix_comboBox.currentText() + str(index).zfill(3)
			self.shotLs.append(shotName)
			previewStr = shotName

		self.ui.shotPreview_plainTextEdit.setPlainText(previewStr)


	def populateJobs(self, reloadDatabase=True):
		""" Populate the jobs combo box.
		"""
		if reloadDatabase:
			self.j.loadXML(quiet=True) # reload XML data

		# Stop the widget from emitting signals
		self.ui.job_comboBox.blockSignals(True)

		# Clear combo box
		self.ui.job_comboBox.clear()

		jobLs = self.j.getActiveJobs()
		if jobLs:
			jobLs = sorted(jobLs, reverse=True)

			for job in jobLs:
				self.ui.job_comboBox.insertItem(0, job)

			# Attempt to set the combo box to the current job
			if self.job in jobLs:
				self.ui.job_comboBox.setCurrentIndex(self.ui.job_comboBox.findText(self.job))
				#self.ui.job_comboBox.setEnabled(False)

			# Set the combo box to the first item
			else:
				self.ui.job_comboBox.setCurrentIndex(0)

		# Re-enable signals
		self.ui.job_comboBox.blockSignals(False)


	def createShots(self):
		""" Create the shot(s).
		"""
		success = 0
		failure = 0
		createdShots = ""
		existingShots = ""
		dialogMsg = ""

		jobPath = self.j.getPath(self.ui.job_comboBox.currentText() , translate=True)
		for shot in self.shotLs:
			path = osOps.absolutePath("%s/$SHOTSROOTRELATIVEDIR/%s/$DATAFILESRELATIVEDIR" %(jobPath, shot))
			if osOps.createDir(path):
				success += 1
				createdShots += shot + " "
			else:
				failure += 1
				existingShots += shot + " "

		if success:
			message = "%d %s created successfully: " %(success, verbose.pluralise('shot', success))
			dialogMsg += "%s\n%s\n\n" %(message, createdShots)
			verbose.message(message + createdShots)

		if failure:
			message = "The following %d shot(s) were not created as they already exist: " %failure
			dialogMsg += "%s\n%s\n\n" %(message, existingShots)
			verbose.warning(message + existingShots)

		# Confirmation dialog
		import pDialog
		dialogTitle = 'Results'
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)


	# def exit(self):
	# 	""" Exit the dialog.
	# 	"""
	# 	self.hide()
	# 	self.returnValue = False


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	# Initialise Icarus environment
	sys.path.append(os.environ['ICWORKINGDIR'])
	import env__init__
	env__init__.setEnv()
	#env__init__.appendSysPaths()

	#import rsc_rc # TODO: Check why this isn't working from within the UI file

	#app.setStyle('fusion') # Set UI style - you can also use a flag e.g. '-style plastique'

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	myApp = shotCreatorApp()
	myApp.show()
	sys.exit(app.exec_())

