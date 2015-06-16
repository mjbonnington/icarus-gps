#!/usr/bin/python
#support    :Nuno Pereira - nuno.pereira@gps-ldn.com
#title      :osOps
#copyright  :Gramercy Park Studios

# Manages OS operations

import os, re


def createDir(path, umask='000'):
	""" Creates directory for the specified path with the specified umask - could probably be rewritten to use Python's own functions
	"""
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


def setPermissions(path, mode='a+w'):
	""" Sets permissions to provided path - could probably be rewritten to use Python's own functions
	"""
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		os.chmod(path, 0777) # Python 2 octal syntax
		#os.chmod(path, 0o777) # Python 3 octal syntax
	else:
		os.system('chmod -R %s %s' % (mode, path))

	return path


def hardLink(source, destination, umask='000'):
	""" Creates hard links
	"""
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		if os.path.isdir(destination): # if destination is a folder, append the filename from the source
			filename = os.path.basename(source)
			destination = os.path.join(destination, filename)

		if os.path.isfile(destination): # delete the destination file if it already exists - this is to mimic the Unix behaviour and force creation of the hard link
			os.system('del %s /f /q' % destination)

		#cmdStr = 'mklink /H %s %s' % (destination, source) # this only works with local NTFS volumes
		cmdStr = 'fsutil hardlink create %s %s >nul' % (destination, source) # works over SMB network shares; suppressing output to null
	else:
		cmdStr = '%s; ln -f %s %s' % (setUmask(umask), source, destination)

	#print cmdStr
	os.system(cmdStr)

	return destination


def recurseRemove(path):
	""" Removes files or folders recursively
	"""
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		if os.path.isdir(path):
			cmdStr = 'rmdir %s /s /q' % path
		else:
			cmdStr = 'del %s /f /q' % path
	else:
		cmdStr = 'rm -rf %s' % path

	#print cmdStr
	os.system(cmdStr)

	return path


def copyDirContents(source, destination, umask='000'):
	""" Copy the contents of a folder recursively - rewrite using shutil.copy / copytree
	"""
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		cmdStr = 'copy %s %s' %(os.path.join(source, '*'), destination)
	else:
		cmdStr = '%s; cp -rf %s %s' % (setUmask(umask), os.path.join(source, '*'), destination)

	#print cmdStr
	os.system(cmdStr)


def setUmask(umask='000'):
	""" Set the umask for permissions on created files and folders (Unix only)
	"""
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		return ""
	else:
		return 'umask %s' % umask


def sanitize(instr, pattern='\W', replace=''):
	""" Sanitizes characters in string. Default removes all non-alphanumeric characters.
	"""
	return re.sub(pattern, replace, instr)

