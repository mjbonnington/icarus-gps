#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:env__init__
#copyright	:Gramercy Park Studios

import os, platform, sys

def setEnv():
	os.environ['ICARUSVERSION'] = 'v0.7.1'
	icarusWorkingDir = os.path.dirname(os.path.realpath(__file__))
	icarusWorkingDir = icarusWorkingDir.replace('/core/ui', '')
	os.environ['PIPELINE'] = icarusWorkingDir
	os.environ['SHOTSROOTRELATIVEDIR'] = 'Vfx'
	os.environ['DATAFILESRELATIVEDIR'] = '.icarus'
	os.environ['JOBDATAFILE'] = 'jobData.py'
	os.environ['SHOTDATAFILE'] = 'shotData.py'
	if platform.system() == 'Darwin':
		os.environ['USERNAME'] = os.environ['USER']
	try:
		os.environ['ICARUSENVAWARE']
	except KeyError:
		os.environ['ICARUSENVAWARE'] = 'STANDALONE'
	appendSysPaths()
	
def appendSysPaths():
	icarusLibs = 'core/libs'
	icarusTools = 'core/tools'
	sys.path.append(os.environ['PIPELINE'])
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusTools, 'gpsPreview'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'gather'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'publish'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'scnMng'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'setJob'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'shared'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'py_modules'))
