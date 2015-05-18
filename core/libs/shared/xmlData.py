#!/usr/bin/python

# XML Data
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Class for handling XML data files via ElementTree


import xml.etree.ElementTree as ET


class xmlData():

	def __init__(self):
		pass

		#print "Attempting to load %s" %datafile
		#self.loadXML()


	def loadXML(self, datafile):
		""" Load XML data
		"""
		self.datafile = datafile

		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
			return True
		except (IOError, ET.ParseError):
			print "Warning: XML data file is invalid or doesn't exist: %s" %datafile
			self.root = ET.Element('root')
			self.tree = ET.ElementTree(self.root)
			return False


	def indent(self, elem, level=0):
		""" Indent elements automatically to create nicely formatted XML
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


	def saveXML(self):
		""" Save XML data
		"""
		try:
			self.indent(self.root)
			self.tree.write(self.datafile, xml_declaration=True, encoding='utf-8')
			return True
		except:
			return False

