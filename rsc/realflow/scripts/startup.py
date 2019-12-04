#!/usr/bin/python

# [GPS] startup.py (RealFlow)
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2017 Gramercy Park Studios
#
# Deploys RealFlow tools and commands organizer shelf.


import os

from shared import os_wrapper
from shared import verbose


def autoDeploy():

	# Deploying commands organizer
	outputMsg = "Deploying GPS tools... "
	try:
		# Deploy commands organizer copying the file to user scenes directory
		# so it's not read directly from master file in pipeline.
		# There's a different commandsOrganizer.dat for osx/win due to file
		# path differences for icons.
		if os.environ['IC_RUNNING_OS'] == 'Windows':
			osdir = 'win'
		else:
			osdir = 'osx'
		src = os.path.join(os.environ['IC_BASEDIR'], 'rsc', 'realflow', 'realflow__env__', osdir, 'commandsOrganizer.dat')
		dst = os.path.join(os.environ['IC_REALFLOW_SCENES_DIR'], '.cmdsOrg', 'commandsOrganizer.dat')
		os_wrapper.copy(src, dst)
		verbose.message("%s Ok" %outputMsg)
	except:
		verbose.error("%s Failed" %outputMsg)


#def setupScene(scene, EXPORT_PREVIEW, IMAGE_FORMAT_JPG):
def setupScene(scene):
	#updating scene with shot settings
	scene.setFps(int(os.environ['IC_FPS']))
	maxFrame = (int(os.environ['IC_ENDFRAME']) - int(os.environ['IC_STARTFRAME']))
	scene.setMaxFrames(int(maxFrame))

