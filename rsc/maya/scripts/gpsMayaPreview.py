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

	##slate##
	#maya scene
	def hudScene(self):
		return os.path.split(mc.file(exn=True, q=True))[1]

	#camera info
	def hudCamera(self):
		activeCamera = self.getActiveCamera()
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, s=True)
		cameraLens = mc.getAttr(cameraShape[0] + '.focalLength')
		cameraLens = round(cameraLens, 2)
		cameraLens = `cameraLens` + ' mm'
		camInfo = '%s %s' % (activeCamera, cameraLens)
		return camInfo

	#time
	def hudTime(self):
		return time.strftime("%d/%m/%Y %H:%M")

	#current project
	def hudJob(self):
		return '%s - %s\t\t' % (os.environ['JOB'], os.environ['SHOT'])

	#current frame
	def hudFrame(self):
		return mc.currentTime(q=True)

	#artist
	def hudArtist(self):
		return os.environ['USERNAME']

	#GPS
	def hudGPS(self):
		return 'GPS'

	#turns slate on
	def slateOn(self):
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

		mc.headsUpDisplay('HUD_GPS',
		section=2,
		block=2,
		blockSize='small',
		command=lambda *args: self.hudGPS(),
		ev='playblasting',
		dataFontSize='large')

		mc.headsUpDisplay('HUD_camera',
		section=4,
		block=1,
		blockSize='small',
		command=lambda *args: self.hudCamera(),
		ev='playblasting',
		dataFontSize='small')
		
		mc.headsUpDisplay('HUD_scene',
		section=4,
		block=2,
		blockSize='small',
		ba='right',
		command=lambda *args: self.hudScene(),
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
		
		mc.headsUpDisplay('HUD_job',
		section=0,
		block=1,
		blockSize='small',
		command=lambda *args: self.hudJob(),
		ev='playblasting',
		dataFontSize='small')
		
		mc.headsUpDisplay('HUD_frame',
		section=9,
		block=5,
		blockSize='small',
		command=lambda *args: self.hudFrame(),
		attachToRefresh = True,
		dataFontSize='large')
		
	#turns slate off
	def slateOff(self):
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
	
	##end slate##


	def playblast_(self):
		""" Sets playblast options and runs playblast.
		"""
		# Change image format globals to jpg
		mc.setAttr('defaultRenderGlobals.imageFormat', 8)

		# Store and then clear selection
		if self.noSelect:
			currentSl = mc.ls(sl=True)
			mc.select(cl=True)

		# Get active camera
		if not self.getActiveCamera():
			return

		# Display slate
		if self.slate:
			self.slateOn()
		else:
			self.slateOff()

		# Display guides
		if self.guides:
			activeCamera = self.getActiveCamera()
			cameraShape = [activeCamera]
			if mc.nodeType(activeCamera) != 'camera':
				cameraShape = mc.listRelatives(activeCamera, s=True)
			pre_safeAction = mc.getAttr('%s.displaySafeAction' % cameraShape[0])
			pre_safeTitle = mc.getAttr('%s.displaySafeTitle' % cameraShape[0])
			mc.setAttr("%s.displaySafeAction" % cameraShape[0], 1)
			mc.setAttr("%s.displaySafeTitle" % cameraShape[0], 1)
		else:
			mc.setAttr("%s.displaySafeAction" % cameraShape[0], 0)
			mc.setAttr("%s.displaySafeTitle" % cameraShape[0], 0)

		# Store current overscan value and set it to 1.0
		overscanValue = self.overscan(get=True)
		self.overscan(set=True)

		# Generate playblast
		self.run_playblast()

		# Hide slate
		if self.slate:
			self.slateOff()

		# Restore overscan to original value
		self.overscan(set=True, setValue=overscanValue)

		# Restore imageFormat globals
		mc.setAttr('defaultRenderGlobals.imageFormat', 7)

		# Restore selection
		if self.noSelect:
			for sl in currentSl:
				mc.select(sl, add=True)

		# Restore guides
		if self.guides:
			if not pre_safeAction:
				mc.setAttr("%s.displaySafeAction" % cameraShape[0], 0)
			if not pre_safeTitle:
				mc.setAttr("%s.displaySafeTitle" % cameraShape[0], 0)

		#returns frRange and file extension
		return self.frRange , 'jpg'


	#stores overscan info and changes to 1.0
	def overscan(self, set=False, setValue=1.0, get=False):
		activeCamera = self.getActiveCamera()
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, s=True)
		if set:
			mc.setAttr('%s.overscan' % cameraShape[0], setValue)
			return
		if get:
			return mc.getAttr('%s.overscan' % cameraShape[0])


	#gets the current active camera
	def getActiveCamera(self):
		try:
			activeCamera = mc.modelPanel(mc.getPanel(wf=True), cam=True, q=True)
			return activeCamera
		except RuntimeError:
			verbose.chooseCameraPreview()
			mc.warning("No active view selected. Please choose a camera view to preview.")


	def run_playblast(self):
		""" Generate playblast.
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

