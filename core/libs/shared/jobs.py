#!/usr/bin/python

# [Icarus] jobs.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2016 Gramercy Park Studios
#
# Manipulates the database of jobs running in the CG department


import os
import xml.etree.ElementTree as ET
import xmlData, verbose
import osOps


class jobs(xmlData.xmlData):
	""" Manipulates XML database for storing jobs.
		Add and remove jobs, make jobs active or inactive, modify job properties.
		Inherits xmlData class.
	"""
	def getDict(self):
		""" Read job database from XML file and return dictionary of active jobs.
		"""
		dic = {}

		# for job in root.findall('job'):
		# 	self.joblist[job.find('name').text] = job.find('path').text, job.get('active')

		try:
			# Get OS-specific root paths defined in jobs.xml. Always replace any backslashes with forward-slashes...
			self.win_root = self.root.find('jobs-root/win').text.replace("\\", "/")
			self.osx_root = self.root.find('jobs-root/osx').text.replace("\\", "/")
			self.linux_root = self.root.find('jobs-root/linux').text.replace("\\", "/")

			for job in self.root.findall('job'):
				if job.get('active') == 'True': # Only add jobs tagged as 'active'
					jobpath = job.find('path').text.replace("\\", "/")

					# Temporary (?) fix for cross-platform paths
					if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
						if jobpath.startswith(self.osx_root):
							jobpath = osOps.absolutePath( jobpath.replace(self.osx_root, self.win_root) )
						elif jobpath.startswith(self.linux_root):
							jobpath = osOps.absolutePath( jobpath.replace(self.linux_root, self.win_root) )
					elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
						if jobpath.startswith(self.win_root):
							jobpath = osOps.absolutePath( jobpath.replace(self.win_root, self.osx_root) )
						elif jobpath.startswith(self.linux_root):
							jobpath = osOps.absolutePath( jobpath.replace(self.linux_root, self.osx_root) )
					else:
						if jobpath.startswith(self.win_root):
							jobpath = osOps.absolutePath( jobpath.replace(self.win_root, self.linux_root) )
						elif jobpath.startswith(self.osx_root):
							jobpath = osOps.absolutePath( jobpath.replace(self.osx_root, self.linux_root) )

					if os.path.exists(jobpath): # Only add jobs which exist on disk
						dic[job.find('name').text] = jobpath

			return dic

		except:
			return False
			#sys.exit("ERROR: Jobs file not found, or contents are invalid.")


	# def ls(self):
	# 	"""Print job database in a human-readable pretty format. - NOT YET IMPLEMENTED
	# 	"""


	# def getPath(self, jobName):
	# 	""" Get path of the specified job.
	# 	"""
	# 	self.loadXML(quiet=True) # reload XML data
	# 	#element = self.root.find("./job[@id='%s']" %jobID)
	# 	element = self.root.find('./job')
	# 	if element.find('name').text == jobName:
	# 		return element.find('path').text


	# def refresh(self):
	# 	"""Reload job database. - REDUNDANT?
	# 	"""
	# 	self.readjobs()


	# def add(self, jobName, jobPath):
	# 	"""Add a new job to the database.
	# 	"""
	# 	self.joblistactive[jobName] = jobPath


	# def rm(self, jobName):
	# 	"""Remove a job from the database.
	# 	"""
	# 	#del self.joblist[jobName]
	# 	print 'deleting %s' %jobName


	# def modify(self, jobName, jobPath, active):
	# 	"""Modify job properties, currently name, path, and active status.
	# 	"""

