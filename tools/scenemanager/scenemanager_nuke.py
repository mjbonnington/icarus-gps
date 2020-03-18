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
from . import convention
from . import file_open
from . import file_save
from shared import os_wrapper
from shared import prompt
from shared import recent_files


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

		except RuntimeError as e:
			if str(e) != "Cancelled":
				dialog = prompt.Dialog()
				dialog.display(str(e), "Error Opening File", conf=True)
			return False


	def file_open(self, filepath):
		""" Open the specified file.
		"""
		if self.confirm():
			try:
				nuke.scriptClear()
				nuke.scriptOpen(filepath)
				recent_files.recents.put(filepath)
				self.update_recents_menu()
				return filepath

			except RuntimeError as e:
				# exc_type, exc_value, exc_traceback = sys.exc_info()
				# # traceback.print_exception(exc_type, exc_value, exc_traceback)
				# dialog_msg = traceback.format_exception_only(exc_type, exc_value)[0]
				dialog = prompt.Dialog()
				dialog.display(str(e), "Error Opening File", conf=True)
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

		except RuntimeError as e:
			if str(e) != "Cancelled":
				dialog = prompt.Dialog()
				dialog.display(str(e), "Error Saving File", conf=True)
			return False


	def file_save(self):
		""" Save the current file.
			If saving for first time take over and show custom dialog.
		"""
		if self.get_current_name() == 'Root':  # Is current file unsaved?
			self.file_save_dialog()

		else:
			nuke.scriptSave()


	def file_save_as(self, filepath):
		""" Save the current file to the specified filepath.
			If the destination dir doesn't exist, create it.
			Nuke automatically prompts if file already exists.
			N.B. try/except to catch RuntimeError when dialog is cancelled.
		"""
		try:
			dirname = os.path.dirname(filepath)
			if not os.path.isdir(dirname):
				os_wrapper.createDir(dirname)
			nuke.scriptSaveAs(filepath)
			recent_files.recents.put(filepath)
			self.update_recents_menu()
			return filepath

		except RuntimeError as e:
			if str(e) != "Cancelled":
				dialog = prompt.Dialog()
				dialog.display(str(e), "Error Saving File", conf=True)
			return False


	def file_save_new_version(self):
		""" Increment the version number and save a new version of a file.
		"""
		current_name = self.get_current_name()

		if current_name == 'Root':  # Is current file unsaved?
			self.file_save_dialog()

		else:
			result = convention.version_next(current_name)
			if result:
				self.file_save_as(result)
			else:
				self.file_save_dialog()


	def file_snapshot(self, dest_dir=None):
		""" Save a copy (snapshot) of the current scene to the destination
			directory, without changing the current file pointer.
			TODO: implement and test properly
		"""
		current_script = nuke.root()['name'].value()
		dirname, basename = os.path.split(current_script)
		snapshot_script = os.path.join(tmpdir, basename)
		base, ext = os.path.splitext(basename)
		timestamp = time.strftime(r"%Y%m%d_%H%M%S")
		snapshot_script = "%s_snapshot_%s%s" % (base, timestamp, ext)
		nuke.scriptSave(snapshot_script)
		nuke.root()['name'].setValue(current_script)
		return snapshot_script


	def get_current_name(self):
		""" Get the name of the current file.
		"""
		return nuke.Root().name()


	def set_current_name(self, new_name):
		""" Change the name of the current file.
		"""
		nuke.root()['name'].setValue(new_name)


	def confirm(self):
		""" Obtain confirmation to proceed with operation if the current file
			is not saved.
		"""
		if nuke.Root().modified():
			return nuke.ask("The current script has been modified. Do you want to continue?")
		else:
			return True


	def update_recents_menu(self, menu=None):
		""" Populate the recent files menu or disable it if no recent files
			in list.
		"""
		if menu is None:
			menu = self.icOpenRecentMenu
		else:
			self.icOpenRecentMenu = menu  # Store a reference to the menu

		recent_files.recents.reload()  # Force reload of datafile
		recent_file_list = recent_files.recents.get('nuke')

		# Delete all items in the pop-up menu
		menu.clearMenu()

		# Re-populate the items in the pop-up menu
		for item in recent_file_list:
			filepath = os_wrapper.absolutePath(item)

			# Create the menu items...
			# Forward slashes need escaping to prevent Nuke from interpreting
			# them as sub-menus.
			# Cast menu command to string as Nuke gives error if unicode.
			menu_name = os.path.basename(filepath).replace('/', '\/')
			menu_cmd = str('session.scnmgr.file_open(\"%s\")' % filepath)
			menu.addCommand(menu_name, menu_cmd)

		# If recent file list contains no entries, disable menu
		enable = True;
		if len(recent_file_list) == 0:
			enable = False
		if len(recent_file_list) == 1 and recent_file_list[0] == "":
			enable = False

		menu.setEnabled(enable)


	# def update_recent_files(self, script=None):
	# 	""" Adds a script to the recent files list config file. If script is
	# 		not specified use current script name.
	# 	"""
	# 	if script == None:
	# 		script = os.path.abspath(nuke.value('root.name'))

	# 	# Add entry to recent files config file
	# 	recent_files.recents.put(script, 'nuke')  # Explicitly stating 'nuke' environment to get around 'nuke_tmp' fix

	# 	# Update custom recent files menu(s) - these are dependent on the
	# 	# menus defined in menu.py so modify with caution
	# 	if os.environ['IC_VENDOR_INITIALS']:
	# 		vendor = os.environ['IC_VENDOR_INITIALS'] + " "
	# 	else:
	# 		vendor = ""

	# 	self.update_recents_menu(nuke.menu('Nuke').menu('File').menu(vendor+'Open Recent'))


	def set_defaults(self):
		""" Automatically set some defaults from the shot settings for a new
			script.
		"""
		plateFormat = '%s %s %s' % (int(os.environ['IC_RESOLUTION_X']), int(os.environ['IC_RESOLUTION_Y']), os.environ['IC_SHOT'])
		proxyFormat = '%s %s %s' % (int(os.environ['IC_PROXY_RESOLUTION_X']), int(os.environ['IC_PROXY_RESOLUTION_Y']), '%s_proxy' % os.environ['IC_SHOT'])
		nuke.addFormat(plateFormat)
		nuke.addFormat(proxyFormat)

		nuke.knobDefault('Root.format', os.environ['IC_SHOT'])
		nuke.knobDefault('Root.proxy_type', 'format')
		nuke.knobDefault('Root.proxy_format', '%s_proxy' % os.environ['IC_SHOT'])
		nuke.knobDefault('Root.fps', os.environ['IC_FPS'])
		nuke.knobDefault('Root.first_frame', os.environ['IC_STARTFRAME'])
		nuke.knobDefault('Root.last_frame', os.environ['IC_ENDFRAME'])


	# def incrementSceneWithoutSave(self):
	# 	""" Increment the minor version number. For Maya, don't save as this
	# 		can be slow for large scenes. Instead copy the previous scene
	# 		file via the OS.
	# 	"""
	# 	if os.environ['SCNMGR_APP'] == "STANDALONE":
	# 		pass  # Do nothing

	# 	elif os.environ['SCNMGR_APP'] == "MAYA":
	# 		# As the scene will have just been saved, we create a copy of the
	# 		# scene and increment the minor version, and point the Maya file
	# 		# to the updated scene file. This gives us a performance gain by
	# 		# avoiding the overhead of a second save operation, which can be
	# 		# slow for large Maya ASCII scenes.
	# 		current_scene = mc.file(query=True, expandName=True)
	# 		ext = os.path.splitext(current_scene)[1]
	# 		updated_scene = convention.version_up(current_scene)
	# 		if updated_scene:
	# 			updated_scene += ext
	# 			oswrapper.copy(current_scene, updated_scene)
	# 			mc.file(rename=updated_scene)
	# 			# self.addSceneEntry(self.ui.mayaScene_comboBox, updated_scene)
	# 			self.getScene()

	# 	elif os.environ['SCNMGR_APP'] == "HOUDINI":
	# 		if convention.version_up():
	# 			self.getScene()

	# 	elif os.environ['SCNMGR_APP'] == "NUKE":
	# 		if convention.version_up():
	# 			self.getScene()
