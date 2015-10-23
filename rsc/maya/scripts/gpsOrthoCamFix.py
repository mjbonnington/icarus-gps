# GPS Ortho Cam Fix
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Automatically sets default orthographic cameras' transform and clipping
# planes to selection. Use when working with large-scale scenes and framing
# the view doesn't work

import maya.cmds as mc

class gpsOrthoCamFix():

	def __init__(self):
		#self.winTitle = "GPS Ortho Cam Fix"
		#self.winName = "gpsOrthoCamFix"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		# Selection list should only contain DAG nodes
		sel = mc.ls(long=True, selection=True, type='dagNode')
		if sel:
			#print "Fit to selection"
			self.orthoCamFix()
		else:
			#print "Fit to all"
			mc.select(allDagObjects=True)
			self.orthoCamFix()
			mc.select(clear=True)

	def orthoCamFix(self):
		bbox = mc.exactWorldBoundingBox()
		x_min = bbox[0]; y_min = bbox[1]; z_min = bbox[2]; x_max = bbox[3]; y_max = bbox[4]; z_max = bbox[5]

		x_len = x_max - x_min
		y_len = y_max - y_min
		z_len = z_max - z_min

		mc.setAttr("side.tx", x_max+x_len*2)
		mc.setAttr("sideShape.nearClipPlane", x_len)
		mc.setAttr("sideShape.farClipPlane", x_len*4)
		mc.setAttr("sideShape.centerOfInterest", x_len*2.5)

		mc.setAttr("top.ty", y_max+y_len*2)
		mc.setAttr("topShape.nearClipPlane", y_len)
		mc.setAttr("topShape.farClipPlane", y_len*4)
		mc.setAttr("topShape.centerOfInterest", y_len*2.5)

		mc.setAttr("front.tz", z_max+z_len*2)
		mc.setAttr("frontShape.nearClipPlane", z_len)
		mc.setAttr("frontShape.farClipPlane", z_len*4)
		mc.setAttr("frontShape.centerOfInterest", z_len*2.5)
