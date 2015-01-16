import maya.cmds as mc
import maya.mel as mel

def negCol(enable=True):
	objLs = mc.ls(sl=True, l=True)
	for obj in objLs:
		if enable:
			mel.eval('vray addAttributesFromGroup %s vray_file_allow_neg_colors 1' % obj)
		else:
			mel.eval('vray addAttributesFromGroup %s vray_file_allow_neg_colors 0' % obj)
