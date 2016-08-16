#!/usr/bin/python

# [Icarus] job_management__main.py
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
		self.jd = jobs.jobs()
		self.jd.loadXML(os.path.join(os.environ['ICCONFIGDIR'], 'jobs.xml'))
		jobDict = self.jd.getDict() # this is a temporary hack in order to setup environment variables

		# Connect signals & slots
		self.ui.jobAdd_toolButton.clicked.connect(self.addJob)
		self.ui.jobDelete_toolButton.clicked.connect(self.deleteJobs)
		self.ui.refresh_toolButton.clicked.connect(self.reloadJobs)
		self.ui.jobEdit_toolButton.clicked.connect(self.editJob)
		self.ui.jobEnable_toolButton.clicked.connect(self.enableJobs)
		self.ui.jobDisable_toolButton.clicked.connect(self.disableJobs)
		self.ui.editPaths_toolButton.clicked.connect(self.editPaths)

		self.ui.jobs_listWidget.itemSelectionChanged.connect(self.updateToolbarUI)
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


	def reloadJobs(self, reloadDatabase=True):
		if reloadDatabase:
			self.jd.loadXML(quiet=True) # reload XML data

		# Stop the widget from emitting signals
		self.ui.jobs_listWidget.blockSignals(True)

		# Clear tree widget
		self.ui.jobs_listWidget.clear()

		for jobElement in self.jd.getJobs():
#			jobID = jobElement.get('id')
			jobActive = jobElement.get('active')
			jobName = self.jd.getValue(jobElement, 'name')
			jobPath = self.jd.getValue(jobElement, 'path')

			item = QtGui.QListWidgetItem(self.ui.jobs_listWidget)
			item.setText(jobName)

			#item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)

			if jobActive == 'True':
				item.setCheckState(QtCore.Qt.Checked)
			else:
				item.setCheckState(QtCore.Qt.Unchecked)
				#item.setForeground(0, QtGui.QColor(102,102,102))

		self.updateToolbarUI()

		# Re-enable signals
		self.ui.jobs_listWidget.blockSignals(False)


	def addJob(self):
		#self.ui.jobs_listWidget.addItem('000000_New_Job')
		# item = QtGui.QListWidgetItem(self.ui.jobs_listWidget)
		# item.setText('000000_New_Job')
		# item.setCheckState(QtCore.Qt.Checked)
		# item.setSelected(True)

		import edit_job
		editJobDialog = edit_job.dialog()
		editJobDialog.dialogWindow("New_Job", '$FILESYSTEMROOT', True)
		if editJobDialog.dialogReturn:
			if self.jd.addJob(editJobDialog.jobName, editJobDialog.jobPath, editJobDialog.jobActive):
				self.reloadJobs(reloadDatabase=False)
			else:
				self.addJob()


	def deleteJobs(self):
		""" Delete the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			self.jd.deleteJob(item.text())
			self.ui.jobs_listWidget.takeItem(self.ui.jobs_listWidget.row(item))


	def enableJobs(self):
		""" Enable the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			self.jd.enableJob(item.text(), True)
			item.setCheckState(QtCore.Qt.Checked)


	def disableJobs(self):
		""" Disable the selected job(s).
		"""
		for item in self.ui.jobs_listWidget.selectedItems():
			self.jd.enableJob(item.text(), False)
			item.setCheckState(QtCore.Qt.Unchecked)


	def itemChecked(self, item):
		""" Set the active status of the job correctly when the checkbox state changes.
		"""
		if item.checkState() == QtCore.Qt.Checked:
			self.jd.enableJob(item.text(), True)
		else:
			self.jd.enableJob(item.text(), False)


	def editJob(self):
		""" Open edit job dialog.
		"""
		item = self.ui.jobs_listWidget.selectedItems()[0]
		jobName = item.text()

		import edit_job
		editJobDialog = edit_job.dialog()
		editJobDialog.dialogWindow(jobName, self.jd.getPath(jobName), self.jd.getEnabled(jobName))
		if editJobDialog.dialogReturn:
			self.jd.enableJob(jobName, editJobDialog.jobActive)
			self.jd.setPath(jobName, editJobDialog.jobPath)
			if self.jd.renameJob(jobName, editJobDialog.jobName): # do this last as jobs are referenced by name
				self.reloadJobs(reloadDatabase=False)
			else:
				self.editJob()


	def editPaths(self):
		""" Open edit job dialog.
		"""
		self.jd.getRootPaths()

		import edit_root_paths
		editPathsDialog = edit_root_paths.dialog()
		editPathsDialog.dialogWindow(self.jd.win_root, self.jd.osx_root, self.jd.linux_root)
		if editPathsDialog.dialogReturn:
			self.jd.setRootPaths(editPathsDialog.winPath, editPathsDialog.osxPath, editPathsDialog.linuxPath)

			jobDict = self.jd.getDict() # this is a temporary hack in order to setup environment variables
			self.jd.saveXML()

		# 	self.jd.setPath(jobName, editPathsDialog.jobPath)
		# 	if self.jd.renameJob(jobName, editPathsDialog.jobName): # do this last as jobs are referenced by name
		# 		self.reloadJobs(reloadDatabase=False)
		# 	else:
		# 		self.editJob()


	def save(self):
		""" Save data.
		"""
		if self.jd.saveXML():
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

