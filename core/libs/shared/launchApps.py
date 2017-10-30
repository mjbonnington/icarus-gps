#!/usr/bin/python

# [Icarus] launchApps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Launches software applications.


import os
import subprocess
import sys

import verbose


def launch(app=None, executable=None, flags=None):
	""" Launch the specified application.
	"""
	cmdStr = ""

	# Build command string depending on app...
	if app is None:
		# executable = ""
		cmdStr = ""

	###################################
	# Special cases for specific apps #
	###################################

	elif app == 'Maya':
		executable = os.environ['MAYAVERSION']
		cmdStr = '"%s" -proj "%s"' %(executable, os.environ['MAYADIR'])

	elif app == 'Bridge':
		executable = os.environ['BRIDGEVERSION']
		cmdStr = '"%s" "%s"' %(executable, os.environ['SHOTPATH'])

	elif app == 'HieroPlayer':
		executable = os.environ['HIEROPLAYERVERSION']
		if executable:
			cmdStr = '"%s"' %executable
		else:
			# Hiero Player is bundled with Nuke 9.x and later.
			executable = os.environ['NUKEVERSION']
			cmdStr = '"%s" --player'% executable

	elif app == 'RealFlow':
		executable = os.environ['REALFLOWVERSION']
		sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'realflow', 'scripts'))
		import startup
		startup.autoDeploy()
		if os.environ['IC_RUNNING_OS'] == 'Windows':
			# Workaround to prevent RealFlow closing the shell on launch
			dirname, basename = os.path.split(executable)
			cmdStr = 'cd /d "%s" & start %s' %(dirname, basename)
		else:
			cmdStr = '"%s"' %executable

	###############
	# Generic app #
	###############

	else:
		cmdStr = '"%s"' %executable

	#######
	# End #
	#######

	if flags:
		cmdStr += " %s" %flags

	# Check executable path is set and exists, and launch app.
	if executable:
		if os.path.isfile(executable):
			verbose.launchApp(app)
			subprocess.Popen(cmdStr, shell=True)
		else:
			verbose.launchAppNotFound(app)
	else:
		verbose.launchAppNotSet(app)

	# Print debug output.
	verbose.print_(cmdStr, 4)


def djv():
	""" Launch djv_view.
		Note this is a special case due to djv_view being required by many
		internal functions and is therefore the app is bundled with Icarus,
		in the 'external_apps' folder.
	"""
	verbose.launchApp('djv_view')
	import djvOps
	# djvOps.viewer(os.environ['SHOTPATH'])
	djvOps.viewer()


def terminal():
	""" Launch the terminal / command prompt.
	"""
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		# subprocess.Popen("cmd /k %s" % os.environ['IC_SHELL_RC'], shell=True)
		subprocess.Popen("start cmd /k %s" %os.environ['IC_SHELL_RC'], shell=True)
	else:
		subprocess.Popen("bash --rcfile %s" %os.environ['IC_SHELL_RC'], shell=True)


def prodBoard():
	""" Launch the production board URL in a web browser.
	"""
	# webbrowser.open(os.environ['PRODBOARD'], new=2, autoraise=True)
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		subprocess.Popen('explorer "%s"' %os.environ['PRODBOARD'], shell=True)
	elif os.environ['IC_RUNNING_OS'] == 'Darwin':
		subprocess.Popen('open "%s"' %os.environ['PRODBOARD'], shell=True)
	else:
		subprocess.Popen('xdg-open "%s"' %os.environ['PRODBOARD'], shell=True)

