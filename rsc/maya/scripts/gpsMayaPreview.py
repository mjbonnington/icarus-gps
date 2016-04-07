#!/usr/bin/python

# [GPS Preview] gpsMayaPreview.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2016 Gramercy Park Studios
#
# Generate playblasts for GPS Preview.


import maya.cmds as mc
import os, time
import verbose


class preview():

	def __init__(self, outputDir, outputFile, res, frRange, offscreen, noSelect, guides, slate):
		self.playblastDir = outputDir
		self.outputFile = outputFile
		self.res = res

		if frRange == 'timeline':
			self.frRange = (int(mc.playbackOptions(min=True, q=True)), int(mc.playbackOptions(max=True, q=True)))
			self.rangeType = frRange
		elif frRange == 'current frame':
			self.frRange = (int(mc.currentTime(q=True)), int(mc.currentTime(q=True)))
			self.rangeType = frRange
		else:
			self.frRange = (int(frRange[0]), int(frRange[1]))
			self.rangeType = self.frRange

		self.offscreen = offscreen
		self.noSelect = noSelect
		self.guides = guides
		self.slate = slate


	def storeAttributes(self, obj, attrLs):
		""" Store the object's specified attribute values in a dictionary.
		"""
		storedAttrDic = {}
		for attr in attrLs:
			storedAttrDic[attr] = mc.getAttr( '%s.%s' %(obj, attr) )

		return storedAttrDic


	def retrieveAttributes(self, obj, storedAttrDic):
		""" Retrieve the stored attribute values in order to re-apply the settings.
		"""
		for key, value in storedAttrDic.iteritems():
			mc.setAttr( '%s.%s' %(obj, key), value )


	def setAttributes(self, obj, attrLs, value):
		""" Set several attribues at once.
		"""
		for attr in attrLs:
			mc.setAttr( '%s.%s' %(obj, attr), value )


	#########
	# Slate #
	#########

	# Maya scene name
	def hudScene(self):
		return os.path.split(mc.file(q=True, exn=True))[1]

	# Camera info
	def hudCamera(self):
		activeCamera = self.getActiveCamera()
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, shapes=True)
		cameraLens = mc.getAttr(cameraShape[0] + '.focalLength')
		cameraLens = round(cameraLens, 2)
		camInfo = '%s %s mm' % (activeCamera, cameraLens)
		#print camInfo
		return camInfo

	# Date & time
	def hudTime(self):
		return time.strftime("%d/%m/%Y %H:%M")

	# Current project
	def hudJob(self):
		return '%s - %s' % (os.environ['JOB'], os.environ['SHOT'])

	# Current frame
	def hudFrame(self):
		return mc.currentTime(q=True)

	# Artist
	def hudArtist(self):
		return os.environ['USERNAME']

	# GPS header
	def hudHeader(self):
		return 'GPS'


	def slateOn(self):
		""" Show slate.
		"""
		mc.headsUpDisplay(rp=(0,0))
		mc.headsUpDisplay(rp=(0,1))
		mc.headsUpDisplay(rp=(0,2))
		mc.headsUpDisplay(rp=(2,2))
		mc.headsUpDisplay(rp=(4,0))
		mc.headsUpDisplay(rp=(4,1))
		mc.headsUpDisplay(rp=(4,2))
		mc.headsUpDisplay(rp=(4,3))
		mc.headsUpDisplay(rp=(5,2))
		mc.headsUpDisplay(rp=(5,3))
		mc.headsUpDisplay(rp=(9,5))

		mc.headsUpDisplay('HUD_header', 
		                  section=2, 
		                  block=2, 
		                  blockSize='small', 
		                  command=lambda *args: self.hudHeader(), 
		                  ev='playblasting', 
		                  dataFontSize='large')

		mc.headsUpDisplay('HUD_job', 
		                  section=0, 
		                  block=1, 
		                  blockSize='small', 
		                  command=lambda *args: self.hudJob(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		mc.headsUpDisplay('HUD_scene', 
		                  section=4, 
		                  block=2, 
		                  blockSize='small', 
		                  #blockAlignment='right', 
		                  command=lambda *args: self.hudScene(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		mc.headsUpDisplay('HUD_camera', 
		                  section=4, 
		                  block=1, 
		                  blockSize='small', 
		                  #blockAlignment='right', 
		                  command=lambda *args: self.hudCamera(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		mc.headsUpDisplay('HUD_artist', 
		                  section=5, 
		                  block=3, 
		                  blockSize='small', 
		                  command=lambda *args: self.hudArtist(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		mc.headsUpDisplay('HUD_time', 
		                  section=5, 
		                  block=2, 
		                  blockSize='small', 
		                  command=lambda *args: self.hudTime(), 
		                  ev='playblasting', 
		                  dataFontSize='small')

		mc.headsUpDisplay('HUD_frame', 
		                  section=9, 
		                  block=5, 
		                  blockSize='small', 
		                  command=lambda *args: self.hudFrame(), 
		                  attachToRefresh = True, 
		                  dataFontSize='large')


	def slateOff(self):
		""" Turn slate off.
		"""
		if mc.headsUpDisplay('HUD_scene', ex=True) == True:
			mc.headsUpDisplay('HUD_scene', rem=True)
		if mc.headsUpDisplay('HUD_camera', ex=True) == True:
			mc.headsUpDisplay('HUD_camera', rem=True)
		if mc.headsUpDisplay('HUD_lens', ex=True) == True:
			mc.headsUpDisplay('HUD_lens', rem=True)
		if mc.headsUpDisplay('HUD_time', ex=True) == True:
			mc.headsUpDisplay('HUD_time', rem=True)
		if mc.headsUpDisplay('HUD_artist', ex=True) == True:
			mc.headsUpDisplay('HUD_artist', rem=True)
		if mc.headsUpDisplay('HUD_job', ex=True) == True:
			mc.headsUpDisplay('HUD_job', rem=True)
		if mc.headsUpDisplay('HUD_frame', ex=True) == True:
			mc.headsUpDisplay('HUD_frame', rem=True)

		mc.headsUpDisplay(rp=(0,0))
		mc.headsUpDisplay(rp=(0,1))
		mc.headsUpDisplay(rp=(0,2))
		mc.headsUpDisplay(rp=(0,3))
		mc.headsUpDisplay(rp=(0,4))
		mc.headsUpDisplay(rp=(0,5))
		mc.headsUpDisplay(rp=(2,2))
		mc.headsUpDisplay(rp=(4,1))
		mc.headsUpDisplay(rp=(4,2))
		mc.headsUpDisplay(rp=(4,3))
		mc.headsUpDisplay(rp=(5,3))
		mc.headsUpDisplay(rp=(5,2))
		mc.headsUpDisplay(rp=(9,5))

	# end slate


	def playblast_(self):
		""" Sets playblast options and runs playblast.
		"""
		# Get active camera
		activeCamera = self.getActiveCamera()
		if not activeCamera:
			return
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, shapes=True)

		# Store current options
		#displayAttrsToStore = ['displayFieldChart', 'displaySafeAction', 'displaySafeTitle', 'displayFilmPivot', 'displayFilmOrigin', 'overscan']
		displayOptions = self.storeAttributes(cameraShape[0], ['displayResolution', 'displayFieldChart', 'displaySafeAction', 'displaySafeTitle', 'displayFilmPivot', 'displayFilmOrigin', 'overscan'])
		#renderOptions = self.storeAttributes('defaultRenderGlobals', ['imageFormat', ])
		displayHUD = self.displayHUD(query=True)

		# Change image format globals to jpg
		#mc.setAttr('defaultRenderGlobals.imageFormat', 8)

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
			self.slateOff()

		# Display guides
		if self.guides:
			mc.setAttr("%s.displayResolution" % cameraShape[0], True)
			mc.setAttr("%s.displaySafeAction" % cameraShape[0], True)
			mc.setAttr("%s.displaySafeTitle" % cameraShape[0], True)
		else:
			#self.setAttributes(cameraShape[0], displayAttrsToStore, False)
			mc.setAttr("%s.displayResolution" % cameraShape[0], False)
			mc.setAttr("%s.displayFieldChart" % cameraShape[0], False)
			mc.setAttr("%s.displaySafeAction" % cameraShape[0], False)
			mc.setAttr("%s.displaySafeTitle" % cameraShape[0], False)
			mc.setAttr("%s.displayFilmPivot" % cameraShape[0], False)
			mc.setAttr("%s.displayFilmOrigin" % cameraShape[0], False)

		# Set overscan value to 1.0
		mc.setAttr("%s.overscan" % cameraShape[0], 1.0)

		# Generate playblast
		self.run_playblast()

		# Hide slate
		if self.slate:
			self.slateOff()

		# Restore selection
		if self.noSelect:
			for sl in currentSl:
				mc.select(sl, add=True)

		# Restore original settings
		self.retrieveAttributes(cameraShape[0], displayOptions)
		#self.retrieveAttributes('defaultRenderGlobals', renderOptions)
		self.displayHUD(setValue=displayHUD)

		# Return frame range and file extension
		return self.frRange , 'jpg'


	def displayHUD(self, query=False, setValue=True):
		""" Show, hide or query the HUD.
		"""
		currentPanel = mc.getPanel(withFocus=True)
		panelType = mc.getPanel(typeOf=currentPanel)
		if panelType == "modelPanel":
			if query:
				return mc.modelEditor(currentPanel, query=True, hud=True)
			else:
				mc.modelEditor(currentPanel, edit=True, hud=setValue)


	def getActiveCamera(self):
		""" Get the current active camera.
		"""
		try:
			activeCamera = mc.modelPanel(mc.getPanel(withFocus=True), cam=True, q=True)
			return activeCamera
		except RuntimeError:
			mc.warning("No active view selected. Please choose a camera view to preview.")
			return False


	def run_playblast(self):
		""" Maya command to generate playblast.
		"""
		mc.playblast(filename='%s/%s' % (self.playblastDir, self.outputFile), 
		             startTime=self.frRange[0], 
		             endTime=self.frRange[1], 
		             framePadding=4, 
		             width=self.res[0], 
		             height=self.res[1], 
		             percent=100, 
		             format='image', 
		             compression='jpg', 
		             viewer=False, 
		             offScreen=self.offscreen, 
		             clearCache=True, 
		             showOrnaments=True)

