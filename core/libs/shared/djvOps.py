#!/usr/bin/python

# [Icarus] djvOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# djv_view operations module.


import os, subprocess
import verbose


def prcImg(input, output, startFrame, endFrame, inExt, outExt='jpg', fps=os.environ['FPS'], resize=None):
	""" Processes image sequences.
	"""
	cmdInput = '%s.%s-%s.%s' % (input, startFrame, endFrame, inExt)
	cmdOutput = '%s.%s.%s' % (output, startFrame, outExt)

	#exporting path to djv codec libraries according to os
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		libsExport = 'export DYLD_FALLBACK_LIBRARY_PATH=%s' % os.environ['DJV_LIB']
	elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		libsExport = ''
	else:
		libsExport = 'export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s' % (os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'],'libquicktime'))

	#setting djv command
	if resize:
		djvCmd = '%s; %s %s %s -resize %s %s -speed %s' % (libsExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], fps)
	else:
		djvCmd = '%s; %s %s %s -speed %s' % (libsExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	os.system(djvCmd)


def prcQt(input, output, startFrame, endFrame, inExt, name='preview', fps=os.environ['FPS'], resize=None):
	""" Processes QuickTime movies.
	"""
	cmdInput = '%s.%s-%s.%s' % (input, startFrame, endFrame, inExt)
	if name:
		cmdOutput = os.path.join(output, '%s.mov' % name)
	else:
		cmdOutput = '%s.mov' % output

	#exporting path to djv codec libraries according to os
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		libsExport = 'export DYLD_FALLBACK_LIBRARY_PATH=%s' % os.environ['DJV_LIB']
	elif os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		libsExport = ''
	else:
		libsExport = 'export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s' % (os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'],'libquicktime'))

	#setting djv command
	if resize:
		djvCmd = '%s; %s %s %s -resize %s %s -speed %s' % (libsExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], fps)
	else:
		djvCmd = '%s; %s %s %s -speed %s' % (libsExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	os.system(djvCmd)


def viewer(path=None):
	""" Launch djv_view.
		If path is specified and is a file, automatically load sequence.
		If path is a directory, start in that directory.
		If path is not specified, use shot directory.
	"""
	cmdStr = ""

	# Get starting directory
	pathIsFile = False
	if path is None:
		startupDir = os.environ['SHOTPATH']
	else:
		if os.path.isfile(path):
			startupDir = os.path.dirname(path)
			pathIsFile = True
		elif os.path.isdir(path):
			startupDir = path

	# Export path to djv codec libraries according to OS
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		cmdStr += "cd /d %s & " % startupDir
	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		cmdStr += "export DYLD_FALLBACK_LIBRARY_PATH=%s; " %os.environ['DJV_LIB']
		cmdStr += "cd %s; " % startupDir
	else:
		cmdStr += "export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s; " %(os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'],'libquicktime'))
		cmdStr += "cd %s; " % startupDir

	# Build the command based on whether path is a file or a directory
	if pathIsFile:
		cmdStr += "%s %s" %(os.environ['DJV_PLAY'], path)
	else:
		cmdStr += os.environ['DJV_PLAY']

	# Call command with subprocess in order to not lock the system while djv is running
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

