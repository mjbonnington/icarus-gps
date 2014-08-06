#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:gpsPreview

import os
	
####connects gpsPreview to the relevant application and passes args to its internal preview API
class connect(object):
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
		
	#detecting enviro
	def appPreview(self):
		if os.environ['ICARUSENVAWARE'] == 'MAYA':
			self.outputDir = '%s/%s' % (os.environ['MAYAPLAYBLASTSDIR'], self.fileInput)
			mayaPreviewOutput = self.mayaPreview()
			if mayaPreviewOutput:
				self.frRange, ext = mayaPreviewOutput
				return self.outputDir, self.outputFile, self.frRange, ext
			else:
				return
			
	#maya preview
	def mayaPreview(self):
		import gpsMayaPreview
		previewSetup = gpsMayaPreview.preview(self.outputDir, self.outputFile, (self.hres, self.vres), self.frRange, self.offscreen, self.noSelect, self.guides, self.slate)
		return previewSetup.playblast_()