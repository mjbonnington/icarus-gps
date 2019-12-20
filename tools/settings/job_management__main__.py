#!/usr/bin/python

# [Icarus] job_management__main__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2016-2018
#
# A UI for managing jobs.


import os
import sys

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
from . import edit_job
from . import edit_root_paths

from shared import jobs
from shared import os_wrapper
from shared import prompt
from shared import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Job Management"
WINDOW_OBJECT = "jobManagementUI"

# Set the UI and the stylesheet
UI_FILE = "job_management.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class JobManagementDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Job Management dialog class.
	"""
	def __init__(self, parent=None):
		super(JobManagementDialog, self).__init__(parent)
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

		# Set icons
		self.ui.jobImport_toolButton.setIcon(self.iconSet('icon_arrow_down.png'))
		self.ui.jobAdd_toolButton.setIcon(self.iconSet('icon_add.png'))
		self.ui.jobDelete_toolButton.setIcon(self.iconSet('icon_minus.png'))
		self.ui.refresh_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.jobEdit_toolButton.setIcon(self.iconSet('edit.svg'))
		self.ui.jobEnable_toolButton.setIcon(self.iconSet('icon_tick.png'))
		self.ui.jobDisable_toolButton.setIcon(self.iconSet('icon_cross.png'))
		self.ui.editPaths_toolButton.setIcon(self.iconSet('folder-symbolic.svg'))

		self.ui.searchFilterClear_toolButton.setIcon(self.iconSet('clear.svg'))

		# Connect signals & slots
		self.accepted.connect(self.save)  # Save settings if dialog accepted

		self.ui.jobImport_toolButton.clicked.connect(self.importJobs)
		self.ui.jobAdd_toolButton.clicked.connect(self.addJob)
		self.ui.jobDelete_toolButton.clicked.connect(self.deleteJobs)
		self.ui.refresh_toolButton.clicked.connect(lambda: self.reloadJobs(reloadDatabase=True))  # Lambda function for PyQt5 compatibility, default keyword argument not supported
		self.ui.jobEdit_toolButton.clicked.connect(self.editJob)
		self.ui.jobEnable_toolButton.clicked.connect(self.enableJobs)
		self.ui.jobDisable_toolButton.clicked.connect(self.disableJobs)
		self.ui.editPaths_toolButton.clicked.connect(self.editPaths)

		self.ui.searchFilter_lineEdit.textChanged.connect(lambda text: self.reloadJobs(reloadDatabase=False, jobFilter=text))
		self.ui.searchFilterClear_toolButton.clicked.connect(self.clearFilter)

		self.ui.jobs_listWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		self.ui.jobs_listWidget.itemDoubleClicked.connect(self.editJob)
		self.ui.jobs_listWidget.itemChanged.connect(lambda item: self.itemChecked(item))

		self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.accept)
		self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)

		# Instantiate jobs class and load data
		self.j = jobs.Jobs()


	def display(self):
		""" Display the dialog.
		"""
		self.reloadJobs(reloadDatabase=False)

		return self.exec_()


	def updateToolbarUI(self):
		""" Update the toolbar UI based on the current selection.
		"""
		# No items selected...
		if len(self.ui.jobs_listWidget.selectedItems()) == 0:
			self.ui.jobDelete_toolButton.setEnabled(False)
			self.ui.jobEdit_toolButton.setEnabled(False)
			self.ui.jobEnable_toolButton.setEnabled(False)
			self.ui.jobDisable_toolButton.setEnabled(False)
		# One item selected...
		elif len(self.ui.jobs_listWidget.selectedItems()) == 1:
			self.ui.jobDelete_toolButton.setEnabled(True)
			self.ui.jobEdit_toolButton.setEnabled(True)
			self.ui.jobEnable_toolButton.setEnabled(True)
			self.ui.jobDisable_toolButton.setEnabled(True)
		# More than one item selected...
		else:
			self.ui.jobDelete_toolButton.setEnabled(True)
			self.ui.jobEdit_toolButton.setEnabled(False)
			self.ui.jobEnable_toolButton.setEnabled(True)
			self.ui.jobDisable_toolButton.setEnabled(True)


	def checkRootPaths(self):
		""" Check if root paths have been set, and if not prompt the user to
			set them up.
		"""
		self.j.getRootPaths()

		if (self.j.win_root is None) or (self.j.osx_root is None) or (self.j.linux_root is None):
			dialogMsg = "Paths to the root of the shared filesystem must be set for each OS to enable cross-platform portability. Please set the values in the next dialog."
			#verbose.print_(dialogMsg, 1)
			verbose.warning("Root filesystem path(s) not set.")

			# Confirmation dialog
			dialogTitle = "Root Paths Not Set"
			dialog = prompt.dialog()
			dialog.display(dialogMsg, dialogTitle, conf=True)

			self.editPaths()


	def clearFilter(self):
		""" Clear the search filter field.
		"""
		self.ui.searchFilter_lineEdit.clear()
		self.ui.searchFilterClear_toolButton.setEnabled(False)


	def reloadJobs(self, reloadDatabase=True, selectItem=None, jobFilter=""):
		""" Refresh the jobs list view.

			'reloadDatabase' will reload the XML data first.
			'selectItem' specifies an item by name that will be selected
			automatically.
			'jobFilter' is a search string to filter the list.
		"""
		if reloadDatabase:
			self.j.loadXML(quiet=True)  # Reload XML data

		# Stop the widget from emitting signals
		self.ui.jobs_listWidget.blockSignals(True)

		# Clear tree widget
		self.ui.jobs_listWidget.clear()

		for jobElement in self.j.getJobs():
			#jobID = jobElement.get('id')
			jobActive = jobElement.get('active')
			jobName = self.j.getValue(jobElement, 'name')
			jobPath = self.j.getValue(jobElement, 'path')

			# Populate list view, using filter
			if jobFilter is not "":
				if jobFilter.lower() in jobName.lower():  # Case-insensitive
					item = self.addJobEntry(jobActive, jobName, jobPath)
				self.ui.searchFilterClear_toolButton.setEnabled(True)

			else:
				item = self.addJobEntry(jobActive, jobName, jobPath)
				self.ui.searchFilterClear_toolButton.setEnabled(False)

			if selectItem == jobName:
				selectedItem = item

		self.updateToolbarUI()
		self.checkRootPaths()

		# Re-enable signals
		self.ui.jobs_listWidget.blockSignals(False)

		# Set selection - view will also scroll to show selection
		if selectItem is not None:
			self.ui.jobs_listWidget.setCurrentItem(selectedItem)


	def addJobEntry(self, jobActive, jobName, jobPath):
		""" Add an entry to the jobs list view.
		"""
		item = QtWidgets.QListWidgetItem(self.ui.jobs_listWidget)
		item.setText(jobName)

		# Check active entries
		if jobActive == 'True':
			item.setCheckState(QtCore.Qt.Checked)
		else:
			item.setCheckState(QtCore.Qt.Unchecked)

		# Grey out entries that don't exist on disk
		if not os.path.isdir(os_wrapper.translatePath(jobPath)):
			item.setForeground(QtGui.QColor(102,102,102))
			item.setToolTip("Job path not found")

		return item


	def deleteJobs(self):
		""" Delete the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			self.j.deleteJob(item.text())
			self.ui.jobs_listWidget.takeItem(self.ui.jobs_listWidget.row(item))


	def enableJobs(self):
		""" Enable the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			item.setCheckState(QtCore.Qt.Checked)
			# self.j.enableJob(item.text(), True)  # Already called via signals/slots


	def disableJobs(self):
		""" Disable the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			item.setCheckState(QtCore.Qt.Unchecked)
			# self.j.enableJob(item.text(), False)  # Already called via signals/slots


	def itemChecked(self, item):
		""" Set the active status of the job correctly when the checkbox state
			changes.
		"""
		if item.checkState() == QtCore.Qt.Checked:
			self.j.enableJob(item.text(), True)
		else:
			self.j.enableJob(item.text(), False)


	def importJobs(self):
		""" Open a dialog to import an XML jobs data file and merge with the
			current data.
		"""
		datafile = self.fileDialog(
			os.environ['IC_CONFIGDIR'], fileFilter='XML files (*.xml)')
		if datafile:
			j = jobs.Jobs(datafile)

			for jobElement in j.getJobs():
				jobName = j.getValue(jobElement, 'name')
				jobPath = j.getValue(jobElement, 'path')
				jobVersion = j.getValue(jobElement, 'version')
				jobActive = jobElement.get('active')

				# print(jobName, jobPath, jobVersion, jobActive)

				if '$JOBSROOT' in jobPath:
					jobPath = jobPath.replace('$JOBSROOT', '$IC_JOBSROOT')
					verbose.message("Updating job path: %s" % jobPath)

				if self.j.addJob(jobName, jobPath, jobVersion, jobActive):
					self.reloadJobs(reloadDatabase=False)
				# else:
				# 	errorMsg = "A job with the name '%s' already exists." % jobName
				# 	dialogMsg = errorMsg \
				# 	+ "\nOld path: %s" % self.j.getPath(jobName) \
				# 	+ "\nNew path: %s" % jobPath \
				# 	+ "\nWould you like to replace it?"
				# 	verbose.warning(errorMsg)

				# 	# Confirmation dialog
				# 	dialogTitle = 'Job Already Exists'
				# 	dialog = prompt.dialog()
				# 	if dialog.display(dialogMsg, dialogTitle):
				# 		self.j.deleteJob(jobName)
				# 		self.j.addJob(jobName, jobPath, jobVersion, jobActive)


	def addJob(self):
		""" Open the edit job dialog to add a new job.
		"""
		editJobDialog = edit_job.dialog(parent=self)
		if editJobDialog.display('', '$IC_JOBSROOT', os.environ['IC_VERSION'], True):
			if self.j.addJob(editJobDialog.jobName, editJobDialog.jobPath, editJobDialog.jobVersion, editJobDialog.jobActive):
				self.reloadJobs(reloadDatabase=False, selectItem=editJobDialog.jobName)
			else:
				errorMsg = "Could not create job as a job with the name '%s' already exists." % editJobDialog.jobName
				dialogMsg = errorMsg + "\nWould you like to create a job with a different name?"
				verbose.error(errorMsg)

				# Confirmation dialog
				dialogTitle = 'Job Not Created'
				dialog = prompt.dialog()
				if dialog.display(dialogMsg, dialogTitle):
					self.addJob()


	def editJob(self):
		""" Open edit job dialog.
		"""
		item = self.ui.jobs_listWidget.selectedItems()[0]
		jobName = item.text()

		editJobDialog = edit_job.dialog(parent=self)
		if editJobDialog.display(jobName, self.j.getPath(jobName), self.j.getVersion(jobName), self.j.getEnabled(jobName)):
			self.j.enableJob(jobName, editJobDialog.jobActive)
			self.j.setVersion(jobName, editJobDialog.jobVersion)
			self.j.setPath(jobName, editJobDialog.jobPath)
			if self.j.renameJob(jobName, editJobDialog.jobName):  # Do this last as jobs are referenced by name
				self.reloadJobs(reloadDatabase=False, selectItem=editJobDialog.jobName)
			else:
				errorMsg = "Could not rename job as a job with the name '%s' already exists." % editJobDialog.jobName
				dialogMsg = errorMsg + "\nWould you still like to edit the job '%s'?" % jobName
				verbose.error(errorMsg)

				# Confirmation dialog
				dialogTitle = 'Job Not Created'
				dialog = prompt.dialog()
				if dialog.display(dialogMsg, dialogTitle):
					self.editJob()


	def editPaths(self):
		""" Open edit paths dialog.
		"""
		#self.j.loadXML()
		self.j.getRootPaths()

		editPathsDialog = edit_root_paths.dialog(parent=self)
		if editPathsDialog.display(self.j.win_root, self.j.osx_root, self.j.linux_root, self.j.jobs_path):
			self.j.setRootPaths(editPathsDialog.winPath, editPathsDialog.osxPath, editPathsDialog.linuxPath, editPathsDialog.jobsRelPath)
			self.j.getRootPaths()
			#self.j.save()


	def save(self):
		""" Save data.
		"""
		if self.j.save():
			verbose.message("Job database saved.")
			return True
		else:
			verbose.error("Job database could not be saved.")
			return False


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
# 	sys.path.append(os.environ['IC_COREDIR'])
# 	import icarus__env__
# 	icarus__env__.set_env()
# 	#icarus__env__.append_sys_paths()

# 	import rsc_rc

# 	# Set UI style - you can also use a flag e.g. '-style plastique'
# 	#app.setStyle('fusion')

# 	# Apply UI style sheet
# 	if STYLESHEET is not None:
# 		qss=os.path.join(os.environ['IC_COREDIR'], STYLESHEET)
# 		with open(qss, "r") as fh:
# 			app.setStyleSheet(fh.read())

# 	myApp = JobManagementDialog()
# 	myApp.show()
# 	sys.exit(app.exec_())

