#!/usr/bin/python

# [Icarus] osOps.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# This module acts as a wrapper for low-level OS operations.


import os, re
import verbose


def createDir(path, umask='000'):
	""" Creates directory for the specified path with the specified umask.
		Could probably be rewritten to use Python's own functions? Also remove redundant umask functionality.
	"""
	path = os.path.normpath(path)

	# if not os.path.isdir(path):
	# 	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
	# 		os.makedirs(path)
	# 		if os.path.basename(path).startswith('.'): # hide the folder if the name starts with a dot, as these files are not automatically hidden on Windows
	# 			setHidden(path)
	# 	else:
	# 		os.system('%s; mkdir -p %s' % (setUmask(umask), path))

	if not os.path.isdir(path):
		os.makedirs(path)
		if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
			if os.path.basename(path).startswith('.'): # hide the folder if the name starts with a dot, as these files are not automatically hidden on Windows
				setHidden(path)

		verbose.print_('mkdir "%s"' %path, 4) # commenting this line out as it causes an error if user config dir doesn't exist
		return path


def setPermissions(path, mode='a+w'):
	""" Sets permissions to provided path.
		Could probably be rewritten to use Python's own functions?
	"""
	path = os.path.normpath(path)

	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		# Removed permissions setting on Windows as it causes problems
		pass
		#os.chmod(path, 0777) # Python 2 octal syntax
		#os.chmod(path, 0o777) # Python 3 octal syntax
	else:
		os.system('chmod -R %s %s' % (mode, path))

	return path


def hardLink(source, destination, umask='000'):
	""" Creates hard links.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		if os.path.isdir(dst): # if destination is a folder, append the filename from the source
			filename = os.path.basename(src)
			dst = os.path.join(dst, filename)

		if os.path.isfile(dst): # delete the destination file if it already exists - this is to mimic the Unix behaviour and force creation of the hard link
			os.system('del %s /f /q' % dst)

		#cmdStr = 'mklink /H %s %s' % (dst, src) # this only works with local NTFS volumes
		cmdStr = 'fsutil hardlink create %s %s >nul' % (dst, src) # works over SMB network shares; suppressing output to null
	else:
		cmdStr = '%s; ln -f %s %s' % (setUmask(umask), src, dst)

	verbose.print_(cmdStr, 4)
	os.system(cmdStr)

	return dst


def recurseRemove(path):
	""" Removes files or folders recursively.
		Could be rewritten to use shutil.rmtree?
	"""
	path = os.path.normpath(path)

	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		if os.path.isdir(path):
			cmdStr = 'rmdir %s /s /q' % path
		else:
			cmdStr = 'del %s /f /q' % path
	else:
		cmdStr = 'rm -rf %s' % path

	verbose.print_(cmdStr, 4)
	os.system(cmdStr)

	return path


def rename(source, destination):
	""" Rename a file or folder.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	verbose.print_('rename "%s" "%s"' % (src, dst), 4)
	os.rename(src, dst)

	# if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
	# 	cmdStr = 'ren "%s" "%s"' % (src, dst)
	# else:
	# 	cmdStr = 'mv "%s" "%s"' % (src, dst)

	# verbose.print_(cmdStr, 4)
	# os.system(cmdStr)


def copy(source, destination):
	""" Copy a file or folder.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		cmdStr = 'copy /Y %s %s' % (src, dst)
	else:
		cmdStr = 'cp -rf %s %s' % (src, dst)

	verbose.print_(cmdStr, 4)
	os.system(cmdStr)


def copyDirContents(source, destination, umask='000'):
	""" Copy the contents of a folder recursively.
		Could rewrite using shutil.copy / copytree?
	"""
	src = os.path.normpath( os.path.join(source, '*') )
	dst = os.path.normpath( destination )

	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		cmdStr = 'copy /Y %s %s' % (src, dst)
	else:
		cmdStr = '%s; cp -rf %s %s' % (setUmask(umask), src, dst)

	verbose.print_(cmdStr, 4)
	os.system(cmdStr)


def setHidden(path):
	""" Hide a file or folder (Windows only).
		Useful if the filename name starts with a dot, as these files are not automatically hidden on Windows.
	"""
	import ctypes
	FILE_ATTRIBUTE_HIDDEN = 0x02
	ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)


def setUmask(umask='000'):
	""" Set the umask for permissions on created files and folders (Unix only).
	"""
	if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
		return ""
	else:
		return 'umask %s' % umask


def absolutePath(relPath):
	""" Convert a relative path to an absolute path.
		Expands environment variables in supplied path and replaces backslashes with forward slashes for compatibility.
	"""
	return os.path.normpath( os.path.expandvars(relPath) ).replace("\\", "/")


def relativePath(absPath, token, tokenFormat='standard'):
	""" Convert an absolute path to a relative path.
		'token' is the name of an environment variable to replace.
		Format specifies the environment variable format:
			standard:  $NAME
			bracketed: ${NAME}
			windows:   %NAME%
			nuke:  [getenv NAME]
	"""
	try:
		if tokenFormat == 'standard':
			formattedToken = '$%s' %token
		elif tokenFormat == 'bracketed':
			formattedToken = '${%s}' %token
		elif tokenFormat == 'windows':
			formattedToken = '%%%s%%' %token
		elif tokenFormat == 'nuke':
			formattedToken = '[getenv %s]' %token

		envVar = os.environ[token].replace('\\', '/')
		relPath = absPath.replace('\\', '/') # ensure backslashes from Windows paths are changed to forward slashes
		relPath = relPath.replace(envVar, formattedToken) # change to relative path

		return os.path.normpath( relPath ).replace("\\", "/")

	except:
		return os.path.normpath( absPath ).replace("\\", "/")


def sanitize(instr, pattern='\W', replace=''):
	""" Sanitizes characters in string. Default removes all non-alphanumeric characters.
	"""
	return re.sub(pattern, replace, instr)

