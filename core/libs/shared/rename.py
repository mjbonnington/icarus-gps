#!/usr/bin/python

# [Icarus] rename.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2016 Gramercy Park Studios
#
# Functions for renaming and renumbering.


import os, string, re, time


def renameUnique(obj, newName):
	""" Rename object.
		Now takes pymel object, rather than string, as first argument.
		Perhaps this function should be moved to an external module?
	"""
#	# Set flags for shape node renaming behaviour
#	ignoreShape = False
#	renameShapes = mc.radioCollection("renameShapes", query=True, select=True) # Re-write to pass in as attribute
#	if not renameShapes == "renameShapesAuto":
#		ignoreShape = True
#
#	# Split new name string after the last pipe character - allows non-unique child objects to be renamed correctly
#	newNameTuple = newName.rpartition("|")
#
#	# Rename shape node(s) if applicable
#	if renameShapes == "renameShapesForce":
#		objName = str(obj) # Cast pymel object to string for the following code to work
#		if mc.nodeType(objName) == "transform":
#			shapeLs = mc.listRelatives(objName, shapes=True, fullPath=True)
#			if shapeLs is not None:
#				for shape in shapeLs:
#					mc.rename(shape, newNameTuple[2] + "Shape")
#
#	# Rename node
#	try:
#		obj.rename(newNameTuple[2], ignoreShape=ignoreShape)
#	except RuntimeError:
#		mc.warning("Cannot rename node: %s" %str(obj))
#		return False


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
				print "Warning: No search string specified."
			return origName

	except:
		if not quiet:
			print "Warning: Regular expression is invalid."


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

	#print padding

	# Regenerate lists
	index = start

	if preserve:
		for num in numLs:
			newNumInt = int( str(num).zfill(padding) ) # casting to string as zfill only works on strings
			newNumLs.append(newNumInt)

	else:
		for num in numLs:
			newNumInt = int( str(index).zfill(padding) ) # casting to string as zfill only works on strings
			newNumLs.append(newNumInt)
			index += step

	return newNumLs, padding

