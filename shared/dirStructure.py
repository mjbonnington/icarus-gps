#!/usr/bin/python

# [Icarus] dirStructure.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2017-2018 Gramercy Park Studios
#
# Represent directory structures as XML.


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
	def _create_tree_recursive(self, element, basedir=None):
		""" Recursively create directory tree.
		"""
		# Create directories
		for directory in element.findall('dir'):
			name = directory.get('name')
			env = directory.get('env')

			# if self.checkIllegalChars(name):
			# newdir = os.path.join(basedir, name)
			newdir = osOps.absolutePath('%s/%s' %(basedir, name))
			if self.createDirs:
				if not os.path.isdir(newdir):
					osOps.createDir(newdir)

			# Set environment variables
			if self.createEnvVars:
				if env:
					os.environ[env] = newdir

			self._create_tree_recursive(directory, newdir)

		# Create files
		for file in element.findall('file'):
			name = file.get('name')
			env = file.get('env')

			newfile = osOps.absolutePath('%s/%s' %(basedir, name))
			if self.createFiles:
				if not os.path.isfile(newfile):
					src = osOps.absolutePath('%s/%s' %(os.path.dirname(self.datafile), name))
					osOps.copy(src, newfile)

			# Set environment variables
			if self.createEnvVars:
				if env:
					os.environ[env] = newfile

		return


	def createDirStructure(self, datafile=None, createDirs=True, 
		                   createFiles=True, createEnvVars=True):
		""" Create folder structure from XML definition.
		"""
		if datafile is not None:
			self.loadXML(datafile)

		self.createDirs = createDirs
		self.createFiles = createFiles
		self.createEnvVars = createEnvVars

		basedir = self.root.get('location')

		if basedir:
			self._create_tree_recursive(self.root, basedir)
		else:
			verbose.warning("Could not create project folders because the root folder was not specified.")


	def createXML(self, basedir, datafile=None):
		""" Create XML definition of folder structure.
		"""
		if datafile is not None:
			self.loadXML(datafile)

		self.root.set('location', basedir) # need to add env vars

		subdirs = next(os.walk(basedir))[1]
		if subdirs:
			subdirs.sort()
			for subdir in subdirs:
				dir_elem = ET.Element('dir')
				dir_elem.set('name', subdir)
				#dir_elem.set('env', env_var)

		self.saveXML(datafile)


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

