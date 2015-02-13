#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title		:recentScn
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
	"""Populate config file with with defaults"""

	config.add_section(os.environ['SHOT'])
	config.set(os.environ['SHOT'], os.environ['ICARUSENVAWARE'], '')

	write()


def updateLs(newEntry):
	"""Update recent files list and save config file to disk"""

	read()
	fileLs = [] # Clear recent file list

	newEntry = newEntry.replace(os.environ['SHOTPATH'], '')

	try:
		fileLs = config.get(os.environ['SHOT'], os.environ['ICARUSENVAWARE']).split('; ')
	except:
		create()
		fileLs = []

	if newEntry in fileLs: # if the entry already exists in the list, delete it
		fileLs.remove(newEntry)
	fileLs.insert(0, newEntry) # prepend entry to the list

	while len(fileLs) > 7: # limit list to 7 entries
		fileLs.pop()

	config.set(os.environ['SHOT'], os.environ['ICARUSENVAWARE'], '; '.join(str(n) for n in fileLs))

	write()


def populateMenu():
	"""Read recent file list and return string to be processed by MEL"""

	read()

	try:
		fileLs = config.get(os.environ['SHOT'], os.environ['ICARUSENVAWARE']).split('; ')
	except:
		fileLs = ['No recent files']

	return fileLs


#def updateMenu(menu):
#	""""""
#
#	import maya.cmds as mc
#	import menus2py
#
#	fileLs = populateMenu()
#	for item in fileLs:
#		#menuItem -l $item -c ("source menus2Py; menus2Py.openRecent(\"" + `getenv SHOTPATH` + $item + "\")")  -p $menu $item;
#		mc.menuItem(item, label=item, parent=menu, command=menus2Py.openRecent(os.path.join(os.environ['SHOTDIR'], item)))


#updates recent files list - CURRENTLY DISABLED
def _updateLs(newEntry):
	filePath = os.path.join(os.environ['RECENTFILESDIR'], '%s_%s_mayaScnLs.ic' %(os.environ['JOB'], os.environ['SHOT']))

	entryExists = False
	#limiting list to 7 entries
	scnFile = open(filePath, 'r')
	fileLs = scnFile.readlines()
	while len(fileLs) >= 7:
		fileLs.pop()
	scnFile.close()
	#writing previous entries and adding new at the end if doesn't exist
	scnFile = open(filePath, 'w')
	scnFile.write('%s' % newEntry)
	for fileEntry in fileLs:
		fileEntry = fileEntry.replace('\n', '')
		if fileEntry != newEntry:
			scnFile.write('\n%s' % fileEntry)
	scnFile.close()

