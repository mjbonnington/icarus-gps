#!/usr/bin/python

# [Icarus] gpsRenderToolsVRay.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# A collection of tools for the V-Ray renderer.


import maya.cmds as mc
import maya.mel as mel


def pluginCheck():
	if mc.pluginInfo("vrayformaya", query=True, loaded=True):
		return True
	else:
		mc.warning("V-Ray plugin not loaded.")
		return False


def createMaterial(materialType, materialName):
	""" Create V-Ray shaders.
	"""
	if not pluginCheck():
		return

	# Check option to pop up naming dialog
	if mc.optionVar(q='vrayDisableShaderNaming') < 1:
		dialogResult = mc.promptDialog( title = 'Create V-Ray Material', 
										message = 'Material Name:', 
										button = ['OK', 'Cancel'], 
										defaultButton = 'OK', 
										cancelButton = 'Cancel', 
										dismissString = 'Cancel' )

		if dialogResult:
			materialName = mc.promptDialog(text=True, q=True)

	# Stash selection
	objLs = mc.ls(sl=True, type='transform')

	# Create the node
	shaderNode = mc.shadingNode(materialType, asShader=True)
	shaderNode = mc.rename(shaderNode, "%s_%s" %(materialName, materialType))

	# Create a shading group
	shadingGrp = mc.sets(empty=True, renderable=True, noSurfaceShader=True)
	shadingGrp = mc.rename(shadingGrp, materialName+"SG")

	# Connect the two together
	mc.connectAttr( (shaderNode+".outColor"), (shadingGrp+".surfaceShader"), force=True)

	# Assign to all the selected objects
#	for obj in objLs:
#		mc.assignSG(shaderNode, obj)

	return shaderNode


def createLight(lightNodeType, lightType):
	""" Create V-Ray lights.
	"""
	if not pluginCheck():
		return

	dialogResult = mc.promptDialog( title = 'Create V-Ray Light', 
									message = 'Light Name:', 
									button = ['OK', 'Cancel'], 
									defaultButton = 'OK', 
									cancelButton = 'Cancel', 
									dismissString = 'Cancel' )

	if dialogResult:
		lightName =	mc.promptDialog(text=True, q=True)

		if not lightName.endswith(lightType):
			lightName = '%s_%s' % (lightName, lightType)

		lightNode = mc.shadingNode(lightNodeType, asLight=True)

		# Make viewport display larger
		mc.setAttr('%s.displayLocalAxis' % lightNode, 1)

		mc.select(lightNode, r=True)
		mc.rename(lightNode, lightName)
		return lightNode

	else:
		return


