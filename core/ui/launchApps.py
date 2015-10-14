#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :launchApps
#copyright  :Gramercy Park Studios

#Launches software applications


import os, sys, subprocess
import verbose, osOps

def mari():
	verbose.launchApp('Mari')
	subprocess.Popen('%s; "%s"' % (osOps.setUmask(), os.environ['MARIVERSION']), shell=True)

def maya():
	verbose.launchApp('Maya')
	subprocess.Popen('%s; "%s" -proj %s' % (osOps.setUmask(), os.environ['MAYAVERSION'], os.environ['MAYADIR']), shell=True)
	#subprocess.Popen("%s; $MAYAVERSION -proj %s" % (osOps.setUmask(), os.path.join('$SHOTPATH', '3D', 'maya')), shell=True)

def mudbox():
	verbose.launchApp('Mudbox')
	subprocess.Popen('%s; "%s"' % (osOps.setUmask(), os.environ['MUDBOXVERSION']), shell=True)

def nuke(nukeType):
	verbose.launchApp(nukeType)
	if nukeType in ('nuke', 'Nuke'):
		subprocess.Popen('%s; "%s"' % (osOps.setUmask(), os.environ['NUKEVERSION']), shell=True)
	elif nukeType in ('nukex', 'NukeX'):
		subprocess.Popen('%s; "%s" --nukex' % (osOps.setUmask(), os.environ['NUKEVERSION']), shell=True)
	elif nukeType in ('nukestudio', 'NukeStudio'):
		subprocess.Popen('%s; "%s" --studio' % (osOps.setUmask(), os.environ['NUKEVERSION']), shell=True)

def terminal():
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		subprocess.Popen("cmd /k %s" % os.environ['GPS_RC'], shell=True)
	else:
		subprocess.Popen("bash --rcfile %s" % os.environ['GPS_RC'], shell=True)

def prodBoard():
	#webbrowser.open(os.environ['PRODBOARD'], new=2, autoraise=True)
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		subprocess.Popen('open "%s"' % os.environ['PRODBOARD'], shell=True)
	elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		subprocess.Popen('explorer "%s"' % os.environ['PRODBOARD'], shell=True)
	else:
		subprocess.Popen('xdg-open "%s"' % os.environ['PRODBOARD'], shell=True)

def realflow():
	sys.path.append(os.path.join(os.environ['PIPELINE'], 'realflow_rsc', 'scripts'))
	import startup
	verbose.launchApp('RealFlow')
	startup.autoDeploy()
	subprocess.Popen('%s; "%s"' % (osOps.setUmask(), os.environ['REALFLOWVERSION']), shell=True)

def hieroPlayer():
	verbose.launchApp('HieroPlayer')
	subprocess.Popen('%s; "%s" -q' % (osOps.setUmask(), os.environ['HIEROPLAYERVERSION']), shell=True)

def djv():
	verbose.launchApp('djv_view')
	import djvOps
	djvOps.viewer()

def deadlineMonitor():
	verbose.launchApp('Deadline Monitor')
	subprocess.Popen('%s; "%s"' % (osOps.setUmask(), os.environ['DEADLINEMONITORVERSION']), shell=True)

def deadlineSlave():
	verbose.launchApp('Deadline Slave')
	subprocess.Popen('%s; "%s"' % (osOps.setUmask(), os.environ['DEADLINESLAVEVERSION']), shell=True)
