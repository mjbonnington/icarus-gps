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
	""" Manipulates XML database to store job settings.
		Inherits xmlData class
		TODO: Rewrite to avoid using XPath expressions, as they are not fully supported by the version of the ElementTree module included with Python 2.6
	"""

	def getValue(self, category, setting):
		""" Get the specified value
		"""
		elem = self.root.find( "./data[@category='%s']/%s" %(category, setting) )
		if elem is not None:
			text = elem.text
			if text is not None:
				return text

		#for catElem in self.root.findall('./data'):
		#	if catElem.attrib.get('category') == category:
		#		for settingElem in catElem.findall(setting):
		#			text = settingElem.text
		#			if text is not None:
		#				return text

		return "" # return an empty string, not None, so value can be stored in an environment variable without raising an error


	def setValue(self, category, setting, newValue):
		""" Set value. Create elements if they don't exist
		"""
		catElem = self.root.find("./data[@category='%s']" %category)
		if catElem is None:
			catElem = ET.SubElement(self.root, 'data')
			catElem.set('category', category)

		settingElem = catElem.find(setting)
		if settingElem is None:
			settingElem = ET.SubElement(catElem, setting)

		settingElem.text = str(newValue)


	def removeElement(self, category, setting):
		""" Remove the selected element
		"""
		cat = self.root.find( "./data[@category='%s']" %category )
		if cat is not None:
			elem = cat.find(setting)
			if elem is not None:
				#print "Removing element: %s" %elem.setting
				cat.remove(elem)
				return True

		return False


#	def getAttr(self, category, setting, attr):
#		""" Get the specified attribute
#		"""
#		return self.root.find( "./data[@category='%s']/%s" %(category, setting) ).attrib[attr]


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

