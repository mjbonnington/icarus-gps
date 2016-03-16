#!/usr/bin/python

# [Icarus] rename.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2014-2016 Gramercy Park Studios
#
# Functions for renaming and renumbering.


import os, string, re, time


def renameUnique(self, obj, newName):
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


def replaceTextRE(objLs, findStr, replaceStr, ignoreCase=False):
	""" Find and replace using regular expressions.
	"""
	if objLs:

		# Check input is valid
		if findStr:

			# Initialise progress bar and start clock
			#mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=len(objLs)) # Initialise progress bar
			startTime = time.time()

			for obj in objLs:
				newName = pattern.sub(replaceStr, str(obj))
				renameUnique(obj, newName)
				#mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Renaming items") # Increment progress bar

			# Complete progress bar and print completion message
			#mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
			totalTime = time.time() - startTime;
			print "Renamed %d items in %f seconds.\n" %(len(objLs), totalTime)

		else:
			print "Warning: No search string specified."

	else:
		print "Warning: Nothing selected."


def renumber(objLs, start=1, step=1, padding=4, preserve=True, autopad=True):
	""" Renumber objects.
	"""
	if objLs:

		# Initialise progress bar and start clock
		#mc.progressBar(self.gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, maxValue=2*len(objLs)) # Initialise progress bar
		startTime = time.time()

		# Calculate padding automatically...
		if autopad:
			numLs = []

			if preserve:
				for obj in objLs:
					match = re.search("[0-9]*$", str(obj))
					currentNumStr = match.group()
					# Check if name has numeric suffix
					if currentNumStr:
						numLs.append(int(currentNumStr))

				if numLs:
					maxNum = max(numLs)
				else:
					print "Error: No numbering sequence detected, unable to calculate padding."
			else:
				maxNum = start + (step*(len(objLs)-1))

			padding = len(str(maxNum))

		# ...or use user specified padding value
		else:
			pass
			#padding = mc.intSliderGrp("padding", query=True, value=True)

		# Loop twice to prevent renumbering to a pre-existing number
		for i in range(2):
			index = start
			#objLs = pm.ls(selection=True) # Get selection again as names will have changed - no longer required as now copying object list at start of function

			if preserve:
				for obj in objLs:
					match = re.search("[0-9]*$", str(obj))
					currentNumStr = match.group()
					# Check if name has numeric suffix
					if currentNumStr:
						currentNumInt = int(currentNumStr) # Cast string to integer - looks pointless but otherwise padding can't be reduced
						newName = re.sub(currentNumStr+"$", str(currentNumInt).zfill(padding), str(obj))
						self.renameUnique(obj, newName)
						#mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Renumbering items") # Increment progress bar
					elif not i: # Only print warning on first iteration
						print "Warning: %s has no numeric suffix, unable to renumber." %obj
			else:
				for obj in objLs:
					newName = re.sub("[0-9]*$", str(index).zfill(padding), str(obj))
					self.renameUnique(obj, newName)
					index += step
					#mc.progressBar(self.gMainProgressBar, edit=True, step=1, status="Renumbering items") # Increment progress bar

		# Complete progress bar and print completion message
		#mc.progressBar(self.gMainProgressBar, edit=True, endProgress=True) # Complete progress bar
		totalTime = time.time() - startTime;
		print "Renumbered %d items in %f seconds.\n" %(len(objLs), totalTime)

	else:
		print "Warning: Nothing selected."

