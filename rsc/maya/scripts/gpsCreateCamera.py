# [GPS] Create Camera
# v0.2
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Create Maya cameras based on presets stored in XML data file. Can also create a camera rig.


import os
import maya.cmds as mc
import maya.mel as mel
import camPresets


class gpsCreateCamera():

	def __init__(self):
		self.winTitle = "[GPS] Create Camera"
		self.winName = "gpsCreateCameraWindow"
		#self.gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')

		self.cp = camPresets.camPresets()
		self.cp.loadXML(os.path.join(os.environ['ICCONFIGDIR'], 'camPresets.xml'))


	def UI(self):

		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=False)

		# Create controls
		#setUITemplate -pushTemplate gpsToolsTemplate;
		mc.columnLayout("windowRoot")
		self.commonOptUI("commonOptPanel", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=2)
		mc.button("btnSubmit", width=198, height=28, label="Create", command=lambda *args: self.createCameraOptions())
		mc.button("btnClose", width=198, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		mc.showWindow(self.winName)


	def commonOptUI(self, name, parent, collapse=False):
		""" Create common options panel UI controls.
		"""
		mc.frameLayout("commonOptRollout", width=400, collapsable=True, cl=collapse, borderStyle="etchedIn", label="Common Options")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.optionMenuGrp("cameraPresets", label="Camera Preset: ")
		mc.menuItem(label="Default")
		mc.menuItem(label=os.environ['SHOT'])
		for item in self.cp.getPresets():
			mc.menuItem(label=item)
		mc.separator(width=396, height=12, style="in")

		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		mc.checkBox( "createRig",
		             label="Create Camera Rig",
		             value=mc.optionVar( q='GPSCreateCameraRig' ),
		             onCommand=lambda *args: mc.optionVar( iv=('GPSCreateCameraRig', 1) ),
		             offCommand=lambda *args: mc.optionVar( iv=('GPSCreateCameraRig', 0) )
		           )
		mc.setParent(name)
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[142, 8])
		mc.checkBox( "physicalCam",
		             label="Add V-Ray Physical Camera Attributes",
		             value=mc.optionVar( q='GPSAddVRayPhysicalCamera' ),
		             enable=mc.pluginInfo( "vrayformaya", query=True, loaded=True ),
		             onCommand=lambda *args: mc.optionVar( iv=('GPSAddVRayPhysicalCamera', 1) ),
		             offCommand=lambda *args: mc.optionVar( iv=('GPSAddVRayPhysicalCamera', 0) )
		           )
		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.setParent(parent)


	def createCameraOptions(self):
		""" Get options and create camera.
		"""
		camera = mc.optionMenuGrp("cameraPresets", query=True, value=True)
		rig = mc.checkBox("createRig", query=True, value=True)
		physical = mc.checkBox("physicalCam", query=True, value=True)

		#print camera, rig, physical
		self.createCamera(camera, rig, physical)


	def createCamera(self, camera="Default", rig=False, physical=False):
		""" Create camera.
		"""
		if rig:
			mc.file(os.path.join(os.environ['PIPELINE'], 'rsc', 'maya', 'scripts', 'GPS_cam_rig.ma'), i=True, iv=True, rnn=True)
			camGrp = 'GPS_cameraRig'
			cam = 'GPS_camera'
			camSh = mc.listRelatives(cam, s=True)[0]
		else:
			camGrp = None
			cam = mc.camera() #(n='%s_camera' % camera)
			camSh = cam[1]; cam = cam[0]

		# If the camera to be created is the shot camera, read shot data and apply values
		if camera == os.environ['SHOT']:
			import jobSettings
			sd = jobSettings.jobSettings()
			shotDataLoaded = sd.loadXML( os.path.join(os.environ['SHOTDATA'], 'shotData.xml') )

			mc.setAttr(camSh+'.horizontalFilmAperture', float(sd.getValue('camera', 'filmbackWidth')) / 25.4)
			mc.setAttr(camSh+'.verticalFilmAperture', float(sd.getValue('camera', 'filmbackHeight')) / 25.4)
			mc.setAttr(camSh+'.cameraAperture', lock=True)
			mc.setAttr(camSh+'.shutterAngle', float(sd.getValue('camera', 'shutterAngle')))
			#self.setAttr(camSh+'.shutterAngle', '%sdeg' % sd.getValue('camera', 'shutterAngle'))
			mc.setAttr(camSh+'.focalLength', float(sd.getValue('camera', 'focalLength')))
			mc.setAttr(camSh+'.fStop', float(sd.getValue('camera', 'aperture')))
			#mc.setAttr(camSh+'.locatorScale', 25)

			self.setAttr(camSh+'.focusDistance', '%sm' % sd.getValue('camera', 'focusDistance'))
			self.setAttr(camSh+'.centerOfInterest', '%sm' % sd.getValue('camera', 'subjectDistance'))

			if not rig:
				# self.setAttr(cam+'.ty', '%sm' % sd.getValue('camera', 'camHeight'))
				# self.setAttr(cam+'.rx', '%sdeg' % sd.getValue('camera', 'camPitch'))
				mc.move(0, '%sm' % sd.getValue('camera', 'camHeight'), 0, cam)
				mc.rotate('%sdeg' % sd.getValue('camera', 'camPitch'), 0, 0, cam)

			# Add extra attributes and notes
			mc.addAttr(camSh, ln='clipRef', nn='Clip / reel ref', dt='string')
			mc.setAttr(camSh+'.clipRef', sd.getValue('camera', 'clipRef'), typ='string')
			mc.addAttr(camSh, ln='filter', nn='Filter(s)', dt='string')
			mc.setAttr(camSh+'.filter', sd.getValue('camera', 'filter'), typ='string')
			mc.addAttr(camSh, ln='notes', dt='string')
			mc.setAttr(camSh+'.notes', sd.getValue('camera', 'notes'), type='string')

			# TODO - attach plate as image plane

		elif camera != "Default":
			filmback_horiz_in, filmback_vert_in = self.cp.getFilmback(camera, inches=True)
			mc.setAttr(camSh+'.horizontalFilmAperture', filmback_horiz_in)
			mc.setAttr(camSh+'.verticalFilmAperture', filmback_vert_in)
			mc.setAttr(camSh+'.cameraAperture', lock=True)
			mc.setAttr(camSh+'.shutterAngle', 180)
			#self.setAttr(camSh+'.shutterAngle', '180deg')

			# Add extra info attributes to camera transform node
			sensorWidth, sensorHeight = self.cp.getFilmback(camera)

			mc.addAttr(cam, ln='cameraType', dt='string')
			mc.setAttr(cam+'.cameraType', lock=False)
			mc.setAttr(cam+'.cameraType', camera, typ='string', lock=True)
			mc.addAttr(cam, ln='sensorWidth', dt='string')
			mc.setAttr(cam+'.sensorWidth', lock=False)
			mc.setAttr(cam+'.sensorWidth', '%s mm' % sensorWidth, type='string', lock=True)
			mc.addAttr(cam, ln='sensorHeight', dt='string')
			mc.setAttr(cam+'.sensorHeight', lock=False)
			mc.setAttr(cam+'.sensorHeight', '%s mm' % sensorHeight, type='string', lock=True)

		# Apply display settings
		mc.setAttr(camSh+'.displayGateMask', 1)
		mc.setAttr(camSh+'.displayFilmGate', 1)
		mc.setAttr(camSh+'.displayResolution', 1)
		mc.setAttr(camSh+'.displayGateMaskColor', 0.028824, 0.10465, 0.14728, type='double3')
		mc.setAttr(camSh+'.displayGateMaskOpacity', 0.4)
		mc.setAttr(camSh+'.displaySafeAction', 1)
		mc.setAttr(camSh+'.displaySafeTitle', 1)
		mc.setAttr(camSh+'.displayFilmPivot', 1)
		mc.setAttr(camSh+'.displayFilmOrigin', 1)
		mc.setAttr(camSh+'.overscan', 1)
		mc.setAttr(camSh+'.panZoomEnabled', 0)
		mc.setAttr(camSh+'.zoom', 1.25)

		# Add frustum
		mc.select(cam, r=True)
		#mel.eval('source makeFrustum; makeFrustumProc();')

		# Rename nodes
		if camGrp:
			camGrpName = mc.rename(camGrp, '%s_%s' % (camGrp, camera))
			mc.rename(cam, '%s_camera' % camGrpName)
		else:
			mc.rename(cam, '%s_camera' % camera)

		if physical:
			self.addPhysical()



	def addPhysical(self):
		""" Apply VRay physical camera without shifting film gate or focal length.
		"""
		if mc.pluginInfo("vrayformaya", query=True, loaded=True):
			try:
				cam = mc.ls(sl=True)[0]
				camSh = mc.listRelatives(cam, s=True)[0]
				if mc.nodeType(camSh) != 'camera':
					raise 'No Camera'
				mc.setAttr('%s.focalLength' % camSh, l=True)
				mc.setAttr('%s.cameraAperture' % camSh, l=True)
				mel.eval('vray addAttributesFromGroup %s vray_cameraPhysical 1' % camSh)
				mc.setAttr('%s.vrayCameraPhysicalSpecifyFOV' % camSh, 2)
				mc.setAttr('%s.vrayCameraPhysicalOn' % camSh, 1)
			except:
				mc.warning('Please select a camera.')
				return
		else:
			mc.warning('V-Ray plugin not loaded.')


	def setAttr(self, attr, dim):
		""" Hacky function to set an attribute with a forced linear unit, e.g. '1cm', '2in', etc.
		"""
		loc = mc.spaceLocator( p=(dim, '0', '0'), absolute=True )
		dim = mc.getAttr(loc[0]+".localPositionX")
		mc.setAttr(attr, dim)
		mc.delete(loc)

