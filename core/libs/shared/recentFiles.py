#!/usr/bin/python
#support	:Mike Bonnington - mike.bonnington@gps-ldn.com
#title		:recentFiles
#copyright	:Gramercy Park Studios


from ConfigParser import SafeConfigParser
import os


config = SafeConfigParser()
configFile = os.path.join(os.environ['RECENTFILESDIR'], '%s.ini' %os.environ['JOB'])


def read():
	"""Read config file - create it if it doesn't exist"""

	if os.path.exists(configFile):
		config.read(configFile)

	else:
		create()


def write():
	"""Write config file to disk"""

	with open(configFile, 'w') as f:
		config.write(f)


def create():
	"""Create config file if it doesn't exist and populate with with defaults"""

	recentFilesDir = os.environ['RECENTFILESDIR']

	if not os.path.isdir(recentFilesDir):
		os.system('mkdir -p %s'  % recentFilesDir)
		os.system('chmod -R 775 %s' % recentFilesDir)

	config.add_section(os.environ['SHOT'])
	config.set(os.environ['SHOT'], os.environ['ICARUSENVAWARE'], '')

	write()


def updateLs(newEntry):
	"""Update recent files list and save config file to disk"""

	read()
	fileLs = [] # Clear recent file list

	if newEntry.startswith(os.environ['SHOTPATH']): # only add files in the current shot
		newEntry = newEntry.replace(os.environ['SHOTPATH'], '')

		fileStr = config.get(os.environ['SHOT'], os.environ['ICARUSENVAWARE'])

		if not fileStr=='':
			fileLs = fileStr.split('; ')
		else:
			fileLs = []


		if newEntry in fileLs: # if the entry already exists in the list, delete it
			fileLs.remove(newEntry)

		fileLs.insert(0, newEntry) # prepend entry to the list

		while len(fileLs) > 10: # limit list to ten entries
			fileLs.pop()

		config.set(os.environ['SHOT'], os.environ['ICARUSENVAWARE'], '; '.join(n for n in fileLs))

		write()


def getLs():
	"""Read recent file list and return list/array to be processed by MEL"""

	read()

	try:
		fileLs = config.get(os.environ['SHOT'], os.environ['ICARUSENVAWARE']).split('; ')
	except:
		fileLs = []

	return fileLs