def createLightSelPass():
	""" Create a light contribution pass (render element) for the selected lights.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True)

	if not objLs:
		mc.warning("No lights selected.")
		return

	dialogResult = mc.promptDialog( title='Create V-Ray Light Pass', 
									message='Light Pass Name:', 
									button=['OK', 'Cancel'], 
									defaultButton='OK', 
									cancelButton='Cancel', 
									dismissString='Cancel' )

	if dialogResult:
		lightPassName = mc.promptDialog(text=True, q=True)
		lightPassSet = mel.eval("vrayAddRenderElement LightSelectElement")
		for obj in objLs:
			mc.sets(obj, forceElement=lightPassSet, e=True)
		mc.setAttr('%s.vray_name_lightselect' % lightPassSet, '%s_lightSel' % lightPassName, type='string')
		mc.rename(lightPassSet, '%s_vrayRE_Light_Select' % lightPassName)


def addStdElements():
	""" Create a standard set of render elements.
	"""
	if not pluginCheck():
		return

	stdElementDict = {'vrayRE_Diffuse':'diffuseChannel', 'vrayRE_Reflection':'reflectChannel', 'vrayRE_Lighting':'lightingChannel', 'vrayRE_Shadow':'shadowChannel'}

	if mc.getAttr("vraySettings.giOn"):
		stdElementDict['vrayRE_GI'] = 'giChannel'

	for key in stdElementDict.keys():
		if not mc.objExists(key):
			mel.eval('vrayAddRenderElement %s;' % stdElementDict[key])
		else:
			print '%s element already exists. Skipped.' % key,

	# Ambient occlusion
	if not mc.objExists('vrayRE_AO'):
		aoDirt = mel.eval('createRenderNodeCB -as2DTexture "" VRayDirt "";')
		aoPass = mel.eval('vrayAddRenderElement ExtraTexElement;')
		mc.connectAttr('%s.outColor' % aoDirt, '%s.vray_texture_extratex' % aoPass)
		mc.rename(aoDirt, 'ambientOcculsion')
		mc.setAttr('%s.vray_name_extratex' % aoPass, 'AO', typ='string')
		mc.setAttr('%s.vray_explicit_name_extratex' % aoPass, 'AO', typ='string')
		mc.rename(aoPass, 'vrayRE_AO')
	else:
		print 'vrayRE_AO element already exists. Skipped.',


def addDataElements():
	""" Create a standard set of utility passes.
	"""
	if not pluginCheck():
		return

	dataElementDict = {'vrayRE_Normals':'normalsChannel', 'vrayRE_BumpNormals':'bumpNormalsChannel', 'vrayRE_Z_depth':'zdepthChannel', 'vrayRE_Velocity':'velocityChannel'}

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
			print '%s element already exists. Skipped.' % key,

	# pWorld pass
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
		print 'vrayRE_pWorld element already exists. Skipped.',

	# Normals in positive world space pass
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
		print 'vrayRE_normals_pws element already exists. Skipped.',

	# uvf pass
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
		print 'vrayRE_uvf element already exists. Skipped',

	# Change the bit depth from 16 to 32 bit exr - disabled this as it's unnecessary
	#mc.setAttr("vraySettings.imgOpt_exr_bitsPerChannel", 32)


def addVRayGamma():
	""" Add V-Ray Texture Input Gamma attributes to selection.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True)

	for obj in objLs:
		if mc.nodeType(obj) == "file":
			mel.eval('vrayAddAttr %s vrayFileGammaEnable;' % obj)
			mel.eval('vrayAddAttr %s vrayFileColorSpace;' % obj)
			mel.eval('vrayAddAttr %s vrayFileGammaValue;' % obj)


def removeVRayGamma():
	""" Remove V-Ray Texture Input Gamma attributes from selection.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True)

	for obj in objLs:
		if mc.nodeType(obj) == "file":
			mel.eval('vrayDeleteAttr %s vrayFileGammaEnable;' % obj)
			mel.eval('vrayDeleteAttr %s vrayFileColorSpace;' % obj)
			mel.eval('vrayDeleteAttr %s vrayFileGammaValue;' % obj)


def addVRayNegCol():
	""" Add V-Ray Allow Negative Colors attributes to selection.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True)

	for obj in objLs:
		if mc.nodeType(obj) == "file":
			mel.eval('vray addAttributesFromGroup %s vray_file_allow_neg_colors 1;' % obj)


def removeVRayNegCol():
	""" Remove V-Ray Allow Negative Colors attributes from selection.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True)

	for obj in objLs:
		if mc.nodeType(obj) == "file":
			mel.eval('vray addAttributesFromGroup %s vray_file_allow_neg_colors 0;' % obj)


def addSubD(subDs = 2):
	""" Add V-Ray subdivision and displacement attributes to selected meshes.
		TODO: Add appropriate presets for data from ZBrush, Mudbox, etc.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True, l=True)
	for obj in objLs:
		objSh = mc.listRelatives(obj, s=True, f=True)[0]
		mel.eval('vray addAttributesFromGroup %s vray_subdivision 1' % objSh)
		mel.eval('vray addAttributesFromGroup %s vray_subquality 1' % objSh)
		mel.eval('vray addAttributesFromGroup %s vray_displacement 1' % objSh)
		mc.setAttr('%s.vrayMaxSubdivs' % objSh, subDs)
		mc.setAttr("%s.vraySubdivUVs" % objSh, 0)
		mc.setAttr("%s.vrayDisplacementKeepContinuity" % objSh, 1)
		mc.setAttr("%s.vray2dDisplacementFilterTexture" % objSh, 0)


