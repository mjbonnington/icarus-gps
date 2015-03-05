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
		ldLibExport = 'export DYLD_FALLBACK_LIBRARY_PATH=%s' % os.environ['DJV_LIB']
	else:
		ldLibExport = 'export LD_LIBRARY_PATH=%s' % os.environ['DJV_LIB']

	#setting djv command
	djvCmd = '%s; %s %s %s -speed %s' % (ldLibExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	os.system(djvCmd)

#processes quicktime movies
def prcQt(input, output, startFrame, endFrame, inExt, name='preview', fps=os.environ['FPS'], resize=None):
	cmdInput = '%s.%s-%s.%s' % (input, startFrame, endFrame, inExt)
	if name:
		cmdOutput = '%s/%s.mov' % (output, name)
	else:
		cmdOutput = '%s.mov' % output

	#exporting path to djv codec libraries according to os
	if os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
		ldLibExport = 'export DYLD_FALLBACK_LIBRARY_PATH=%s' % os.environ['DJV_LIB']
	else:
		ldLibExport = 'export LD_LIBRARY_PATH=%s' % os.environ['DJV_LIB']

	#setting djv command
	if resize:
		djvCmd = '%s; %s %s %s -resize %s %s -speed %s' % (ldLibExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, resize[0], resize[1], fps)
	else:
		djvCmd = '%s; %s %s %s -speed %s' % (ldLibExport, os.environ['DJV_CONVERT'], cmdInput, cmdOutput, fps)

	os.system(djvCmd)