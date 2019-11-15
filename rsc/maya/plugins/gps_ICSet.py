import os
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

kNodeName = "ICSet"
kNodeId = OpenMaya.MTypeId(0x00122580)


# Node definition
class ICSet(OpenMayaMPx.MPxObjectSet):
	def __init__(self):
		OpenMayaMPx.MPxObjectSet.__init__(self)

# creator
def nodeCreator():
	return OpenMayaMPx.asMPxPtr(ICSet())

# initializer
def nodeInitializer():
	#Storing Attribute types
	icAsset = OpenMaya.MFnTypedAttribute()
	icRefTagAttr = OpenMaya.MFnTypedAttribute()
	icAssetTypeAttr = OpenMaya.MFnTypedAttribute()
	icVersionAttr = OpenMaya.MFnTypedAttribute()
	icAssetCompatibilityAttr = OpenMaya.MFnTypedAttribute()
	icAssetExtAttr = OpenMaya.MFnTypedAttribute()
	icNotesAttr = OpenMaya.MFnTypedAttribute()
	icAssetDisplayAttr = OpenMaya.MFnEnumAttribute()
	overrideComponentDisplayAttr = OpenMaya.MFnNumericAttribute()
	overrideComponentColorAttr = OpenMaya.MFnNumericAttribute()
	#Creating attributes
	ICSet.icAsset = icRefTagAttr.create("icAsset", "asset", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.icAsset)
	ICSet.icRefTag = icRefTagAttr.create("icRefTag", "tag", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.icRefTag)
	ICSet.icAssetType = icAssetTypeAttr.create("icAssetType", "type", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.icAssetType)
	ICSet.icVersion = icVersionAttr.create("icVersion", "version", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.icVersion)
	ICSet.icAssetCompatibility = icAssetCompatibilityAttr.create("icAssetCompatibility", "compatibility", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.icAssetCompatibility)
	ICSet.icAssetExt = icAssetExtAttr.create("icAssetExt", "ext", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.icAssetExt)
	ICSet.notes = icNotesAttr.create("Notes", "notes", OpenMaya.MFnData.kString)
	ICSet.addAttribute(ICSet.notes)
	ICSet.ICAssetDisplay = icAssetDisplayAttr.create("icAssetDisplay", "icAssetDisplay")
	icAssetDisplayAttr.addField("bbox", 0)
	icAssetDisplayAttr.addField("wireframe", 1)
	icAssetDisplayAttr.addField("full", 2)
	ICSet.addAttribute(ICSet.ICAssetDisplay)
	ICSet.overrideComponentDisplay = overrideComponentDisplayAttr.create("overrideComponentDisplay", "overrideComponentDisplay", OpenMaya.MFnNumericData.kBoolean)
	ICSet.addAttribute(ICSet.overrideComponentDisplay)
	ICSet.overrideComponentColor = overrideComponentColorAttr.create("overrideComponentColor", "overrideComponentColor", OpenMaya.MFnNumericData.kInt, 26)
	ICSet.addAttribute(ICSet.overrideComponentColor)

# initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, os.environ['IC_VENDOR'], "1.0", "Any")
	try:
		mplugin.registerNode(kNodeName, kNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kObjectSet)
	except:
		sys.stderr.write("Failed to register node: %s" % kNodeName)
		raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(kNodeId)
	except:
		sys.stderr.write("Failed to deregister node: %s" % kNodeName)
		raise
