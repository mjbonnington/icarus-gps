#!/usr/bin/python

# [Icarus] appPaths.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Manipulate an XML database of application version paths.


import xml.etree.ElementTree as ET

# Import custom modules
import verbose
import xmlData


class appPaths(xmlData.XMLData):
	""" Manipulates XML database to store application version paths.
		Inherits XMLData class.
	"""

	def getApps(self):
		""" Return all apps as elements.
		"""
		return self.root.findall('./app')


	def sortByName(self, elem):
		return elem.get("name")

	def sortByCategory(self, elem):
		return elem.findtext("category")

	def sortByVendor(self, elem):
		return elem.findtext("vendor")


	def getVisibleApps(self, sortBy=None):
		""" Return all visible (launchable) apps as elements.
		"""
		apps = self.root.findall("./app[@visible='True']")
		if sortBy == "Name":
			apps[:] = sorted(apps, key=self.sortByName)
		elif sortBy == "Category":
			apps[:] = sorted(apps, key=self.sortByCategory)
		elif sortBy == "Vendor":
			apps[:] = sorted(apps, key=self.sortByVendor)
		return apps


	def getAppIDs(self):
		""" Return list of apps (short name / ID).
		"""
		apps = self.root.findall('./app')
		a = []
		for app in apps:
			a.append( app.get('id') )
		return a


	def getAppNames(self):
		""" Return list of apps (long / display name).
		"""
		apps = self.root.findall('./app')
		a = []
		for app in apps:
			a.append( app.get('name') )
		return a


	def deleteApp(self, app):
		""" Delete selected app.
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			self.root.remove(appElem)
		except ValueError:
			verbose.appPaths_noApp(app)


	def getVersions(self, app):
		""" Return list of versions associated with app.
		"""
		vers = self.root.findall("./app[@name='%s']/path" %app)
		v = []
		for ver in vers:
			v.append( ver.get('version') )
		return v


	def deleteVersion(self, app, ver):
		""" Delete selected version.
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			verElem = appElem.find("path[@version='%s']" %ver)
		except AttributeError:
			verbose.appPaths_noApp(app)

		try:
			appElem.remove(verElem)
		except (AttributeError, ValueError):
			verbose.appPaths_noVersion(app, ver)


	def getPath(self, app, ver, os):
		""" Return executable path.
		"""
		elem = self.root.find( "./app[@name='%s']/path[@version='%s']/%s" %(app, ver, os) )
		if elem is not None:
			text = elem.text
			if text is not None:
				return text

		return ""


	def setPath(self, app, ver, os, newText):
		""" Set path. Create elements if they don't exist.
		"""
		if (ver == "") or (ver is None):
			verbose.appPaths_enterVersion()

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
		""" Guess app path based on template (if it exists).
		"""
		path = self.root.find( "./app[@name='%s']/path[@version='[template]']/%s" %(app, os) )

		ver_major = ver.split('v')[0]  # Hack for Nuke major version

		try:
			guessedPath = path.text.replace( "[ver]", ver )
			guessedPath = guessedPath.replace( "[ver-major]", ver_major )
		except AttributeError:
			verbose.appPaths_guessPathFailed(os)
			guessedPath =  None

		return guessedPath


	def getSubMenus(self, app):
		""" Return list of sub-menu items associated with app.
		"""
		return self.root.findall("./app[@id='%s']/submenu[@visible='True']" %app)
		# items = self.root.findall("./app[@id='%s']/submenu[@visible='True']" %app)
		# item_ls = []
		# for item in items:
		# 	item_ls.append((item.get('name'), item.findtext('flag')))
		# return item_ls

