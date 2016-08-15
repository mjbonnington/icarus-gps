#!/usr/bin/python

# [Icarus] appPaths.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Manipulate an XML database of application version paths.


import xml.etree.ElementTree as ET
import xmlData, verbose


class appPaths(xmlData.xmlData):
	""" Manipulates XML database to store application version paths
		Inherits xmlData class
	"""

	def getApps(self):
		""" Return list of apps
		"""
		apps = self.root.findall('./app')
		a = []
		for app in apps:
			a.append( app.get('name') )
		return a


	def deleteApp(self, app):
		""" Delete selected app
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			self.root.remove(appElem)
		except ValueError:
			verbose.appPaths_noApp(app)
			#print "Warning: Application '%s' does not exist." %app


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
			verbose.appPaths_noApp(app)
			#print "Warning: Application '%s' does not exist." %app

		try:
			appElem.remove(verElem)
		except (AttributeError, ValueError):
			verbose.appPaths_noVersion(app, ver)
			#print "Warning: Application '%s' has no '%s' version." %(app, ver)


	def getPath(self, app, ver, os):
		""" Return executable path
		"""
		elem = self.root.find( "./app[@name='%s']/path[@version='%s']/%s" %(app, ver, os) )
		if elem is not None:
			text = elem.text
			if text is not None:
				return text

		return ""


	def setPath(self, app, ver, os, newText):
		""" Set path. Create elements if they don't exist
		"""
		if (ver == "") or (ver is None):
			verbose.appPaths_enterVersion()
			#print "Please enter a version."

		else:
			appElem = self.root.find("app[@name='%s']" %app)
			if appElem is None:
				appElem = ET.SubElement(self.root, 'app')
				appElem.set('name', app)

			verElem = appElem.find("path[@version='%s']" %ver)
			if verElem is None:
				verElem = ET.SubElement(appElem, 'path')
				verElem.set('version', ver)

			pathElem = verElem.find(os)
			if pathElem is None:
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
			verbose.appPaths_guessPathFailed(os)
			#print "Warning: Failed to guess %s path." %os
			guessedPath =  None

		return guessedPath

