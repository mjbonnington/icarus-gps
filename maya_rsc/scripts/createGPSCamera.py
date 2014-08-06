import os
import maya.cmds as mc
import maya.mel as mel
import getFilmback
reload(getFilmback)

#creates a camera with correct film back factory settings.

def createCamera(camera, rig=False):
	#applying stock camera settings
	if rig:
		mc.file(os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'scripts', 'GPS_cam_rig.ma'), i=True, iv=True, rnn=True)
		camGrp = 'GPS_cameraRig'
		cam = 'GPS_camera'
		camSh = mc.listRelatives(cam, s=True)[0]
	else:
		camGrp = None
		cam = mc.camera(n='%s_camera' % camera)
		camSh = cam[1]; cam = cam[0]
	if camera != 'default':
		Hfilmback, Vfilmback = getFilmback.get(camera, inches=True)
		inches = True
		mc.setAttr('%s.horizontalFilmAperture' % camSh, Hfilmback)
		mc.setAttr('%s.verticalFilmAperture' % camSh, Vfilmback)
		mc.setAttr('%s.cameraAperture' % camSh, l=True)
		#adds info attributes to camera
		if inches:
			HSensor = round(Hfilmback * 25.4, 1)
			VSensor = round(Vfilmback * 25.4, 1)
		mc.addAttr(cam, ln='Camera', dt='string')
		mc.setAttr('%s.Camera' % cam, l=False)
		mc.setAttr('%s.Camera' % cam, camera, typ='string', l=True)
		mc.addAttr(cam, ln='HSensor', dt='string')
		mc.setAttr('%s.HSensor' % cam, l=False)
		mc.setAttr('%s.HSensor' % cam, '%s mm' % HSensor, typ='string', l=True)
		mc.addAttr(cam, ln='VSensor', dt='string')
		mc.setAttr('%s.VSensor' % cam, l=False)
		mc.setAttr('%s.VSensor' % cam, '%s mm' % VSensor, typ='string', l=True)
	#applying display settings
	mc.setAttr('%s.displayGateMask' % camSh, 1)
	mc.setAttr('%s.displayFilmGate' % camSh, 1)
	mc.setAttr('%s.displayResolution' % camSh, 0)
	mc.setAttr('%s.displayGateMaskColor' % camSh, 0.0288243, 0.104645, 0.14728, type='double3')
	mc.setAttr('%s.displayGateMaskOpacity' % camSh, 0.475 )
	mc.setAttr('%s.displaySafeTitle' % camSh, 1)
	mc.setAttr('%s.displaySafeAction' % camSh, 1)
	mc.setAttr('%s.overscan' % camSh, 1.2)
	mc.setAttr('%s.displayFilmPivot' % camSh, 1)
	mc.setAttr('%s.displayFilmOrigin' % camSh, 1)
	#adding frustum
	mc.select(cam, r=True)
	mel.eval('source makeFrustum; makeFrustumProc();')
	#renaming nodes
	if camGrp:
		camGrpName = mc.rename(camGrp, '%s_%s' % (camGrp, camera))
		mc.rename(cam, '%s_camera' % camGrpName)
	
#Adds Physical applies vray physical camera without shifting film gate or focal length
def addPhysical():
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
		print '\n\nPlease select a camera'
		return
