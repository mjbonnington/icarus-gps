#!/usr/bin/python
#support		:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:startup
#copyright	:Gramercy Park Studios

#this file deploys realflow tools and commands organizer shelf
import os, sys

def autoDeploy():
	rf_envPath = '%s/realflow_rsc/realflow__env__' % os.getenv('PIPELINE')
	rf_userPath = '%s/Documents/realflow' % os.environ['HOME']
	rf_cmdsOrgDir = '.cmdsOrg'
	rf_cmdsOrg = 'commandsOrganizer.dat'
	
	#deploying commands organizer
	outputMsg = 'Deploying GPS tools - '
	try:
		#deploying commands organizer copying the file to user scenes directory so it's not read directly from master file in pipeline
		os.system('cp -f %s/%s %s/%s/%s' % (rf_envPath, rf_cmdsOrg, os.environ['REALFLOWSCENESDIR'], rf_cmdsOrgDir, rf_cmdsOrg))
		print '%s Ok' % outputMsg 
	except:
		print '%s Failed' % outputMsg
		
def setupScene(scene):
	#updating scene with shot settings
	scene.setFps(int(os.environ['FPS']))
	maxFrame = (int(os.environ['ENDFRAME']) - int(os.environ['STARTFRAME']))
	scene.setMaxFrames(int(maxFrame))
	

	
	
	
	
	
	