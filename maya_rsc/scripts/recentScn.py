#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:recentScn
#copyright	:Gramercy Park Studios

import os

#updates recent files list
def updateLs(newEntry):
	filePath = '%s/%s_%s_mayaScnLs.ic' % (os.environ['RECENTFILESDIR'], os.environ['JOB'], os.environ['SHOT'])

	#folder = os.path.join(os.environ['RECENTFILESDIR'], 'maya')
	#if not os.path.exists(folder):
	#	os.system('mkdir -p %s'  %folder)

	#filePath = os.path.join(folder, '%s_%s' %(os.environ['JOB'], os.environ['SHOT']))

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
	