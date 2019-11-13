#!/usr/bin/python

# [Icarus] shot_management__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2018 Gramercy Park Studios
#
# A UI for managing shots.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import jobs
import os_wrapper
import settingsData
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Shot Management"
WINDOW_OBJECT = "shotManagementUI"

# Set the UI and the stylesheet
UI_FILE = "shot_management_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class ShotManagementDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Job Management dialog class.
	"""
	def __init__(self, parent=None):
		super(ShotManagementDialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
		             window_title=WINDOW_TITLE, 
		             ui_file=UI_FILE, 
		             stylesheet=STYLESHEET, 
		             store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set other Qt attributes
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Connect signals & slots
		# self.accepted.connect(self.save)  # Save settings if dialog accepted

		self.ui.job_comboBox.currentIndexChanged.connect(self.populateShots)

		# self.ui.shotAdd_toolButton.clicked.connect(self.addShot)
		# self.ui.shotDelete_toolButton.clicked.connect(self.deleteShots)
		self.ui.refresh_toolButton.clicked.connect(self.populateShots)
		# self.ui.jobEdit_toolButton.clicked.connect(self.editJob)
		# self.ui.jobEnable_toolButton.clicked.connect(self.enableJobs)
		# self.ui.jobDisable_toolButton.clicked.connect(self.disableJobs)
		# self.ui.editPaths_toolButton.clicked.connect(self.editPaths)

		# self.ui.searchFilter_lineEdit.textChanged.connect(lambda text: self.reloadJobs(reloadDatabase=False, jobFilter=text))
		# self.ui.searchFilterClear_toolButton.clicked.connect(self.clearFilter)

		# self.ui.jobs_listWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		# self.ui.jobs_listWidget.itemDoubleClicked.connect(self.editJob)
		# self.ui.jobs_listWidget.itemChanged.connect(lambda item: self.itemChecked(item))

		# self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.accept)
		# self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)

		# Instantiate jobs class and load data
		self.j = jobs.Jobs()


	def display(self, job=None):
		""" Display the dialog.
		"""
		self.job = job

		# self.reloadJobs(reloadDatabase=False)
		self.populateJobs(reloadDatabase=False)
		self.populateShots()
		# self.updateShotsPreview()

		return self.exec_()


	# def updateToolbarUI(self):
	# 	""" Update the toolbar UI based on the current selection.
	# 	"""
	# 	# No items selected...
	# 	if len(self.ui.jobs_listWidget.selectedItems()) == 0:
	# 		self.ui.jobDelete_toolButton.setEnabled(False)
	# 		self.ui.jobEdit_toolButton.setEnabled(False)
	# 		self.ui.jobEnable_toolButton.setEnabled(False)
	# 		self.ui.jobDisable_toolButton.setEnabled(False)
	# 	# One item selected...
	# 	elif len(self.ui.jobs_listWidget.selectedItems()) == 1:
	# 		self.ui.jobDelete_toolButton.setEnabled(True)
	# 		self.ui.jobEdit_toolButton.setEnabled(True)
	# 		self.ui.jobEnable_toolButton.setEnabled(True)
	# 		self.ui.jobDisable_toolButton.setEnabled(True)
	# 	# More than one item selected...
	# 	else:
	# 		self.ui.jobDelete_toolButton.setEnabled(True)
	# 		self.ui.jobEdit_toolButton.setEnabled(False)
	# 		self.ui.jobEnable_toolButton.setEnabled(True)
	# 		self.ui.jobDisable_toolButton.setEnabled(True)


	def clearFilter(self):
		""" Clear the search filter field.
		"""
		self.ui.searchFilter_lineEdit.clear()


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
		""" Update the shots view table widget.
		"""
		currentJob = self.ui.job_comboBox.currentText()
		jobPath = self.j.getPath(currentJob, translate=True)
		shotLs = self.j.listShots(currentJob)

		self.ui.shots_tableWidget.clearContents()

		if shotLs:
			self.ui.shots_tableWidget.setRowCount(len(shotLs))
			for row, shotName in enumerate(shotLs):
				newRowHeaderItem = QtWidgets.QTableWidgetItem(shotName)
				newItem = QtWidgets.QTableWidgetItem(shotName)
				self.ui.shots_tableWidget.setVerticalHeaderItem(row, newRowHeaderItem)
				shotDataPath = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s/$IC_METADATA/shotData.xml" %(jobPath, shotName))
				shotData = settingsData.SettingsData()
				shotData.loadXML(shotDataPath)

				text = "%s-%s" %(shotData.getValue('time', 'rangeStart'), shotData.getValue('time', 'rangeEnd'))
				self.ui.shots_tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(text))

				text = shotData.getValue('time', 'fps')
				self.ui.shots_tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(text))

				text = "%sx%s" %(shotData.getValue('resolution', 'fullWidth'), shotData.getValue('resolution', 'fullHeight'))
				self.ui.shots_tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(text))

				text = "%sx%s" %(shotData.getValue('resolution', 'proxyWidth'), shotData.getValue('resolution', 'proxyHeight'))
				self.ui.shots_tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(text))

				text = shotData.getValue('camera', 'camera')
				self.ui.shots_tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(text))

				text = "%sx%s" %(shotData.getValue('camera', 'filmbackWidth'), shotData.getValue('camera', 'filmbackHeight'))
				self.ui.shots_tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(text))

				text = shotData.getValue('camera', 'focalLength')
				self.ui.shots_tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(text))

				text = shotData.getValue('shot', 'title')
				self.ui.shots_tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(text))

				# self.ui.shots_tableWidget.resizeRowToContents(row)

		self.ui.shots_tableWidget.resizeRowsToContents()


	# def reloadJobs(self, reloadDatabase=True, selectItem=None, jobFilter=""):
	# 	""" Refresh the jobs list view.

	# 		'reloadDatabase' will reload the XML data first.
	# 		'selectItem' specifies an item by name that will be selected
	# 		automatically.
	# 		'jobFilter' is a search string to filter the list.
	# 	"""
	# 	if reloadDatabase:
	# 		self.j.loadXML(quiet=True)  # Reload XML data

	# 	# Stop the widget from emitting signals
	# 	self.ui.jobs_listWidget.blockSignals(True)

	# 	# Clear tree widget
	# 	self.ui.jobs_listWidget.clear()

	# 	for jobElement in self.j.getJobs():
	# 		#jobID = jobElement.get('id')
	# 		jobActive = jobElement.get('active')
	# 		jobName = self.j.getValue(jobElement, 'name')
	# 		jobPath = self.j.getValue(jobElement, 'path')

	# 		# Populate list view, using filter
	# 		if jobFilter is not "":
	# 			if jobFilter.lower() in jobName.lower():  # Case-insensitive
	# 				item = self.addJobEntry(jobActive, jobName, jobPath)
	# 			self.ui.searchFilterClear_toolButton.setEnabled(True)

	# 		else:
	# 			item = self.addJobEntry(jobActive, jobName, jobPath)
	# 			self.ui.searchFilterClear_toolButton.setEnabled(False)

	# 		if selectItem == jobName:
	# 			selectedItem = item

	# 	self.updateToolbarUI()
	# 	self.checkRootPaths()

	# 	# Re-enable signals
	# 	self.ui.jobs_listWidget.blockSignals(False)

	# 	# Set selection - view will also scroll to show selection
	# 	if selectItem is not None:
	# 		self.ui.jobs_listWidget.setCurrentItem(selectedItem)


	# def addJobEntry(self, jobActive, jobName, jobPath):
	# 	""" Add an entry to the jobs list view.
	# 	"""
	# 	item = QtWidgets.QListWidgetItem(self.ui.jobs_listWidget)
	# 	item.setText(jobName)

	# 	# Check active entries
	# 	if jobActive == 'True':
	# 		item.setCheckState(QtCore.Qt.Checked)
	# 	else:
	# 		item.setCheckState(QtCore.Qt.Unchecked)

	# 	# Grey out entries that don't exist on disk
	# 	if not os.path.isdir(os_wrapper.translatePath(jobPath)):
	# 		item.setForeground(QtGui.QColor(102,102,102))
	# 		item.setToolTip("Job path not found")

	# 	return item


	# def deleteJobs(self):
	# 	""" Delete the selected job(s).
	# 	"""
	# 	for item in self.ui.jobs_listWidget.selectedItems():
	# 		self.j.deleteJob(item.text())
	# 		self.ui.jobs_listWidget.takeItem(self.ui.jobs_listWidget.row(item))


	# def enableJobs(self):
	# 	""" Enable the selected job(s).
	# 	"""
	# 	for item in self.ui.jobs_listWidget.selectedItems():
	# 		item.setCheckState(QtCore.Qt.Checked)
	# 		# self.j.enableJob(item.text(), True)  # Already called via signals/slots


	# def disableJobs(self):
	# 	""" Disable the selected job(s).
	# 	"""
	# 	for item in self.ui.jobs_listWidget.selectedItems():
	# 		item.setCheckState(QtCore.Qt.Unchecked)
	# 		# self.j.enableJob(item.text(), False)  # Already called via signals/slots


	# def itemChecked(self, item):
	# 	""" Set the active status of the job correctly when the checkbox state
	# 		changes.
	# 	"""
	# 	if item.checkState() == QtCore.Qt.Checked:
	# 		self.j.enableJob(item.text(), True)
	# 	else:
	# 		self.j.enableJob(item.text(), False)


	# def addJob(self):
	# 	""" Open the edit job dialog to add a new job.
	# 	"""
	# 	import edit_job
	# 	editJobDialog = edit_job.dialog(parent=self)
	# 	if editJobDialog.display('', '$IC_JOBSROOT', True):
	# 		if self.j.addJob(editJobDialog.jobName, editJobDialog.jobPath, editJobDialog.jobActive):
	# 			self.reloadJobs(reloadDatabase=False, selectItem=editJobDialog.jobName)
	# 		else:
	# 			errorMsg = "Could not create job as a job with the name '%s' already exists." %editJobDialog.jobName
	# 			dialogMsg = errorMsg + "\nWould you like to create a job with a different name?"
	# 			verbose.error(errorMsg)

	# 			# Confirmation dialog
	# 			import pDialog
	# 			dialogTitle = 'Job Not Created'
	# 			dialog = pDialog.dialog()
	# 			if dialog.display(dialogMsg, dialogTitle):
	# 				self.addJob()


	# def editJob(self):
	# 	""" Open edit job dialog.
	# 	"""
	# 	item = self.ui.jobs_listWidget.selectedItems()[0]
	# 	jobName = item.text()

	# 	import edit_job
	# 	editJobDialog = edit_job.dialog(parent=self)
	# 	if editJobDialog.display(jobName, self.j.getPath(jobName), self.j.getEnabled(jobName)):
	# 		self.j.enableJob(jobName, editJobDialog.jobActive)
	# 		self.j.setPath(jobName, editJobDialog.jobPath)
	# 		if self.j.renameJob(jobName, editJobDialog.jobName):  # Do this last as jobs are referenced by name
	# 			self.reloadJobs(reloadDatabase=False, selectItem=editJobDialog.jobName)
	# 		else:
	# 			errorMsg = "Could not rename job as a job with the name '%s' already exists." %editJobDialog.jobName
	# 			dialogMsg = errorMsg + "\nWould you still like to edit the job '%s'?" %jobName
	# 			verbose.error(errorMsg)

	# 			# Confirmation dialog
	# 			import pDialog
	# 			dialogTitle = 'Job Not Created'
	# 			dialog = pDialog.dialog()
	# 			if dialog.display(dialogMsg, dialogTitle):
	# 				self.editJob()


	# def editPaths(self):
	# 	""" Open edit paths dialog.
	# 	"""
	# 	#self.j.loadXML()
	# 	self.j.getRootPaths()

	# 	import edit_root_paths
	# 	editPathsDialog = edit_root_paths.dialog(parent=self)
	# 	if editPathsDialog.display(self.j.win_root, self.j.osx_root, self.j.linux_root, self.j.jobs_path):
	# 		self.j.setRootPaths(editPathsDialog.winPath, editPathsDialog.osxPath, editPathsDialog.linuxPath, editPathsDialog.jobsRelPath)
	# 		self.j.getRootPaths()
	# 		#self.j.saveXML()


	# def save(self):
	# 	""" Save data.
	# 	"""
	# 	if self.j.saveXML():
	# 		verbose.message("Job database saved.")
	# 		return True
	# 	else:
	# 		verbose.error("Job database could not be saved.")
	# 		return False


	# def saveAndExit(self):
	# 	""" Save data and exit.
	# 	"""
	# 	if self.save():
	# 		# self.ui.hide()
	# 		self.returnValue = True
	# 		self.ui.accept()
	# 	else:
	# 		self.returnValue = False
	# 		# self.exit()
	# 		self.ui.accept()


	# def exit(self):
	# 	""" Exit the dialog.
	# 	"""
	# 	# self.ui.hide()
	# 	self.returnValue = False
	# 	self.ui.reject()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			return


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.storeWindow()  # Store window geometry


	# def closeEvent(self, event):
	# 	""" Event handler for when window is closed.
	# 	"""
	# 	#self.save()  # Save settings
	# 	self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main dialog class
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Run as standalone app
# ----------------------------------------------------------------------------

# if __name__ == "__main__":
# 	app = QtWidgets.QApplication(sys.argv)

# 	# Initialise Icarus environment
# 	sys.path.append(os.environ['IC_WORKINGDIR'])
# 	import env__init__
# 	env__init__.setEnv()
# 	#env__init__.appendSysPaths()

# 	import rsc_rc

# 	# Set UI style - you can also use a flag e.g. '-style plastique'
# 	#app.setStyle('fusion')

# 	# Apply UI style sheet
# 	if STYLESHEET is not None:
# 		qss=os.path.join(os.environ['IC_WORKINGDIR'], STYLESHEET)
# 		with open(qss, "r") as fh:
# 			app.setStyleSheet(fh.read())

# 	myApp = ShotManagementDialog()
# 	myApp.show()
# 	sys.exit(app.exec_())

