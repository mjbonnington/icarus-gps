#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :osOps
#copyright  :Gramercy Park Studios

# Manages OS operations

import os, re

#creates directory for the specified path with the specified umask
def createDir(path, umask='000'):
	if not os.path.isdir(path):
		if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
			os.makedirs(path)
			if os.path.basename(path).startswith('.'): # hide the folder if the name starts with a dot, as these files are not automatically hidden on Windows
				import ctypes
				FILE_ATTRIBUTE_HIDDEN = 0x02
				ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)
		else:
			os.system('%s; mkdir -p %s' % (setUmask(umask), path))
		return path

#Sets permissions to provided path
def setPermissions(path, mode='a+w'):
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.chmod(path, 0o777)
	else:
		os.system('chmod -R %s %s' % (mode, path))
	return path

#hardlinks files with the set umask
def hardLink(source, destination, umask='000'):
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.system('mklink /H %s %s' % (destination, source))
	else:
		os.system('%s; ln -f %s %s' % (setUmask(umask), source, destination))
	return destination

#removes files or folders recursively
def recurseRemove(path):
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		if os.path.isdir(path):
			os.system('rmdir %s /s /q' % path)
		else:
			os.system('del %s /f /q' % path)
	else:
		os.system('rm -rf %s' % path)
	return path

#copy the contents of a folder recursively - rewrite using shutil.copy / copytree
def copyDirContents(source, destination, umask='000'):
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.system('copy %s %s' %(os.path.join(source, '*'), destination))
	else:
		os.system('%s; cp -rf %s %s' % (setUmask(umask), os.path.join(source, '*'), destination))

def setUmask(umask='000'):
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		return ""
	else:
		return 'umask %s' % umask

#sanitizes characters in string. Default replaces all non-alphanumeric characters with nothing.
def sanitize(instr, pattern='\W', replace=''):
	return re.sub(pattern, replace, instr)
