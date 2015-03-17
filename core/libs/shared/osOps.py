#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:dirOps
#copyright	:Gramercy Park Studios


#manages OS operations
import os

#creates directory for the specified path with the specified umask
def createDir(path, umask='000'):
	if not os.path.isdir(path):
		os.system('%s; mkdir -p %s' % (setUmask(umask), path))
		return path

#Sets permissions to provided path
def setPermissions(path, mode='a+w'):
	os.system('chmod -R %s %s' % (mode, path))
	return path

#hardlinks files with the set umask
def hardLink(source, destination, umask='000'):
	os.system('%s; ln -f %s %s' % (setUmask(umask), source, destination))
	return destination

#removes files or folders recursively
def recurseRemove(path):
	os.system('rm -rf %s' % path)
	return path

def copyDirContents(source, destination, umask='000'):
	os.system('%s; cp -rf %s %s' % (setUmask(umask), os.path.join(source, '*'), destination))

def setUmask(umask='000'):
	return 'umask %s' % umask