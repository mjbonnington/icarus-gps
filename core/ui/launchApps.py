#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:launchApps
#copyright	:Gramercy Park Studios

import os, sys, subprocess
import verbose

def mari():
	verbose.launchApp('Mari')
	subprocess.Popen("$MARIVERSION", shell=True)

def maya():
	verbose.launchApp('Maya')
	subprocess.Popen("$MAYAVERSION -proj $SHOTPATH/3D/maya", shell=True)
	
def mudbox():
	verbose.launchApp('Mudbox')
	subprocess.Popen("$MUDBOXVERSION", shell=True)
	
def nuke(nukeType):
	verbose.launchApp(nukeType)
	if nukeType == 'Nuke':
		subprocess.Popen("$NUKEVERSION", shell=True)
	elif nukeType == 'NukeX':
		subprocess.Popen("$NUKEXVERSION", shell=True)

def terminal():
	subprocess.Popen("bash --rcfile %s" % os.environ['GPS_RC'], shell=True)

def prodBoard():
	subprocess.Popen('open %s' % os.environ['PRODBOARD'], shell=True)

def realflow():
	sys.path.append(os.path.join(os.environ['PIPELINE'], 'realflow_rsc', 'scripts'))
	import startup
	verbose.launchApp('Realflow')
	startup.autoDeploy()
	subprocess.Popen('"$REALFLOWVERSION"', shell=True)

	
def hieroPlayer():
	verbose.launchApp('HieroPlayer')
	subprocess.Popen("$HIEROPLAYERVERSION -q", shell=True)
		
	