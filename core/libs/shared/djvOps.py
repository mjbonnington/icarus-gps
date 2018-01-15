#!/usr/bin/python

# [Icarus] djvOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2017 Gramercy Park Studios
#
# djv_view operations module.


import os
import subprocess

import verbose


def exportDjvLibs():
	""" Export path to djv codec libraries according to OS.
	"""
	if os.environ['IC_RUNNING_OS'] == 'Darwin':
		libsExport = 'export DYLD_FALLBACK_LIBRARY_PATH=%s; ' % os.environ['DJV_LIB']
	elif os.environ['IC_RUNNING_OS'] == 'Linux':
		libsExport = 'export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s; ' % (os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'],'libquicktime'))
	else:
		libsExport = ''

	return libsExport


def prcImg(inBasename, outBasename, startFrame, endFrame, inExt, outExt='jpg', fps=os.environ['FPS'], resize=None):
	""" Processes image sequences.
	"""
	cmdInput = '%s.%s-%s.%s' % (inBasename, startFrame, endFrame, inExt)
	cmdOutput = '%s.%s.%s' % (outBasename, startFrame, outExt)

	# Export path to djv codec libraries according to OS
	djvCmd = exportDjvLibs()

	# Set up djv command
	if resize:
		djvCmd += '%s %s %s -resize %s %s -speed %s' % (os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], fps)
	else:
		djvCmd += '%s %s %s -speed %s' % (os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	verbose.print_(djvCmd, 4)
	os.system(djvCmd)


def prcQt(inBasename, outBasename, startFrame, endFrame, inExt, name='preview', fps=os.environ['FPS'], resize=None):
	""" Processes QuickTime movies.
	"""
	cmdInput = '%s.%s-%s.%s' % (inBasename, startFrame, endFrame, inExt)
	if name:
		cmdOutput = os.path.join(outBasename, '%s.mov' % name)
	else:
		cmdOutput = '%s.mov' % outBasename

	# Export path to djv codec libraries according to OS
	djvCmd = exportDjvLibs()

	# Set djv command
	if resize:
		djvCmd += '%s %s %s -resize %s %s -speed %s' % (os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], fps)
	else:
		djvCmd += '%s %s %s -speed %s' % (os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	verbose.print_(djvCmd, 4)
	os.system(djvCmd)


def viewer(path=None):
	""" Launch djv_view.
		If path is specified and is a file, automatically load sequence.
		If path is a directory, start in that directory.
		If path is not specified, use shot directory.
	"""
	cmdStr = ""

	# Get starting directory
	startupDir = os.environ['SHOTPATH']
	pathIsFile = False
	if path is not None:
		if os.path.isfile(path):
			startupDir = os.path.dirname(path)
			pathIsFile = True
		elif os.path.isdir(path):
			startupDir = path

	# Export path to djv codec libraries according to OS
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		cmdStr += 'cd /d "%s" & ' % startupDir
	elif os.environ['IC_RUNNING_OS'] == 'Darwin':
		cmdStr += "export DYLD_FALLBACK_LIBRARY_PATH=%s; " %os.environ['DJV_LIB']
		cmdStr += "cd %s; " % startupDir
	else:
		cmdStr += "export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s; " %(os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'],'libquicktime'))
		cmdStr += "cd %s; " % startupDir

	# Build the command based on whether path is a file or a directory
	if pathIsFile:
		cmdStr += '"%s" "%s"' %(os.environ['DJV_PLAY'], path)
	else:
		cmdStr += '"%s"' %os.environ['DJV_PLAY']

	# Call command with subprocess in order to not lock the system while djv
	# is running
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

