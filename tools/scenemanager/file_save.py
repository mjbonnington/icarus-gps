#!/usr/bin/python

# [scenemanager] file_save.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Scene Manager - Save File Dialog
# A UI for saving files/scenes/scripts.
# - Automatically handle file save locations, naming conventions and versions.
# - Provide a consistent experience across DCC apps.
# - Make it easier to find latest versions regardless of the last user to work
#   on the file.
# Current support is for Maya, Nuke and Houdini.


import os
import sys
# import time
# import traceback

from Qt import QtCore, QtGui, QtWidgets

# Import custom modules
import ui_template as UI

from shared import os_wrapper
from shared import recentFiles
from shared import sequence

try:
	import maya.cmds as mc
except ImportError:
	pass

try:
	import hou
except ImportError:
	pass

try:
	import nuke
	import nukescripts
except ImportError:
	pass


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
	def __init__(self, parent=None):
		super(FileSaveUI, self).__init__(parent)
		self.parent = parent

		self.setupUI(**cfg)
		self.conformFormLayoutLabels(self.ui)

		# Set window icon, flags and other Qt attributes
		self.setWindowFlags(QtCore.Qt.Dialog)

		# Set icons
		# self.ui.shot_toolButton.setIcon(self.iconSet('configure.svg'))  # causes crash?

		# Connect signals & slots
		# self.ui.shot_toolButton.clicked.connect(self.setShot)

		self.ui.discipline_comboBox.currentIndexChanged.connect(self.updateFilename)
		self.ui.description_comboBox.currentIndexChanged.connect(self.updateFilename)
		self.ui.description_comboBox.lineEdit().textChanged.connect(self.updateFilename)
		self.ui.version_spinBox.valueChanged.connect(self.updateFilename)
		self.ui.versionPadding_spinBox.valueChanged.connect(self.updateFilename)

		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.saveFile)
		self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.close)

		# # Context menus
		# self.addContextMenu(self.ui.shot_toolButton, "Change", self.setShot)
		# self.addContextMenu(self.ui.shot_toolButton, "Reset to current", self.setShot)

		# Set input validators
		desc_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w_]{1,32}'), self.ui.description_comboBox.lineEdit())
		self.ui.description_comboBox.lineEdit().setValidator(desc_validator)

		# Show initialisation message
		info_ls = []
		for key, value in self.getInfo().items():
			info_ls.append("{} {}".format(key, value))
		info_str = " | ".join(info_ls)
		print("%s v%s\n%s" % (cfg['window_title'], VERSION, info_str))


	def display(self):
		""" Display the window.
		"""
		self.returnValue = False

		self.setWindowTitle("%s - %s" % (cfg['window_title'], os.environ['SCNMGR_JOB']))

		self.ui.shot_lineEdit.setText(os.environ['SCNMGR_SHOT'])
		self.ui.shot_toolButton.setEnabled(False)  # temp until implemented

		self.file_ext = os.environ['SCNMGR_FILE_EXT'].split(os.pathsep)

		self.updateFilename()

		self.show()
		self.raise_()

		return self.returnValue


	def updateFilename(self):
		""" Update the filename field based on the other inputs.
		"""
		shot = self.ui.shot_lineEdit.text()
		discipline = self.ui.discipline_comboBox.currentText()
		description = self.ui.description_comboBox.currentText()

		#version = self.ui.version_comboBox.currentText()
		version = self.ui.version_spinBox.value()
		padding = self.ui.versionPadding_spinBox.value()
		v_str = "v" + str(version).zfill(padding)

		#os.environ['SCNMGR_CONVENTION'] = "<shot>.<discipline>.[description].<version>.ext"
		# valid_tokens = {
		# 	'<user>': 'SCNMGR_USER', 
		# 	'<user-initials>': 'SCNMGR_USER_INITIALS', 
		# 	'<job>': 'SCNMGR_JOB', 
		# 	'<shot>': 'SCNMGR_SHOT', 
		# 	'<discipline>': 'SCNMGR_DISCIPLINE', 
		# }

		# filename = os.environ['SCNMGR_CONVENTION']
		# filename = filename.replace('<artist>', os.environ['SCNMGR_USER'])
		# filename = filename.replace('<shot>', os.environ['SCNMGR_SHOT'])
		# filename = filename.replace('<discipline>', discipline)
		# filename = filename.replace('[description]', description)
		# filename = filename.replace('<version>', v_str)
		# computed_filename = filename + self.file_ext[0]  # Append file extension

		if description == "":
			computed_filename = ".".join([shot, discipline, v_str])
		else:
			computed_filename = ".".join([shot, discipline, description, v_str])
		computed_filename += self.file_ext[0]  # Add file extension
		self.ui.filename_lineEdit.setText(computed_filename)

		return computed_filename


	def saveFile(self):
		""" Dialog accept function.
		"""
		filename = os.path.join(os.environ['SCNMGR_SAVE_DIR'], self.updateFilename())
		# filename = oswrapper.absolutePath('$SCNMGR_SAVE_DIR/' +  self.updateFilename())

		if os.environ['SCNMGR_APP'] == "STANDALONE":
			pass

		elif os.environ['SCNMGR_APP'] == "MAYA":
			mc.file(rename=filename)
			recentFiles.updateLs(mc.file(options='v=0', force=True, save=True, type='mayaAscii'))

		elif os.environ['SCNMGR_APP'] == "HOUDINI":
			pass

		elif os.environ['SCNMGR_APP'] == "NUKE":
			nuke.scriptSaveAs(filename)
			recentFiles.updateLs(filename)

		self.returnValue = filename
		self.accept()


	# def snapshot(self, scene=None):
	# 	""" Save a copy (snapshot) of the current scene to a temp folder.
	# 		Return the path to the snapshot, ready to be submitted.
	# 	"""
	# 	#timestamp = time.strftime(r"%Y%m%d_%H%M%S")

	# 	if os.environ['SCNMGR_APP'] == "MAYA":
	# 		if scene:
	# 			uhub_origFilePath = scene
	# 		else:
	# 			uhub_origFilePath = mc.file(query=True, expandName=True)
	# 		uhub_tmpDir = os.path.join(os.environ['UHUB_MAYA_SCENES_PATH'], '.tmp')
	# 		oswrapper.createDir(uhub_tmpDir)
	# 		uhub_sceneName = mc.file(query=True, sceneName=True, shortName=True)
	# 		uhub_tmpFilePath = os.path.join(uhub_tmpDir, uhub_sceneName)

	# 		# Ensure output file naming convention is correct
	# 		if self.getRenderer() == 'vray':
	# 			mc.setAttr("vraySettings.fileNamePrefix", lock=False)
	# 			mc.setAttr("vraySettings.fileNamePrefix", MAYA_OUTPUT_FORMAT_VRAY, type="string")
	# 			mc.setAttr("vraySettings.fileNameRenderElementSeparator", lock=False)
	# 			mc.setAttr("vraySettings.fileNameRenderElementSeparator", ".", type="string")

	# 		else:  # Maya Common Default and Arnold
	# 			mc.setAttr("defaultRenderGlobals.imageFilePrefix", MAYA_OUTPUT_FORMAT, type="string")

	# 		mc.file(rename=uhub_tmpFilePath)
	# 		snapshotScene = mc.file(save=True)
	# 		mc.file(rename=uhub_origFilePath)
	# 		#mc.file(save=True)
	# 		print("Saved snapshot: %s" % snapshotScene)
	# 		return snapshotScene

	# 	# elif os.environ['SCNMGR_APP'] == "NUKE":
	# 	# 	currentScript = nuke.root()['name'].value()
	# 	# 	#dirname, basename = os.path.split(currentScript)
	# 	# 	#snapshotScript = os.path.join(tmpdir, basename)
	# 	# 	base, ext = os.path.splitext(basename)
	# 	# 	snapshotScript = "%s_snapshot_%s%s" % (base, timestamp, ext)
	# 	# 	nuke.scriptSave(snapshotScript)
	# 	# 	nuke.root()['name'].setValue(currentScript)
	# 	# 	return snapshotScript


