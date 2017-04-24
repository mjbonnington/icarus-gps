#!/usr/bin/python

# [GPS Preview] appConnect.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2017 Gramercy Park Studios
#
# App-specific funcions for GPS Preview.


import os


class connect(object):
	""" Connects gpsPreview to the relevant application and passes args to its
		internal preview API.
	"""
	def __init__(self, fileInput, res, frRange, offscreen, noSelect, guides, slate):
		self.fileInput = fileInput
		self.outputFile = os.path.split(self.fileInput)[1]
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
		if os.environ['ICARUSENVAWARE'] == 'MAYA':
			self.outputDir = os.path.join(os.environ['MAYAPLAYBLASTSDIR'], self.fileInput)
			mayaPreviewOutput = self.mayaPreview()
			if mayaPreviewOutput:
				self.frRange, ext = mayaPreviewOutput
				return self.outputDir, self.outputFile, self.frRange, ext
			else:
				return


	def mayaPreview(self):
		""" Begin Maya preview (playblast).
		"""
		import gpsMayaPreview
		previewSetup = gpsMayaPreview.preview(self.outputDir, self.outputFile, (self.hres, self.vres), self.frRange, self.offscreen, self.noSelect, self.guides, self.slate)
		return previewSetup.playblast_()


def getScene():
	""" Returns name of scene/script/project file.
	"""
	if os.environ['ICARUSENVAWARE'] == 'MAYA':
		import mayaOps
		return os.path.splitext(os.path.basename(mayaOps.getScene()))[0]


def getResolution():
	""" Returns the current resolution of scene/script/project file as a
		tuple (integer, integer).
	"""
	if os.environ['ICARUSENVAWARE'] == 'MAYA':
		import maya.cmds as mc
		return mc.getAttr("defaultResolution.w"), mc.getAttr("defaultResolution.h")


def getFrameRange():
	""" Returns the frame range of scene/script/project file as a tuple
		(integer, integer).
	"""
	if os.environ['ICARUSENVAWARE'] == 'MAYA':
		import maya.cmds as mc
		return int(mc.playbackOptions(min=True, q=True)), int(mc.playbackOptions(max=True, q=True))


def getCurrentFrame():
	""" Returns the current frame of scene/script/project file as an integer.
	"""
	if os.environ['ICARUSENVAWARE'] == 'MAYA':
		import maya.cmds as mc
		return int(mc.currentTime(q=True))

