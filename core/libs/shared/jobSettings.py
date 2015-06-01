#!/usr/bin/python

# Job Settings
# v0.2
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Manipulates job settings data stored in an XML database


import xml.etree.ElementTree as ET
import xmlData


class jobSettings(xmlData.xmlData):
	""" Manipulates XML database to store job settings
		Inherits xmlData class
	"""

	def getValue(self, category, tag):
		""" Get the specified value
		"""
		elem = self.root.find( "./data[@category='%s']/%s" %(category, tag) )
		if elem is not None:
			text = elem.text
			if text is not None:
				return text

		return ""
	#	try:
	#		return self.root.find( "./data[@category='%s']/%s" %(category, tag) ).text
	#	except AttributeError:
	#		return "" # Must return string if value is being returned into an environment variable


	def setValue(self, category, tag, newValue):
		""" Set value. Create elements if they don't exist
		"""
		catElem = self.root.find("./data[@category='%s']" %category)
		if catElem is None:
			catElem = ET.SubElement(self.root, 'data')
			catElem.set('category', category)

		tagElem = catElem.find(tag)
		if tagElem is None:
			tagElem = ET.SubElement(catElem, tag)

		tagElem.text = str(newValue)


#	def getAttr(self, category, tag, attr):
#		""" Get the specified attribute
#		"""
#		return self.root.find( "./data[@category='%s']/%s" %(category, tag) ).attrib[attr]


	def getCategories(self):
		""" Return a list of settings categories
		"""
		cats = self.root.findall("./data")
		c = []
		for cat in cats:
			c.append( cat.get('category') )
		return c


	def getSettings(self, category):
		""" Return a list of settings for a given category
		"""
		settings = self.root.findall("./data[@category='%s']/option" %category)
		s = []
		for setting in settings:
			s.append( setting.get('type'), setting.get('name'), setting.get('value') )
		return s


	def getAppVersion(self, app):
		""" Return version for specified app
		"""
		#appElem = self.root.find("./data[@category='apps']/app[@name='%s']" %app)
		#return appElem.attrib['version']
		return self.root.find( "./data[@category='apps']/%s" %app ).text

