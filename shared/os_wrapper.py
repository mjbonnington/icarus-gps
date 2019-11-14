#!/usr/bin/python

# os_wrapper.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# This module acts as a wrapper for low-level OS operations.


import os
import re
import shutil
import subprocess
import sys
import traceback

# Import custom modules
from shared import verbose


# Prevent spawned processes from opening a shell window
CREATE_NO_WINDOW = 0x08000000


def execute(args):
	""" Wrapper to execute a command using subprocess.check_output().
	"""
	verbose.print_(" ".join(arg for arg in args))

	try:
		if os.environ['IC_RUNNING_OS'] == "Windows":
			output = subprocess.check_output(args, creationflags=CREATE_NO_WINDOW)
		else:
			output = subprocess.check_output(args)
		return True, output.decode()

	except subprocess.CalledProcessError as e:
		error_msg = e.output.decode()
		# verbose.error(error_msg)
		# raise RuntimeError(error_msg)
		return False, error_msg


def createDir(path):
	""" Create a directory with the specified path.
	"""
	path = os.path.normpath(path)

	if os.path.isdir(path):
		verbose.print_("Directory already exists: %s" %path)
		pass

	else:
		try:
			os.makedirs(path)

			# Hide the folder if its name starts with a dot, as these files
			# are not automatically hidden on Windows
			if os.environ['IC_RUNNING_OS'] == "Windows":
				if os.path.basename(path).startswith('.'):
					setHidden(path)

			verbose.print_('mkdir "%s"' %path)  # This causes an error if user config dir doesn't exist
			return path

		except:
			verbose.error("Cannot create directory: %s" %path)
			return False


def setPermissions(path, mode='a+w'):
	""" Sets permissions to provided path.
		Could probably be rewritten to use Python's own functions?
		And we probably shouldn't be doing this anyway.
	"""
	path = os.path.normpath(path)

	if os.environ['IC_RUNNING_OS'] == "Windows":
		# Removed permissions setting on Windows as it causes problems
		pass
		#os.chmod(path, 0777) # Python 2 octal syntax
		#os.chmod(path, 0o777) # Python 3 octal syntax
	else:
		os.system('chmod -R %s %s' %(mode, path))

	return path


def hardLink(source, destination, umask='000', verify=True):
	""" Creates hard links.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	if os.environ['IC_RUNNING_OS'] == "Windows":
		# If destination is a folder, append the filename from the source
		if os.path.isdir(dst):
			filename = os.path.basename(src)
			dst = os.path.join(dst, filename)

		# Delete the destination file if it already exists - this is to mimic
		# the Unix behaviour and force creation of the hard link
		if os.path.isfile(dst):
			os.system('del "%s" /f /q' %dst)

		# Create the hardlink
		#cmdStr = 'mklink /H "%s" "%s"' %(dst, src)  # This only works with local NTFS volumes
		cmdStr = 'fsutil hardlink create "%s" "%s" >nul' %(dst, src)  # Works over SMB network shares; suppressing output to null
	else:
		#cmdStr = '%s; ln -f %s %s' %(setUmask(umask), src, dst)
		cmdStr = 'ln -f %s %s' %(src, dst)

	verbose.print_(cmdStr)
	os.system(cmdStr)

	# Make sure source and destination files match
	if verify:
		if verify_hardlink(src, dst):
			return dst
		else:
			verbose.warning("Failed to create hardlink. Attempting to copy file instead.")
			copy(src, dst)
	else:
		return dst


def verify_hardlink(src, dst):
	""" Compare os.stat() for src and dst files to check for hardlink.
	"""
	try:
		if os.stat(src) == os.stat(dst):
			return True
	except:
		pass

	return False


# def recurseRemove(path):
# 	""" Removes files or folders recursively.
# 		Could be rewritten to use shutil.rmtree?
# 	"""
# 	path = os.path.normpath(path)

# 	if os.environ['IC_RUNNING_OS'] == "Windows":
# 		if os.path.isdir(path):
# 			cmdStr = 'rmdir %s /s /q' %path
# 		else:
# 			cmdStr = 'del %s /f /q' %path
# 	else:
# 		cmdStr = 'rm -rf %s' %path

# 	verbose.print_(cmdStr, 4)
# 	os.system(cmdStr)

# 	return path


def remove(path, quiet=False):
	""" Removes files or folders recursively.
	"""
	path = os.path.normpath(path)

	try:
		if os.path.isfile(path):
			os.remove(path)
		elif os.path.isdir(path):
			shutil.rmtree(path)
		return True, path
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		msg = traceback.format_exception_only(exc_type, exc_value)[0]
		if not quiet:
			verbose.error(msg)
		return False, msg


def rename(source, destination, quiet=False):
	""" Rename a file or folder.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	if not quiet:
		verbose.print_('rename "%s" -> "%s"' %(src, dst))
	try:
		os.rename(src, dst)
		return True, dst
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		msg = traceback.format_exception_only(exc_type, exc_value)[0]
		if not quiet:
			verbose.error(msg)
		return False, msg


def copy(source, destination, quiet=False):
	""" Copy a file or folder.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	if not quiet:
		verbose.print_('copy "%s" -> "%s"' %(src, dst))
	try:
		shutil.copyfile(src, dst)
		return True, dst
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		msg = traceback.format_exception_only(exc_type, exc_value)[0]
		if not quiet:
			verbose.error(msg)
		return False, msg


