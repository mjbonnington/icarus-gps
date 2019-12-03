#!/usr/bin/python

# [scenemanager] file_save.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Scene Manager - Save File Dialog
# A UI for saving files/scenes/scripts.


import os
# import sys

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from . import convention
# from shared import os_wrapper
# from shared import recentFiles
from shared import verbose

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

VERSION = "0.1.0"

cfg = {}

# Set window title and object names
cfg['window_object'] = "fileSaveUI"
if os.environ['SCNMGR_VENDOR_INITIALS']:
	cfg['window_title'] = "%s Save" % os.environ['SCNMGR_VENDOR_INITIALS']
else:
	cfg['window_title'] = "Save"

# Set the UI and the stylesheet
cfg['ui_file'] = 'file_save.ui'
cfg['stylesheet'] = 'style.qss'  # Set to None to use the parent app's stylesheet

# Other options
cfg['prefs_file'] = os.path.join(
	os.environ['SCNMGR_USER_PREFS_DIR'], 'scenemanager_prefs.json')
cfg['store_window_geometry'] = True

# ----------------------------------------------------------------------------
# Begin main window class
# ----------------------------------------------------------------------------

class FileSaveUI(QtWidgets.QDialog, UI.TemplateUI):
#class FileSaveUI(QtWidgets.QMainWindow, UI.TemplateUI):
	""" File Save UI.
	"""
	def __init__(self, parent=None, session=None):
		super(FileSaveUI, self).__init__(parent)
		self.parent = parent
		self.session = session

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui)

		# Set window icon, flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set icons
		# self.ui.shot_toolButton.setIcon(self.iconSet('configure.svg'))  # causes crash?
		self.ui.nativeDialog_toolButton.setIcon(self.iconSet('folder-open.svg'))  # find better icon

		# Connect signals & slots
		# self.ui.shot_toolButton.clicked.connect(self.setShot)
		# self.ui.shotChange_toolButton.clicked.connect(self.setShot)
		# self.ui.shotReset_toolButton.clicked.connect(self.resetShot)

		self.ui.discipline_comboBox.currentIndexChanged.connect(self.updateFilename)
		self.ui.description_comboBox.currentIndexChanged.connect(self.updateFilename)
		self.ui.description_comboBox.lineEdit().textChanged.connect(self.updateFilename)
		# self.ui.version_spinBox.valueChanged.connect(self.updateFilename)

		self.ui.nativeDialog_toolButton.clicked.connect(self.nativeDialog)

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveFile)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

		# # Context menus
		# self.addContextMenu(self.ui.shot_toolButton, "Change", self.setShot)
		# self.addContextMenu(self.ui.shot_toolButton, "Reset to current", self.setShot)

		# Set input validators
		desc_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w_]{1,32}'), self.ui.description_comboBox.lineEdit())
		self.ui.description_comboBox.lineEdit().setValidator(desc_validator)

		# # Show initialisation message
		# info_ls = []
		# for key, value in self.getInfo().items():
		# 	info_ls.append("{} {}".format(key, value))
		# info_str = " | ".join(info_ls)
		# verbose.message("%s v%s" % (cfg['window_title'], VERSION))
		# verbose.print_(info_str)


	def display(self, current=None):
		""" Display the window. Pass in the current scene/script name to be
			parsed and autofill dialog fields.
		"""
		self.returnValue = False

		self.setWindowTitle("%s - %s" % (cfg['window_title'], os.environ['SCNMGR_JOB']))

		self.ui.shot_lineEdit.setText(os.environ['SCNMGR_SHOT'])
		self.ui.shot_toolButton.setEnabled(False)  # temp until implemented
		self.ui.version_spinBox.hide()

		self.file_ext = os.environ['SCNMGR_FILE_EXT'].split(os.pathsep)

		# Set values from current file if possible
		# TODO: optimise
		presets = convention.parse(self.session.get_current_name())
		if presets is not None:
			try:
				self.ui.shot_lineEdit.setText(presets['<shot>'])
				self.ui.discipline_comboBox.setCurrentIndex(
					self.ui.discipline_comboBox.findText(
						presets['<discipline>']))
				widget = self.ui.description_comboBox
				if '<description>' in presets:
					value = presets['<description>']
				else:
					value = ""
				if widget.findText(value) == -1:
					widget.insertItem(0, value)
				widget.setCurrentIndex(widget.findText(value))

			except KeyError:
				pass

		self.updateFilename()

		self.show()
		self.raise_()

		return self.returnValue


	def updateFilename(self):
		""" Update the filename field based on the other inputs.
		"""
		ignore_list = ["[any]", "[please select]", "", None]

		shot = self.ui.shot_lineEdit.text()
		discipline = self.ui.discipline_comboBox.currentText()
		description = self.ui.description_comboBox.currentText()

		# version = self.ui.version_spinBox.value()
		# v_str = convention.version_to_str(version)
		v_str = convention.version_to_str(1)  # Set version to 1

		if discipline in ignore_list:
			# Modify UI elements
			self.ui.filename_lineEdit.setText("Please select a discipline")
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(False)
			self.setDynamicProperty(self.ui.filename_lineEdit, "warning", True)
			self.setDynamicProperty(self.ui.discipline_comboBox, "warning", True)

			return None

		# Generate filename - this should be rewritten to adhere to convention
		else:
			if description == "":
				computed_filename = ".".join([shot, discipline, v_str])
			else:
				computed_filename = ".".join([shot, discipline, description, v_str])

			computed_filename += self.file_ext[0]  # Add file extension

			# Detect the latest version
			message = ""
			result, n = convention.version_next_meta(shot, discipline, description)
			if result:
				computed_filename = os.path.basename(result)
				message = "%d existing %s found" % (n, verbose.pluralise("version", n))
				# self.ui.version_spinBox.setEnabled(False)
			else:
				message = "new"

			# Modify UI elements
			self.ui.v_info_label.setText(message)
			self.ui.filename_lineEdit.setText(computed_filename)
			self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
			self.setDynamicProperty(self.ui.filename_lineEdit, "warning", False)
			self.setDynamicProperty(self.ui.discipline_comboBox, "warning", False)

			return computed_filename


	def saveFile(self):
		""" Dialog accept function.
		"""
		filename = os.path.join(os.environ['SCNMGR_SAVE_DIR'], self.updateFilename())
		# filename = os_wrapper.absolutePath('$SCNMGR_SAVE_DIR/' +  self.updateFilename())

		if self.session.file_save_as(filename):
			self.returnValue = filename
			self.accept()


	def nativeDialog(self):
		""" Save file using application-native dialog.
		"""
		self.hide()

		if self.session.file_save_native_dialog():
			self.close()
		else:  # Return to custom dialog
			self.show()


	def keyPressEvent(self, event):
		""" Override function to prevent Enter / Esc keypresses triggering
			OK / Cancel buttons.
		"""
		if event.key() == QtCore.Qt.Key_Return \
		or event.key() == QtCore.Qt.Key_Enter:
			return


	def closeEvent(self, event):
		""" Event handler for when window is closed.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main window class
# ============================================================================
# Run functions
# ----------------------------------------------------------------------------

def dialog(session, app='standalone'):
	""" Instantiate UI object parented to appropriate app's main window
	"""
	if app == 'standalone':
		pass
	elif app == 'maya':
		parent = UI._maya_main_window()
	elif app == 'houdini':
		parent = UI._houdini_main_window()
	elif app == 'nuke':
		parent = UI._nuke_main_window()

	return FileSaveUI(parent=parent, session=session)
