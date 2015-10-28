#creates an ocean surface. Accepts vray, maya and hot as ocean types
#Vray Ocean Type uses vRay water texture assign to a displacement slot with the shape node displacement options set to vector displacement
#Maya Ocean type uses an iDisplace node connected with a maya Ocean texture. This method allows to visualize the effect in the viewport in realtime
#Hot (Houdini ocean toolkit) ocean type is a plugin that needs to be compiled for each version of Maya. Currently not in use

import maya.cmds as mc
import maya.mel as mel

def createOcean(type):
	if type == 'hot':
		return
		#creating ocean geo
		#oceanGeo = mc.polyPlane(n='hot_oceanDeformer1', w=100, h=100, sx=100, sy=100, ax=(0,1,0), cuv=2, ch=1)
		#oceanGeoSh = mc.listRelatives(oceanGeo, s=True)
		#mel.eval('deformer -type hotOceanDeformer)
	elif type == 'vray':
		import vraySubDsMulti
		#creating ocean geo
		oceanGeo = mc.polyPlane(n='vray_oceanDeformer1', w=100, h=100, sx=30, sy=30, ax=(0,1,0), cuv=2, ch=1)
		oceanGeoSh = mc.listRelatives(oceanGeo, s=True)
		#creating vRay shader, water shader, shading group, making connections assiging to ocean geo
		shader = mc.shadingNode('VRayMtl', asShader=True)
		shadingGrp = mc.sets(n='%sSG' % shader, r=True, nss=True, em=True)
		vRayWater = mc.shadingNode('VRayWater', asTexture=True)
		mc.connectAttr('%s.outColor' % shader, '%s.surfaceShader' % shadingGrp, f=True)
		mc.connectAttr('%s.outColor' % vRayWater, '%s.displacementShader' % shadingGrp, f=True)
		mc.select(oceanGeo[0], r=True)
		mc.sets(forceElement=shadingGrp, e=True)
		#adding sub division and displacement properties to oceanGeo.
		vraySubDsMulti.subDivide(subDs = 4)
		mc.setAttr("%s.vrayDisplacementType" % oceanGeoSh[0], 2)
		#Multiplying vrayWater scale by 10
		mc.setAttr('%s.heightMult' % vRayWater, 10)
	elif type == 'maya':
		import maya.mel as mel
		#creating ocean geo
		oceanGeo = mc.polyPlane(n='maya_oceanDeformer1', w=100, h=100, sx=100, sy=100, ax=(0,1,0), cuv=2, ch=1)
		oceanGeoSh = mc.listRelatives(oceanGeo, s=True)
		mel.eval('loadPlugin -qt iDeform; iDisplace()')
		#getting oceanGeo connections and retrieving iDisplace node
		for connection in mc.listConnections(oceanGeoSh):
		  if mc.nodeType(connection) == 'iDisplace':
			 iDisplaceNode = connection
		#creating maya ocean texture and assigning it to the iDisplace node
		oceanTx = mc.shadingNode('ocean', asTexture=True)
		mc.connectAttr('%s.outColor' % oceanTx, '%s.texture' % iDisplaceNode)
		#ocean settings
		mc.setAttr('%s.scale' % iDisplaceNode, 10)
		mc.setAttr('%s.scale' % oceanTx, 15)
		mc.setAttr('%s.numFrequencies' % oceanTx, 25)
		mc.setAttr('%s.waveDirSpread' % oceanTx, 0.75)
		mc.setAttr('%s.waveLengthMin' % oceanTx, 0.25)
		mc.setAttr('%s.waveLengthMax' % oceanTx, 8)
		mc.expression(o=oceanTx, s='%s.time = time' % oceanTx, ae=1, uc=all)