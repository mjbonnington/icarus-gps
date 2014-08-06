import maya.cmds as mc
import maya.mel as mel
import verbose

################adds vray obj ids attr####################
def objID(single=False):
	allObjLs = mc.ls(tr=True, l=True)
	objLs = mc.ls(sl=True, l=True)
	newId = 1
	idLs = []
	if not objLs:
		verbose.noSel()
	for allObj in allObjLs:
		try:
			allObjSh = mc.listRelatives(allObj, s=True, f=True)[0]
			try:
				idLs.append(mc.getAttr('%s.vrayObjectID' % allObj))
			except:
				pass
		except TypeError:
			pass
	for obj in objLs:
		try:
			objSh = mc.listRelatives(obj, s=True, f=True)[0]
			if not mc.objExists('%s.vrayObjectID'% objSh):
				mel.eval('vrayAddAttr %s vrayObjectID' % objSh)
				while newId in idLs:
					newId += 1
				mc.setAttr('%s.vrayObjectID' % objSh, newId)
			if not single:
				newId += 1
		except TypeError:
			pass

###############creates vRay multimattes#################
def multiMatte(all=False):
	idLs = []
	if all:
		objLs = mc.ls(tr=True, l=True)
	else:
		objLs = mc.ls(sl=True, l=True)
	if not objLs:
		verbose.noSel()
	for obj in objLs:
		try:
			objSh = mc.listRelatives(obj, s=True, f=True)[0]
			idLs.append(mc.getAttr('%s.vrayObjectID' % objSh))
		except:
			pass
	idLs = list(set(idLs))
	idLs.sort()
	mmLs = [idLs[i:i+3] for i in range(0, len(idLs), 3)]
	for mm in mmLs:
		mm = list(set(mm))
		mm.sort()
		mmElement = mel.eval("vrayAddRenderElement MultiMatteElement")
		mc.setAttr('%s.vray_redid_multimatte' % mmElement, mm[0])
		mc.setAttr('%s.vray_name_multimatte' % mmElement, 'idR%s' % mm[0], typ='string')
		mc.setAttr('%s.vray_considerforaa_multimatte' % mmElement, 1)
		mmElement = mc.rename(mmElement, 'idR%s' % mm[0])
		try:
			mc.setAttr('%s.vray_greenid_multimatte' % mmElement, mm[1])
			mc.setAttr('%s.vray_name_multimatte' % mmElement, 'idR%sG%s' % (mm[0], mm[1]), typ='string')
			mmElement = mc.rename(mmElement, 'idR%sG%s' % (mm[0], mm[1]))
		except:
			mc.setAttr('%s.vray_greenon_multimatte' % mmElement, 0)
		try:
			mc.setAttr('%s.vray_blueid_multimatte' % mmElement, mm[2])
			mc.setAttr('%s.vray_name_multimatte' % mmElement, 'idR%sG%sB%s' % (mm[0], mm[1], mm[2]), typ='string')
			mmElement = mc.rename(mmElement, 'idR%sG%sB%s' % (mm[0], mm[1], mm[2]))
		except:
			mc.setAttr('%s.vray_blueon_multimatte' % mmElement, 0)


