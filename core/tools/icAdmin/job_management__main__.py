#!/usr/bin/python

# [Icarus] job_management__main__.py
# v0.1
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# A UI for managing jobs.


from PySide import QtCore, QtGui
from job_management_ui import *
import os, sys

# Import custom modules
import jobs, verbose


class jobManagementApp(QtGui.QDialog):

	def __init__(self, parent = None):
		super(jobManagementApp, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.returnValue = False

		# Instantiate render queue class and load data
		self.j = jobs.jobs()

		# Connect signals & slots
		self.ui.jobAdd_toolButton.clicked.connect(self.addJob)
		self.ui.jobDelete_toolButton.clicked.connect(self.deleteJobs)
		self.ui.refresh_toolButton.clicked.connect(self.reloadJobs)
		self.ui.jobEdit_toolButton.clicked.connect(self.editJob)
		self.ui.jobEnable_toolButton.clicked.connect(self.enableJobs)
		self.ui.jobDisable_toolButton.clicked.connect(self.disableJobs)
		self.ui.editPaths_toolButton.clicked.connect(self.editPaths)

		self.ui.jobs_listWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		self.ui.jobs_listWidget.itemDoubleClicked.connect(self.editJob)
		self.ui.jobs_listWidget.itemChanged.connect(lambda item: self.itemChecked(item))

		self.ui.main_buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.saveAndExit)
		self.ui.main_buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.exit)

		self.reloadJobs(reloadDatabase=False)


	def updateToolbarUI(self):
		""" Update the toolbar UI based on the current selection.
		"""
		if len(self.ui.jobs_listWidget.selectedItems()) == 0:
			self.ui.jobDelete_toolButton.setEnabled(False)
			self.ui.jobEdit_toolButton.setEnabled(False)
			self.ui.jobEnable_toolButton.setEnabled(False)
			self.ui.jobDisable_toolButton.setEnabled(False)
		elif len(self.ui.jobs_listWidget.selectedItems()) == 1:
			self.ui.jobDelete_toolButton.setEnabled(True)
			self.ui.jobEdit_toolButton.setEnabled(True)
			self.ui.jobEnable_toolButton.setEnabled(True)
			self.ui.jobDisable_toolButton.setEnabled(True)
		else: # more than one item selected
			self.ui.jobDelete_toolButton.setEnabled(True)
			self.ui.jobEdit_toolButton.setEnabled(False)
			self.ui.jobEnable_toolButton.setEnabled(True)
			self.ui.jobDisable_toolButton.setEnabled(True)


	def checkRootPaths(self):
		""" Check if root paths have been set, and if not prompt the user to set them up.
		"""
		self.j.getRootPaths()

		if (self.j.win_root is None) or (self.j.osx_root is None) or (self.j.linux_root is None):
			dialogMsg = 'Paths to the root of the shared filesystem must be set for each OS to enable cross-platform portability. Please set the values in the next dialog.\n'
			verbose.print_(dialogMsg, 1)

			# Confirmation dialog
			import pDialog
			dialogTitle = 'Root paths not set'
			dialog = pDialog.dialog()
			dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

			self.editPaths()


	def reloadJobs(self, reloadDatabase=True):
		if reloadDatabase:
			self.j.loadXML(quiet=True) # reload XML data

		# Stop the widget from emitting signals
		self.ui.jobs_listWidget.blockSignals(True)

		# Clear tree widget
		self.ui.jobs_listWidget.clear()

		for jobElement in self.j.getJobs():
			#jobID = jobElement.get('id')
			jobActive = jobElement.get('active')
			jobName = self.j.getValue(jobElement, 'name')
			jobPath = self.j.getValue(jobElement, 'path')

			item = QtGui.QListWidgetItem(self.ui.jobs_listWidget)
			item.setText(jobName)

			if jobActive == 'True':
				item.setCheckState(QtCore.Qt.Checked)
			else:
				item.setCheckState(QtCore.Qt.Unchecked)
				#item.setForeground(0, QtGui.QColor(102,102,102))

		self.updateToolbarUI()
		self.checkRootPaths()

		# Re-enable signals
		self.ui.jobs_listWidget.blockSignals(False)


	def addJob(self):
		import edit_job
		editJobDialog = edit_job.dialog()
		editJobDialog.dialogWindow('', '$JOBSROOT', True)
		if editJobDialog.dialogReturn:
			if self.j.addJob(editJobDialog.jobName, editJobDialog.jobPath, editJobDialog.jobActive):
				self.reloadJobs(reloadDatabase=False)
			else:
				errorMsg = "Could not create job as a job with the name '%s' already exists." %editJobDialog.jobName
				dialogMsg = errorMsg + "\nWould you like to create a job with a different name?"
				verbose.error(errorMsg)

				# Confirmation dialog
				import pDialog
				dialogTitle = 'Job Not Created'
				dialog = pDialog.dialog()
				if dialog.dialogWindow(dialogMsg, dialogTitle):
					self.addJob()


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
			self.j.enableJob(item.text(), True)
			item.setCheckState(QtCore.Qt.Checked)


	def disableJobs(self):
		""" Disable the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			self.j.enableJob(item.text(), False)
			item.setCheckState(QtCore.Qt.Unchecked)


	def itemChecked(self, item):
		""" Set the active status of the job correctly when the checkbox state changes.
		"""
		if item.checkState() == QtCore.Qt.Checked:
			self.j.enableJob(item.text(), True)
		else:
			self.j.enableJob(item.text(), False)


	def editJob(self):
		""" Open edit job dialog.
		"""
		item = self.ui.jobs_listWidget.selectedItems()[0]
		jobName = item.text()

		import edit_job
		editJobDialog = edit_job.dialog()
		editJobDialog.dialogWindow(jobName, self.j.getPath(jobName), self.j.getEnabled(jobName))
		if editJobDialog.dialogReturn:
			self.j.enableJob(jobName, editJobDialog.jobActive)
			self.j.setPath(jobName, editJobDialog.jobPath)
			if self.j.renameJob(jobName, editJobDialog.jobName): # do this last as jobs are referenced by name
				self.reloadJobs(reloadDatabase=False)
			else:
				errorMsg = "Could not rename job as a job with the name '%s' already exists." %editJobDialog.jobName
				dialogMsg = errorMsg + "\nWould you still like to edit the job '%s'?" %jobName
				verbose.error(errorMsg)

				# Confirmation dialog
				import pDialog
				dialogTitle = 'Job Not Created'
				dialog = pDialog.dialog()
				if dialog.dialogWindow(dialogMsg, dialogTitle):
					self.editJob()


	def editPaths(self):
		""" Open edit job dialog.
		"""
		#self.j.loadXML()
		self.j.getRootPaths()

		import edit_root_paths
		editPathsDialog = edit_root_paths.dialog()
		editPathsDialog.dialogWindow(self.j.win_root, self.j.osx_root, self.j.linux_root)
		if editPathsDialog.dialogReturn:
			self.j.setRootPaths(editPathsDialog.winPath, editPathsDialog.osxPath, editPathsDialog.linuxPath)
			self.j.getRootPaths()
			#self.j.saveXML()


	def save(self):
		""" Save data.
		"""
		if self.j.saveXML():
			verbose.message("Job database saved.")
			return True
		else:
			verbose.error("Job database could not be saved.")
			return False


	def saveAndExit(self):
		""" Save data and exit.
		"""
		if self.save():
			self.hide()
			self.returnValue = True
		else:
			self.exit()


	def exit(self):
		""" Exit the dialog.
		"""
		self.hide()
		self.returnValue = False


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

	myApp = jobManagementApp()
	myApp.show()
	sys.exit(app.exec_())

