#!/usr/bin/python

# appPaths.py
# support	: Michael Bonnington - mike.bonnington@gps-ldn.com
# copyright	: Gramercy Park Studios

# Stores an XML database of application version paths.


#import os
import xml.etree.ElementTree as ET
#from xml.dom import minidom


class appPaths():
	"""Manipulates XML database to store application version paths.
	"""
	def __init__(self, datafile):
		self.datafile = datafile

		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
		except (IOError, ET.ParseError):
			print "Warning: XML data file is invalid or doesn't exist."
			self.root = ET.Element('root')
			self.tree = ET.ElementTree(self.root)


	def getApps(self):
		"""Return list of apps.
		"""
		apps = self.root.findall('./app')
		a = []
		for app in apps:
			a.append( app.get('name') )
		return a


	def deleteApp(self, app):
		"""Delete selected app.
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			self.root.remove(appElem)
		except ValueError:
			print "Warning: Application '%s' does not exist." %app


	def getVersions(self, app):
		"""Return list of versions associated with app.
		"""
		vers = self.root.findall("./app[@name='%s']/path" %app)
		v = []
		for ver in vers:
			v.append( ver.get('version') )
		return v


	def deleteVersion(self, app, ver):
		"""Delete selected version.
		"""
		appElem = self.root.find("./app[@name='%s']" %app)
		try:
			verElem = appElem.find("path[@version='%s']" %ver)
		except AttributeError:
			print "Warning: Application '%s' does not exist." %app

		try:
			appElem.remove(verElem)
		except AttributeError:
			print "Warning: Application '%s' has no '%s' version." %(app, ver)


	def getPath(self, app, ver, os):
		"""Return executable path.
		"""
		path = self.root.find( "./app[@name='%s']/path[@version='%s']/%s" %(app, ver, os) )
		if path is not None:
			return path.text
		else:
			return ""


	def setPath(self, app, ver, os, newText):
		"""Set path. Create elements if they don't exist.
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
		"""Guess app path based on template (if it exists).
		"""
		path = self.root.find( "./app[@name='%s']/path[@version='[template]']/%s" %(app, os) )

		# hack for nuke major version
		ver_major = ver.split('v')[0]

		try:
			guessedPath = path.text.replace( "[ver]", ver )
			guessedPath = guessedPath.replace( "[ver-major]", ver_major )
		except AttributeError:
			print "Warning: Failed to guess %s path." %os
			guessedPath =  None

		return guessedPath


#	def prettify(self, elem):
#		"""Return a pretty-printed XML string for the element.
#		"""
#		rough_string = ET.tostring(elem, 'utf-8')
#		reparsed = minidom.parseString(rough_string)
#		return reparsed.toprettyxml(indent="\t")


	def indent(self, elem, level=0):
		"""Indent elements automatically to create nicely formatted XML.
		"""
		i = "\n" + level*"\t"
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "\t"
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				self.indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i


	def saveXML(self):
		"""Save XML data.
		"""
		#print self.prettify(self.root)
		self.indent(self.root)
		self.tree.write(self.datafile, xml_declaration=True, encoding='utf-8')