# 	def saveScene(self):
# 		""" Save the current scene/script if it has been modified.
# 		"""
# 		if os.environ['SCNMGR_APP'] == "STANDALONE":
# 			pass  # Do nothing

# 		elif os.environ['SCNMGR_APP'] == "MAYA":
# 			# Check if scene is modified before saving, as Maya scene files
# 			# can be quite large and saving can be slow.
# 			if mc.file(q=True, modified=True):
# 				mc.file(save=True)

# 		elif os.environ['SCNMGR_APP'] == "HOUDINI":
# 			hou.hipFile.save()

# 		elif os.environ['SCNMGR_APP'] == "NUKE":
# 			nuke.scriptSave()


# 	def incrementScene(self):
# 		""" Increment the minor version number. For Maya, don't save as this
# 			can be slow for large scenes. Instead copy the previous scene
# 			file via the OS.
# 		"""
# 		if os.environ['SCNMGR_APP'] == "STANDALONE":
# 			pass  # Do nothing

# 		elif os.environ['SCNMGR_APP'] == "MAYA":
# 			# As the scene will have just been saved, we create a copy of the
# 			# scene and increment the minor version, and point the Maya file
# 			# to the updated scene file. This gives us a performance gain by
# 			# avoiding the overhead of a second save operation, which can be
# 			# slow for large Maya ASCII scenes.
# 			from u_vfx.u_maya.scripts.python import sceneManager
# 			current_scene = mc.file(query=True, expandName=True)
# 			ext = os.path.splitext(current_scene)[1]
# 			updated_scene = sceneManager.versionUp(saveScene=False)
# 			if updated_scene:
# 				updated_scene += ext
# 				oswrapper.copy(current_scene, updated_scene)
# 				mc.file(rename=updated_scene)
# 				# self.addSceneEntry(self.ui.mayaScene_comboBox, updated_scene)
# 				self.getScene()

