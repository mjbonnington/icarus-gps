#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:mayaOps
#copyright	:Gramercy Park Studios


#maya operations module
import os, shutil
import maya.cmds as mc
import maya.mel as mel



####################applies tranforms#####################
def applyTransforms(obj, objT, objR, objS):
	try:
		mc.xform(obj, s=objS, ws=True)
		mc.xform(obj, ro=objR, ws=True)
		mc.xform(obj, t=objT, ws=True)
		return -1
	except TypeError:
		return

#########adds asset name tag as extra attr################
def assetTag(obj, assetName):
	refTag = mc.listAttr(obj, st='asset')
	if not refTag:
		mc.addAttr(obj, ln='asset', dt='string')
	mc.setAttr('%s.asset' % obj, l=False)
	mc.setAttr('%s.asset' % obj, assetName, typ='string', l=True)
	
###################adds asset type tag as extra attr#######
def assetExtTag(obj, assetExt):
	refTag = mc.listAttr(obj, st='assetExt')
	if not refTag:
		mc.addAttr(obj, ln='assetExt', dt='string')
	mc.setAttr('%s.assetExt' % obj, l=False)
	mc.setAttr('%s.assetExt' % obj, assetExt, typ='string', l=True)
	
###################adds asset type tag as extra attr#######
def assetTypeTag(obj, assetType):
	refTag = mc.listAttr(obj, st='IcAssetType')
	if not refTag:
		mc.addAttr(obj, ln='IcAssetType', dt='string')
	mc.setAttr('%s.IcAssetType' % obj, l=False)
	mc.setAttr('%s.IcAssetType' % obj, assetType, typ='string', l=True)

#######################bakes camera anim###################
def cameraBake(objLs, assetPblName):
	#if camera with publish name exists renames to *_old to bypass maya conflict
	if mc.objExists(assetPblName):
		mc.rename(assetPblName, '%s_old' % assetPblName)
	originalcamLs = [objLs[0]]
	originalcamShape = mc.listRelatives(originalcamLs[0], s=True, pa=True)
	newcamLs = mc.duplicate(originalcamLs[0], n=assetPblName, rc=True)
	newcam = assetPblName
	#placing new camera under world root
	if mc.listRelatives(assetPblName, p=True) != None:
		mc.parent(newcam, w=True)
	newcamShape = mc.listRelatives(newcam, s=True)
	minFrame = int(mc.playbackOptions(min=True, q=True))
	maxFrame = int(mc.playbackOptions(max=True, q=True))
	#unlocking new camera attr
	attrLs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz', '.fl']
	lockAttr([newcam], attrLs, lock=False, children=False)
	#deleting any existent constraints
	for newcamNode in newcamLs:
		if 'Constraint' in newcamNode:
			mc.delete(newcamNode)
	#creating parent constraint for new camera
	if mc.objExists('renderCamera_bake_parentCstrt'):
		mc.delete('renderCamera_bake_parentCstrt')
	mc.parentConstraint(originalcamLs[0], newcam, mo=False, n='renderCamera_bake_parentCstrt')
	#connecting bakable attributes
	attrBakeLs = ['.focalLength']
	for attrBake in attrBakeLs:
		mc.connectAttr(originalcamShape[0] + attrBake, newcamShape[0] + attrBake, f=True)
	#baking camera in world space
	mc.bakeResults(newcam, hi='both', s=True, dic=True, sm=True, time=(minFrame, maxFrame))
	#applying euler filter
	if mc.objExists(newcam + '_rotateX'):
		mc.filterCurve( newcam + '_rotateX')
	if mc.objExists(newcam + '_rotateY'):
		mc.filterCurve( newcam + '_rotateY')
	if mc.objExists(newcam + '_rotateZ'):
		mc.filterCurve( newcam + '_rotateZ')	
	mc.delete('renderCamera_bake_parentCstrt')
	return newcamLs

###################camera node check######################
def cameraNodeCheck(obj):
	try:
		objSh = mc.listRelatives(obj, s=True, pa=True)[0]
		if mc.nodeType(objSh) == 'camera':
			return 1
		else:
			return
	except (TypeError, RuntimeError):
		return
	
