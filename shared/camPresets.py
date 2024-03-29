#!/usr/bin/python

# [Icarus] camPresets.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Manipulates camera presets stored in an XML database.


#import xml.etree.ElementTree as ET

# Import custom modules
from . import xml_data


class CamPresets(xml_data.XMLData):
	""" Manipulates XML database to store camera presets.
		Inherits XMLData class.
	"""

	def getPresets(self, activeOnly=False):
		""" Return a list of camera presets.
			If 'activeOnly' is True, only cameras marked as active will be
			returned.
		"""
		elements = self.root.findall('./camera')
		presets = []
		for element in elements:
			if activeOnly:
				if element.get('active') == 'True':
					presets.append(element.get('name'))
			else:
				presets.append(element.get('name'))
		return presets


	def getFilmback(self, camera, inches=False):
		""" Get the filmback (as a tuple) for the specified camera.
			Units in millimetres unless 'inches' is True.
		"""
		try:
			sensor_w = float(self.root.find("./camera[@name='%s']/sensor_w_mm" %camera).text)
			sensor_h = float(self.root.find("./camera[@name='%s']/sensor_h_mm" %camera).text)
		except AttributeError:  # Defaults
			sensor_w = 36
			sensor_h = 24

		if(inches):
			sensor_w = sensor_w / 25.4
			sensor_h = sensor_h / 25.4

		return (sensor_w, sensor_h)

