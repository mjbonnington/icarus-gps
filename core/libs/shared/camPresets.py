#!/usr/bin/python

# Camera Presets
# v0.1
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Manipulates camera presets data stored in an XML database


import xml.etree.ElementTree as ET
import xmlData


class camPresets(xmlData.xmlData):
	""" Manipulates XML database to store camera presets.
		Inherits xmlData class
	"""

	def getPresets(self, activeOnly=False):
		""" Return a list of camera presets
		"""
		elements = self.root.findall("./camera")
		presets = []
		for element in elements:
			if activeOnly:
				if element.get('active') == 'True':
					presets.append( element.get('name') )
			else:
				presets.append( element.get('name') )
		return presets


	def getFilmback(self, camera, inches=False):
		""" Get the filmback (as a tuple) for the specified camera.
			Units in millimetres unless 'inches' is true
		"""
		sensor_w = float( self.root.find("./camera[@name='%s']/sensor_w_mm" %camera).text )
		sensor_h = float( self.root.find("./camera[@name='%s']/sensor_h_mm" %camera).text )

		if(inches):
			sensor_w = sensor_w / 25.4
			sensor_h = sensor_h / 25.4

		return (sensor_w, sensor_h)


	def getValue(self, preset, setting):
		""" Get the specified value
		"""
		element = self.root.find( "./camera[@name='%s']/%s" %(preset, setting) )
		if element is not None:
			text = element.text
			if text is not None:
				return text

		return ""
