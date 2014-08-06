import os, re
import maya.cmds as mc
import maya.mel as mel


gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
filePath = "/Users/mikebonnington/Downloads/swissalti3dxyzlv03/2m/swissALTI3D_.xyz"

if os.path.isfile(filePath):
	xyzFile = open(filePath, 'r')
	xyzFileLine = xyzFile.readlines()
	mc.progressBar(gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=len(xyzFileLine)) # Initialise progress bar
#	pattern = re.compile("^X Y Z\s$")
#	if xyzFileLine[0] == "^X Y Z\s$":
	#xyzParticle = mc.particle(n="topo")
	for i in range(1, len(xyzFileLine)):
		x,y,z = xyzFileLine[i].split(" ")
		mc.xform("pPlane1.vtx[%d]" %(i-1), absolute=True, t=(float(x),float(y),float(z)), worldSpace=True)
		#mc.emit(object="topo", position=(float(x),float(y),float(z)))
		mc.progressBar(gMainProgressBar, edit=True, step=1, status="Working...") # Increment progress bar
#	else:
#		mc.error("Invalid format")
	mc.progressBar(gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
else:
	mc.error("File doesn't exist")
