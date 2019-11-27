#!/usr/bin/python

# [nuke] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures for Nuke.


import os
import nuke
# import sys
# import traceback

# Import custom modules
from . import file_open
from . import file_save
# from shared import os_wrapper
from shared import pDialog
from shared import recentFiles


class SceneManager(object):
	""" Interface to wrap Nuke's file open/save functionality.
	"""
	def __init__(self):
		self.app = 'nuke'
		self.file_open_ui = file_open.dialog(self, app=self.app)
		self.file_save_ui = file_save.dialog(self, app=self.app)


	def file_new(self):
		""" Start a new file with some default settings.
		"""
		if self.confirm():
			nuke.scriptClear()
			self.set_defaults()


	def file_open_dialog(self, **kwargs):
		""" Display a custom dialog to select a file to open.
		"""
		return self.file_open_ui.display(**kwargs)


	def file_open_native_dialog(self, starting_dir=None):
		""" Display a native dialog to select a file to open.
			N.B. try/except to catch RuntimeError when dialog is cancelled.
		"""
		try:
			if starting_dir is None:
				nuke.scriptOpen()

			else:
				nuke.scriptOpen(os.path.join(starting_dir, '.'))

			return True

		except RuntimeError:
			return False


	def file_open(self, filepath):
		""" Open the specified file.
		"""
		if self.confirm():
			try:
				nuke.scriptClear()
				nuke.scriptOpen(filepath)
				recentFiles.updateLs(filepath)
				return filepath

			except RuntimeError as e:
				# exc_type, exc_value, exc_traceback = sys.exc_info()
				# # traceback.print_exception(exc_type, exc_value, exc_traceback)
				# dialog_msg = traceback.format_exception_only(exc_type, exc_value)[0]
				dialog = pDialog.dialog()
				dialog.display(str(e), "Message", conf=True)
				return False

		else:
			return False


	def file_save_dialog(self, **kwargs):
		""" Display a custom dialog for saving a file.
		"""
		return self.file_save_ui.display(**kwargs)


	def file_save_native_dialog(self, starting_dir=None):
		""" Display a native dialog for saving a file.
			N.B. try/except to catch RuntimeError when dialog is cancelled.
		"""
		try:
			if starting_dir is None:
				nuke.scriptSaveAs()

			else:
				nuke.scriptSaveAs(os.path.join(starting_dir, '.'))

			return True

		except RuntimeError:
			return False


	def file_save(self):
		""" Save the current file.
			If saving for first time take over and show custom dialog.
		"""
		if nuke.Root().name() == 'Root':  # Is current file unsaved?
			self.file_save_dialog()

		else:
			nuke.scriptSave()


	def file_save_as(self, filepath):
		""" Save the current file to the specified filepath.
			Nuke automatically prompts if file already exists.
			N.B. try/except to catch RuntimeError when dialog is cancelled.
		"""
		try:
			nuke.scriptSaveAs(filepath)
			recentFiles.updateLs(filepath)
			return True

		except RuntimeError:
			return False


	def file_save_new_version(self):
		""" Convenience function to save a new version of a file.
		"""
		pass


	def file_snapshot(self, dest_dir=None):
		""" Save a copy (snapshot) of the current scene to the destination
			directory, without changing the current file pointer.
		"""
		pass


	def file_get_name(self):
		""" Get the name of the current file.
		"""
		return nuke.Root().name()


	def file_set_name(self, new_name):
		""" Change the name of the current file.
		"""
		pass


	def confirm(self):
		""" Obtain confirmation to proceed with operation if the current file
			is not saved.
		"""
		if nuke.Root().modified():
			return nuke.ask("The current script has been modified. Do you want to continue?")
		else:
			return True


	def update_recents_menu(self, menu):
		""" Populate the recent files menu or disable it if no recent files
			in list.
		"""
		enable = True;
		fileLs = recentFiles.getLs('nuke')  # Explicitly stating 'nuke' environment to get around 'nuke_tmp' fix

		# Delete all items in the pop-up menu
		menu.clearMenu()

		# Re-populate the items in the pop-up menu
		for item in fileLs:
			# openRecentCmdStr = 'nuke.scriptOpen(\"%s%s\")' % (os.environ['IC_SHOTPATH'], item)
			openRecentCmdStr = 'session.scnmgr.file_open(\"%s%s\")' % (os.environ['IC_SHOTPATH'], item)
			menu.addCommand(item.replace('/', '\/'), openRecentCmdStr.replace('\\', '/'))  # Forward slashes need escaping to prevent Nuke from interpreting them as sub-menus

		# If recent file list contains no entries, disable menu
		if len(fileLs) == 0:
			enable = False
		if len(fileLs) == 1 and fileLs[0] == "":
			enable = False

		menu.setEnabled(enable)


	def update_recent_files(self, script=None):
		""" Adds a script to the recent files list config file. If script is
			not specified use current script name.
		"""
		if script == None:
			script = os.path.abspath(nuke.value('root.name'))

		# Add entry to recent files config file
		recentFiles.updateLs(script, 'nuke')  # Explicitly stating 'nuke' environment to get around 'nuke_tmp' fix

		# Update custom recent files menu(s) - these are dependent on the
		# menus defined in menu.py so modify with caution
		if os.environ['IC_VENDOR_INITIALS']:
			vendor = os.environ['IC_VENDOR_INITIALS'] + " "
		else:
			vendor = ""
		self.update_recents_menu(nuke.menu('Nuke').menu('File').menu(vendor+'Open Recent'))
		self.update_recents_menu(nuke.menu('Nodes').menu('Open').menu('Open Recent'))


	def set_defaults(self):
		""" Automatically set some defaults from the shot settings for a new
			script.
		"""
		plateFormat = '%s %s %s' % (int(os.environ['RESOLUTIONX']), int(os.environ['RESOLUTIONY']), os.environ['IC_SHOT'])
		proxyFormat = '%s %s %s' % (int(os.environ['PROXY_RESOLUTIONX']), int(os.environ['PROXY_RESOLUTIONY']), '%s_proxy' % os.environ['IC_SHOT'])
		nuke.addFormat(plateFormat)
		nuke.addFormat(proxyFormat)

		nuke.knobDefault('Root.format', os.environ['IC_SHOT'])
		nuke.knobDefault('Root.proxy_type', 'format')
		nuke.knobDefault('Root.proxy_format', '%s_proxy' % os.environ['IC_SHOT'])
		nuke.knobDefault('Root.fps', os.environ['FPS'])
		nuke.knobDefault('Root.first_frame', os.environ['STARTFRAME'])
		nuke.knobDefault('Root.last_frame', os.environ['ENDFRAME'])


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


