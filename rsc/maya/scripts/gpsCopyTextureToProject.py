import maya.cmds as mc
import os
import osOps

selLs = mc.ls(sl=1)

for fileNode in selLs:
	if mc.nodeType(fileNode) == 'file':
		srcpath = mc.getAttr(fileNode+".fileTextureName")
		srcdir, srcfile = os.path.split(srcpath)
		dstpath = osOps.absolutePath("$MAYASOURCEIMAGESDIR/%s" %srcfile)
		mayaproj = os.environ['MAYADIR']+"/"
		dstrelpath = dstpath.split(mayaproj)[1]

		osOps.copy(srcpath, dstpath)
		mc.setAttr(fileNode+".fileTextureName", dstrelpath, type='string')