##########checks if obj is a icarus data set##############
def chkIcDataSet(obj=None):
	if not obj:
		obj = mc.ls(sl=True)
	if obj:
		if 'icRefTag' in mc.listAttr(obj):
			return obj
	return
###########adds asset requirement tag as extra attr#######
def compatibleTag(obj, compatibleTag):
	comptTag = mc.listAttr(obj, st='icAssetCompatibility')
	if not comptTag:
		mc.addAttr(obj, ln='icAssetCompatibility', dt='string')
	mc.setAttr('%s.icAssetCompatibility' % obj, l=False)
	mc.setAttr('%s.icAssetCompatibility' % obj, compatibleTag, typ='string', l=True)

######################creates lod system###################
def createLodSystem(objLs):
	lodsMasterGrp = objLs[0]
	attrLs = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
	lodsMasterGrp = mc.group(n='%s_lodsTmpMasterGRP' % objLs[0], em=True)
	#lodC
	lodC = generateLods(objLs, lodLvl='lodC', reduceIter=4)
	mc.parent(lodC, lodsMasterGrp)
	lockAttr([lodC], attrLs)
	#renameHrq(lodC, 'lodC')
	#lodB
	lodB = generateLods(objLs, lodLvl='lodB', reduceIter=2)
	mc.parent(lodB, lodsMasterGrp)
	lockAttr([lodB], attrLs)
	#renameHrq(lodB, 'lodB')
	#lodA
	lodA = mc.rename(objLs[0], '%s_lodA' % objLs[0])
	mc.parent(lodA, lodsMasterGrp)
	#lodsMaster			
	lodsMasterGrp = mc.rename(lodsMasterGrp, objLs[0])
	#creating lods visibility switch
	if not mc.objExists('%s.lod' % lodsMasterGrp):
		createVisibilitySwitch(lodsMasterGrp, [lodA, lodB, lodC])
	#deleting history
	deleteHist(objLs)
	return lodsMasterGrp

##################creates set for selection################
def createSet(setName, rm=False):
	if mc.objExists(setName):
		if rm:
			mc.lockNode(setName, lock=False)
			mc.rename(setName, '%s_' % setName)
		else:
			return
	newSet = mc.sets(n=setName)
	return newSet
	
###################connects lods visibility##################
def createVisibilitySwitch(masterGrp, slaveGrpLs):
	mc.select(masterGrp, r=True)
	mc.addAttr(ln="lod", at="enum", en="lodA:lodB:lodC:")
	lodAGrp, lodBGrp, lodCGrp = slaveGrpLs
	lodACndt = mc.shadingNode('condition', asUtility=True)
	lodBCndt = mc.shadingNode('condition', asUtility=True)
	lodCCndt = mc.shadingNode('condition', asUtility=True)
	cndtNodeLs = [lodACndt, lodBCndt, lodCCndt]
	cndtSecondTerm = 0
	for cndtNode in cndtNodeLs:
   		mc.setAttr('%s.colorIfTrueR' % cndtNode, 1)
   		mc.setAttr('%s.colorIfFalseR' % cndtNode, 0)
   		mc.setAttr('%s.secondTerm' % cndtNode, cndtSecondTerm)
   		cndtSecondTerm += 1
	mc.connectAttr('%s.lod' % masterGrp, '%s.firstTerm' % lodACndt)
	mc.connectAttr('%s.outColorR' % lodACndt, '%s.visibility' % lodAGrp)
	mc.connectAttr('%s.lod' % masterGrp, '%s.firstTerm' % lodBCndt)
	mc.connectAttr('%s.outColorR' % lodBCndt, '%s.visibility' % lodBGrp)
	mc.connectAttr('%s.lod' % masterGrp, '%s.firstTerm' % lodCCndt)
	mc.connectAttr('%s.outColorR' % lodCCndt, '%s.visibility' % lodCGrp)
	
	
#################decimates obj mesh###########################
def decimate(objLs, iterations=1):
	for obj in objLs:
		mc.select(obj, r=True)
		for i in range(0, iterations):
			mc.polyReduce(ver=1, trm=0, p=25, top=True, kqw=1, shp=0.5)
			
