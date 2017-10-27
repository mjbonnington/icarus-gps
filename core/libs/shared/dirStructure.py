#!/usr/bin/python

# [Icarus] dirStructure.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017 Gramercy Park Studios
#
# Create folder structures as defined by XML files.


import os
import re
import xml.etree.ElementTree as ET

# Import custom modules
import osOps
import verbose
import xmlData


class DirStructure(xmlData.XMLData):
	""" Manipulates XML data to create folder structures on disk.
		Inherits XMLData class.
	"""
	def createDirRecursive(self, element, basedir=None):
		""" Recursively create directories from XML definition.
		"""
		# Create directories
		for directory in element.findall("dir"):
			name = directory.get("name")
			env = directory.get("env")

			# if self.checkIllegalChars(name):
			# newdir = os.path.join(basedir, name)
			newdir = osOps.absolutePath("%s/%s" %(basedir, name))
			if not os.path.isdir(newdir):
				osOps.createDir(newdir)

			# Set environment variables
			if env:
				os.environ[env] = newdir

			self.createDirRecursive(directory, newdir)

		# Create files
		for file in element.findall("file"):
			name = file.get("name")
			env = file.get("env")

			newfile = osOps.absolutePath("%s/%s" %(basedir, name))
			if not os.path.isfile(newfile):
				src = osOps.absolutePath("%s/%s" %(os.path.dirname(self.datafile), name))
				osOps.copy(src, newfile)

			# Set environment variables
			if env:
				os.environ[env] = newfile

		return


	def createDirStructure(self, datafile=None):
		""" Create folder structure from XML definition.
		"""
		if datafile is not None:
			self.loadXML(datafile)

		basedir = self.root.get("location")

		if basedir:
			self.createDirRecursive(self.root, basedir)
		else:
			verbose.warning("Could not create project folders because the root folder was not specified.")


	# def createXML(self, basedir, datafile=None):
	# 	""" Create XML definition of folder structure.
	# 	"""
	# 	if datafile is not None:
	# 		self.loadXML(datafile)

	# 	basedir = self.root.get("location")

	# 	if basedir:
	# 		self.createDirRecursive(self.root, basedir)
	# 	else:
	# 		verbose.warning("Could not create project folders because the root folder was not specified.")

	# 	self.saveXML(datafile)


	# def createDefault(self):
	# 	""" Create default folder structure if XML doesn't exist.
	# 	"""


	# def checkIllegalChars(self, instr):
	# 	""" Check for illegal characters.
	# 	"""
	# 	clean = re.sub('[\W]+', '', instr)
	# 	if clean == instr:
	# 		return True
	# 	else:
	# 		verbose.error("%s contains non-alphanumeric characters." %instr)
	# 		return False

