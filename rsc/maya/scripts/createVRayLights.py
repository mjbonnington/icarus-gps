#!/usr/bin/python
#support  :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :createVRayLights
#copyright  :Gramercy Park Studios

import maya.cmds as mc


def create(lightNodeType, lightType):

  dialogResult = mc.promptDialog(
      title = 'Create Light',
      message = 'Light Name:',
      button = ['OK', 'Cancel'],
      defaultButton = 'OK', 
      cancelButton = 'Cancel',
      dismissString = 'Cancel')

  if dialogResult:
    lightName =  mc.promptDialog(text=True, q=True)

    if not lightName.endswith(lightType):
      lightName = '%s_%s' % (lightName, lightType)

    lightNode = mc.shadingNode(lightNodeType, asLight=True)
    
    #make viewport display larger
    mc.setAttr('%s.displayLocalAxis' % lightNode, 1)

    mc.select(lightNode, r=True)
    mc.rename(lightNode, lightName)
    return lightNode
  
  else:
    return