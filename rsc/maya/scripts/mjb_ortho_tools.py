# mjb_ortho_tools.py
# v0.2
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2018
#
# Tools to improve the functionality of Maya's orthographic views.
#
# Automatically sets default orthographic cameras' transform and clipping
# planes to selection. Use when working with large-scale scenes and framing
# the view doesn't work.


import maya.cmds as mc


class OrthoCamFix():

	def __init__(self):
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

		x_min = bbox[0]; x_max = bbox[3]
		y_min = bbox[1]; y_max = bbox[4]
		z_min = bbox[2]; z_max = bbox[5]

		x_len = abs(x_max - x_min)
		y_len = abs(y_max - y_min)
		z_len = abs(z_max - z_min)

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


class OrthoCamLink():

	def __init__(self):
		# Store default panel arrangement
		self.topPanel = self.get_panel_from_camera('top')[0]
		self.sidePanel = self.get_panel_from_camera('side')[0]
		self.perspPanel = self.get_panel_from_camera('persp')[0]


	def get_active_view(self):
		""" Returns currently active panel. If panel has no camera attached,
			return False.
		"""
		panel = mc.getPanel(withFocus=True)
		camera = self.get_active_camera(panel)

		if camera is not "":
			return camera, panel
		else:
			return False, False


	def get_active_camera(self, panel):
		""" Returns camera for the specified panel.
		"""
		try:
			camera = mc.modelPanel(panel, cam=True, q=True)
		except:
			camera = ""

		return camera


	def get_panel_from_camera(self, camera):
		""" Returns the panel(s) containing the specified camera.
		"""
		listPanel=[]
		for panel in mc.getPanel(type='modelPanel'):
			if mc.modelPanel(panel, query=True, camera=True) == camera:
				listPanel.append(panel)

		return listPanel


	def reset(self):
		""" Reset (break links between views)
		"""
		#print "reset"

		# Reset panel arrangement
		mc.modelPanel(self.topPanel, edit=True, camera='top')
		mc.modelPanel(self.sidePanel, edit=True, camera='side')
		mc.modelPanel(self.perspPanel, edit=True, camera='persp')

		try:
			self.deactivate_top()
		except:
			pass

		try:
			self.deactivate_front()
		except:
			pass

		try:
			self.deactivate_side()
		except:
			pass


	def activate_top(self):
		""" Link top view to others.
		"""
		self.reset()

		#print "link to top"
		mc.connectAttr('top.translateX', 'front.translateX', force=True)
		mc.connectAttr('top.translateZ', 'side.translateZ', force=True)
		#mc.connectAttr('front.translateY', 'side.translateY', force=True)
		mc.connectAttr('topShape.orthographicWidth', 'frontShape.orthographicWidth', force=True)
		mc.connectAttr('topShape.orthographicWidth', 'sideShape.orthographicWidth', force=True)

		# Swap side panel with persp
		mc.modelPanel(self.sidePanel, edit=True, camera='persp')
		mc.modelPanel(self.perspPanel, edit=True, camera='side')

		# Rotate side view
		mc.setAttr('side.rx', -90)
		mc.setAttr('side.ry', 0)
		mc.setAttr('side.rz', -90)


	def deactivate_top(self):
		""" Unlink from top view.
		"""
		mc.disconnectAttr('top.translateX', 'front.translateX')
		mc.disconnectAttr('top.translateZ', 'side.translateZ')
		#mc.disconnectAttr('front.translateY', 'side.translateY')
		mc.disconnectAttr('topShape.orthographicWidth', 'frontShape.orthographicWidth')
		mc.disconnectAttr('topShape.orthographicWidth', 'sideShape.orthographicWidth')

		mc.setAttr('side.rx', 0)
		mc.setAttr('side.ry', 90)
		mc.setAttr('side.rz', 0)


	def activate_front(self):
		""" Link front view to others.
		"""
		self.reset()

		#print "link to front"
		mc.connectAttr('front.translateX', 'top.translateX', force=True)
		mc.connectAttr('front.translateY', 'side.translateY', force=True)
		mc.connectAttr('frontShape.orthographicWidth', 'topShape.orthographicWidth', force=True)
		mc.connectAttr('frontShape.orthographicWidth', 'sideShape.orthographicWidth', force=True)


	def deactivate_front(self):
		""" Unlink from front view.
		"""
		mc.disconnectAttr('front.translateX', 'top.translateX')
		mc.disconnectAttr('front.translateY', 'side.translateY')
		mc.disconnectAttr('frontShape.orthographicWidth', 'topShape.orthographicWidth')
		mc.disconnectAttr('frontShape.orthographicWidth', 'sideShape.orthographicWidth')


	def activate_side(self):
		""" Link side view to others.
		"""
		self.reset()

		#print "link to side"
		mc.connectAttr('side.translateY', 'front.translateY', force=True)
		mc.connectAttr('side.translateZ', 'top.translateZ', force=True)
		#mc.connectAttr('front.translateX', 'top.translateX', force=True)
		mc.connectAttr('sideShape.orthographicWidth', 'frontShape.orthographicWidth', force=True)
		mc.connectAttr('sideShape.orthographicWidth', 'topShape.orthographicWidth', force=True)

		# Swap top panel with persp
		mc.modelPanel(self.topPanel, edit=True, camera='persp')
		mc.modelPanel(self.perspPanel, edit=True, camera='top')

		# Rotate top view
		mc.setAttr('top.rx', -90)
		mc.setAttr('top.ry', 90)
		mc.setAttr('top.rz', 0)


	def deactivate_side(self):
		""" Unlink from side view.
		"""
		mc.disconnectAttr('side.translateY', 'front.translateY')
		mc.disconnectAttr('side.translateZ', 'top.translateZ')
		#mc.disconnectAttr('front.translateX', 'top.translateX')
		mc.disconnectAttr('sideShape.orthographicWidth', 'frontShape.orthographicWidth')
		mc.disconnectAttr('sideShape.orthographicWidth', 'topShape.orthographicWidth')

		mc.setAttr('top.rx', -90)
		mc.setAttr('top.ry', 0)
		mc.setAttr('top.rz', 0)


	def link_to_active():
		""" Link other ortho cam views to currently active view.
		"""
		camera, panel = self.get_active_view()
		self.reset()

		print camera, panel
		if camera == 'top':
			self.activate_top()
		elif camera == 'front':
			self.activate_front()
		elif camera == 'side':
			self.activate_side()
		#else:
			#self.reset()


