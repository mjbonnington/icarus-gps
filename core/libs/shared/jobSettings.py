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

	def getText(self, xpath):
		""" Get the specified value
		"""
		return self.root.find(xpath).text


	def getAttr(self, xpath, attr):
		""" Get the specified attribute
		"""
		return self.root.find(xpath).attrib[attr]


	def getApps(self):
		""" Return a list of apps with preferred versions
		"""
		apps = self.root.findall("./apps/app")
		a = []
		for app in apps:
			a.append( (app.get('name'), app.get('version')) )
		return a


	def deleteApp(self, app):
		""" Delete selected app
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			self.root.remove(appElem)
		except ValueError:
			print "Warning: Application '%s' does not exist." %app


	def getVersions(self, app):
		""" Return list of versions associated with app
		"""
		vers = self.root.findall("./app[@name='%s']/path" %app)
		v = []
		for ver in vers:
			v.append( ver.get('version') )
		return v


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


	def setPath(self, app, ver, os, newText):
		""" Set path. Create elements if they don't exist
		"""
		if (ver == "") or (ver is None):
			print "Please enter a version."

		else:
			appElem = self.root.find("app[@name='%s']" %app)
			if(appElem is None):
				appElem = ET.SubElement(self.root, 'app')
				appElem.set('name', app)

			verElem = appElem.find("path[@version='%s']" %ver)
			if(verElem is None):
				verElem = ET.SubElement(appElem, 'path')
				verElem.set('version', ver)

			pathElem = verElem.find(os)
			if(pathElem is None):
				pathElem = ET.SubElement(verElem, os)

			pathElem.text = newText


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