##################deletes channels############################
def deleteChannels(objLs, hierarchy=False):
	if hierarchy:
		for obj in objLs:
			mc.delete(obj, c=True, hi='None', cp=True, s=True)
	else:
		mc.delete(objLs[0], c=True, hi='None', cp=True, s=True)

##################deletes animation###########################
def deleteAnimation(objLs):
	try:
		objConn = mc.listConnections(allObj)
		for conn in objConn:
			connType = mc.nodeType(conn)
			if connType.startswith('animCurve'):
				mc.delete(conn)
	except TypeError:
		pass
		
#############deletes full or partial history##################
def deleteHist(objLs, partial=False):
	for obj in objLs:
		if partial:
			mc.bakePartialHistory(ppt=True )
		else:
			mc.delete(ch=True, c=True, e=True, cn=True)

			
###########deletes icSets connected to selection##############			
def deleteICDataSet(objLs):
	for obj in objLs:
			objShdLs = mc.listSets(ets=True, t=1, object=obj)
			if objShdLs:
				for objShd in objShdLs:
					if mc.objExists('%s.icARefTag' % objShd):
						mc.setAttr('%s.icARefTag' % objShd,l=False)
						mc.delete(mc.listConnections('%s.icARefTag' % objShd)[0])
						mc.deleteAttr('%s.icARefTag' % objShd)	
			if mc.objExists('%s.icARefTag' % obj):
				mc.setAttr('%s.icARefTag' % obj,l=False)
				try:
					mc.delete(mc.listConnections('%s.icARefTag' % obj)[0])
				except:
					pass
				mc.deleteAttr('%s.icARefTag' % obj)	
				
#############deletes imgPlane from camera#####################
def deleteIM(objLs):
	objLsShape = mc.listRelatives(objLs[0], s=True)
	connectionsLs = mc.listConnections(objLsShape[0])
	imPlane = ''
	#getting imgPlane
	if connectionsLs != None:
		for connection in connectionsLs:
			if mc.nodeType(connection) == 'imagePlane':
				imPlane = connection
	if imPlane != '':
		mc.delete(imPlane)

########################exports all#######################
def exportAll(pathToPblAsset, fileType):
	mc.file(pathToPblAsset, typ=fileType, f=True, ea=True)
	
##############exports animation curves via atom###########
def exportAnimation(pathToPblAsset, pblDir, objLs):
	mayaAppPath = os.path.split(os.environ['MAYAVERSION'])[0]
	plugin = os.path.join(mayaAppPath, 'plug-ins/atomImportExport.bundle')
	mc.loadPlugin(plugin, qt=True)
	startFr = mc.playbackOptions(min=True, q=True)
	endFr = mc.playbackOptions(max=True, q=True)
	mc.select(objLs[0], r=True)
	mc.file(pathToPblAsset,
	typ='atomExport',
	op="precision=8;statics=1;baked=0;sdk=1;constraint=1;animLayers=1;selected=childrenToo;whichRange=2;range=%s:%s;hierarchy=none;controlPoints=0;useChannelBox=1;options=keys;copyKeyCmd=-animation objects -time >%s:%s> -float >%s:%s> -option keys -hierarchy none -controlPoints 0" % (startFr, endFr, startFr, endFr, startFr, endFr),
	es=True,
	f=True)

