# GPS Common Tools
# v0.2
#
# Michael Bonnington 2014
# Gramercy Park Studios
#
# Contains a group of common functions used by various GPS tools

import string, re, math
import maya.cmds as mc
import maya.mel as mel
from maya.OpenMaya import MVector


def isMesh(obj):
	"""Return true if obj is a poly mesh
	This function may need to be rewritten to support node types other than
	transforms that can have shape nodes below them... needs research
	"""

	if mc.nodeType(obj) == "transform":
		shapeLs = mc.listRelatives(obj, shapes=True)
		if shapeLs == None:
			return False
		else:
			if mc.nodeType(shapeLs[0]) == "mesh":
				return True
			else:
				return False


def renameUnique(obj, newName, renameShapes="auto"):
	"""Rename obj as newName
	Works correctly, even if newName contains full path.
	Options for renaming shape nodes:
	'auto'  - Uses Maya's default strategy
	'force' - Force shape nodes to be renamed as 'newNameShape'
	'off'   - Shape nodes will not be renamed
	"""

	names = []

	# Set flags for shape node renaming behaviour
	ignoreShape = False
	if not renameShapes == "auto":
		ignoreShape = True

	# Split new name string after the last pipe character - allows non-unique child objects to be renamed correctly
	newNameTuple = newName.rpartition("|")

	# Rename shape node(s) if applicable - do this first otherwise shape node name might have been changed
	if renameShapes == "force":
		if mc.nodeType(obj) == "transform": # Fix this as it's not only transforms that have shape nodes
			shapeLs = mc.listRelatives(obj, shapes=True, fullPath=True)
			for shape in shapeLs:
				sn = mc.rename(shape, newNameTuple[2] + "Shape")
				names.append(sn)

	# Rename node
	tn = mc.rename(obj, newNameTuple[2], ignoreShape=ignoreShape)
	names[:0] = tn # work out a better way

	return names


def resetSelection(selOrig):
	"""Reset selection
	selOrig is a Python list defining the original set of selected items.
	"""

	try:
		mc.select(selOrig, replace=True)

	except (TypeError, ValueError, IndexError):
		mc.warning("No items selected.")


def distanceBetween(p, q):
	"""Return the distance between two points (vectors)
	The input vectors should be Python lists or tuples with 3 elements.
	"""

	v1 = MVector(*p)
	v2 = MVector(*q)
	v3 = v1-v2

	return v3.length()
	#return math.sqrt( (p[0] - q[0])**2 + (p[1] - q[1])**2 + (p[2] - q[2])**2 ) # Mathematical solution


def getVertexNormals(vertex):
	"""Returns a list of MVector objects for each normal associated with the
	specified vertex (one per attached face)
	"""

	mc.select(vertex, replace=True)
	n = mc.polyNormalPerVertex(query=True, xyz=True)
	normalLs = []
	for i in range(0, len(n), 3): # Pack returned values into a list of MVector objects
		normal = MVector(n[i], n[i+1], n[i+2])
		normalLs.append(normal)

	return normalLs


def averageNormals(normalLs, normalise):
	"""Return the average vector of a list of MVectors
	If normalise is true, return the normalised vector (length 1)
	"""

	sumX = sumY = sumZ = 0
	count = len(normalLs)
	for normal in normalLs:
		sumX += normal.x
		sumY += normal.y
		sumZ += normal.z
	avg = MVector(sumX / count, sumY / count, sumZ / count)

	if normalise:
		avg = avg.normal()

	return avg


def fractionalOffset(vertex, ws):
	"""Calculate the fractional offset
	Returns the distance between a specified vertex and its closest connected
	vertex.
	"""

	vtxLs = getSurroundingVertices(vertex)
	distLs = []
	for vtx in vtxLs:
		p = mc.pointPosition(vertex, local=not ws, world=ws)
		q = mc.pointPosition(vtx, local=not ws, world=ws)
		dist = distanceBetween(p, q)
		distLs.append(dist)

	return min(distLs)


def getSurroundingVertices(vertex):
	"""Return list of vertices directly connected to the specified vertex
	"""

	mc.select(vertex, replace=True)         # Select the vertex
	mel.eval("GrowPolygonSelectionRegion;") # Grow the selection
	mc.select(vertex, deselect=True)        # Remove the original vertex from the selection

	return mc.ls(selection=True, flatten=True)


def pluralise(noun):
	"""Pluralise nouns
	In the name of simplicity, this function is far from exhaustive.
	"""

	if re.search('[^fhms][ei]x$', noun):
		return re.sub('[ei]x$', 'ices', noun)
	elif re.search('[sxz]$', noun):
		return re.sub('$', 'es', noun)
	elif re.search('[^aeioudgkprt]h$', noun):
		return re.sub('$', 'es', noun)
	elif re.search('[^aeiou]y$', noun):
		return re.sub('y$', 'ies', noun)
	elif re.search('ies$', noun):
		return noun
	else:
		return noun + 's'


