#!/usr/bin/python

# [Icarus] rename.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2017 Gramercy Park Studios
#
# Functions for renaming and renumbering.


import re

from . import verbose


def replaceTextRE(origName, findStr, replaceStr, ignoreCase=False, regex=True, quiet=True):
	""" Find and replace using regular expressions.
	"""
	try:
		# If findStr is not designated as regex, escape all special characters
		if not regex:
			findStr = re.escape(findStr)

		if ignoreCase:
			pattern = re.compile(r"(?i)%s" %findStr)
		else:
			pattern = re.compile(r"%s" %findStr)

		# Perform replacement and return new name if input is valid
		if findStr:
			newName = pattern.sub(replaceStr, origName)
			return newName

		else:
			if not quiet:
				verbose.warning("No search string specified.")
			return origName

	except:
		if not quiet:
			verbose.warning("Regular expression is invalid.")


def renumber(numLs, start=1, step=1, padding=4, preserve=True, autopad=True):
	""" Renumber objects.
	"""
	newNumLs = []

	# Calculate padding automatically...
	if autopad:

		if preserve:
			maxNum = max(numLs)
		else:
			maxNum = start + (step*(len(numLs)-1))

		padding = len(str(maxNum))

	#print(padding)

	# Regenerate lists
	index = start

	if preserve:
		for num in numLs:
			newNumInt = int(str(num).zfill(padding))  # Cast to string as zfill only works on strings
			newNumLs.append(newNumInt)

	else:
		for num in numLs:
			newNumInt = int(str(index).zfill(padding))  # Cast to string as zfill only works on strings
			newNumLs.append(newNumInt)
			index += step

	return newNumLs, padding

