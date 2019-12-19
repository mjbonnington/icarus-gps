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

VERSION = "0.2.0"

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

		# Show initialisation message
		verbose.message("%s v%s" % (cfg['window_title'], VERSION))

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui.sidebar_frame)

		# Set window icon, flags and other Qt attributes
		# self.setWindowIcon(self.iconSet('filmgrain.svg', tintNormal=False))
		self.setWindowFlags(QtCore.Qt.Dialog)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Restore splitter size state
		try:
			self.ui.splitter.restoreState(self.settings.value("splitterSizes")) #.toByteArray())
			self.ui.shots_tableWidget.horizontalHeader().restoreState(self.settings.value("shotsTableView")) #.toByteArray())
		except:
			pass

		# Set icons
		self.ui.shotCreate_toolButton.setIcon(self.iconSet('filmgrain.svg'))
		self.ui.shotDelete_toolButton.setIcon(self.iconSet('edit-delete.svg'))
		self.ui.shotSettings_toolButton.setIcon(self.iconSet('configure.svg'))
		self.ui.refresh_toolButton.setIcon(self.iconSet('icon_refresh.png'))
		self.ui.import_toolButton.setIcon(self.iconSet('icon_arrow_down.png'))
		self.ui.export_toolButton.setIcon(self.iconSet('icon_arrow_up.png'))

		self.ui.searchFilterClear_toolButton.setIcon(self.iconSet('clear.svg'))

		# Connect signals & slots
		self.ui.job_comboBox.currentIndexChanged.connect(self.reloadJobData)

		self.ui.shotCreate_toolButton.toggled.connect(lambda checked: self.toggleSidebar(checked))
		self.ui.shotDelete_toolButton.clicked.connect(self.deleteShots)
		self.ui.shotSettings_toolButton.clicked.connect(self.shotSettings)
		self.ui.refresh_toolButton.clicked.connect(lambda: self.populateShots())

		self.ui.searchFilter_lineEdit.textChanged.connect(lambda text: self.populateShots(shot_filter=text))
		self.ui.searchFilterClear_toolButton.clicked.connect(self.clearFilter)

		self.ui.shots_tableWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		# self.ui.shots_tableWidget.itemDoubleClicked.connect(lambda: self.editCell)
		# self.ui.shots_tableWidget.itemChanged.connect(lambda item: self.itemChecked(item))

		self.ui.seq_comboBox.currentIndexChanged.connect(self.updateShotsPreview)
		self.ui.seq_comboBox.editTextChanged.connect(self.updateShotsPreview)
		self.ui.prefix_comboBox.currentIndexChanged.connect(self.updateShotsPreview)
		self.ui.prefix_comboBox.editTextChanged.connect(self.updateShotsPreview)
		self.ui.shotCount_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.start_spinBox.valueChanged.connect(self.updateShotsPreview)
		self.ui.increment_spinBox.valueChanged.connect(self.updateShotsPreview)

		self.ui.create_pushButton.clicked.connect(self.createShots)

		self.ui.main_buttonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(self.accept)

		# Set input validators
		seq_pattern = r'\w*'
		seq_pattern_validator = QtGui.QRegExpValidator(QtCore.QRegExp(seq_pattern), self.ui.seq_comboBox.lineEdit())
		self.ui.seq_comboBox.lineEdit().setValidator(seq_pattern_validator)

		shot_pattern = r'^\w+#{0,8}\w*$'
		shot_pattern_validator = QtGui.QRegExpValidator(QtCore.QRegExp(shot_pattern), self.ui.prefix_comboBox.lineEdit())
		self.ui.prefix_comboBox.lineEdit().setValidator(shot_pattern_validator)

		# Instantiate jobs and metadata classes
		self.j = jobs.Jobs()
		self.job_data = metadata.Metadata()
		self.shot_data = metadata.Metadata()


	def display(self, job=None):
		""" Display the dialog.
		"""
		self.job = job
		self.shot = None

		self.columns = [
			'time.rangestart', 
			'time.rangeend', 
			'units.fps', 
			'resolution.fullwidth', 
			'resolution.fullheight', 
			'camera.filmbackwidth', 
			'camera.filmbackheight', 
			'camera.focallength', 
			'camera.clipref',
			'shot.notes']

		# self.reloadJobs(reload_database=False)
		self.populateJobs(reload_database=False)
		self.reloadJobData()
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

		# # One item selected...
		# elif len(widget.selectedItems()) == 1:
		# 	self.ui.shotDelete_toolButton.setEnabled(True)
		# 	self.ui.shotSettings_toolButton.setEnabled(True)
		# 	row = widget.currentItem().row()
		# 	self.shot = widget.verticalHeaderItem(row).text()
		# 	# print(self.shot)

		# # More than one item selected...
		# else:
		# 	self.ui.shotDelete_toolButton.setEnabled(True)
		# 	self.ui.shotSettings_toolButton.setEnabled(False)

		else:
			self.ui.shotDelete_toolButton.setEnabled(True)
			self.ui.shotSettings_toolButton.setEnabled(True)
			row = widget.currentItem().row()
			self.shot = widget.verticalHeaderItem(row).text()


	def clearFilter(self):
		""" Clear the search filter field.
		"""
		self.ui.searchFilter_lineEdit.clear()
		self.ui.searchFilterClear_toolButton.setEnabled(False)


	def getInheritedValue(self, shot_data, category, setting):
		""" First try to get the value from the shot data, if it returns
			nothing then look in job data instead.
		"""
		inherited = False
		value = shot_data.get_attr(category, setting)
		if value is None:
			value = self.job_data.get_attr(category, setting)
			inherited = True

		if value is None:
			return "", inherited
		else:
			return value, inherited


	def getJobDatafile(self):
		""" Return the path to the JSON metadata file for the current job.
		"""
		return os_wrapper.absolutePath("%s/$IC_SHOTSDIR/$IC_METADATA/job_data.json" % self.job_path)


	def getShotDatafile(self, shot_name):
		""" Return the path to the JSON metadata file for the specified shot.
		"""
		return os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s/$IC_METADATA/shot_data.json" % (self.job_path, shot_name))


	def populateJobs(self, reload_database=True):
		""" Populate the jobs combo box.
		"""
		if reload_database:
			self.j.loadXML(quiet=True)  # Reload XML data

		# Stop the widget from emitting signals
		self.ui.job_comboBox.blockSignals(True)

		# Clear combo box
		self.ui.job_comboBox.clear()

		joblist = self.j.getActiveJobs()
		if joblist:
			joblist = sorted(joblist, reverse=True)

			for job in joblist:
				self.ui.job_comboBox.insertItem(0, job)

			# Attempt to set the combo box to the current job
			if self.job in joblist:
				self.ui.job_comboBox.setCurrentIndex(self.ui.job_comboBox.findText(self.job))

			# Set the combo box to the first item
			else:
				self.ui.job_comboBox.setCurrentIndex(0)

		self.updateToolbarUI()

		# Re-enable signals
		self.ui.job_comboBox.blockSignals(False)


	def reloadJobData(self):
		""" Reload job data when job combobox value is changed.
		"""
		self.job = self.ui.job_comboBox.currentText()
		self.job_path = self.j.getPath(self.job, translate=True)
		self.job_data.load(self.getJobDatafile())

		self.populateShots()


	def populateShots(self, shot_filter=""):
		""" Update the shots view table widget.
			TODO: optimise - currently very inefficient
		"""
		shotlist = self.j.listShots(self.job)  # S L O W

		widget = self.ui.shots_tableWidget
		widget.clearContents()
		widget.setColumnCount(len(self.columns))
		for col, attr in enumerate(self.columns):
			category, attribute = attr.split('.')
			newColHeaderItem = QtWidgets.QTableWidgetItem(attribute)
			widget.setHorizontalHeaderItem(col, newColHeaderItem)

		if shotlist:
			widget.setRowCount(len(shotlist))
			for row, shot_name in enumerate(shotlist):
				# Populate list view, using filter
				if shot_filter is not "":
					if shot_filter.lower() in shot_name.lower():  # Case-insensitive
						item = self.addShotEntry(row, shot_name)
					self.ui.searchFilterClear_toolButton.setEnabled(True)

				else:
					item = self.addShotEntry(row, shot_name)
					self.ui.searchFilterClear_toolButton.setEnabled(False)

		# widget.resizeColumnsToContents()


	def addShotEntry(self, row, shot_name):
		""" Add an entry to the shot list table view.
			TODO: optimise - currently very inefficient
		"""
		widget = self.ui.shots_tableWidget
		newRowHeaderItem = QtWidgets.QTableWidgetItem(shot_name)
		# newItem = QtWidgets.QTableWidgetItem(shot_name)
		widget.setVerticalHeaderItem(row, newRowHeaderItem)

		shot_datafile = self.getShotDatafile(shot_name)
		shot_data = metadata.Metadata()
		shot_data.load(shot_datafile)

		for col, attr in enumerate(self.columns):
			category, attribute = attr.split('.')
			value, inherited = self.getInheritedValue(shot_data, category, attribute)
			item = QtWidgets.QTableWidgetItem(str(value))
			if inherited:
				item.setForeground(self.col['disabled'])
			widget.setItem(row, col, item)

		# rangestart = self.getInheritedValue(shot_data, 'time', 'rangestart')
		# rangeend = self.getInheritedValue(shot_data, 'time', 'rangeend')
		# text = "%s-%s" % (rangestart, rangeend)
		# widget.setItem(row, 0, QtWidgets.QTableWidgetItem(text))

		# text = str(self.getInheritedValue(shot_data, 'units', 'fps'))
		# widget.setItem(row, 1, QtWidgets.QTableWidgetItem(text))

		# w = self.getInheritedValue(shot_data, 'resolution', 'fullwidth')
		# h = self.getInheritedValue(shot_data, 'resolution', 'fullheight')
		# text = "%sx%s" % (w, h)
		# widget.setItem(row, 2, QtWidgets.QTableWidgetItem(text))

		# w = self.getInheritedValue(shot_data, 'resolution', 'proxywidth')
		# h = self.getInheritedValue(shot_data, 'resolution', 'proxyheight')
		# text = "%sx%s" % (w, h)
		# widget.setItem(row, 3, QtWidgets.QTableWidgetItem(text))

		# text = str(self.getInheritedValue(shot_data, 'camera', 'camera'))
		# widget.setItem(row, 4, QtWidgets.QTableWidgetItem(text))

		# w = self.getInheritedValue(shot_data, 'camera', 'filmbackwidth')
		# h = self.getInheritedValue(shot_data, 'camera', 'filmbackheight')
		# text = "%sx%s" % (w, h)
		# widget.setItem(row, 5, QtWidgets.QTableWidgetItem(text))

		# text = str(self.getInheritedValue(shot_data, 'camera', 'focallength'))
		# widget.setItem(row, 6, QtWidgets.QTableWidgetItem(text))

		# text = str(self.getInheritedValue(shot_data, 'shot', 'notes'))
		# widget.setItem(row, 7, QtWidgets.QTableWidgetItem(text))

		widget.resizeRowToContents(row)

		# return newItem


	def deleteShots(self):
		""" Delete the selected shot(s).
			TODO: implement properly
		"""
		# Confirmation dialog
		dialog_title = "Delete shot: %s" % self.shot
		dialog_msg = "Are you sure?"
		dialog = prompt.dialog()
		if dialog.display(dialog_msg, dialog_title):
			shot_path = os_wrapper.absolutePath("%s/$IC_SHOTSDIR/%s" % (self.job_path, self.shot))
			result, msg = os_wrapper.remove(shot_path)
			if result:
				verbose.message("Shot '%s' deleted: %s" % (self.shot, self.job_path))
				self.populateShots()
			else:
				dialog.display(msg, "Failed to delete shot", conf=True)


	def openSettings(self, settingsType):
		""" Open settings dialog.
		"""
		if settingsType == "Job":
			selfName = self.job
			categoryLs = ['job', 'apps', 'units', 'time', 'resolution', 'other']
			settingsFile = self.getJobDatafile()
			inherit = None
		elif settingsType == "Shot":
			selfName = self.shot
			categoryLs = ['shot', 'units', 'time', 'resolution', 'camera']
			settingsFile = self.getShotDatafile(self.shot)
			inherit = self.getJobDatafile()

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

		seq_name = self.ui.seq_comboBox.currentText()
		if seq_name != "":
			seq_name += '/'

		shot_name = self.ui.prefix_comboBox.currentText()

		count = self.ui.shotCount_spinBox.value()
		index = self.ui.start_spinBox.value()
		step = self.ui.increment_spinBox.value()
		re_digits_pattern = re.compile(r'#+')
		match = re.findall(re_digits_pattern, shot_name)

		# Create multiple shots
		if match:
			hashes = str(match[0])
			padding = len(hashes)
			for shot in range(count):
				self.shots_to_create.append(
					seq_name + shot_name.replace(hashes, str(index).zfill(padding)))
				index += step
			for widget in multi_ui:
				eval('self.ui.%s.setEnabled(True)' % widget)

		# Create single shot
		else:
			verbose.warning("Cannot create multiple shots as there are no hashes (#) in shot name pattern.")
			self.shots_to_create.append(seq_name + shot_name)
			for widget in multi_ui:
				eval('self.ui.%s.setEnabled(False)' % widget)

		# Update UI elements
		self.ui.shotPreview_listWidget.clear()
		self.ui.shotPreview_listWidget.addItems(self.shots_to_create)
		num_shots = len(self.shots_to_create)
		if num_shots and shot_name != "":
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
		shots_created = ""
		shots_existing = ""
		shots_failed = ""
		dialog_msg = ""

		for shot in self.shots_to_create:
			shot_datafile = self.getShotDatafile(shot)
			os_wrapper.createDir(os.path.dirname(shot_datafile))

			if self.shot_data.load(shot_datafile):
				existing += 1
				shots_existing += shot + "\n"
			elif self.shot_data.save():
				success += 1
				shots_created += shot + "\n"
			else:
				failure += 1
				shots_failed += shot + "\n"

		if success:
			message = "%d %s created successfully: " % (success, verbose.pluralise('shot', success))
			dialog_msg += "%s\n%s\n" % (message, shots_created)
			verbose.message(message + shots_created)

		if existing:
			message = "The following %d shot(s) were not created as they already exist: " % existing
			dialog_msg += "%s\n%s\n" % (message, shots_existing)
			verbose.warning(message + shots_existing)

		if failure:
			message = "The following %d shot(s) could not be created - please check write permissions and try again: " % failure
			dialog_msg += "%s\n%s\n" % (message, shots_failed)
			verbose.error(message + shots_failed)

		# Confirmation dialog
		dialog_title = "Shot Creator Results"
		dialog = prompt.dialog()
		dialog.display(dialog_msg, dialog_title, conf=True)

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
