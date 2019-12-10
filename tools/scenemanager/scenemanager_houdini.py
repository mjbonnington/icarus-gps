#!/usr/bin/python

# [houdini] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures for Houdini.


import os
import hou

# Import custom modules
from . import convention
from . import file_open
from . import file_save
from shared import os_wrapper
from shared import prompt
from shared import recentFiles


class SceneManager(object):
	""" Interface to wrap Houdini's file open/save functionality.
	"""
	def __init__(self):
		self.app = 'houdini'
		self.file_open_ui = file_open.dialog(self, app=self.app)
		self.file_save_ui = file_save.dialog(self, app=self.app)


	def file_new(self):
		""" Start a new file with some default settings.
		"""
		hou.hipFile.clear()
		self.set_defaults()


	def file_open_dialog(self, **kwargs):
		""" Display a custom dialog to select a file to open.
		"""
		return self.file_open_ui.display(**kwargs)


	def file_open_native_dialog(self, starting_dir=None):
		""" Display a native dialog to select a file to open.
		"""
		filepath = hou.ui.selectFile(
			start_directory=starting_dir, 
			title='Open', 
			pattern='*.hip, *.hiplc, *.hipnc, *.hip*')

		if filepath:
			return self.file_open(filepath)
		else:
			return False


	def file_open(self, filepath):
		""" Open the specified file.
		"""
		# Remove backslashes from path as this causes issues on Windows...
		filepath = os_wrapper.absolutePath(filepath)
		# print("Loading: %s" % filepath)

		# Hide UI to prevent is stealing focus from Houdini's own dialog...
		self.file_open_ui.hide()

		try:
			hou.hipFile.load(file_name=filepath)
			self.set_hip_and_job_vars(
				set_hip_explicit=os.path.dirname(filepath))
			return filepath

		except hou.OperationFailed as e:
			dialog = prompt.dialog()
			dialog.display(str(e), "Error Opening File", conf=True)
			return False

		except hou.LoadWarning as e:
			dialog = prompt.dialog()
			dialog.display(str(e), "Warning", conf=True)
			return False


	def file_save_dialog(self, **kwargs):
		""" Display a custom dialog for saving a file.
		"""
		return self.file_save_ui.display(**kwargs)


	def file_save_native_dialog(self, starting_dir=None):
		""" Display a native dialog for saving a file.
		"""
		filepath = hou.ui.selectFile(
			start_directory=starting_dir, 
			title='Save As', 
			pattern='*.hip, *.hiplc, *.hipnc, *.hip*')

		if filepath:
			return self.file_save_as(filepath)
		else:
			return False


	def file_save(self):
		""" Save the current file.
			If saving for first time take over and show custom dialog.
		"""
		if hou.hipFile.name() == 'untitled.hip':  # Is this scene empty?
			self.file_save_dialog()

		else:
			hou.hipFile.save()


	def file_save_as(self, filepath):
		""" Save the current file to the specified filepath.
			If the destination dir doesn't exist, Houdini will automatically
			create it.
		"""
		# Remove backslashes from path as this causes issues on Windows...
		filepath = os_wrapper.absolutePath(filepath)
		# print("Saving: %s" % filepath)

		# Hide UI to prevent is stealing focus from Houdini's own dialog...
		self.file_save_ui.hide()

		try:
			hou.hipFile.save(filepath)
			self.set_hip_and_job_vars(
				set_hip_explicit=os.path.dirname(filepath))
			recentFiles.updateLs(filepath)
			return filepath

		except hou.OperationFailed as e:
			dialog = prompt.dialog()
			dialog.display(str(e), "Error Saving File", conf=True)
			return False


	def file_save_new_version(self):
		""" Increment the version number and save a new version of a file.
		"""
		current_name = self.get_current_name()

		if hou.hipFile.name() == 'untitled.hip':  # Is current file unsaved?
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
		"""
		pass


	def get_current_name(self):
		""" Get the name of the current file.
		"""
		return hou.hipFile.path()


	def set_current_name(self, new_name):
		""" Change the name of the current file.
		"""
		hou.hipFile.setName(new_name)


	def confirm(self):
		""" Obtain confirmation to proceed with operation if the current file
			is not saved.
		"""
		pass
		# if hou.hipFile.hasUnsavedChanges():
		# 	return nuke.ask("The current scene has been modified. Do you want to continue?")
		# else:
		# 	return True


	def update_recents_menu(self):
		""" Populate the recent files menu or disable it if no recent files
			in list.
			Returns a list to populate the custom recent files menu.
		"""
		recent_file_list = recentFiles.getLs('houdini')

		menu_items = []
		for item in recent_file_list:
			full_path = os_wrapper.absolutePath('$IC_SHOTPATH/%s' % item)
			menu_items.append(full_path); menu_items.append(item)
			# menu_items.append(item); menu_items.append(os.path.basename(item))

		return menu_items


	def set_defaults(self):
		""" Automatically set some defaults from the shot settings for a new
			scene.
		"""
		startFrame = int(os.environ['IC_STARTFRAME'])
		endFrame = int(os.environ['IC_ENDFRAME'])
		fps = float(os.environ['IC_FPS'])

		startTime = (float(startFrame)-1) / float(fps)
		endTime = float(endFrame) / float(fps)
		hou.setFps(fps)
		hou.hscript('tset %s %s' % (startTime, endTime))
		hou.playbar.setPlaybackRange(startFrame, endFrame)
		# hou.setFrame(startFrame)

		self.set_hip_and_job_vars()


	def set_hip_and_job_vars(self, set_hip_explicit=None):
		""" Set the $HIP and $JOB env vars to the correct location.
			$HIP defaults to user scene dir unless set_hip_explicit is given.
		"""
		if set_hip_explicit is None:
			hip_dir = os_wrapper.absolutePath('$IC_HOUDINI_SCENES_DIR/$IC_USERNAME')
		else:
			hip_dir = os_wrapper.absolutePath(set_hip_explicit)
		job_dir = os_wrapper.absolutePath('$IC_HOUDINI_PROJECT_DIR')

		# Create $HIP dir if it doesn't exist
		if not os.path.isdir(hip_dir):
			os_wrapper.createDir(hip_dir)

		# Set vars
		os.environ['HIP'] = hip_dir
		hou.putenv('HIP', hip_dir)
		os.environ['JOB'] = job_dir
		hou.putenv('JOB', job_dir)
