import maya.cmds as mc
import os
from core import os_wrapper

selLs = mc.ls(sl=1)

for fileNode in selLs:
	if mc.nodeType(fileNode) == 'file':
		srcpath = mc.getAttr(fileNode+".fileTextureName")
		srcdir, srcfile = os.path.split(srcpath)
		dstpath = os_wrapper.absolutePath("$MAYASOURCEIMAGESDIR/%s" %srcfile)
		mayaproj = os.environ['MAYADIR']+"/"
		dstrelpath = dstpath.split(mayaproj)[1]

		os_wrapper.copy(srcpath, dstpath)
		mc.setAttr(fileNode+".fileTextureName", dstrelpath, type='string')
