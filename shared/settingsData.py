#!/usr/bin/python

# [Icarus] settingsData.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2018 Gramercy Park Studios
#
# Manipulates settings data stored in an XML database.
# This class is also used to manage asset metadata.


import re
import xml.etree.ElementTree as ET

# Import custom modules
from . import xmlData


class SettingsData(xmlData.XMLData):
	""" Manipulates XML database to store job settings.
		Inherits XMLData class.
	"""

	def getValue(self, category, setting, type='str'):
		""" Get the specified value.
			'type' can be specified in order to return a value of a given
			type, valid values are 'str', 'int', 'float', 'bool'.
		"""
		elem = self.root.find( "./data[@category='%s']/%s" %(category, setting) )
		if elem is not None:
			text = elem.text
			if text is not None:
				if type == 'str':
					return text
				elif type == 'int':
					return int(text)
				elif type == 'float':
					return float(text)
				elif type == 'bool':
					return bool(text)

		#for catElem in self.root.findall('./data'):
		#	if catElem.attrib.get('category') == category:
		#		for settingElem in catElem.findall(setting):
		#			text = settingElem.text
		#			if text is not None:
		#				return text

		return ""  # Return an empty string, not None, so value can be stored in an environment variable without raising an error


	def setValue(self, category, setting, new_value):
		""" Set value. Create elements if they don't exist.
		"""
		catElem = self.root.find("./data[@category='%s']" %category)
		if catElem is None:
			catElem = ET.SubElement(self.root, 'data')
			catElem.set('category', category)

		settingElem = catElem.find(setting)
		if settingElem is None:
			settingElem = ET.SubElement(catElem, setting)

		settingElem.text = str(new_value)


	def removeElement(self, category, setting):
		""" Remove the selected element.
		"""
		cat = self.root.find( "./data[@category='%s']" %category )
		if cat is not None:
			elem = cat.find(setting)
			if elem is not None:
				#print("Removing element: %s" %elem.setting)
				cat.remove(elem)
				return True

		return False


#	def getAttr(self, category, setting, attr):
#		""" Get the specified attribute.
#		"""
#		return self.root.find( "./data[@category='%s']/%s" %(category, setting) ).attrib[attr]


	def getCategories(self):
		""" Return a list of settings categories.
		"""
		cats = self.root.findall("./data")
		c = []
		for cat in cats:
			c.append( cat.get('category') )
		return c


	def getSettings(self, category):
		""" Return a list of settings for a given category.
		"""
		settings = self.root.findall("./data[@category='%s']/option" %category)
		s = []
		for setting in settings:
			s.append( setting.get('type'), setting.get('name'), setting.get('value') )
		return s


	# def getApps(self):
	# 	""" Return list of apps that have been specified in the job settings.
	# 	"""
	# 	a = self.root.find("./data[@category='apps']")
	# 	# a = list(elem.iter())
	# 	print([(elem.tag, elem.text) for elem in a.iter() if elem is not a])
	# 	# print(a)
	# 	# for app in apps:
	# 	# 	a.append((app.get('id'), app.findtext("vendor")))
	# 	# return a


	def getAppVersion(self, app):
		""" Return version for specified app.
		"""
		#appElem = self.root.find("./data[@category='apps']/app[@name='%s']" %app)
		#return appElem.attrib['version']
		try:
			return self.root.find("./data[@category='apps']/%s" %app).text
		except AttributeError:
			return None


	def autoFill(self, path):
		""" Auto-fill the job and project number fields.
			(this function should probably be moved elsewhere)
		"""
		self.setValue('job', 'projnum', self.parseJobPath(path, 'projnum'))
		self.setValue('job', 'jobnum', self.parseJobPath(path, 'jobnum'))


	def parseJobPath(self, path, element):
		""" Find the element (project number, job number) in the job path.
			(this function should probably be moved elsewhere)
		"""
		if element == 'projnum':
			pattern = re.compile(r'\d{6}')
		elif element == 'jobnum':
			pattern = re.compile(r'\d{7}')
		match = pattern.search(path)
		if match is not None:
			return match.group()

		return ""

