import maya.cmds as mc
import maya.mel as mel

def subDivide(subDs = 2):
	objLs = mc.ls(sl=True, l=True)
	for obj in objLs:
		objSh = mc.listRelatives(obj, s=True, f=True)[0]
		mel.eval('vray addAttributesFromGroup %s vray_subdivision 1' % objSh)
		mel.eval('vray addAttributesFromGroup %s vray_subquality 1' % objSh)
		mel.eval('vray addAttributesFromGroup %s vray_displacement 1' % objSh)
		mc.setAttr('%s.vrayMaxSubdivs' % objSh, subDs)