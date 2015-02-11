#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:inProgress
#copyright	:Gramercy Park Studios


import os

#Publish in progress tmp file manager

def start(pblDir):
	in_progressFile = open(os.path.join(pblDir, 'in_progress.tmp'), 'w')
	in_progressFile.close()

def end(pblDir):
	in_progressFile = os.path.join(pblDir, 'in_progress.tmp')
	if os.path.isfile(in_progressFile):
		os.system('rm -f %s' % in_progressFile)