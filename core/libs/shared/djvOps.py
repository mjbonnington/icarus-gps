#!/usr/bin/python

# [Icarus] djvOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2018 Gramercy Park Studios
#
# djv_view operations module.


import os
import subprocess

import verbose


def exportDjvLibs():
	""" Export path to djv codec libraries according to OS.
	"""
	if os.environ['IC_RUNNING_OS'] == 'Darwin':
		libsExport = "export DYLD_FALLBACK_LIBRARY_PATH=%s; " %os.environ['DJV_LIB']
	elif os.environ['IC_RUNNING_OS'] == 'Linux':
		libsExport = "export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s; " %(os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'], "libquicktime"))
	else:
		libsExport = ""

	return libsExport


def processSpeed(arg, fps=None):
	""" Process playback speed string.
		'arg' is the name of the argument to pass to djv_view. This can be
		"speed" or "playback_speed" depending on the command.
		'fps' is a float value representing the frames per second. If not
		specified, get value from shot settings.
	"""
	valid_fps = [1, 3, 6, 12, 15, 16, 18, 23.976, 24, 25, 29.97, 30, 50, 59.94, 60, 120]

	if fps is None:
		fps = float(os.environ.get('FPS', '25'))
	if fps == int(fps):
		fps = int(fps)  # Convert to integer if it can be represented as such
	if fps in valid_fps:
		#print(type(fps), fps)
		actual_fps = fps
	else:
		actual_fps = min(valid_fps, key=lambda x:abs(x-fps))
		verbose.warning("The playback speed of %s fps is not supported by djv_view.\nUsing the closest allowable value: %s fps." %(fps, actual_fps))

	return "-%s %s" %(arg, actual_fps)


def prcImg(inBasename, outBasename, startFrame, endFrame, inExt, outExt='jpg', fps=None, resize=None):
	""" Processes image sequences.
	"""
	cmdInput = '%s.%s-%s.%s' %(inBasename, startFrame, endFrame, inExt)
	cmdOutput = '%s.%s.%s' %(outBasename, startFrame, outExt)

	# Export path to djv codec libraries according to OS
	cmdStr = exportDjvLibs()

	# Process playback speed string
	speedArg = processSpeed("speed", fps)

	# Set up djv command
	if resize:
		cmdStr += '"%s" %s %s -resize %s %s %s' %(os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], speedArg)
	else:
		cmdStr += '"%s" %s %s %s' %(os.environ['DJV_CONVERT'], cmdInput, cmdOutput, speedArg)

	verbose.print_(cmdStr, 4)
	os.system(cmdStr)


def prcQt(inBasename, outBasename, startFrame, endFrame, inExt, name='preview', fps=None, resize=None):
	""" Processes QuickTime movies.
	"""
	cmdInput = '%s.%s-%s.%s' %(inBasename, startFrame, endFrame, inExt)
	if name:
		cmdOutput = os.path.join(outBasename, '%s.mov' %name)
	else:
		cmdOutput = '%s.mov' %outBasename

	# Export path to djv codec libraries according to OS
	cmdStr = exportDjvLibs()

	# Process playback speed string
	speedArg = processSpeed("speed", fps)

	# Set djv command
	if resize:
		cmdStr += '"%s" %s %s -resize %s %s %s' %(os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], speedArg)
	else:
		cmdStr += '"%s" %s %s %s' %(os.environ['DJV_CONVERT'], cmdInput, cmdOutput, speedArg)

	verbose.print_(cmdStr, 4)
	os.system(cmdStr)


def viewer(path=None):
	""" Launch djv_view.
		If path is specified and is a file, automatically load sequence.
		If path is a directory, start in that directory.
		If path is not specified, use shot directory.
	"""
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
	cmdStr = exportDjvLibs()
	if os.environ['IC_RUNNING_OS'] == 'Windows':
		cmdStr += 'cd /d "%s" & ' %startupDir
	else:
		cmdStr += "cd %s; " %startupDir

	# Process playback speed string
	playbackSpeedArg = processSpeed("playback_speed")

	# Build the command based on whether path is a file or a directory
	if pathIsFile:
		cmdStr += '"%s" %s "%s"' %(os.environ['DJV_PLAY'], playbackSpeedArg, path)
	else:
		cmdStr += '"%s" %s' %(os.environ['DJV_PLAY'], playbackSpeedArg)

	# Call command with subprocess in order to not lock the system while djv
	# is running
	verbose.print_(cmdStr, 4)
	subprocess.Popen(cmdStr, shell=True)

