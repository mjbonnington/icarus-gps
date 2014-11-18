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
		
	#normals in positive world space pass
	if not mc.objExists('vrayRE_normals_pws'):
		normals_ws_SI = mel.eval('createRenderNodeCB -asUtility "" samplerInfo "";')
		multXYZ = mel.eval('createRenderNodeCB -asUtility "" multiplyDivide "";')
		condX = mel.eval('createRenderNodeCB -asUtility "" condition "";')
		condY = mel.eval('createRenderNodeCB -asUtility "" condition "";')
		condZ = mel.eval('createRenderNodeCB -asUtility "" condition "";')
		vectorProd = mel.eval('createRenderNodeCB -asUtility "" vectorProduct "";')
		normals_ws_Pass = mel.eval('vrayAddRenderElement ExtraTexElement;')
		mc.connectAttr('%s.normalCamera' % normals_ws_SI, '%s.input1' % vectorProd)
		mc.connectAttr('%s.matrixEyeToWorld' % normals_ws_SI, '%s.matrix' % vectorProd)
		mc.setAttr('%s.operation' % vectorProd, 3)
		mc.connectAttr('%s.output' % vectorProd, '%s.input1' % multXYZ)
		mc.setAttr('%s.input2X' % multXYZ, -1)
		mc.setAttr('%s.input2Y' % multXYZ, -1)
		mc.setAttr('%s.input2Z' % multXYZ, -1)
		mc.connectAttr('%s.outputX' % multXYZ, '%s.colorIfTrueR' % condX)
		mc.connectAttr('%s.outputY' % multXYZ, '%s.colorIfTrueG' % condY)
		mc.connectAttr('%s.outputZ' % multXYZ, '%s.colorIfTrueB' % condZ)
		mc.connectAttr('%s.outputX' % vectorProd, '%s.colorIfFalseR' % condX)
		mc.connectAttr('%s.outputX' % vectorProd, '%s.firstTerm' % condX)
		mc.connectAttr('%s.outputY' % vectorProd, '%s.colorIfFalseG' % condY)
		mc.connectAttr('%s.outputY' % vectorProd, '%s.firstTerm' % condY)
		mc.connectAttr('%s.outputZ' % vectorProd, '%s.colorIfFalseB' % condZ)
		mc.connectAttr('%s.outputZ' % vectorProd, '%s.firstTerm' % condZ)
		mc.connectAttr('%s.outColorR' % condX, '%s.vray_texture_extratex.vray_texture_extratexR' % normals_ws_Pass)
		mc.connectAttr('%s.outColorG' % condY, '%s.vray_texture_extratex.vray_texture_extratexG' % normals_ws_Pass)
		mc.connectAttr('%s.outColorB' % condZ, '%s.vray_texture_extratex.vray_texture_extratexB' % normals_ws_Pass)
		mc.setAttr('%s.operation' % condX, 4)
		mc.setAttr('%s.operation' % condY, 4)
		mc.setAttr('%s.operation' % condZ, 4)
		mc.setAttr('%s.vray_name_extratex' % normals_ws_Pass, 'normals_pws', typ='string')
		mc.setAttr('%s.vray_explicit_name_extratex' % normals_ws_Pass, 'normals_pws', typ='string')
		mc.setAttr('%s.vray_considerforaa_extratex' % normals_ws_Pass, 0)
		mc.setAttr('%s.vray_affectmattes_extratex' % normals_ws_Pass, 0)
		mc.rename(normals_ws_SI, 'normals_pws')
		mc.rename(multXYZ, 'normals_pws_XYZ_mult')
		mc.rename(condX, 'normals_pws_conditionX')
		mc.rename(condY, 'normals_pws_conditionY')
		mc.rename(condZ, 'normals_pws_conditionZ')
		mc.rename(vectorProd, 'normals_pws_vectorProduct')
		mc.rename(normals_ws_Pass, 'vrayRE_normals_pws')
	else:
		print 'vrayRE_normals_pws element already exsits. Skipped'

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
