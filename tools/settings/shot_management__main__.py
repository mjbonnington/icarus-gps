#!/usr/bin/python

# [Icarus] shot_management__main__.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2018-2019
#
# A UI for managing shots.


import os
import re
import sys

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from shared import jobs
from shared import json_metadata as metadata
from shared import os_wrapper
from shared import prompt
from shared import verbose

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

cfg = {}

# Set window title and object names
cfg['window_title'] = "Shot Management"
cfg['window_object'] = "shotManagementUI"

# Set the UI and the stylesheet
cfg['ui_file'] = 'shot_management.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
prefs_location = os.environ['IC_USERPREFS']
cfg['prefs_file'] = os.path.join(prefs_location, 'shot_management_prefs.json')
cfg['store_window_geometry'] = True

# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class ShotManagementDialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Job Management dialog class.
	"""
	def __init__(self, parent=None):
		super(ShotManagementDialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui.sidebar_frame)

		# Set window icon, flags and other Qt attributes
		self.setWindowIcon(self.iconSet('filmgrain.svg', tintNormal=False))
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Restore splitter size state
		try:
			self.ui.splitter.restoreState(self.settings.value("splitterSizes")) #.toByteArray())
			self.ui.shots_tableWidget.horizontalHeader().restoreState(self.settings.value("shotsTableView")) #.toByteArray())
		except:
			pass

		# Connect signals & slots
		self.ui.job_comboBox.currentIndexChanged.connect(lambda: self.populateShots())

		self.ui.shotCreate_toolButton.toggled.connect(lambda checked: self.toggleSidebar(checked))
		# self.ui.shotDelete_toolButton.clicked.connect(self.deleteShots)
		self.ui.shotSettings_toolButton.clicked.connect(self.shotSettings)
		self.ui.refresh_toolButton.clicked.connect(lambda: self.populateShots())

		self.ui.searchFilter_lineEdit.textChanged.connect(lambda text: self.populateShots(shot_filter=text))
		self.ui.searchFilterClear_toolButton.clicked.connect(self.clearFilter)

		self.ui.shots_tableWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		# self.ui.shots_tableWidget.itemDoubleClicked.connect(self.editJob)
		# self.ui.shots_tableWidget.itemChanged.connect(lambda item: self.itemChecked(item))

		self.ui.seq_comboBox.currentIndexChanged.connect(self.updateShotsPreview)
		self.ui.seq_comboBox.editTextChanged.connect(self.updateShotsPreview)
		self.ui.prefix_comboBox.currentIndexChanged.connect(self.updateShotsPreview)
		self.ui.prefix_comboBox.editTextChanged.connect(self.updateShotsPreview)
		self.ui.shotCount_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.start_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.increment_spinBox.valueChanged.connect(self.updateShotsPreview)
		# self.ui.suffix_lineEdit.textChanged.connect(self.updateShotsPreview)

		self.ui.create_pushButton.clicked.connect(self.createShots)

		self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.accept)

		# Set input validators
		seq_pattern = r'\w*'
		seq_pattern_validator = QtGui.QRegExpValidator(QtCore.QRegExp(seq_pattern), self.ui.seq_comboBox.lineEdit())
		self.ui.seq_comboBox.lineEdit().setValidator(seq_pattern_validator)

		shot_pattern = r'^\w+#{0,8}\w*$'
		shot_pattern_validator = QtGui.QRegExpValidator(QtCore.QRegExp(shot_pattern), self.ui.prefix_comboBox.lineEdit())
		self.ui.prefix_comboBox.lineEdit().setValidator(shot_pattern_validator)

		# alphanumeric_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w]+'), self.ui.suffix_lineEdit)
		# self.ui.suffix_lineEdit.setValidator(alphanumeric_validator)

		# Instantiate jobs class and load data
		self.j = jobs.Jobs()
		self.sd = metadata.Metadata()


	def display(self, job=None):
		""" Display the dialog.
		"""
		self.job = job
		self.shot = None

		# self.reloadJobs(reloadDatabase=False)
		self.populateJobs(reloadDatabase=False)
		self.populateShots()
		# self.populateComboBox(self.ui.seq_comboBox, ['shots', 'build'], replace=False)
		# self.populateComboBox(self.ui.prefix_comboBox, ['sh###'], replace=False)

		self.toggleSidebar(False)

		return self.exec_()


	@QtCore.Slot(bool)
	def toggleSidebar(self, visible):
		""" Toggle the visibility of the Create Shot sidebar UI.
		"""
		if visible:
			self.ui.sidebar_frame.show()
			self.updateShotsPreview()

		else:
			self.ui.sidebar_frame.hide()


	def updateToolbarUI(self):
		""" Update the toolbar UI based on the current selection.
		"""
		widget = self.ui.shots_tableWidget
		self.shot = None

		# No items selected...
		if len(widget.selectedItems()) == 0:
			self.ui.shotDelete_toolButton.setEnabled(False)
			self.ui.shotSettings_toolButton.setEnabled(False)

		# One item selected...
		elif len(widget.selectedItems()) == 1:
			self.ui.shotDelete_toolButton.setEnabled(True)
			self.ui.shotSettings_toolButton.setEnabled(True)
			row = widget.currentItem().row()
			self.shot = widget.verticalHeaderItem(row).text()
			# print self.shot

		# More than one item selected...
		else:
			self.ui.shotDelete_toolButton.setEnabled(True)
			self.ui.shotSettings_toolButton.setEnabled(False)


	def getInheritedValue(self, shot_data, job_data, category, setting):
		""" First try to get the value from the shot data, if it returns
			nothing then look in job data instead.
		"""
		value = shot_data.get_attr(category, setting)
		if value is None:
			value = job_data.get_attr(category, setting)

		return value


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

		self.updateToolbarUI()

		# Re-enable signals
		self.ui.job_comboBox.blockSignals(False)


	def populateShots(self, shot_filter=""):
		""" Update the shots view table widget.
		"""
		currentJob = self.ui.job_comboBox.currentText()
		jobPath = self.j.getPath(currentJob, translate=True)
		shotLs = self.j.listShots(currentJob)

		self.ui.shots_tableWidget.clearContents()

		if shotLs:
			self.ui.shots_tableWidget.setRowCount(len(shotLs))
			for row, shotName in enumerate(shotLs):
				# Populate list view, using filter
				if shot_filter is not "":
					if shot_filter.lower() in shotName.lower():  # Case-insensitive
						item = self.addShotEntry(row, shotName, jobPath)
					self.ui.searchFilterClear_toolButton.setEnabled(True)

				else:
					item = self.addShotEntry(row, shotName, jobPath)
					self.ui.searchFilterClear_toolButton.setEnabled(False)

		self.ui.shots_tableWidget.resizeRowsToContents()


	def addShotEntry(self, row, shotName, jobPath):
		""" Add an entry to the shot list table view.
			TODO: optimise - currently very inefficient
		"""
		newRowHeaderItem = QtWidgets.QTableWidgetItem(shotName)
		newItem = QtWidgets.QTableWidgetItem(shotName)
		self.ui.shots_tableWidget.setVerticalHeaderItem(row, newRowHeaderItem)
		shot_datafile = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s/$IC_METADATA/shot_data.json" % (jobPath, shotName))
		job_datafile = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/$IC_METADATA/job_data.json" % jobPath)  # only read when switching jobs?
		shot_data = metadata.Metadata()
		job_data = metadata.Metadata()
		shot_data.load(shot_datafile)
		job_data.load(job_datafile)

		rangestart = self.getInheritedValue(shot_data, job_data, 'time', 'rangestart')
		rangeend = self.getInheritedValue(shot_data, job_data, 'time', 'rangeend')
		text = "%s-%s" % (rangestart, rangeend)
		self.ui.shots_tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(text))

		text = str(self.getInheritedValue(shot_data, job_data, 'units', 'fps'))
		self.ui.shots_tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(text))

		w = self.getInheritedValue(shot_data, job_data, 'resolution', 'fullwidth')
		h = self.getInheritedValue(shot_data, job_data, 'resolution', 'fullheight')
		text = "%sx%s" % (w, h)
		self.ui.shots_tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(text))

		w = self.getInheritedValue(shot_data, job_data, 'resolution', 'proxywidth')
		h = self.getInheritedValue(shot_data, job_data, 'resolution', 'proxyheight')
		text = "%sx%s" % (w, h)
		self.ui.shots_tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(text))

		text = shot_data.get_attr('camera', 'camera')
		self.ui.shots_tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(text))

		text = "%sx%s" %(shot_data.get_attr('camera', 'filmbackwidth'), shot_data.get_attr('camera', 'filmbackheight'))
		self.ui.shots_tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(text))

		text = str(shot_data.get_attr('camera', 'focallength'))
		self.ui.shots_tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(text))

		text = shot_data.get_attr('shot', 'notes')
		self.ui.shots_tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(text))

		# self.ui.shots_tableWidget.resizeRowToContents(row)

		return newItem


	# def deleteJobs(self):
	# 	""" Delete the selected job(s).
	# 	"""
	# 	for item in self.ui.shots_tableWidget.selectedItems():
	# 		self.j.deleteJob(item.text())
	# 		self.ui.shots_tableWidget.takeItem(self.ui.shots_tableWidget.row(item))


	# def itemChecked(self, item):
	# 	""" Set the active status of the job correctly when the checkbox state
	# 		changes.
	# 	"""
	# 	if item.checkState() == QtCore.Qt.Checked:
	# 		self.j.enableJob(item.text(), True)
	# 	else:
	# 		self.j.enableJob(item.text(), False)


	def openSettings(self, settingsType):
		""" Open settings dialog.
		"""
		jobPath = self.j.getPath(self.job, translate=True)
		shot_datafile = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s/$IC_METADATA/shot_data.json" % (jobPath, self.shot))
		job_datafile = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/$IC_METADATA/job_data.json" % jobPath)

		if settingsType == "Job":
			selfName = self.job
			categoryLs = ['job', 'apps', 'units', 'time', 'resolution', 'other']
			settingsFile = job_datafile
			inherit = None
		elif settingsType == "Shot":
			selfName = self.shot
			categoryLs = ['shot', 'units', 'time', 'resolution', 'camera']
			settingsFile = shot_datafile
			inherit = job_datafile

		from tools.settings import settings
		self.settingsEditor = settings.SettingsDialog(parent=self)
		result = self.settingsEditor.display(
			settings_type=settingsType, 
			self_name=selfName, 
			category_list=categoryLs, 
			prefs_file=settingsFile, 
			inherit=inherit)

		return result


	def jobSettings(self):
		""" Open job settings dialog wrapper function.
		"""
		if self.openSettings("Job"):
			self.populateShots()


	def shotSettings(self):
		""" Open shot settings dialog wrapper function.
		"""
		if self.openSettings("Shot"):
			self.populateShots()


	def updateShotsPreview(self):
		""" Update the preview field showing the shot directories to be
			created.
		"""
		multi_ui = [
			'shotCount_label', 'shotCount_spinBox', 
			'start_label', 'start_spinBox', 
			'increment_label', 'increment_spinBox']
		self.shots_to_create = []
		shotSeq = self.ui.seq_comboBox.currentText()
		if shotSeq != "":
			shotSeq += '/'

		shotName = self.ui.prefix_comboBox.currentText()

		count = self.ui.shotCount_spinBox.value()
		index = self.ui.start_spinBox.value()
		step = self.ui.increment_spinBox.value()
		re_digits_pattern = re.compile(r'#+')
		match = re.findall(re_digits_pattern, shotName)

		# Create multiple shots
		if match:
			hashes = str(match[0])
			padding = len(hashes)
			for shot in range(count):
				self.shots_to_create.append(
					shotSeq + shotName.replace(hashes, str(index).zfill(padding)))
				index += step
			for widget in multi_ui:
				eval('self.ui.%s.setEnabled(True)' % widget)

		# Create single shot
		else:
			verbose.warning("Cannot create multiple shots as there are no hashes (#) in shot name pattern.")
			self.shots_to_create.append(shotSeq + shotName)
			for widget in multi_ui:
				eval('self.ui.%s.setEnabled(False)' % widget)

		# Update UI elements
		self.ui.shotPreview_listWidget.clear()
		self.ui.shotPreview_listWidget.addItems(self.shots_to_create)
		num_shots = len(self.shots_to_create)
		if num_shots and shotName != "":
			self.ui.create_pushButton.setEnabled(True)
			self.ui.create_pushButton.setText(
				"Create %d %s" % (num_shots, verbose.pluralise('Shot', num_shots)))
		else:
			self.ui.create_pushButton.setEnabled(False)
			self.ui.create_pushButton.setText("Create")


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
		for shot in self.shots_to_create:
			path = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s/$IC_METADATA" % (jobPath, shot))
			os_wrapper.createDir(path)
			shotData = os.path.join(path, "shot_data.json")
			if self.sd.load(shotData):
				existing += 1
				existingShots += shot + " "
			elif self.sd.save():
				success += 1
				createdShots += shot + " "
			else:
				failure += 1
				failedShots += shot + " "

		if success:
			message = "%d %s created successfully: " % (success, verbose.pluralise('shot', success))
			dialogMsg += "%s\n%s\n\n" % (message, createdShots)
			verbose.message(message + createdShots)

		if existing:
			message = "The following %d shot(s) were not created as they already exist: " % existing
			dialogMsg += "%s\n%s\n\n" % (message, existingShots)
			verbose.warning(message + existingShots)

		if failure:
			message = "The following %d shot(s) could not be created - please check write permissions and try again: " % failure
			dialogMsg += "%s\n%s\n\n" % (message, failedShots)
			verbose.error(message + failedShots)

		# Confirmation dialog
		dialogTitle = "Shot Creator Results"
		dialog = prompt.dialog()
		dialog.display(dialogMsg, dialogTitle, conf=True)

		self.populateShots()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return \
		or event.key() == QtCore.Qt.Key_Enter:
			return


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

		# Store splitter size state
		self.settings.setValue("splitterSizes", self.ui.splitter.saveState())
		self.settings.setValue("shotsTableView", self.ui.shots_tableWidget.horizontalHeader().saveState())

# ----------------------------------------------------------------------------
# End of main dialog class
# ============================================================================
# Run as standalone app
# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	myApp = ShotManagementDialog()
	myApp.show()
	sys.exit(app.exec_())
