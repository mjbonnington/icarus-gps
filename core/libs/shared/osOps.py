#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:dirOps
#copyright	:Gramercy Park Studios


#manages OS operations
import os

#creates directory for the specified path with the specified umask
def createDir(path, umask='000'):
	if not os.path.isdir(path):
		os.system('umask %s; mkdir -p %s' % (umask, path))
		return path

#Sets permissions to provided path
def setPermissions(path, mode='777'):
	os.system('chmod -R %s %s' % (path, mode))
	return path

#hardlinks files with the set umask
def hardLink(source, destination, umask='000'):
	os.system('umask %s; ln -f %s %s' % (umask, source, destination))
	return destination

#removes files or folders recursively
def recurseRemove(path):
	os.system('rm -rf %s' % path)
	return path
