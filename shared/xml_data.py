#!/usr/bin/python

# [Icarus] xml_data.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2019 Gramercy Park Studios
#
# Class for handling generic XML data files via ElementTree.
# Classes written to handle specific data files should inherit this class.


import os
import xml.etree.ElementTree as ET

# Import custom modules
from . import os_wrapper
from . import verbose


class XMLData(object):

	def __init__(self, datafile=None):
		if datafile is not None:
			self.datafile = os.path.normpath(datafile)


	def createXML(self):
		""" Create empty XML data file.
		"""
		self.root = ET.Element('root')
		self.tree = ET.ElementTree(self.root)


	def loadXML(self, datafile=None, use_template=False, quiet=False):
		""" Load XML data.
			Omit the keyword argument 'datafile' to reload the data.
			If 'use_template' is true, look for a copy of the XML data in the
			templates directory and copy it over if the datafile doesn't
			already exist.
			The 'quiet' argument suppresses the warning message if the file
			doesn't exist.
		"""
		if datafile is not None:
			self.datafile = os.path.normpath(datafile)

		# If datafile doesn't exist, try to copy it from templates
		if use_template and not os.path.isfile(self.datafile):
			xml_file = os.path.basename(self.datafile)
			template_file = os.path.join(os.environ['IC_BASEDIR'], 'templates', xml_file)
			success, msg = os_wrapper.copy(template_file, self.datafile, quiet=quiet)
			if not quiet:
				if success:
					verbose.print_('XML file "%s" copied from templates.' %xml_file)
				else:
					verbose.warning("XML template could not be copied.")

		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
			verbose.print_('XML read: "%s"' %self.datafile)
			return True

		except (IOError, ET.ParseError):
			if not quiet:
				verbose.warning('XML data file is invalid or doesn\'t exist: "%s"' %self.datafile)
			self.createXML()
			return False


	def saveXML(self):
		""" Save XML data.
		"""
		try:
			self.indent(self.root)
			self.tree.write(self.datafile, xml_declaration=True, encoding='utf-8')
			verbose.print_('XML write: "%s"' %self.datafile)
			return True

		except:
			verbose.error('XML data file could not be written: "%s"' %self.datafile)
			return False


	def indent(self, elem, level=0):
		""" Indent elements automatically to prepare nicely formatted XML for
			output.
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


	def getValue(self, element, tag):
		""" Return the value of 'tag' belonging to 'element'.
		"""
		elem = element.find(tag)
		if elem is not None:
			text = elem.text
			if text is not None:
				return text

