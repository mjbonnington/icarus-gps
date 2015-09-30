#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:djvOps
#copyright	:Gramercy Park Studios


#djv operations module

import os, subprocess

#processes image sequences
def prcImg(input, output, startFrame, endFrame, inExt, outExt='jpg', fps=os.environ['FPS']):
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
	djvCmd = '%s; %s %s %s -speed %s' % (libsExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	os.system(djvCmd)

#processes quicktime movies
def prcQt(input, output, startFrame, endFrame, inExt, name='preview', fps=os.environ['FPS'], resize=None):
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


def viewer(path=os.environ['SHOTPATH']):
	""" Launch djv_view.
		If path is specified and is a file, automatically load sequence.
		If path is a directory, start in that directory.
		If path is not specified, use shot directory.
	"""
	# Export path to djv codec libraries according to OS
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		command_str = ""
	elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		command_str = "export DYLD_FALLBACK_LIBRARY_PATH=%s; " %os.environ['DJV_LIB']
	else:
		command_str = "export LD_LIBRARY_PATH=%s; export LIBQUICKTIME_PLUGIN_DIR=%s; " %(os.environ['DJV_LIB'], os.path.join(os.environ['DJV_LIB'],'libquicktime'))

	# Build the command based on whether path is a file or a directory
	if os.path.isdir(path):
		command_str += "cd %s; %s" %(path, os.environ['DJV_PLAY'])
	elif os.path.isfile(path):
		command_str += "cd %s; %s %s" %(os.path.dirname(path), os.environ['DJV_PLAY'], path)

	# Call command with subprocess in order to not lock the system while djv is running
	#print command_str
	subprocess.Popen(command_str, shell=True)

