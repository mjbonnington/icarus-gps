#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :env__init__
#copyright  :Gramercy Park Studios

#Initializes main pipeline environment

import os, platform, sys

def setEnv():
	if platform.system() == 'Darwin':
		os.environ['ICARUS_RUNNING_OS'] = 'Darwin'
		os.environ['USERNAME'] = os.environ['USER']
	elif platform.system() == 'Windows':
		os.environ['ICARUS_RUNNING_OS'] = 'Windows'
	else:
		os.environ['ICARUS_RUNNING_OS'] = 'Linux'
	try:
		os.environ['ICARUSENVAWARE']
	except KeyError:
		os.environ['ICARUSENVAWARE'] = 'STANDALONE'

	os.environ['ICARUSVERSION'] = 'v0.8.7-20150604'
	icarusWorkingDir = os.path.dirname(os.path.realpath(__file__))
	os.environ['ICWORKINGDIR'] = icarusWorkingDir
	icarusUIDir = os.path.join('core', 'ui')
	os.environ['PIPELINE'] = icarusWorkingDir.replace(icarusUIDir, '')
	os.environ['ICCONFIGDIR'] = os.path.join(os.environ['PIPELINE'], 'core', 'config')
	os.environ['ICUSERPREFS'] = os.path.join(os.environ['ICCONFIGDIR'], 'users', os.environ['USERNAME']) # User prefs stored on server
	#os.environ['ICUSERPREFS'] = os.path.join(os.environ['HOME'], '.icarus') # User prefs stored in user home folder

	os.environ['SHOTSROOTRELATIVEDIR'] = 'Vfx'
	os.environ['DATAFILESRELATIVEDIR'] = '.icarus'
	#os.environ['JOBDATAFILE'] = 'jobData' # Change when data is stored as XML
	#os.environ['SHOTDATAFILE'] = 'shotData' # Change when data is stored as XML
	appendSysPaths()

def appendSysPaths():
	icarusLibs = os.path.join('core', 'libs')
	icarusTools = os.path.join('core', 'tools')
	sys.path.append(os.environ['PIPELINE'])
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusTools, 'icAdmin'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusTools, 'gpsSubmit'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusTools, 'gpsPreview'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'ui'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'gather'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'publish'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'scnMng'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'setJob'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'shared'))
	sys.path.append(os.path.join(os.environ['PIPELINE'], icarusLibs, 'py_modules'))
