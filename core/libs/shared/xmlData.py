#!/usr/bin/python

# [Icarus] xmlData.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Class for handling generic XML data files via ElementTree.
# Classes written to handle specific data files should inherit this class.


import xml.etree.ElementTree as ET
import os
import verbose


class xmlData():

	def __init__(self):
		pass


	def loadXML(self, datafile=None, quiet=False):
		""" Load XML data.
			Omit the keyword argument 'datafile' to reload the data.
			The 'quiet' argument suppresses the warning message if the file doesn't exist.
		"""
		if datafile is not None:
			self.datafile = os.path.normpath(datafile)

		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
			verbose.print_("XML read: %s" %self.datafile, 4)
			return True

		except (IOError, ET.ParseError):
			if not quiet:
				verbose.warning("XML data file is invalid or doesn't exist: %s" %self.datafile)
			self.root = ET.Element('root')
			self.tree = ET.ElementTree(self.root)
			return False


	def saveXML(self):
		""" Save XML data.
		"""
		try:
			self.indent(self.root)
			self.tree.write(self.datafile, xml_declaration=True, encoding='utf-8')
			verbose.print_("XML write: %s" %self.datafile, 4)
			return True

		except:
			verbose.error("XML data file could not be written: %s" %self.datafile)
			return False


	def indent(self, elem, level=0):
		""" Indent elements automatically to prepare nicely formatted XML for output.
		"""
		i = "\n" + level*"\t"
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "\t"
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				self.indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i

