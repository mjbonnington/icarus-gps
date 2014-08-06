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
		#deploying commands organizer
		if not os.path.isdir(rf_userPath):
			os.system('mkdir -p %s' % rf_userPath)
		#copying the file to the user documents direcotry so users can overried shelf manually to workaournd realflow erratic loading behaviours
		os.system('cp -f %s/%s %s/%s' % (rf_envPath, rf_cmdsOrg, rf_userPath, rf_cmdsOrg))
		os.system('cp -f %s/%s %s/%s/%s' % (rf_envPath, rf_cmdsOrg, os.environ['REALFLOWSCENESDIR'], rf_cmdsOrgDir, rf_cmdsOrg))
		print '%s Ok' % outputMsg 
	except:
		print '%s Failed' % outputMsg
		
def setupScene(scene):
	#appending realflow pipeline paths to sys
	sys.path.append(os.path.join(os.getenv('PIPELINE'), 'realflow_rsc', 'scripts'))
	sys.path.append(os.path.join(os.getenv('PIPELINE'), 'realflow_rsc', 'realflow__env__'))
	sys.path.append(os.path.join(os.getenv('PIPELINE'), 'icarus', 'ui'))
	sys.path.append(os.path.join(os.getenv('PIPELINE'), 'icarus', 'libs', 'shared'))


	#setting shot settings
	scene.setFps(int(os.environ['FPS']))
	maxFrame = (int(os.environ['ENDFRAME']) - int(os.environ['STARTFRAME']))
	scene.setMaxFrames(int(maxFrame))