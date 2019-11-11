#!/usr/bin/python

# [Icarus] resPresets.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Manipulates resolution presets data stored in an XML database.


#import xml.etree.ElementTree as ET

# Import custom modules
import xmlData


class ResPresets(xmlData.XMLData):
	""" Manipulates XML database to store resolution presets.
		Inherits XMLData class.
	"""

	def getPresets(self):
		""" Return a list of resolution presets.
		"""
		elements = self.root.findall("./resolution")
		presets = []
		for element in elements:
			presets.append( element.get('name') )
		return presets


	def getValue(self, preset, setting):
		""" Get the specified value.
		"""
		element = self.root.find( "./resolution[@name='%s']/%s" %(preset, setting) )
		if element is not None:
			text = element.text
			if text is not None:
				return text

		return ""


	def getPresetFromRes(self, width, height, par=1.0):
		""" Return a resolution preset given the pixel dimensions (width and
			height).
			PAR (pixel aspect ratio) is optional.
		"""
		elements = self.root.findall('./resolution')
		presets = []
		for element in elements:
			w = element.find('./width').text
			h = element.find('./height').text
			p = element.find('./par').text
			if w==str(width) and h==str(height) and p==str(par):
				#print(w, h, p)
				return element.get('name')

		return "Custom"

