import os
import maya.cmds as mc

#creates a product pack rig based on object selection

def createPackRig():
	#detecting and renaming conflicting nodes in scene
	nodeLs = ('GPS_packRig', 'GPS_packRig_bbox_condition', 'GPS_packRig_wireframe_condition')
	for node in nodeLs:
		if mc.objExists(node):
			mc.rename(node, '%s_' % node)
			
	rigHierarchy = '|GPS_packRig|transformA|transformA_offset|transformB|transformB_offset'
	rigScale = 0.5
	
	#getting selected object
	objLs = mc.ls(sl=True)
	if not objLs or len(objLs)>1:
		print 'Please select one item'
		return
	obj = objLs[0]
	#grouping selection
	objGrp = mc.group(obj, n='bbox_GRP')
	
	#importing pack rig. Getting bbox, shake and condition nodes
	packRigNodes = mc.file(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'maya', 'scripts', 'GPS_pack_rig.ma'), i=True, iv=True, rnn=True)
	packRigGrp = 'GPS_packRig'
	bboxNode = packRigNodes.index('|bbox'); bboxNode = packRigNodes[bboxNode]
	shakeNode = packRigNodes.index('%s|shake' % rigHierarchy); shakeNode = packRigNodes[shakeNode]
	bboxCondition = packRigNodes.index('GPS_packRig_bbox_condition'); bboxCondition= packRigNodes[bboxCondition]
	wireframeCondition = packRigNodes.index('GPS_packRig_wireframe_condition'); wireframeCondition = packRigNodes[wireframeCondition]
	
	#getting all selection's dependants and performing connections to rig
	allObjLs = mc.listRelatives(obj, ad=True, f=True, typ='transform')
	if allObjLs:
	    allObjLs.append(obj)
	else:
	    allObjLs = [obj]
	try:
	    for allObj in allObjLs:
		   allObjSh = mc.listRelatives(allObj, s=True)[0]
		   mc.setAttr('%s.overrideEnabled' % allObjSh, 1)
		   mc.setAttr('%s.overrideDisplayType' % allObjSh, 2)
		   mc.connectAttr('%s.outColorR' % bboxCondition, '%s.overrideLevelOfDetail' % allObjSh, f=True)
		   mc.connectAttr('%s.outColorR' % wireframeCondition, '%s.overrideShading' % allObjSh, f=True)
	except TypeError:
	    pass
	
	#getting obj bbox and pivot information
	mc.xform(objGrp, cp=True)
	objBbox = mc.xform(obj, bb=True, q=True)
	objrPivot = mc.xform(obj, rp=True, q=True)
	objSx = float(objBbox[3]) - float(objBbox[0])
	objSy = float(objBbox[4]) - float(objBbox[1])
	objSz = float(objBbox[5]) - float(objBbox[2])
	objBbox_largestLength = max(objSx, objSy, objSz) *  rigScale
	
	#getting objGrp bbox and pivot information in order to center scale the overall display bounding box
	visBbox = mc.xform(objGrp, bb=True, q=True)
	visBboxrPivot = mc.xform(objGrp, rp=True, q=True)
	visBboxSx = float(visBbox[3]) - float(visBbox[0])
	visBboxSy = float(visBbox[4]) - float(visBbox[1])
	visBboxSz = float(visBbox[5]) - float(visBbox[2])
	mc.xform(bboxNode, scale=[visBboxSx, visBboxSy, visBboxSz], a=True)
	mc.xform(bboxNode, translation=[visBboxrPivot[0], visBboxrPivot[1], visBboxrPivot[2]], a=True)
	mc.makeIdentity(bboxNode, s=True, t=True, a=True)
	
	#centering and scaling rig with obj.
	mc.xform(packRigGrp, scale=[objBbox_largestLength, objBbox_largestLength, objBbox_largestLength], a=True)
	mc.xform(packRigGrp, translation=[objrPivot[0], objrPivot[1], objrPivot[2]], a=True)
	
	#parenting bbox node to packRigGrp
	mc.parent(bboxNode, shakeNode, a=True)
	bboxNode = '%s|shake|bbox' % rigHierarchy
	
	#locking packRigGrp
	mc.setAttr('%s.scaleX' % packRigGrp, l=True)
	mc.setAttr('%s.scaleY' % packRigGrp, l=True)
	mc.setAttr('%s.scaleZ' % packRigGrp, l=True)
	mc.setAttr('%s.translateX' % packRigGrp, l=True)
	mc.setAttr('%s.translateY' % packRigGrp, l=True)
	mc.setAttr('%s.translateZ' % packRigGrp, l=True)
	
	#parenting obj to rig	
	mc.parent(objGrp, bboxNode, a=True)
	
	#renaming packrig group with obj name
	mc.rename(packRigGrp, '%s_%s' % (packRigGrp, obj))