#####################export geo types#####################
def exportGeo(objLs, geoType, pathToPblAsset):
	mayaAppPath = os.path.split(os.environ['MAYAVERSION'])[0]
	if geoType == 'abc':
		plugin = os.path.join(mayaAppPath, 'plug-ins/AbcExport.bundle')
		mc.loadPlugin(plugin, qt=True)
		minFrame = int(mc.playbackOptions(min=True, q=True))
		maxFrame = int(mc.playbackOptions(max=True, q=True))
		abcJob = '-fr %s %s -s 1 -uv -ws -ef -rt %s -f %s' % (minFrame, maxFrame, objLs[0], pathToPblAsset)
		mc.AbcExport(j=abcJob)
		return
	if geoType == 'vrmesh':
		objLs[0] = pathToPblAsset.split('/')[-1]
		pathToPblAsset = pathToPblAsset.split('/')[:-1]
		pathToPblAsset = '/'.join(pathToPblAsset)
		mel.eval('''vrayCreateProxy -exportType 1 -previewFaces 75000 -dir "%s" -fname "%s" -animOn -animType 1 
		-velocityOn -velocityIntervalStart 0.0 -velocityIntervalEnd 0.05;''' % (pathToPblAsset, objLs[0]))
		return
	if geoType == 'sd':
		plugin = os.path.join(os.environ['PIPELINE'], 'maya_rsc', 'plugins', 'realflow.bundle')
		mc.loadPlugin(plugin, qt=True)
		mc.realflow(exportSD=True, selected=True, usePlaybackRange=True, deformation=True, file=pathToPblAsset)
		return
	if geoType == 'obj':
		fileType = 'OBJexport'
		fileExtension = '.obj'
		plugin = os.path.join(mayaAppPath, 'plug-ins/objExport.bundle')
		fileOptions = 'groups=1;ptgroups=1;materials=0;smoothing=1;normals=1'
	elif geoType == 'fbx':
		fileType = 'FBX export'
		fileExtension = '.fbx'
		plugin = os.path.join(mayaAppPath, 'plug-ins/fbxmaya.bundle')
		fileOptions = 'v=0'
	mc.loadPlugin(plugin, qt=True)
	mc.select(objLs[0])
	mc.file(pathToPblAsset,
	op=fileOptions, 
	typ=fileType, 
	force=True, 
	es=True)


#################exports locators as nulls#################
def exportNulls(objSel, objLs, pathToPblAsset):
	nullLs = []
	nullCount = 1
	nullGrp =  mc.group(n='nullGrp_tmp', em=True)
	minFrame = int(mc.playbackOptions(min=True, q=True))
	maxFrame = int(mc.playbackOptions(max=True, q=True))
	for obj in objLs:
		if mc.nodeType(mc.listRelatives(obj, s=True)) == 'locator':
			null = mc.duplicate(obj, n='null_%s' % nullCount, ic=True)
			mc.parent(null, nullGrp)
			mc.bakeResults(null, hi='both', sm=True, s=True, dic=True, time=(minFrame, maxFrame))
			nullCount += 1
	mc.rename(objSel, '%s_tmp' % objSel)
	nullGrp = mc.rename(nullGrp, objSel)
	mc.select(nullGrp, r=True)
	mc.file(pathToPblAsset, typ='mayaAscii', es=True, f=True)
	mc.delete(nullGrp)	
	mc.rename('%s_tmp' % objSel, objSel)


##################exports selection#######################
def exportSelection(pathToPblAsset, fileType):
	mc.file(pathToPblAsset, typ=fileType, es=True, f=True)
	
####################freezes transforms####################
def freezeTrnsf(objLs):
	for obj in objLs:
		mc.select(obj, r=True)
		mc.makeIdentity(apply=True, t=True, r=True, s=True)
		
###########generates  a lower level of detail#############
def generateLods(objLs, lodLvl, reduceIter):
	mc.select(objLs[0])
	objLod = mc.duplicate(n='%s_%s' % (objLs[0], lodLvl), rr=True, rc=True)[0]
	allObjLs = mc.listRelatives(objLod, ad=True, typ='transform')
	for obj in allObjLs:
		try:
			mc.listRelatives(obj, s=True)[0]
			mc.select(obj, r=True)
			mel.eval('polyCleanupArgList 3 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","0" }')
			for i in range(0, reduceIter):
				mc.polyReduce(ver=1, trm=0, p=25, top=True, kqw=1, shp=0.5)
			mc.select(obj, r=True)
			mc.delete(ch=True, c=True, e=True, cn=True)
		except:
			pass
	return objLod

################gets current maya file####################
def getScene():
	actFile = mc.file(exn=True, q=True)
	return actFile


