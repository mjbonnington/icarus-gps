#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsMayaPreview

import maya.cmds as mc
import os, time


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
		sceneFile = os.path.split(mc.file(exn=True, q=True))[1]
		return sceneFile
		
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
		currentTime = time.strftime("%d/%b/%Y %H:%M")
		return currentTime
	
	#current project
	def hudJob(self):
		job = os.environ['JOB']
		shot_ = os.environ['SHOT']
		return '%s - %s\t\t' % (job, shot_)
	
	#current frame
	def hudFrame(self):
		currentFrame = mc.currentTime(q=True)
		return currentFrame
	
	#artist
	def hudArtist(self):
		artistName = os.environ['USERNAME']
		return artistName
	
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

	#sets playblast options and runs playblast
	def playblast_(self):
		#changing image foramt globals to jpg
		mc.setAttr('defaultRenderGlobals.imageFormat', 8)
		
		#stores and then clears selection
		if self.noSelect:
			currentSl = mc.ls(sl=True)
			mc.select(cl=True)
		
		#gets active camera
		if not self.getActiveCamera():
			return

		#turns slate on
		if self.slate:
			self.slateOn()
		else:
			self.slateOff()

		#turns guides on
		if self.guides:
		    activeCamera = self.getActiveCamera()
		    cameraShape = [activeCamera]
		    if mc.nodeType(activeCamera) != 'camera':
		        cameraShape = mc.listRelatives(activeCamera, s=True)
			mc.setAttr("%s.displaySafeAction" % cameraShape[0], 1)
			mc.setAttr("%s.displaySafeTitle" % cameraShape[0], 1)
			
		#storing current overscan value and sets it to 1.0
		overscanValue = self.overscan(get=True)
		self.overscan(set=True)

		#running playblast
		self.run_playblast()
		
		#turning off sltate
		if self.slate:
			self.slateOff()
			
		#restoring overscan to original
		self.overscan(set=True, setValue=overscanValue)
		
		#restoring imageFormat globals
		mc.setAttr('defaultRenderGlobals.imageFormat', 7)

		#restoring selection
		if self.noSelect:
			for sl in currentSl:
				mc.select(sl, add=True)
		
		#restoring guides
		if self.guides:
			mc.setAttr("%s.displaySafeAction" % cameraShape[0], 0)
			mc.setAttr("%s.displaySafeTitle" % cameraShape[0], 0)
			
			
		#returns frRange and file extension
		return self.frRange , 'jpg'
	
	
	#stores averscan info and changes to 1.0
	def overscan(self, set=False, setValue=1.0, get=False):
		activeCamera = self.getActiveCamera()
		cameraShape = [activeCamera]
		if mc.nodeType(activeCamera) != 'camera':
			cameraShape = mc.listRelatives(activeCamera, s=True)
		if set:
			mc.setAttr('%s.overscan' % cameraShape[0], setValue)
			return
		if get:
			setValue = (mc.getAttr('%s.overscan' % cameraShape[0]))
			return setValue
			
	
	#gets the current active camera
	def getActiveCamera(self):
		try:
			activeCamera = mc.modelPanel(mc.getPanel(wf=True), cam=True, q=True)
			return activeCamera
		except RuntimeError:
			print 'Please choose a camera view to preview from'
			
			
	#runs playblast
	def run_playblast(self):
		mc.playblast(f='%s/%s' % (self.playblastDir, self.outputFile), 
		st=self.frRange[0], 
		et=self.frRange[1],
		fp=4, 
		w=self.res[0], 
		h=self.res[1], 
		p=100,
		fmt='image',
		c='jpg',
		v=False,
		os=self.offscreen, 
		cc=True, 
		orn=True)
