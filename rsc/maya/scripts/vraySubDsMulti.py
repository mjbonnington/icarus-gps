import maya.cmds as mc
import maya.mel as mel

def subDivide(subDs = 2):
	""" Add V-Ray subdivision and displacement attributes to selected meshes.
		TODO: Add appropriate presets for data from ZBrush, Mudbox, etc.
	"""
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
