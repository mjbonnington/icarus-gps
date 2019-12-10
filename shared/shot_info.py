#!/usr/bin/python

# [Icarus] shot_info.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2019
#
# Display some basic shot information.


import os

from shared import prompt


def show():
	dialog = prompt.dialog()
	title = '%s - %s' % (os.environ['IC_JOB'], os.environ['IC_SHOT'])
	message = """Shot info:

Job: %s
Shot: %s
User: %s

Linear unit: %s
Angular unit: %s

Time unit: %s
Frame range: %s-%s
FPS: %s

Resolution: %sx%s
Proxy: %sx%s
""" % (
	os.environ['IC_JOB'], 
	os.environ['IC_SHOT'], 
	os.environ['IC_USERNAME'], 
	os.environ['IC_LINEAR_UNIT'], 
	os.environ['IC_ANGULAR_UNIT'], 
	os.environ['IC_TIME_UNIT'], 
	os.environ['IC_STARTFRAME'], os.environ['IC_ENDFRAME'], 
	os.environ['IC_FPS'], 
	os.environ['IC_RESOLUTION_X'], os.environ['IC_RESOLUTION_Y'], 
	os.environ['IC_PROXY_RESOLUTION_X'], os.environ['IC_PROXY_RESOLUTION_Y'])

	dialog.display(message, title, conf=True)
