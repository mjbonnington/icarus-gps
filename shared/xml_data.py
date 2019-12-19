#!/usr/bin/python

# [Icarus] xml_data.py
#
# Mike Bonnington <mjbonnington@gmail.com>
# (c) 2015-2019
#
# Class for handling generic XML data files via ElementTree.
# Classes written to handle specific data files should inherit this class.


import os
import xml.etree.ElementTree as ET

# Import custom modules
from . import os_wrapper
from . import verbose


class XMLData(object):
	""" Class for XML data.
	"""
	def __init__(self, datafile=None):
		""" Initialise class. If datafile is not specified, create bare
			class. The data should then be loaded with the load() method.
		"""
		verbose.debug("%s" % self)

		self._create()
		if datafile is not None:
			self.load(datafile)


	def _create(self):
		""" Create empty ElementTree XML data structure.
		"""
		self.root = ET.Element('root')
		self.tree = ET.ElementTree(self.root)


	def load(self, datafile):
		""" Load data from datafile and store in an ElementTree.
		"""
		self.datafile = os.path.normpath(datafile)
		return self.reload()


	def reload(self):
		""" Reload data from current datafile.
		"""
		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
			verbose.print_('XML load: "%s"' % self.datafile)
			return True

		except (IOError, ET.ParseError):
			verbose.warning('XML file is invalid or doesn\'t exist: "%s"' % self.datafile)
			return False


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
					verbose.print_('XML file "%s" copied from templates.' % xml_file)
				else:
					verbose.warning("XML template could not be copied.")

		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
			verbose.print_('XML load: "%s"' % self.datafile)
			return True

		except (IOError, ET.ParseError):
			if not quiet:
				verbose.warning('XML file is invalid or doesn\'t exist: "%s"' % self.datafile)
			# self._create()
			return False


	def save(self):
		""" Save ElementTree to datafile.
		"""
		try:
			self._indent(self.root)
			self.tree.write(
				self.datafile, xml_declaration=True, encoding='utf-8')
			verbose.print_('XML save: "%s"' % self.datafile)
			return True

		except IOError:
			verbose.error('XML file could not be written: "%s"' % self.datafile)
			return False


	def clear(self):
		""" Clear all data from the ElementTree.
		"""
		self._create()


	def _indent(self, elem, level=0):
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
				self._indent(elem, level+1)
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
