#!/usr/bin/python

# [Icarus] shot_creator__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# A UI for creating shots.


import os
import sys

# Initialise Icarus environment
# if __name__ == "__main__":
# 	sys.path.append("J:/dev/icarus/core/run")  # Temporary
# 	import env__init__
# 	env__init__.setEnv()

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
from shared import jobs
from shared import os_wrapper
from shared import pDialog
from shared import settingsData
from shared import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Shot Creator"
WINDOW_OBJECT = "shotCreatorUI"

# Set the UI and the stylesheet
UI_FILE = "shot_creator_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class ShotCreatorDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Shot Creator dialog class.
	"""
	def __init__(self, parent=None):
		super(ShotCreatorDialog, self).__init__(parent)
		self.parent = parent

		# xml_data = os.path.join(os.environ['IC_USERPREFS'], 'shotCreator.xml')
		xml_data = os.path.join(os.environ['IC_USERPREFS'], 'shotcreator_prefs.json')

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             prefs_file=xml_data, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		self.ui.job_comboBox.currentIndexChanged.connect(self.populateShots)
		self.ui.prefix_comboBox.currentIndexChanged.connect(self.updateShotsPreview)
		self.ui.createSeq_checkBox.stateChanged.connect(self.updateShotsPreview)
		self.ui.start_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.shotCount_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.increment_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.suffix_lineEdit.textChanged.connect(self.updateShotsPreview)

		self.ui.shotCreator_buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.createShots)

		# Set input validators
		alphanumeric_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\w]+'), self.ui.suffix_lineEdit)
		self.ui.suffix_lineEdit.setValidator(alphanumeric_validator)

		# Instantiate jobs class and load data
		self.j = jobs.Jobs()
		self.sd = settingsData.SettingsData()


	def display(self, job=None):
		""" Display the dialog.
		"""
		self.job = job

		self.populateJobs(reloadDatabase=False)
		self.populateShots()
		self.updateShotsPreview()

		return self.exec_()


	def populateJobs(self, reloadDatabase=True):
		""" Populate the jobs combo box.
		"""
		if reloadDatabase:
			self.j.loadXML(quiet=True)  # Reload XML data

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


	def populateShots(self):
		""" Update the text field showing the existing shots.
		"""
		shotLs = self.j.listShots(self.ui.job_comboBox.currentText())
		previewStr = ""
		if shotLs:
			for shotName in shotLs:
				previewStr += shotName + "\n"
		self.ui.shots_plainTextEdit.setPlainText(previewStr)


	def updateShotsPreview(self):
		""" Update the preview field showing the shot directories to be
			created.
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
				previewStr += shotName + "\n"
				index += step

		else:
			if self.ui.suffix_lineEdit.text():
				shotName = self.ui.prefix_comboBox.currentText() + self.ui.suffix_lineEdit.text()
			else:
				shotName = self.ui.prefix_comboBox.currentText() + str(index).zfill(3)
			self.shotLs.append(shotName)
			previewStr = shotName

		self.ui.shotPreview_plainTextEdit.setPlainText(previewStr)


	def createShots(self):
		""" Create the shot(s).

		"""
		success = 0
		existing = 0
		failure = 0
		createdShots = ""
		existingShots = ""
		failedShots = ""
		dialogMsg = ""

		jobPath = self.j.getPath(self.ui.job_comboBox.currentText(), translate=True)
		for shot in self.shotLs:
			path = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s/$IC_METADATA" %(jobPath, shot))
			os_wrapper.createDir(path)
			shotData = os.path.join(path, "shotData.xml")
			# sd.createXML()
			# sd.saveXML()
			if self.sd.loadXML(shotData):
				existing += 1
				existingShots += shot + " "
			elif self.sd.saveXML():
				success += 1
				createdShots += shot + " "
			else:
				failure += 1
				failedShots += shot + " "

		if success:
			message = "%d %s created successfully: " %(success, verbose.pluralise('shot', success))
			dialogMsg += "%s\n%s\n\n" %(message, createdShots)
			verbose.message(message + createdShots)

		if existing:
			message = "The following %d shot(s) were not created as they already exist: " %existing
			dialogMsg += "%s\n%s\n\n" %(message, existingShots)
			verbose.warning(message + existingShots)

		if failure:
			message = "The following %d shot(s) could not be created - please check write permissions and try again: " %failure
			dialogMsg += "%s\n%s\n\n" %(message, failedShots)
			verbose.error(message + failedShots)

		# Confirmation dialog
		dialogTitle = "Shot Creator Results"
		dialog = pDialog.dialog()
		dialog.display(dialogMsg, dialogTitle, conf=True)

		self.populateShots()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			return


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry


	# def exit(self):
	# 	""" Exit the dialog.
	# 	"""
	# 	self.ui.hide()
	# 	self.returnValue = False

# ----------------------------------------------------------------------------
# End of main dialog class
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Run as standalone app
# ----------------------------------------------------------------------------

# if __name__ == "__main__":
# 	app = QtWidgets.QApplication(sys.argv)

# 	import rsc_rc

# 	# # Apply UI style sheet
# 	# if STYLESHEET is not None:
# 	# 	qss=os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
# 	# 	with open(qss, "r") as fh:
# 	# 		app.setStyleSheet(fh.read())

# 	myApp = ShotCreatorDialog()
# 	myApp.display()
# 	sys.exit(app.exec_())

