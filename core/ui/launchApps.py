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
	
def nuke():
	verbose.launchApp('Nuke')
	subprocess.Popen("$NUKEVERSION", shell=True)

def terminal():
	gpsrc = "$PIPELINE/icarus/ui/.gps_rc"
	subprocess.Popen("bash --rcfile %s" % gpsrc, shell=True)

def trello():
	subprocess.Popen('open %s' % os.environ['TRELLOBOARD'], shell=True)

def realflow():
	sys.path.append(os.path.join(os.environ['PIPELINE'], 'realflow_rsc', 'scripts'))
	import startup
	verbose.launchApp('Realflow')
	startup.autoDeploy()
	subprocess.Popen('"$REALFLOWVERSION"', shell=True)

	
def hieroPlayer():
	verbose.launchApp('HieroPlayer')
	subprocess.Popen("$HIEROPLAYERVERSION -q", shell=True)
		
	