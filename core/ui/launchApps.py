#!/usr/bin/python

# [Icarus] launchApps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2015 Gramercy Park Studios
#
# Launches software applications.


import os, sys, subprocess
import verbose, osOps


def maya():
	verbose.launchApp('Maya')
	cmdStr = '%s; "%s" -proj %s' % (osOps.setUmask(), os.environ['MAYAVERSION'], os.environ['MAYADIR'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def mudbox():
	verbose.launchApp('Mudbox')
	cmdStr = '%s; "%s"' % (osOps.setUmask(), os.environ['MUDBOXVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def mari():
	verbose.launchApp('Mari')
	cmdStr = '%s; "%s"' % (osOps.setUmask(), os.environ['MARIVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def hieroPlayer():
	verbose.launchApp('HieroPlayer')
	cmdStr = '%s; "%s" -q' % (osOps.setUmask(), os.environ['HIEROPLAYERVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def deadlineMonitor():
	verbose.launchApp('Deadline Monitor')
	cmdStr = '%s; "%s"' % (osOps.setUmask(), os.environ['DEADLINEMONITORVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def deadlineSlave():
	verbose.launchApp('Deadline Slave')
	cmdStr = '%s; "%s"' % (osOps.setUmask(), os.environ['DEADLINESLAVEVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def nuke(nukeType):
	verbose.launchApp(nukeType)
	if nukeType in ('nuke', 'Nuke'):
		cmdStr = '%s; "%s"' % (osOps.setUmask(), os.environ['NUKEVERSION'])
	elif nukeType in ('nukex', 'NukeX'):
		cmdStr = '%s; "%s" --nukex' % (osOps.setUmask(), os.environ['NUKEVERSION'])
	elif nukeType in ('nukestudio', 'NukeStudio'):
		cmdStr = '%s; "%s" --studio' % (osOps.setUmask(), os.environ['NUKEVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def realflow():
	sys.path.append(os.path.join(os.environ['PIPELINE'], 'rsc', 'realflow', 'scripts'))
	import startup
	verbose.launchApp('RealFlow')
	startup.autoDeploy()
	cmdStr = '%s; "%s"' % (osOps.setUmask(), os.environ['REALFLOWVERSION'])
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

def djv():
	verbose.launchApp('djv_view')
	import djvOps
	#djvOps.viewer(os.environ['SHOTPATH'])
	djvOps.viewer()

def terminal():
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		#subprocess.Popen("cmd /k %s" % os.environ['GPS_RC'], shell=True)
		subprocess.Popen("start cmd /k %s" % os.environ['GPS_RC'], shell=True)
	else:
		subprocess.Popen("bash --rcfile %s" % os.environ['GPS_RC'], shell=True)

def prodBoard():
	#webbrowser.open(os.environ['PRODBOARD'], new=2, autoraise=True)
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		subprocess.Popen('explorer "%s"' % os.environ['PRODBOARD'], shell=True)
	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		subprocess.Popen('open "%s"' % os.environ['PRODBOARD'], shell=True)
	else:
		subprocess.Popen('xdg-open "%s"' % os.environ['PRODBOARD'], shell=True)