# 		elif os.environ['SCNMGR_APP'] == "HOUDINI":
# 			from u_vfx.u_houdini.scripts import sceneManager
# 			if sceneManager.versionUp():
# 				self.getScene()

# 		elif os.environ['SCNMGR_APP'] == "NUKE":
# 			from u_vfx.u_nuke.scripts import compManager
# 			if compManager.versionUp():
# 				self.getScene()


# 	def about(self):
# 		""" Show about dialog.
# 		"""
# 		import about

# 		info_ls = []
# 		sep = " | "
# 		for key, value in self.getInfo().items():
# 			if key in ['Environment', 'OS']:
# 				pass
# 			else:
# 				info_ls.append("{} {}".format(key, value))
# 		info_str = sep.join(info_ls)

# 		about_msg = """
# %s
# v%s

# A UI for saving files/scenes/scripts.
# - Automatically handle file save locations, naming conventions and versions.
# - Provide a consistent experience across DCC apps.
# - Make it easier to find latest versions regardless of the last user to work on the file.
# Current support is for Maya, Nuke and Houdini.

# Developer: Mike Bonnington
# (c) 2019

# %s
# """ % (cfg['window_title'], VERSION, info_str)

# 		aboutDialog = about.AboutDialog(parent=self)
# 		aboutDialog.display(
# 			bg_color=QtGui.QColor('#5b6368'), 
# 			icon_pixmap=self.iconTint(
# 				'clapperboard.png', 
# 				tint=QtGui.QColor('#6e777d')), 
# 			message=about_msg)


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

def run_maya(session, **kwargs):
	""" Run in Maya.
	"""
	try:  # Show the UI
		session.fileSaveUI.display(**kwargs)
	except:  # Create the UI
		UI._maya_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.fileSaveUI = FileSaveUI(parent=UI._maya_main_window())
		session.fileSaveUI.display(**kwargs)


# def run_houdini(session, **kwargs):
# 	""" Run in Houdini.
# 	"""
# 	try:  # Show the UI
# 		session.fileSaveUI.display(**kwargs)
# 	except:  # Create the UI
# 		#UI._houdini_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
# 		#session = UI._houdini_get_session()
# 		session.fileSaveUI = FileSaveUI(parent=UI._houdini_main_window())
# 		session.fileSaveUI.display(**kwargs)


def run_nuke(session, **kwargs):
	""" Run in Nuke.
	"""
	try:  # Show the UI
		session.fileSaveUI.display(**kwargs)
	except:  # Create the UI
		UI._nuke_delete_ui(cfg['window_object'], cfg['window_title'])  # Delete any existing UI
		session.fileSaveUI = FileSaveUI(parent=UI._nuke_main_window())
		session.fileSaveUI.display(**kwargs)
