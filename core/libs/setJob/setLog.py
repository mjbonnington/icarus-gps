#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:setLog
#copyright	:Gramercy Park Studios


#Writes and reads user log file for last used job and shot

import os


#reading from user log file	
def read(entry=-1):
	userPrefsFolder = os.environ['ICUSERPREFS']
	try:
		logFile = open('%s/setlog' % userPrefsFolder , 'r')
		entryLs = logFile.read().split('\n')
		entryLs = entryLs[entry].split(',')
		logFile.close()
		if len(entryLs) == 2:
			return entryLs
	except IOError:
		return
		

#writing to user log file. allows max of 5 entries
def write(newEntry):
	userPrefsFolder = os.environ['ICUSERPREFS']
	try:
		logFile = open('%s/setlog' % userPrefsFolder , 'r+')
		#limiting entry list
		entryLs = logFile.read().split('\n')
		if len(entryLs) >= 2:
			entryLs = [entryLs[-1], newEntry]
			logFile.close()
			logFile = open('%s/setlog' % userPrefsFolder , 'w')
		else:
			entryLs = [newEntry]
	except IOError:
		logFile = open('%s/setlog' % userPrefsFolder , 'w')
		entryLs = [newEntry]
		
	#writing entries
	for entry in entryLs:
		logFile.write('\n%s' % entry)
	logFile.close()
