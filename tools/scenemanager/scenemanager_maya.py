#!/usr/bin/python

# [maya] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures for Maya.


import os
import maya.cmds as mc

# Import custom modules
from . import convention
from . import file_open
from . import file_save
from shared import os_wrapper
from shared import recentFiles


class SceneManager(object):
	""" Interface to wrap Maya's file open/save functionality.
	"""
	def __init__(self):
		self.app = 'maya'
		self.file_open_ui = file_open.dialog(self, app=self.app)
		self.file_save_ui = file_save.dialog(self, app=self.app)


	def file_new(self):
		""" Start a new file with some default settings.
			Maya automatically prompts if scene has unsaved changes.
		"""
		mc.NewScene()
		self.set_defaults()


	def file_open_dialog(self, **kwargs):
		""" Display a custom dialog to select a file to open.
		"""
		return self.file_open_ui.display(**kwargs)


	def file_open_native_dialog(self, starting_dir=None):
		""" Display a native dialog to select a file to open.
		"""
		mc.OpenScene()
		return True


	def file_open(self, filepath):
		""" Open the specified file.
		"""
		if self.confirm():
			recentFiles.updateLs(
				mc.file(filepath, open=True, force=True, ignoreVersion=True))
			return filepath

		else:
			return False


	def file_save_dialog(self, **kwargs):
		""" Display a custom dialog for saving a file.
		"""
		return self.file_save_ui.display(**kwargs)


	def file_save_native_dialog(self, starting_dir=None):
		""" Display a native dialog for saving a file.
		"""
		mc.SaveSceneAs()
		return True


	def file_save(self):
		""" Save the current file.
			If saving for first time take over and show custom dialog.
		"""
		if self.get_current_name():  # Is this scene empty?
			self.file_save_dialog()

		else:
			mc.SaveScene()


	def file_save_as(self, filepath):
		""" Save the specified file.
			TODO: prompt if save will overwrite existing file
			TODO: add updateRecentFiles flag
		"""
		mc.file(rename=filepath)
		mc.SaveScene()
		recentFiles.updateLs(filepath)
		# recentFiles.updateLs(
		# 	mc.file(options='v=0', force=True, save=True, type='mayaAscii'))
		return True


	def file_save_new_version(self):
		""" Increment the version number and save a new version of a file.
		"""
		current_name = self.get_current_name()

		if current_name:  # Is current file unsaved?
			result = convention.version_next(current_name)
			if result:
				self.file_save_as(result)
			else:
				self.file_save_dialog()

		else:
			self.file_save_dialog()


	def file_snapshot(self, dest_dir=None):
		""" Save a copy (snapshot) of the current scene to the destination
			directory, without changing the current file pointer.
			TODO: implement and test properly
		"""
		current_file = mc.file(query=True, expandName=True)
		# tmp_dir = os.path.join(os.environ['SCNMGR_SAVE_DIR'], '.tmp')
		tmp_dir = dest_dir
		os_wrapper.createDir(tmp_dir)
		scene_name = mc.file(query=True, sceneName=True, shortName=True)
		snapshot_file = os.path.join(tmp_dir, scene_name)

		mc.file(rename=snapshot_file)
		snapshot_scene = mc.file(save=True)
		mc.file(rename=current_file)
		#mc.file(save=True)
		# print("Saved snapshot: %s" % snapshot_scene)
		return snapshot_scene


	def get_current_name(self):
		""" Get the name of the current file.
		"""
		return mc.file(query=True, sceneName=True)


	def set_current_name(self, new_name):
		""" Change the name of the current file.
		"""
		mc.file(rename=new_name)


	def confirm(self):
		""" Obtain confirmation to proceed with operation if the current file
			is not saved.
		"""
		if mc.file(query=True, sceneName=True) \
		and mc.file(query=True, modified=True):
			if 'Yes' == mc.confirmDialog(
				title='Unsaved Changes', 
				message='The current scene has been modified. Do you want to continue?', 
				button=['Yes', 'No'], 
				defaultButton='Yes', 
				cancelButton='No'):
				return True
			else:
				return False
		else:
			return True


	def update_recents_menu(self):
		""" Populate the recent files menu or disable it if no recent files
			in list.
		"""
		pass


	def set_defaults(self):
		""" Automatically set some defaults from the shot settings for a new
			scene.
		"""
		unit = os.getenv('IC_LINEAR_UNIT', 'cm')
		angle = os.getenv('IC_ANGULAR_UNIT', 'deg')
		timeFormat = os.getenv('IC_TIME_UNIT', 'pal')
		startFrame = int(os.getenv('IC_STARTFRAME', '1001'))
		endFrame = int(os.getenv('IC_ENDFRAME', '1100'))
		inFrame = int(os.getenv('IC_INFRAME', startFrame))
		outFrame = int(os.getenv('IC_OUTFRAME', endFrame))
		psExecutable = os.getenv('IC_PS_EXECUTABLE', '')
		djvExecutable = os.getenv('IC_DJV_EXECUTABLE', '')

		# Set defaults for Maya startup
		# mc.currentUnit(l=unit, a=angle, t=timeFormat)
		try:
			mc.currentUnit(l=unit)
			mc.optionVar(sv=('workingUnitLinear', unit))
			mc.optionVar(sv=('workingUnitLinearDefault', unit))
		except RuntimeError:
			mc.warning("Unable to set linear unit.")

		try:
			mc.currentUnit(a=angle)
			mc.optionVar(sv=('workingUnitAngular', angle))
			mc.optionVar(sv=('workingUnitAngularDefault', angle))
		except RuntimeError:
			mc.warning("Unable to set angular unit.")

		try:
			mc.currentUnit(t=timeFormat)
			mc.optionVar(sv=('workingUnitTime', timeFormat))
			mc.optionVar(sv=('workingUnitTimeDefault', timeFormat))
		except RuntimeError:
			mc.warning('Unable to set time unit.')

		mc.optionVar(fv=('playbackMinRangeDefault', startFrame))
		mc.optionVar(fv=('playbackMinDefault', inFrame))
		mc.optionVar(fv=('playbackMaxRangeDefault', endFrame))
		mc.optionVar(fv=('playbackMaxDefault', outFrame))

		mc.optionVar(sv=('upAxisDirection', 'y'))

		mc.optionVar(sv=('EditImageDir', psExecutable))
		mc.optionVar(sv=('PhotoshopDir', psExecutable))

		mc.optionVar(sv=('PlayblastCmdAvi', djvExecutable))
		mc.optionVar(sv=('PlayblastCmdQuicktime', djvExecutable))
		mc.optionVar(sv=('ViewImageDir', djvExecutable))
		mc.optionVar(sv=('ViewSequenceDir', djvExecutable))

		mc.playbackOptions(
			animationStartTime=startFrame, 
			minTime=inFrame, 
			maxTime=outFrame, 
			animationEndTime=endFrame, 
			playbackSpeed=0, 
			maxPlaybackSpeed=1)

		# # Ensure output file naming convention is correct
		# if self.getRenderer() == 'vray':
		# 	mc.setAttr("vraySettings.fileNamePrefix", lock=False)
		# 	mc.setAttr("vraySettings.fileNamePrefix", MAYA_OUTPUT_FORMAT_VRAY, type="string")
		# 	mc.setAttr("vraySettings.fileNameRenderElementSeparator", lock=False)
		# 	mc.setAttr("vraySettings.fileNameRenderElementSeparator", ".", type="string")

		# else:  # Maya Common Default and Arnold
		# 	mc.setAttr("defaultRenderGlobals.imageFilePrefix", MAYA_OUTPUT_FORMAT, type="string")