def move(source, destination, quiet=False):
	""" Move a file or folder.
	"""
	src = os.path.normpath(source)
	dst = os.path.normpath(destination)

	if not quiet:
		verbose.print_('move "%s" -> "%s"' %(src, dst))
	try:
		shutil.move(src, dst)
		return True
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		msg = traceback.format_exception_only(exc_type, exc_value)[0]
		if not quiet:
			verbose.error(msg)
		return False


def copyDirContents(source, destination, umask='000'):
	""" Copy the contents of a folder recursively.
		Could rewrite using shutil.copy / copytree?
	"""
	src = os.path.normpath(os.path.join(source, "*"))
	dst = os.path.normpath(destination)

	if os.environ['IC_RUNNING_OS'] == "Windows":
		cmdStr = 'copy /Y "%s" "%s"' %(src, dst)
	elif os.environ['IC_RUNNING_OS'] == "Linux":  # Quick bodge
		cmdStr = 'cp -rf %s %s' %(src, dst)
	else:
		cmdStr = 'cp -rf "%s" "%s"' %(src, dst)

	verbose.print_(cmdStr)
	os.system(cmdStr)


def setHidden(path):
	""" Hide a file or folder (Windows only).
		Useful if the filename name starts with a dot, as these files are not
		automatically hidden on Windows.
	"""
	import ctypes
	FILE_ATTRIBUTE_HIDDEN = 0x02
	ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)


# def setUmask(umask='000'):
# 	""" Set the umask for permissions on created files and folders (Unix only).
# 	"""
# 	if os.environ['IC_RUNNING_OS'] == "Windows":
# 		return ""
# 	else:
# 		return 'umask %s' %umask


def absolutePath(relPath, stripTrailingSlash=False):
	""" Convert a relative path to an absolute path.
		Expands environment variables in supplied path and replaces
		backslashes with forward slashes for compatibility.
		If 'stripTrailingSlash' is True, remove trailing slash(es) from
		returned path.
	"""
	if relPath:
		if stripTrailingSlash:
			return os.path.normpath(os.path.expandvars(relPath)).replace("\\", "/").rstrip('/')
		else:
			return os.path.normpath(os.path.expandvars(relPath)).replace("\\", "/")
	else:
		return ""


def relativePath(absPath, token, tokenFormat='standard'):
	""" Convert an absolute path to a relative path.
		'token' is the name of an environment variable to replace.
		'tokenFormat' specifies the environment variable format:
			standard:   $VAR
			bracketed:  ${VAR}
			windows:    %VAR%
			nuke (TCL): [getenv VAR]
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
		relPath = absPath.replace('\\', '/')  # ensure backslashes from Windows paths are changed to forward slashes
		relPath = relPath.replace(envVar, formattedToken)  # change to relative path

		return os.path.normpath(relPath).replace("\\", "/")

	except:
		return os.path.normpath(absPath).replace("\\", "/")


def translatePath(path):
	""" Translate paths for cross-platform support.
	"""
	try:
		path_tr = path
		if os.environ['IC_RUNNING_OS'] == "Windows":
			if path.startswith(os.environ['FILESYSTEMROOTOSX']):
				path_tr = path.replace(os.environ['FILESYSTEMROOTOSX'], os.environ['FILESYSTEMROOTWIN'])
			elif path.startswith(os.environ['FILESYSTEMROOTLINUX']):
				path_tr = path.replace(os.environ['FILESYSTEMROOTLINUX'], os.environ['FILESYSTEMROOTWIN'])
		elif os.environ['IC_RUNNING_OS'] == "MacOS":
			if path.startswith(os.environ['FILESYSTEMROOTWIN']):
				path_tr = path.replace(os.environ['FILESYSTEMROOTWIN'], os.environ['FILESYSTEMROOTOSX'])
			elif path.startswith(os.environ['FILESYSTEMROOTLINUX']):
				path_tr = path.replace(os.environ['FILESYSTEMROOTLINUX'], os.environ['FILESYSTEMROOTOSX'])
		else:  # Linux
			if path.startswith(os.environ['FILESYSTEMROOTWIN']):
				path_tr = path.replace(os.environ['FILESYSTEMROOTWIN'], os.environ['FILESYSTEMROOTLINUX'])
			elif path.startswith(os.environ['FILESYSTEMROOTOSX']):
				path_tr = path.replace(os.environ['FILESYSTEMROOTOSX'], os.environ['FILESYSTEMROOTLINUX'])

		#print("Performing path translation:\n%s\n%s\n" %(path, absolutePath(path_tr)))
		return absolutePath(path_tr)

	except (KeyError, TypeError):
		return path


def checkIllegalChars(path, pattern=r'[^\w\.-]'):
	""" Checks path for illegal characters, ignoring delimiter characters such
		as / \ : etc.
		Returns True if no illegal characters are found.
	"""
	clean_str = re.sub(r'[/\\]', '', os.path.splitdrive(path)[1])
	if re.search(pattern, clean_str) is None:
		return True
	else:
		return False


def sanitize(instr, pattern=r'\W', replace=''):
	""" Sanitizes characters in string. Default removes all non-alphanumeric
		characters.
	"""
	return re.sub(pattern, replace, instr)
