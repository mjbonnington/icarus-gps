#!/usr/bin/python

# [Icarus] launchApps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# Launches software applications.
# This module will be deprecated soon.


import os
import subprocess
import sys

from . import verbose


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
		# os.environ['PYTHONPATH'] = os.environ['MAYA_SCRIPT_PATH']
		executable = os.environ['IC_MAYA_EXECUTABLE']
		cmdStr = '"%s" -proj "%s"' %(executable, os.environ['IC_MAYA_PROJECT_DIR'])

	# elif app == 'Nuke':
	# 	# Workaround to allow Nuke 11 to launch correctly by deleting
	# 	# PYTHONPATH environment variable
	# 	try:
	# 		os.environ.pop('PYTHONPATH')
	# 		verbose.message("Deleted 'PYTHONPATH' environment variable.")
	# 	except KeyError:
	# 		pass
	# 	cmdStr = '"%s"' % executable

	elif app == 'Bridge':
		executable = os.environ['IC_BRIDGE_EXECUTABLE']
		cmdStr = '"%s" "%s"' %(executable, os.environ['IC_SHOTPATH'])

	elif app == 'HieroPlayer':
		try:
			executable = os.environ['IC_HIEROPLAYER_EXECUTABLE']
			cmdStr = '"%s"' %executable
		except KeyError:
			# Hiero Player is bundled with Nuke 9.x and later.
			executable = os.environ['IC_NUKE_EXECUTABLE']
			cmdStr = '"%s" --player' %executable

	elif app == 'RealFlow':
		executable = os.environ['IC_REALFLOW_EXECUTABLE']
		sys.path.append(os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'realflow', 'scripts'))
		import startup
		startup.autoDeploy()
		if os.environ['IC_RUNNING_OS'] == 'Windows':
			# Workaround to prevent RealFlow closing the shell on launch
			dirname, basename = os.path.split(executable)
			cmdStr = 'cd /d "%s" & start %s' %(dirname, basename)
		else:
			cmdStr = '"%s"' %executable

	elif app == 'djv_view':
		djv()
		return

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
	from . import djvOps
	# djvOps.viewer(os.environ['IC_SHOTPATH'])
	djvOps.viewer()


def terminal():
	""" Launch the terminal / command prompt.
	"""
	if os.environ['IC_RUNNING_OS'] == "Windows":
		# subprocess.Popen("cmd /k %s" % os.environ['IC_SHELL_RC'], shell=True)
		subprocess.Popen("start cmd /k %s" %os.environ['IC_SHELL_RC'], shell=True)
	else:
		subprocess.Popen("bash --rcfile %s" %os.environ['IC_SHELL_RC'], shell=True)


def prodBoard():
	""" Launch the production board URL in a web browser.
	"""
	# webbrowser.open(os.environ['IC_PRODUCTION_BOARD'], new=2, autoraise=True)
	if os.environ['IC_RUNNING_OS'] == "Windows":
		subprocess.Popen('explorer "%s"' %os.environ['IC_PRODUCTION_BOARD'], shell=True)
	elif os.environ['IC_RUNNING_OS'] == "MacOS":
		subprocess.Popen('open "%s"' %os.environ['IC_PRODUCTION_BOARD'], shell=True)
	else:
		subprocess.Popen('xdg-open "%s"' %os.environ['IC_PRODUCTION_BOARD'], shell=True)

