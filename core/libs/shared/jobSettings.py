#!/usr/bin/python

# Job Settings
# v0.1
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

	def getText(self, category, tag):
		""" Get the specified value
		"""
		return self.root.find( "./data[@category='%s']/%s" %(category, tag) ).text


	def getAttr(self, category, tag, attr):
		""" Get the specified attribute
		"""
		return self.root.find( "./data[@category='%s']/%s" %(category, tag) ).attrib[attr]


	def getCategories(self):
		""" Return a list of settings categories
		"""
		cats = self.root.findall("./data")
		c = []
		for cat in cats:
			c.append( cat.get('category') )
		return c


	def getAppVersion(self, app):
		""" Return version for specified app
		"""
		appElem = self.root.find("./data[@category='apps']/app[@name='%s']" %app)
		return appElem.attrib['version']


	def getSettings(self, category):
		""" Return a list of settings for a given category
		"""
		settings = self.root.findall("./data[@category='%s']/option" %category)
		s = []
		for setting in settings:
			s.append( setting.get('type'), setting.get('name'), setting.get('value') )
		return s


	def setText(self, category, tag, newText):
		""" Set text. Create elements if they don't exist
		"""
		catElem = self.root.find("./data[@category='%s']" %category)
		if catElem is None:
			catElem = ET.SubElement(self.root, 'data')
			catElem.set('category', category)

		tagElem = catElem.find(tag)
		if tagElem is None:
			tagElem = ET.SubElement(catElem, tag)

		tagElem.text = newText


#	def getApps(self):
#		""" Return a list of apps with preferred versions
#		"""
#		apps = self.root.findall("./apps/app")
#		a = []
#		for app in apps:
#			a.append( (app.get('name'), app.get('version')) )
#		return a


	def deleteApp(self, app):
		""" Delete selected app
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			self.root.remove(appElem)
		except ValueError:
			print "Warning: Application '%s' does not exist." %app


	def deleteVersion(self, app, ver):
		""" Delete selected version
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			verElem = appElem.find("path[@version='%s']" %ver)
		except AttributeError:
			print "Warning: Application '%s' does not exist." %app

		try:
			appElem.remove(verElem)
		except (AttributeError, ValueError):
			print "Warning: Application '%s' has no '%s' version." %(app, ver)


	def getPath(self, app, ver, os):
		""" Return executable path
		"""
		path = self.root.find( "./app[@name='%s']/path[@version='%s']/%s" %(app, ver, os) )
		if path is not None:
			return path.text
		else:
			return ""


	def guessPath(self, app, ver, os):
		""" Guess app path based on template (if it exists)
		"""
		path = self.root.find( "./app[@name='%s']/path[@version='[template]']/%s" %(app, os) )

		ver_major = ver.split('v')[0]	# hack for nuke major version

		try:
			guessedPath = path.text.replace( "[ver]", ver )
			guessedPath = guessedPath.replace( "[ver-major]", ver_major )
		except AttributeError:
			print "Warning: Failed to guess %s path." %os
			guessedPath =  None

		return guessedPath

