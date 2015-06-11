#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :userSetup.py
#copyright  :Gramercy Park Studios

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
ma_pluginLs = [
'AbcExport', 
'AbcImport',
'fbxmaya',
'objExport',
'OpenEXRLoader',
'tiffFloatReader']

for ma_plugin in ma_pluginLs:
	mc.loadPlugin(ma_plugin, qt=True)