#########gets selected obj worldspace transforms##########
def getTransforms(obj):
	try:
		objSLs = mc.xform(obj, q=True, s=True, ws=True)
		objRLs = mc.xform(obj, q=True, ro=True, ws=True)
		objTLs = mc.xform(obj, q=True, t=True, ws=True)
		for i in range(len(objSLs)):
		    objSLs[i] = round(objSLs[i], 3)
		for i in range(len(objRLs)):
		    objRLs[i] = round(objRLs[i], 3)
		for i in range(len(objTLs)):
		    objTLs[i] = round(objTLs[i], 3)	
		return objTLs, objRLs, objSLs
	except:
		return

#groups manual lods in model and creates visibility switch#
def groupManualLods(objLs, lodA, lodB, lodC):
	lodsMasterGrp = objLs[0]
	if not lodA:
		return
	else:
		lodA = mc.rename(lodA, '%s_lodA' % objLs[0])
	if not lodB:
		lodB = mc.group(n='%s_lodB' % objLs[0], em=True)
		mc.parent(lodB, objLs[0])
	if not lodC:
		lodC = mc.group(n='%s_lodC' % objLs[0], em=True)
		mc.parent(lodC, objLs[0])
	#creating lods visibility switch
	if not mc.objExists('%s.lod' % lodsMasterGrp):
		createVisibilitySwitch(lodsMasterGrp, [lodA, lodB, lodC])
	#deleting history
	deleteHist(objLs)
	return lodsMasterGrp

#######################creates icarus data set#############
def icDataSet(obj, icData, update=None):
	#stores current selection
	currentSlLs = mc.ls(sl=True)
	if update:
		dataSet = update
	else:
		#clears current selection and selects all nodes gathered in objLs
		mc.select(cl=True)
		if mc.objExists(obj):
			mc.select(obj)
		#creates set with selection
		dataSet = createSet('ICSet_%s' % icData.assetPblName, rm=True)
	#adds ic data to set
	referenceTag(dataSet, icData.assetPblName)
	#assetTag(dataSet, icData.asset)
	assetTypeTag(dataSet, icData.assetType)
	#assetExtTag(dataSet, icData.assetExt)
	versionTag(dataSet, icData.version)
	#asset version compatibility tag
	try:
		compatibleTag(dataSet, icData.compatible)
	except AttributeError:
		pass

	notesTag(dataSet, icData.notes)
	#clears gather selection and restores original selection
	mc.select(cl=True)
	if currentSlLs:
		for currentSl in currentSlLs:
			mc.select(currentSl, add=True)
	return dataSet

########################imports referenced nodes#################
def importRefs(objLs):
	for obj in objLs: 
		if mc.referenceQuery(obj, inr=True):
			refFile = mc.referenceQuery(obj, f=True)
			mc.file(refFile, ir=True)
	
#################locks object attributes#####################
def lockAttr(objLs, attrLs, lock=True, children=True):
	for obj in objLs:
		if children:
			try:
				allObjLs = mc.listRelatives(obj, ad=True, typ='transform')
				allObjLs.append(obj)
			except:
				allObjLs = [obj]
		else:
			allObjLs = [obj]
		for allObj in allObjLs:
			for attr in attrLs:
				if lock:
					mc.setAttr(allObj + attr, lock=True)
				else:
					mc.setAttr(allObj + attr, lock=False)

###########################locks node########################
def lockNode(objLs, lock=True):
	for obj in objLs:
		if lock:
			mc.lockNode(obj, lock=True)
		else:
			mc.lockNode(obj, lock=False)

############checks if lods already exist in model############
def lodSystemCheck(objLs):
	lodA, lodB, lodC = None, None, None
	for child in mc.listRelatives(objLs[0], c=True):
		if 'loda' in child.lower():
			lodA = child
		elif 'lodb' in child.lower():
			lodB = child
		elif 'lodc' in child.lower():
			lodC = child
		else:
			return
	return lodA, lodB, lodC

################opens new maya scene######################
def newScene():
	mc.NewScene()
	update()

###################node type check########################
def nodetypeCheck(obj):
	nodeType_ = mc.nodeType(obj)
	return nodeType_

