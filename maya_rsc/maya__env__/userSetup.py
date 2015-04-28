#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:userSetup.py
#copyright	:Gramercy Park Studios

import autoDeploy, maya.cmds as mc, os, sys
sys.path.append(os.path.join(os.environ['PIPELINE'], 'core', 'ui'))
#import icarus__main__, env__init__
import env__init__
env__init__.appendSysPaths()
os.environ['ICARUSENVAWARE'] = 'MAYA'
import mayaOps
#autodeploying maya tools and env files.
autoDeploy.deploy()

#loading default plugins
mayaAppPath = os.path.split(os.environ['MAYAVERSION'])[0]
ma_pluginLs = [
'AbcExport.bundle', 
'AbcImport.bundle',
'fbxmaya.bundle',
'objExport.bundle',
'OpenEXRLoader.bundle',
'tiffFloatReader.bundle']

for ma_plugin in ma_pluginLs:
	mc.loadPlugin(os.path.join(mayaAppPath, 'plug-ins', ma_plugin), qt=True)