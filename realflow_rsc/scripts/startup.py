#!/usr/bin/python
#support   :Nuno Pereira - nuno.pereira@gps-ldn.com
#support   :Mike Bonnington - mike.bonnington@gps-ldn.com
#title     :Startup (RealFlow)
#copyright :Gramercy Park Studios

#this file deploys realflow tools and commands organizer shelf
import os, osOps

def autoDeploy():

	#deploying commands organizer
	outputMsg = 'Deploying GPS tools... '
	try:
		#deploying commands organizer copying the file to user scenes directory so it's not read directly from master file in pipeline
		if os.environ['ICARUS_RUNNING_OS'] == 'Windows': # there's a different commandsOrganizer.dat for osx/win due to file path differences for icons
			osdir = 'win'
		else:
			osdir = 'osx'
		src = os.path.join(os.environ['PIPELINE'], 'realflow_rsc', 'realflow__env__', osdir, 'commandsOrganizer.dat')
		dst = os.path.join(os.environ['REALFLOWSCENESDIR'], '.cmdsOrg', 'commandsOrganizer.dat')
		osOps.copy(src, dst)
		print '%s Ok' % outputMsg
	except:
		print '%s Failed' % outputMsg

#def setupScene(scene, EXPORT_PREVIEW, IMAGE_FORMAT_JPG):
def setupScene(scene):
	#updating scene with shot settings
	scene.setFps(int(os.environ['FPS']))
	maxFrame = (int(os.environ['ENDFRAME']) - int(os.environ['STARTFRAME']))
	scene.setMaxFrames(int(maxFrame))
