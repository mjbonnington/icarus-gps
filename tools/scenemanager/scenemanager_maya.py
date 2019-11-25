#!/usr/bin/python

# [maya] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures.


import os
import maya.cmds as mc
# import maya.mal as mel

# Import custom modules
from shared import os_wrapper
from shared import recentFiles


class SceneManager(object):
	""" File Open UI.
	"""
	def __init__(self):
		pass


	def file_new(self):
		""" Start a new file.
		"""
		mc.NewScene()
		self.set_defaults()


	def file_open_dialog(self, starting_dir=None):
		""" Display a dialog to select a file to open.
		"""
		mc.OpenScene()


	def file_open(self, filepath):
		""" Open the specified file.
			TODO: prompt if current scene has been modified
		"""
		recentFiles.updateLs(
			mc.file(filepath, open=True, force=True, ignoreVersion=True))


	def file_save_dialog(self, starting_dir=None):
		""" Display a dialog for saving a file.
		"""
		mc.SaveSceneAs()


	def file_save(self):
		""" Save the current file.
			TODO: if saving for first time take over and show custom dialog
		"""
		mc.SaveScene()


	def file_save_as(self, filepath):
		""" Save the specified file.
			TODO: prompt if save will overwrite existing file
		"""
		mc.file(rename=filepath)
		recentFiles.updateLs(
			mc.file(options='v=0', force=True, save=True, type='mayaAscii'))


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
		""" Change the name of the current file.
		"""
		pass


	def file_set_name(self, new_name):
		""" Change the name of the current file.
		"""
		mc.file(rename=new_name)


	def update_recents_menu(self):
		""" Populate the recent files menu or disable it if no recent files
			in list.
		"""
		pass


	def set_defaults(self):
		""" Automatically set some defaults from the shot settings for a new
			scene.
		"""
		unit = os.getenv('UNIT', 'cm')
		angle = os.getenv('ANGLE', 'deg')
		timeFormat = os.getenv('TIMEFORMAT', 'pal')
		startFrame = int(os.getenv('STARTFRAME', '1001'))
		endFrame = int(os.getenv('ENDFRAME', '1100'))
		inFrame = int(os.getenv('INFRAME', startFrame))
		outFrame = int(os.getenv('OUTFRAME', endFrame))
		psExecutable = os.getenv('PSVERSION', '')
		djvExecutable = os.getenv('DJVVERSION', '')

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
