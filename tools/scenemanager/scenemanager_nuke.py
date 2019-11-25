#!/usr/bin/python

# [nuke] scenemanager.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Custom file opening/saving procedures.


import os
import nuke

# Import custom modules
# from . import file_open
# from . import file_save
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
		nuke.scriptClear()
		self.set_defaults()


	def file_open_dialog(self, starting_dir=None):
		""" Display a dialog to select a file to open.
		"""
		if starting_dir is None:
			nuke.scriptOpen()

		else:
			nuke.scriptOpen(os.path.join(starting_dir, '.'))


	def file_open(self, filepath):
		""" Open the specified file.
		"""
		nuke.scriptOpen(filepath)
		recentFiles.updateLs(filepath)


	def file_save_dialog(self, starting_dir=None):
		""" Display a dialog for saving a file.
		"""
		if starting_dir is None:
			nuke.scriptSaveAs()

		else:
			nuke.scriptSaveAs(os.path.join(starting_dir, '.'))


	def file_save(self):
		""" Save the current file.
		"""
		nuke.scriptSave()


	def file_save_as(self, filepath):
		""" Save the current file to the specified filepath.
		"""
		nuke.scriptSaveAs(filepath)
		recentFiles.updateLs(filepath)


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
		pass


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
			openRecentCmdStr = 'nuke.scriptOpen(\"%s%s\")' % (os.environ['IC_SHOTPATH'], item)
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