###############adds publish notes as custom attr##########
def notesTag(obj, pblNotes):
	notesAttr = mc.listAttr(obj, st='notes')
	if not notesAttr:
		mc.addAttr(obj, ln='notes', dt='string')
	mc.setAttr('%s.notes' % obj, l=False)
	mc.setAttr('%s.notes' % obj, pblNotes, typ='string', l=True)
	
###################opens maya file########################
def openScene(filePath, extension=None, dialog=True):
	if mel.eval('saveChanges("")'):
		if dialog:
			openFolder = mc.fileDialog2(ds=2, fm=1, ff=extension, dir=filePath, cap='Gramercy Park Studios - Open', okc='Open')
			if openFolder == None:
				return
		else:
			openFolder = [filePath]
		mc.file(openFolder[0], o=True, f=True, iv=True)

######parent constraints two identical hierarchies########
def parentCnstrHrq(obj1, obj2):
	hrq1 = mc.listRelatives(obj1, ad=True, typ='transform')
	hrq2 = mc.listRelatives(obj2, ad=True, typ='transform')
	for i in range(0, len(hrq1)):
		mc.parentConstraint(hrq1[i], hrq2[i])

##############redirects scene name and path###############
def redirectScene(sceneFile):
	mc.file(rn=sceneFile)

#####relinks cacheNode path and retrieves controlled geo######
def relinkCache(cacheLs, cachePath, asset, version):
	originalcachePath = mc.getAttr(cacheLs[0]+'.cachePath')
	if os.path.isdir(originalcachePath) == True:
		cacheFile_ls = os.listdir(originalcachePath)
		if len(cacheFile_ls) > 1:
			for cacheFile in cacheFile_ls:
				filePath = '%s/%s' % (originalcachePath, cacheFile)
				shutil.copy(filePath, cachePath)
			mc.setAttr(cacheLs[0]+'.cachePath', cachePath, type='string')
			mc.rename(cacheLs[0], asset  + '_%s' % version)
			
###############relinks camera imagePlane####################
def relinkImPlate(objLs, texturePath):
	objLsShape = mc.listRelatives(objLs[0], s=True)
	connectionsLs = mc.listConnections(objLsShape[0])
	imPath = ''
	#getting imgPlane path
	if connectionsLs != None:
		for connection in connectionsLs:
			if mc.nodeType(connection) == 'imagePlane':
				imPlane = connection
				imPath = mc.getAttr(imPlane + '.imageName')
	#copying img seq to publish path
	if imPath != '' :
		imPath = imPath.split('/')
		del imPath[-1]
		imPath = '/'.join(imPath)
		if os.path.isdir(imPath) == True:
			imFilesLs = os.listdir(imPath); imFilesLs.sort()
			for imFile in imFilesLs:
				copyFile = imPath + '/%s' % imFile
				imFile = imFile
				shutil.copy(copyFile, texturePath)
			mc.setAttr(imPlane + '.imageName', texturePath + '/%s' % imFile, type='string')

###################adds reference tag as extra attr#######
def referenceTag(obj, assetPblName):
	refTag = mc.listAttr(obj, st='icRefTag')
	if not refTag:
		mc.addAttr(obj, ln='icRefTag', dt='string')
	mc.setAttr('%s.icRefTag' % obj, l=False)
	mc.setAttr('%s.icRefTag' % obj, assetPblName, typ='string', l=True)

################relinks fileNode paths######################
def relinkTexture(txPaths, txObjLs=None, updateMaya=True, copy=True):
	txFullPath, txRelPath = txPaths
	if not txObjLs:
		fileNode = mc.itemFilter(byType='file')
		fileNodeLs = mc.lsThroughFilter(fileNode)
	else:
		txObjLsHist = mc.listHistory(txObjLs, f=True)
		txObjLsHist = list(set(txObjLsHist))
		txObjLsShd = mc.listHistory(txObjLsHist)
		txObjLsShd = list(set(txObjLsShd))
		fileNodeLs = mc.ls(txObjLsShd, type='file')
		fileNodeLs = list(set(fileNodeLs))
	if fileNodeLs:
		fileNodeLs = list(set(fileNodeLs))
		for fileNode in fileNodeLs:
			if not mc.getAttr('%s.useFrameExtension' % fileNode):
				filePath = mc.getAttr(fileNode + '.fileTextureName')
				#getting full path from mayaAttributes
				filePath = os.path.expandvars(filePath)
				if os.path.isfile(filePath):
					fileName = filePath.split('/')
					fileName = fileName.pop()
					if copy:
						shutil.copy(filePath, txFullPath)
					if updateMaya:
						#vray does not support relative path env vars in texures. Until this changes full path is written
						#mc.setAttr(fileNode + '.fileTextureName', '%s/%s' % (txRelPath, fileName), type='string')
						mc.setAttr(fileNode + '.fileTextureName', '%s/%s' % (txFullPath, fileName), type='string')

