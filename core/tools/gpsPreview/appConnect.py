#!/usr/bin/python

# [GPS Preview] appConnect.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2018 Gramercy Park Studios
#
# App-specific functions for GPS Preview.


import os


# ----------------------------------------------------------------------------
# Main class
# ----------------------------------------------------------------------------

#class connect(object):
class AppConnect(object):
	""" Connects gpsPreview to the relevant application and passes args to its
		internal preview API.
	"""
	def __init__(self, fileInput, format, activeView, camera, res, frRange, offscreen, noSelect, guides, slate):
	#def __init__(self, **kwargs):
		self.fileInput = fileInput
		self.outputFile = os.path.split(self.fileInput)[1]
		self.format = format
		self.activeView = activeView
		self.camera = camera
		self.hres = int(res[0])
		self.vres = int(res[1])
		self.frRange = frRange
		try:
			self.range = (int(self.frRange[0]), int(self.frRange[1]))
		except ValueError:
			pass
		self.offscreen = offscreen
		self.noSelect = noSelect
		self.guides = guides
		self.slate = slate


	def appPreview(self):
		""" Detect environment.
		"""
		if os.environ['IC_ENV'] == 'MAYA':
			self.outputDir = os.path.join(os.environ['MAYAPLAYBLASTSDIR'], self.fileInput)
			mayaPreviewOutput = self.mayaPreview()
			if mayaPreviewOutput:
				# self.frRange, ext = mayaPreviewOutput
				# return self.outputDir, self.outputFile, self.frRange, ext
				return mayaPreviewOutput
			else:
				return


	def mayaPreview(self):
		""" Begin Maya preview (playblast).
		"""
		import gpsMayaPreview
		previewSetup = gpsMayaPreview.Preview(self.outputDir, self.outputFile, self.format, self.activeView, self.camera, (self.hres, self.vres), self.frRange, self.offscreen, self.noSelect, self.guides, self.slate)
		return previewSetup.playblast_()

# ----------------------------------------------------------------------------
# End of main class
# ----------------------------------------------------------------------------

def getScene():
	""" Returns name of scene/script/project file.
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import mayaOps
		return os.path.splitext(os.path.basename(mayaOps.getScene()))[0]


def getCameras(renderableOnly=False):
	""" Returns list of cameras in the scene. Renderable cameras will be
		listed first.
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import maya.cmds as mc
		# noSelectText = ""
		# camera_list = [noSelectText, ]
		camera_list = []
		# cameras = mc.ls(cameras=True)
		persp_cameras = mc.listCameras(perspective=True)
		ortho_cameras = mc.listCameras(orthographic=True)
		cameras = persp_cameras+ortho_cameras
		for camera in cameras:
			if mc.getAttr(camera+'.renderable'):
				camera_list.insert(0, camera)
			elif renderableOnly == False:
				camera_list.append(camera)

		return camera_list


def getActiveCamera(panel=None):
	""" Returns camera for the specified panel. If no panel is specified,
		use the currently active panel.
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import maya.cmds as mc
		if panel is None:
			panel = mc.getPanel(withFocus=True)
		camera = mc.modelPanel(panel, cam=True, q=True)

		#print(camera)

		return camera


def getActiveView():
	""" Returns currently active panel. If panel has no camera attached,
		return False.
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import maya.cmds as mc
		panel = mc.getPanel(withFocus=True)
		try:
			camera = mc.modelPanel(panel, cam=True, q=True)
		except:
			camera = None

		#print(panel, camera)

		if camera is not None:
			return panel
		else:
			return False


def getResolution():
	""" Returns the current resolution of scene/script/project file as a
		tuple (integer, integer).
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import maya.cmds as mc
		return mc.getAttr("defaultResolution.w"), mc.getAttr("defaultResolution.h")


def getFrameRange():
	""" Returns the frame range of scene/script/project file as a tuple
		(integer, integer).
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import maya.cmds as mc
		return int(mc.playbackOptions(min=True, q=True)), int(mc.playbackOptions(max=True, q=True))


def getCurrentFrame():
	""" Returns the current frame of scene/script/project file as an integer.
	"""
	if os.environ['IC_ENV'] == 'MAYA':
		import maya.cmds as mc
		return int(mc.currentTime(q=True))

