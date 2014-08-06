import maya.cmds as mc
import maya.mel as mel


def addStdElements():
	stdElementDict = {'vrayRE_Diffuse':'diffuseChannel','vrayRE_Reflection':'reflectChannel','vrayRE_Lighting':'lightingChannel',
	'vrayRE_Matte_shadow':'matteShadowChannel'}

	if mc.getAttr("vraySettings.giOn"):
		stdElementDict['vrayRE_GI'] = 'giChannel'
	
	for key in stdElementDict.keys():
		if not mc.objExists(key):
			mel.eval('vrayAddRenderElement %s;' % stdElementDict[key])
		else:
			print '%s element already exsits. Skipped.' % key

	#ambient occlusion
	if not mc.objExists('vrayRE_AO'):
		aoDirt = mel.eval('createRenderNodeCB -as2DTexture "" VRayDirt "";')
		aoPass = mel.eval('vrayAddRenderElement ExtraTexElement;')
		mc.connectAttr('%s.outColor' % aoDirt, '%s.vray_texture_extratex' % aoPass)
		mc.rename(aoDirt, 'ambientOcculsion')
		mc.setAttr('%s.vray_name_extratex' % aoPass, 'AO', typ='string')
		mc.setAttr('%s.vray_explicit_name_extratex' % aoPass, 'AO', typ='string')
		mc.rename(aoPass, 'vrayRE_AO')
	else:
		print 'vrayRE_AO element already exsits. Skipped'

def addDataElements():
	dataElementDict = {'vrayRE_Normals':'normalsChannel',
				    'vrayRE_BumpNormals':'bumpNormalsChannel',
				    'vrayRE_Z_depth':'zdepthChannel',
				    'vrayRE_Velocity':'velocityChannel'}

	for key in dataElementDict.keys():
		if not mc.objExists(key):
			addedElement = mel.eval('vrayAddRenderElement %s;' % dataElementDict[key])
			#unclamping z-depth
			if key == 'vrayRE_Z_depth':
				mc.setAttr('%s.vray_depthClamp' % addedElement, 0)
				mc.setAttr('%s.vray_filtering_zdepth' % addedElement, 0)
			if key == 'vrayRE_Velocity':
				mc.setAttr('%s.vray_clamp_velocity' % addedElement, 0)
				mc.setAttr('%s.vray_filtering_velocity' % addedElement, 0)
		else:
			print '%s element already exsits. Skipped.' % key
			
	#pWorld pass
	if not mc.objExists('vrayRE_pWorld'):
		pWorldSI = mel.eval('createRenderNodeCB -asUtility "" samplerInfo "";')
		pWorldPass = mel.eval('vrayAddRenderElement ExtraTexElement;')
		mc.connectAttr('%s.pointWorldX' % pWorldSI, '%s.vray_texture_extratex.vray_texture_extratexR' % pWorldPass)
		mc.connectAttr('%s.pointWorldY' % pWorldSI, '%s.vray_texture_extratex.vray_texture_extratexG' % pWorldPass)
		mc.connectAttr('%s.pointWorldZ' % pWorldSI, '%s.vray_texture_extratex.vray_texture_extratexB' % pWorldPass)
		mc.rename(pWorldSI, 'pWorld')
		mc.setAttr('%s.vray_name_extratex' % pWorldPass, 'pWorld', typ='string')
		mc.setAttr('%s.vray_explicit_name_extratex' % pWorldPass, 'pWorld', typ='string')
		mc.setAttr('%s.vray_filtering_extratex' % pWorldPass, 0)
		mc.setAttr('%s.vray_considerforaa_extratex' % pWorldPass, 0)
		mc.setAttr('%s.vray_affectmattes_extratex' % pWorldPass, 0)
		mc.rename(pWorldPass, 'vrayRE_pWorld')
	else:
		print 'vrayRE_pWorld element already exsits. Skipped'

	#uvf pass
	if not mc.objExists('vrayRE_uvf'):
		uvfSI = mel.eval('createRenderNodeCB -asUtility "" samplerInfo "";')
		uvfPass = mel.eval('vrayAddRenderElement ExtraTexElement;')
		mc.connectAttr('%s.uCoord' % pWorldSI, '%s.vray_texture_extratex.vray_texture_extratexR' % uvfPass)
		mc.connectAttr('%s.vCoord' % pWorldSI, '%s.vray_texture_extratex.vray_texture_extratexG' % uvfPass)
		mc.connectAttr('%s.facingRatio' % pWorldSI, '%s.vray_texture_extratex.vray_texture_extratexB' % uvfPass)
		mc.rename(uvfSI, 'uvf')
		mc.setAttr('%s.vray_name_extratex' % uvfPass, 'uvf', typ='string')
		mc.setAttr('%s.vray_explicit_name_extratex' % uvfPass, 'uvf', typ='string')
		mc.rename(uvfPass, 'vrayRE_uvf')
	else:
		print 'vrayRE_uvf element already exsits. Skipped'

	#changes the bit depth from 16 to 32 bit exr
	mc.setAttr("vraySettings.imgOpt_exr_bitsPerChannel", 32)