####################renames paired hierarchy###################
def renameHrq(hrq, suffix):
	hrq = mc.listRelatives(hrq, ad=True, typ='transform')
	for i in range(0, len(hrq)):
		mc.rename(hrq[i], '%s_%s' % (hrq[i], suffix))

####################renames objects in list####################
def renameObj(objLs, newName, oldName=False):
	for obj in objLs:
		if oldName:
			newName = obj.replace(oldName, newName)
		mc.rename(obj, newName)
		newName = ''
			
#####################saves maya file######################
def saveFile(fileType):
	if fileType == 'ma':
		fileType = 'mayaAscii'
	elif fileType == 'mb':
		fileType = 'mayaBinary'
	mc.file(op='v=0', f=True, s=True, typ=fileType)

###################saves maya file as#####################
def saveFileAs(filePath, extension):
	saveFolder = mc.fileDialog2(ds=2, fm=0, ff=extension, dir=filePath, cap='Gramercy Park Studios - Save As', okc='Save')
	if saveFolder == None:
		return
	else:
		fileType = saveFolder[0].split('.'); fileType = fileType.pop()
		if fileType == 'ma':
			fileType = 'mayaAscii'
		elif fileType == 'mb':
			fileType = 'mayaBinary'
			
		mc.file(rename=saveFolder[0])
		mc.file(op='v=0', f=True, s=True, typ=fileType)
		
################creates viewport snapshot##################
def snapShot(pblDir):
	pbFrame = mc.currentTime(q=True)
	mc.setAttr('defaultRenderGlobals.imageFormat', 8)
	#mc.viewFit(f=1)
	actSel=mc.ls(sl=True)
	mc.select(cl=True)
	mc.playblast(f='%s/preview' % (pblDir), 
	fr=(pbFrame), 
	fp=1, 
	w=255, 
	h=160, 
	p=100, 
	fmt='image',
	c='jpg',
	v=False, 
	os=True, 
	cc=True, 
	orn=False)
	mc.setAttr('defaultRenderGlobals.imageFormat', 7)
	##RESELECTING USER ORIGINAL SELECTION##
	for sel in actSel:
		mc.select(sel, add=True)

#################updates maya scene#######################
def update():
	startFrame = os.environ['STARTFRAME']
	endFrame = os.environ['ENDFRAME']
	timeFormat = os.environ['TIMEFORMAT']
	unit = os.environ['UNIT']
	angle = os.environ['ANGLE']

	#settings default for maya startup
	mc.optionVar(sv=('workingUnitAngular','%s' % angle))
	mc.optionVar(sv=('workingUnitAngularDefault','%s' % angle))
	mc.optionVar(sv=('workingUnitAngularHold','%s' % angle))
	mc.optionVar(sv=('workingUnitLinear','%s' % unit))
	mc.optionVar(sv=('workingUnitLinearDefault','%s' % unit))
	mc.optionVar(sv=('workingUnitLinearHold','%s' % unit))
	mc.optionVar(sv=('workingUnitTime','%s' % timeFormat))
	mc.optionVar(sv=('workingUnitTimeDefault','%s' % timeFormat))
	mc.optionVar(sv=('workingUnitTimeHold','%s' % timeFormat))
	mc.optionVar(fv = ('playbackMinRangeDefault',int(startFrame)))
	mc.optionVar(fv = ('playbackMinDefault',int(startFrame)))
	mc.optionVar(fv = ('playbackMaxRangeDefault',int(endFrame)))
	mc.optionVar(fv = ('playbackMaxDefault',int(endFrame)))
	mc.optionVar(sv = ('upAxisDirection','y'))
	mc.optionVar(sv = ('workingUnitLinear','%s' % unit))
	mc.optionVar(sv = ('workingUnitAngular','%s' % angle))
	mc.optionVar(sv = ('workingUnitTime','%s' % timeFormat))
	mc.currentUnit(l='%s' % unit, a='%s' % angle, t='%s' % timeFormat)	
	mc.playbackOptions(min=startFrame, 
	ast=startFrame, 
	max=endFrame, 
	aet=endFrame, 
	ps=0, 
	mps=1)