def removeSubD():
	""" Remove V-Ray subdivision and displacement attributes from selected meshes.
	"""
	if not pluginCheck():
		return

	objLs = mc.ls(sl=True, l=True)
	for obj in objLs:
		objSh = mc.listRelatives(obj, s=True, f=True)[0]
		mel.eval('vray addAttributesFromGroup %s vray_subdivision 0' % objSh)
		mel.eval('vray addAttributesFromGroup %s vray_subquality 0' % objSh)
		mel.eval('vray addAttributesFromGroup %s vray_displacement 0' % objSh)


def objID(single=False):
	""" Add V-Ray object ID attributes.
	"""
	if not pluginCheck():
		return

	allObjLs = mc.ls(tr=True, l=True)
	objLs = mc.ls(sl=True, l=True)
	newId = 1
	idLs = []
	if not objLs:
		mc.warning("Nothing selected.")
	for allObj in allObjLs:
		try:
			allObjSh = mc.listRelatives(allObj, s=True, f=True)[0]
			try:
				idLs.append(mc.getAttr('%s.vrayObjectID' % allObj))
			except:
				pass
		except TypeError:
			pass
	for obj in objLs:
		try:
			objSh = mc.listRelatives(obj, s=True, f=True)[0]
			if not mc.objExists('%s.vrayObjectID'% objSh):
				mel.eval('vrayAddAttr %s vrayObjectID' % objSh)
				while newId in idLs:
					newId += 1
				mc.setAttr('%s.vrayObjectID' % objSh, newId)
			if not single:
				newId += 1
		except TypeError:
			pass


def objMultiMatte(all=False):
	""" Create V-Ray multimatte render elements automatically.
	"""
	if not pluginCheck():
		return

	idLs = []
	if all:
		objLs = mc.ls(tr=True, l=True)
	else:
		objLs = mc.ls(sl=True, l=True)
	if not objLs:
		mc.warning("Nothing selected.")
	for obj in objLs:
		try:
			objSh = mc.listRelatives(obj, s=True, f=True)[0]
			idLs.append(mc.getAttr('%s.vrayObjectID' % objSh))
		except:
			pass
	idLs = list(set(idLs))
	idLs.sort()
	mmLs = [idLs[i:i+3] for i in range(0, len(idLs), 3)]
	for mm in mmLs:
		mm = list(set(mm))
		mm.sort()
		mmElement = mel.eval("vrayAddRenderElement MultiMatteElement")
		mc.setAttr('%s.vray_redid_multimatte' % mmElement, mm[0])
		mc.setAttr('%s.vray_name_multimatte' % mmElement, 'oIDR%s' % mm[0], typ='string')
		mc.setAttr('%s.vray_considerforaa_multimatte' % mmElement, 1)
		mmElement = mc.rename(mmElement, 'oIDR%s' % mm[0])
		try:
			mc.setAttr('%s.vray_greenid_multimatte' % mmElement, mm[1])
			mc.setAttr('%s.vray_name_multimatte' % mmElement, 'oIDR%sG%s' % (mm[0], mm[1]), typ='string')
			mmElement = mc.rename(mmElement, 'oIDR%sG%s' % (mm[0], mm[1]))
		except:
			mc.setAttr('%s.vray_greenon_multimatte' % mmElement, 0)
		try:
			mc.setAttr('%s.vray_blueid_multimatte' % mmElement, mm[2])
			mc.setAttr('%s.vray_name_multimatte' % mmElement, 'oIDR%sG%sB%s' % (mm[0], mm[1], mm[2]), typ='string')
			mmElement = mc.rename(mmElement, 'oIDR%sG%sB%s' % (mm[0], mm[1], mm[2]))
		except:
			mc.setAttr('%s.vray_blueon_multimatte' % mmElement, 0)

