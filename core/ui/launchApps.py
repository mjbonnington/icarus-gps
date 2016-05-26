#!/usr/bin/python

# [Icarus] launchApps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Launches software applications.


import os, sys, subprocess
import verbose


def launch(app=None):
	""" Launch the specified application.
	"""
	execPath = ""
	cmdStr = ""

	# Build command string depending on app
	if app is None:
		execPath = ""
		cmdStr = ""

	elif app is 'Maya':
		execPath = os.environ['MAYAVERSION']
		cmdStr = '"%s" -proj "%s"' % (execPath, os.environ['MAYADIR'])

	elif app is 'Mudbox':
		execPath = os.environ['MUDBOXVERSION']
		cmdStr = '"%s"' % execPath

	elif app is 'Nuke':
		execPath = os.environ['NUKEVERSION']
		cmdStr = '"%s"' % execPath

	elif app is 'NukeX':
		execPath = os.environ['NUKEVERSION']
		cmdStr = '"%s" --nukex' % execPath

	elif app is 'NukeStudio':
		execPath = os.environ['NUKEVERSION']
		cmdStr = '"%s" --studio' % execPath

	elif app is 'Mari':
		execPath = os.environ['MARIVERSION']
		cmdStr = '"%s"' % execPath

	elif app is 'HieroPlayer':
		execPath = os.environ['HIEROPLAYERVERSION']
		cmdStr = '"%s" -q' % execPath

	elif app is 'RealFlow':
		execPath = os.environ['REALFLOWVERSION']
		sys.path.append(os.path.join(os.environ['PIPELINE'], 'rsc', 'realflow', 'scripts'))
		import startup
		startup.autoDeploy()
		cmdStr = '"%s"' % execPath

	elif app is 'DeadlineMonitor':
		execPath = os.environ['DEADLINEMONITORVERSION']
		cmdStr = '"%s"' % execPath

	elif app is 'DeadlineSlave':
		execPath = os.environ['DEADLINESLAVEVERSION']
		cmdStr = '"%s"' % execPath

	#elif app is 'djv_view':
	#	execPath = os.environ['DJVVERSION']
	#	import djvOps
	#	#djvOps.viewer(os.environ['SHOTPATH'])
	#	djvOps.viewer()
	#	cmdStr = '"%s"' % execPath

	# Check executable path is set and exists, and launch app
	if execPath:
		if os.path.isfile(execPath):
			verbose.launchApp(app)
			subprocess.Popen(cmdStr, shell=True)
		else:
			verbose.launchAppNotFound(app)
	else:
		verbose.launchAppNotSet(app)

	# Print debug output
	verbose.print_(cmdStr, 4)


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