###################adds version tag as extra attr#########
def versionTag(obj, version):
	vTag = mc.listAttr(obj, st='icVersion')
	if not vTag:
		mc.addAttr(obj, ln='icVersion', dt='string')
	mc.setAttr('%s.icVersion' % obj, l=False)
	mc.setAttr('%s.icVersion' % obj, version, typ='string', l=True)

#########################.nk camera export####################
def nkCameraExport(objLs, pblDir, assetPblName, version):
	pathtoPblAsset = '%s/%s.nk' % (pblDir, assetPblName)
	objlsShape = mc.listRelatives(objLs[0], s=True)
	minFrame = int(mc.playbackOptions(min=True, q=True))
	maxFrame = int(mc.playbackOptions(max=True, q=True))
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile = open(pathtoPblAsset, 'w')
	nkFile.write('Camera {\n selectable false\n rot_order XYZ\n')
	#translation 
	#tx
	nkFile.write(' translate {{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    tx = str(mc.getAttr(objLs[0] + '.tx', t=currentFrame))
	    nkFile.write(' ' + tx)
	    currentFrame += 1
	nkFile.write('} ')
	#ty
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    ty = str(mc.getAttr(objLs[0] + '.ty', t=currentFrame))
	    nkFile.write(' ' + ty)
	    currentFrame += 1
	nkFile.write('} ')
	#tz
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    tz = str(mc.getAttr(objLs[0] + '.tz', t=currentFrame))
	    nkFile.write(' ' + tz)
	    currentFrame += 1
	nkFile.write('}}\n')
	#rotation
	#rx
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write(' rotate {{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    rx = str(mc.getAttr(objLs[0] + '.rx', t=currentFrame))
	    nkFile.write(' ' + rx)
	    currentFrame += 1
	nkFile.write('} ')
	#ry
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    ry = str(mc.getAttr(objLs[0] + '.ry', t=currentFrame))
	    nkFile.write(' ' + ry)
	    currentFrame += 1
	nkFile.write('} ')
	#rz
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write('{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    rz = str(mc.getAttr(objLs[0] + '.rz', t=currentFrame))
	    nkFile.write(' ' + rz)
	    currentFrame += 1
	nkFile.write('}}\n')
	#focal lenght
	mc.currentTime(minFrame)
	currentFrame = mc.currentTime(q=True)
	nkFile.write(' focal {{curve x%s' % minFrame)
	while currentFrame <= maxFrame:
	    fl = str(mc.getAttr(objlsShape[0] + '.fl', t=currentFrame))
	    nkFile.write(' ' + fl)
	    currentFrame += 1
	nkFile.write('}}\n')
	#horizontal and vertical apertures
	haperture = mc.getAttr(objlsShape[0] + '.horizontalFilmAperture')
	vaperture = mc.getAttr(objlsShape[0] + '.verticalFilmAperture')
	#maya's camera aperture settings are in inches and nuke mm. This needs to be converted.
	#converting aperture for inches to milimeters
	haperture = haperture * 25.4
	vaperture = vaperture * 25.4
	nkFile.write(' haperture %s' % haperture + '\n vaperture %s' % vaperture )
	#camera scale
	nkFile.write('\n win_scale {1 1}\n')
	#camera name and label
	nkFile.write(' name %s\n }' % assetPblName)
	nkFile.close()
	
	
