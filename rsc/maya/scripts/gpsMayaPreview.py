#!/usr/bin/python

# [GPS Preview] gpsMayaPreview.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2018 Gramercy Park Studios
#
# Generate Maya playblasts for GPS Preview.


import maya.cmds as mc
import os
import time

import verbose


# ----------------------------------------------------------------------------
# Main class
# ----------------------------------------------------------------------------

class Preview():

	def __init__(self, outputDir, outputFile, format, activeView, camera, res, frRange, offscreen, noSelect, guides, slate, interruptible):
		self.playblastDir = outputDir
		self.outputFile = outputFile
		if format == "JPEG sequence":
			self.format = "image"
			self.compression = "jpg"
			self.sound = ""
		elif format == "QuickTime":
			self.format = "qt"
			self.compression = "H.264"
			self.sound = self.getActiveAudioNode()
		self.activeView = activeView
		self.camera = camera
		self.res = res
		self.frRange = (int(frRange[0]), int(frRange[1]))
		self.offscreen = offscreen
		self.noSelect = noSelect
		self.guides = guides
		self.slate = slate
		self.interruptible = interruptible


	def storeAttributes(self, obj, attrLs):
		""" Store the object's specified attribute values in a dictionary.
		"""
		storedAttrDic = {}
		for attr in attrLs:
			storedAttrDic[attr] = mc.getAttr('%s.%s' %(obj, attr))

		return storedAttrDic


	def retrieveAttributes(self, obj, storedAttrDic):
		""" Retrieve the stored attribute values in order to re-apply the
			settings.
		"""
		for key, value in storedAttrDic.iteritems():
			mc.setAttr('%s.%s' %(obj, key), value)


	def setAttributes(self, obj, attrLs, value):
		""" Set several attribues at once.
		"""
		for attr in attrLs:
			mc.setAttr('%s.%s' %(obj, attr), value)


	# ------------------------------------------------------------------------
	# Slate / HUD

	def displayHUD(self, query=False, setValue=True):
		""" Show, hide or query the entire HUD.
		"""
		currentPanel = mc.getPanel(withFocus=True)
		panelType = mc.getPanel(typeOf=currentPanel)
		if panelType == "modelPanel":
			if query:
				return mc.modelEditor(currentPanel, query=True, hud=True)
			else:
				mc.modelEditor(currentPanel, edit=True, hud=setValue)


	def storeHUD(self):
		""" Store the current state of the HUD in a dictionary.
		"""
		hudLs = mc.headsUpDisplay(listHeadsUpDisplays=True)

		hudDic = {}
		for hud in hudLs:
			hudDic[hud] = mc.headsUpDisplay(hud, query=True, vis=True)

		return hudDic


	def showHUD(self, vis):
		""" Hide or show all HUD elements at once.
		"""
		hudLs = mc.headsUpDisplay(listHeadsUpDisplays=True)

		for hud in hudLs:
			mc.headsUpDisplay(hud, edit=True, vis=vis)


	def restoreHUD(self, hudDic):
		""" Restore the HUD from the state stored in the dictionary.
		"""
		hudLs = mc.headsUpDisplay(listHeadsUpDisplays=True)

		for hud, vis in hudDic.iteritems():
			mc.headsUpDisplay(hud, edit=True, vis=vis)


	# Header
	def hudHeader(self):
		return 'GPS'

	# Current project
	def hudJob(self):
		return '%s - %s' %(os.environ['JOB'], os.environ['SHOT'])

	# Maya scene name
	def hudScene(self):
		return os.path.split(mc.file(q=True, exn=True))[1]

	# Camera and lens info
	def hudCamera(self):
		#activeCamera = self.getActiveCamera(mc.getPanel(withFocus=True))
		activeCamera = self.camera
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, shapes=True)
		if mc.getAttr(cameraShape[0] + '.orthographic'):
			orthoWidth = mc.getAttr(cameraShape[0] + '.orthographicWidth')
			orthoWidth = round(orthoWidth, 2)
			camInfo = '%s (ortho %s)' %(activeCamera, orthoWidth)
		else:
			cameraLens = mc.getAttr(cameraShape[0] + '.focalLength')
			cameraLens = round(cameraLens, 2)
			camInfo = '%s (%s mm)' %(activeCamera, cameraLens)
		return camInfo

	# Date & time
	def hudTime(self):
		return time.strftime("%d/%m/%Y %H:%M")

	# Artist
	def hudArtist(self):
		return os.environ['IC_USERNAME']

	# Current frame
	def hudFrame(self):
		return mc.currentTime(q=True)


	def slateOn(self):
		""" Create GPS slate elements and add them to the HUD.
			Names of all custom HUDs must begin with 'GPS_slate'.
		"""
		# Hide all current HUD elements
		self.showHUD(0)

		# Delete pre-existing custom HUD elements
		self.slateOff()

		# Create custom HUD elements
		section = 2
		mc.headsUpDisplay('GPS_slate_header', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  command=lambda *args: self.hudHeader(), 
		                  ev='playblasting', 
		                  dataFontSize='large')

		section = 0
		mc.headsUpDisplay('GPS_slate_job', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  command=lambda *args: self.hudJob(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		section = 4
		mc.headsUpDisplay('GPS_slate_scene', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  #blockAlignment='right', 
		                  command=lambda *args: self.hudScene(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		section = 4
		mc.headsUpDisplay('GPS_slate_camera', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  #blockAlignment='right', 
		                  command=lambda *args: self.hudCamera(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		section = 5
		mc.headsUpDisplay('GPS_slate_time', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  command=lambda *args: self.hudTime(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		section = 5
		mc.headsUpDisplay('GPS_slate_artist', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  command=lambda *args: self.hudArtist(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		section = 9
		mc.headsUpDisplay('GPS_slate_frame', 
		                  section=section, 
		                  block=mc.headsUpDisplay(nextFreeBlock=section), 
		                  blockSize='small', 
		                  command=lambda *args: self.hudFrame(), 
		                  attachToRefresh = True, 
		                  dataFontSize='large')


	def slateOff(self):
		""" Remove the GPS slate elements.
		"""
		hudLs = mc.headsUpDisplay(listHeadsUpDisplays=True)

		for hud in hudLs:
			if hud.startswith('GPS_slate'):
				if mc.headsUpDisplay(hud, exists=True):
					mc.headsUpDisplay(hud, remove=True)

	# End Slate / HUD
	# ------------------------------------------------------------------------


	def getActiveAudioNode(self):
		""" Gets active audio node from Maya's time slider control.
		"""
		import maya.mel as mel

		aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
		return mc.timeControl(aPlayBackSliderPython, q=True, sound=True)


	def playblast_(self):
		""" Sets playblast options and runs playblast.
		"""
		if not self.activeView:
			msg = "No active view selected. Please select a camera panel to playblast and try again."
			mc.warning(msg)
			return False, msg

		# Get current active panel camera
		try:
			activeCameraOrig = mc.modelPanel(self.activeView, cam=True, q=True)
		except:
			msg = "Panel '%s' not found. Please select a camera panel to playblast and try again." %self.activeView
			mc.warning(msg)
			return False, msg

		# Get active camera and shape
		activeCamera = self.camera
		if not activeCamera:
			msg = "Unable to generate playblast as no camera was specified."
			mc.warning(msg)
			return False, msg
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, shapes=True)

		# Disable undo
		mc.undoInfo(openChunk=True, chunkName='gpsPreview')
		# undoState = mc.undoInfo(q=True, state=True)
		# if undoState:
		# 	mc.undoInfo(state=False)

		# Look through camera if no active panel
		mc.lookThru(self.activeView, activeCamera)

		# Store current options
		displayOptions = self.storeAttributes(cameraShape[0], ['displayResolution', 'displayFieldChart', 'displaySafeAction', 'displaySafeTitle', 'displayFilmPivot', 'displayFilmOrigin', 'overscan', 'panZoomEnabled'])
		displayHUD = self.displayHUD(query=True)
		hudState = self.storeHUD()

		# Store and then clear selection
		if self.noSelect:
			currentSl = mc.ls(sl=True)
			mc.select(cl=True)

		# Display slate
		if self.slate:
			self.displayHUD(setValue=True)
			self.slateOn()
		else:
			self.displayHUD(setValue=False)

		# Display guides
		if self.guides:
			mc.setAttr(cameraShape[0]+".displayResolution", True)
			mc.setAttr(cameraShape[0]+".displaySafeAction", True)
			mc.setAttr(cameraShape[0]+".displaySafeTitle", True)
		else:
			mc.setAttr(cameraShape[0]+".displayResolution", False)
			mc.setAttr(cameraShape[0]+".displayFieldChart", False)
			mc.setAttr(cameraShape[0]+".displaySafeAction", False)
			mc.setAttr(cameraShape[0]+".displaySafeTitle", False)
			mc.setAttr(cameraShape[0]+".displayFilmPivot", False)
			mc.setAttr(cameraShape[0]+".displayFilmOrigin", False)

		# Set overscan value to 1.0 & disable 2D pan/zoom
		mc.setAttr(cameraShape[0]+".overscan", 1.0)
		mc.setAttr(cameraShape[0]+".panZoomEnabled", 0)

		# Actually generate playblast!
		output = self.run_playblast()

		# Hide slate
		if self.slate:
			self.slateOff()

		# Restore selection
		if self.noSelect:
			for sl in currentSl:
				mc.select(sl, add=True)

		# Restore original settings
		self.retrieveAttributes(cameraShape[0], displayOptions)
		self.restoreHUD(hudState)
		self.displayHUD(setValue=displayHUD)

		# Restore camera panel
		mc.lookThru(self.activeView, activeCameraOrig)

		# Re-enable undo
		mc.undoInfo(closeChunk=True, chunkName='gpsPreview')
		# if undoState:
		# 	mc.undoInfo(state=True)

		# Return file output
		# print(output)
		if output:
			return True, output
		# Return the output file path even if the playblast was interrupted.
		# In the playblast command's return value, Maya automatically adds the
		# extension for jpg, but not mov. We are replicating that behaviour
		# here.
		else:
			if self.interruptible:
				if self.format == "image":
					output = os.path.join(self.playblastDir, '%s.#.%s' %(self.outputFile, self.compression))
				elif self.format == "qt":
					output = os.path.join(self.playblastDir, self.outputFile)
				return True, output
			else:  # Fail on interrupt
				return False, "Playblast was interrupted."


	def run_playblast(self):
		""" Maya command to generate playblast.
		"""
		pb_args = {}
		pb_args['filename'] = '%s/%s' %(self.playblastDir, self.outputFile)
		pb_args['startTime'] = self.frRange[0]
		pb_args['endTime'] = self.frRange[1]
		pb_args['framePadding'] = 4
		pb_args['width'] = self.res[0]
		pb_args['height'] = self.res[1]
		pb_args['percent'] = 100
		pb_args['format'] = self.format
		pb_args['compression'] = self.compression
		if self.sound:
			pb_args['sound'] = self.sound
		pb_args['viewer'] = False
		pb_args['offScreen'] = self.offscreen
		pb_args['clearCache'] = True
		pb_args['showOrnaments'] = True
		pb_args['editorPanelName'] = self.activeView

		return mc.playblast(**pb_args)

# ----------------------------------------------------------------------------
# End of main class
# ----------------------------------------------------------------------------

