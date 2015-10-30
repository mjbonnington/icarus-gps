import maya.cmds as mc
import maya.mel as mel

def lightSelPass():
    
    objLs = mc.ls(sl=True)
    
    if not objLs:
        print '\nNo lights selected'
        return
    
    pDialog = mc.promptDialog(
		title='Light Pass',
		message='Light Pass Name:',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')

    if pDialog == 'OK':
        lightPassName = mc.promptDialog(text=True, q=True)
        lightPassSet = mel.eval("vrayAddRenderElement LightSelectElement")
        for obj in objLs:
            mc.sets(obj, forceElement=lightPassSet, e=True)
        mc.setAttr('%s.vray_name_lightselect' % lightPassSet, '%s_lightSel' % lightPassName, type='string')
        mc.rename(lightPassSet, '%s_vrayRE_Light_Select' % lightPassName)