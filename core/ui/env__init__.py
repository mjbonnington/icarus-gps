#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:env__init__
#copyright	:Gramercy Park Studios

#Initializes main pipeline environment

import os, platform, sys

def setEnv():
	os.environ['ICARUSVERSION'] = 'v0.7.8'
	icarusWorkingDir = os.path.dirname(os.path.realpath(__file__))
	os.environ['ICWORKINGDIR'] = icarusWorkingDir
	icarusUIDir = os.path.join('core', 'ui')
	os.environ['PIPELINE'] = icarusWorkingDir.replace(icarusUIDir, '')
	os.environ['ICCONFIGDIR'] = os.path.join(os.environ['PIPELINE'], 'core', 'config')
	os.environ['SHOTSROOTRELATIVEDIR'] = 'Vfx'
	os.environ['DATAFILESRELATIVEDIR'] = '.icarus'
	os.environ['JOBDATAFILE'] = 'jobData.py'
	os.environ['SHOTDATAFILE'] = 'shotData.py'
	if platform.system() == 'Darwin':
		os.environ['ICARUS_RUNNING_OS'] = 'Darwin'
		os.environ['USERNAME'] = os.environ['USER']
	else:
		os.environ['ICARUS_RUNNING_OS'] = 'Linux'
	try:
		os.environ['ICARUSENVAWARE']
	except KeyError:
		os.environ['ICARUSENVAWARE'] = 'STANDALONE'
	appendSysPaths()

def appendSysPaths():
	icarusLibs = os.path.join('core', 'libs')
	icarusTools = os.path.join('core', 'tools')
	sys.path.append(os.environ['PIPELINE'])
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusTools, 'gpsPreview'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'gather'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'publish'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'scnMng'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'setJob'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'shared'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'py_modules'))
