#!/usr/bin/python

# Resolution Presets
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Manipulates resolution presets data stored in an XML database


import xml.etree.ElementTree as ET
import xmlData


class resPresets(xmlData.xmlData):
	""" Manipulates XML database to store resolution presets
		Inherits xmlData class
	"""

	def getPresets(self):
		""" Return a list of resolution presets
		"""
		elements = self.root.findall("./resolution")
		presets = []
		for element in elements:
			presets.append( element.get('name') )
		return presets


	def getValue(self, preset, tag):
		""" Get the specified value
		"""
		element = self.root.find( "./resolution[@name='%s']/%s" %(preset, tag) )
		if element is not None:
			text = element.text
			if text is not None:
				return text

		return ""


	def getPresetFromRes(self, width, height, par=1.0):
		""" Return a resolution preset given the pixel dimensions (width and height).
			PAR (pixel aspect ratio) is optional
		"""
		elements = self.root.findall("./resolution")
		presets = []
		for element in elements:
			w = element.find("./width").text
			h = element.find("./height").text
			p = element.find("./par").text
			if w==str(width) and h==str(height) and p==str(par):
				#print w, h, p
				return element.get('name')

		return "Custom"


#	def setValue(self, category, tag, newValue):
#		""" Set value. Create elements if they don't exist
#		"""
#		catElem = self.root.find("./data[@category='%s']" %category)
#		if catElem is None:
#			catElem = ET.SubElement(self.root, 'data')
#			catElem.set('category', category)
#
#		tagElem = catElem.find(tag)
#		if tagElem is None:
#			tagElem = ET.SubElement(catElem, tag)
#
#		tagElem.text = newValue

