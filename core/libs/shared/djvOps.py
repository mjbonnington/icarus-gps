#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:djvOps
#copyright	:Gramercy Park Studios


#djv operations module

import os

#processes image sequences
def prcImg(input, output, startFrame, endFrame, inExt, outExt='jpg', fps=os.environ['FPS']):
	#passing arguments to djv to process the files in DJV
	cmdInput = '%s.%s-%s.%s' % (input, startFrame, endFrame, inExt)
	cmdOutput = '%s.%s.%s' % (output, startFrame, outExt)
	os.system('%s/djv_convert %s %s -speed_default %s' % (os.environ['DJVCONVERTPATH'], cmdInput, cmdOutput, fps))

#processes quicktime movies
def prcQt(input, output, startFrame, endFrame, inExt, name='preview', fps=os.environ['FPS'], resize=None):
	#passing arguments to djv to process the files in DJV
	cmdInput = '%s.%s-%s.%s' % (input, startFrame, endFrame, inExt)
	if name:
		cmdOutput = '%s/%s.mov' % (output, name)
	else:
		cmdOutput = '%s.mov' % output
	if resize:
		os.system('%s/djv_convert %s %s -resize %s %s -speed_default %s' % (os.environ['DJVCONVERTPATH'], cmdInput, cmdOutput, resize[0], resize[1], os.environ['FPS']))
	else:
		os.system('%s/djv_convert %s %s -speed_default %s' % (os.environ['DJVCONVERTPATH'], cmdInput, cmdOutput, os.environ['FPS']))