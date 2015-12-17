#!/usr/bin/python

# Jobs
# v0.2
#
# Michael Bonnington 2015
# Gramercy Park Studios
#
# Manipulates the database of jobs running in the CG department


import os, sys
import xml.etree.ElementTree as ET


# Legacy code to work with current icarus implementation...
dic = {}
try:
	tree = ET.parse(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'jobs.xml'))
	root = tree.getroot()

	# Get OS-specific root paths defined in jobs.xml. Always replace any backslashes with forward-slashes...
	win_root = root.find('jobs-root/win').text.replace("\\", "/")
	osx_root = root.find('jobs-root/osx').text.replace("\\", "/")
	linux_root = root.find('jobs-root/linux').text.replace("\\", "/")

	for job in root.findall('job'):
		if job.get('active') == 'True': # Only add jobs tagged as 'active'
			jobpath = job.find('path').text.replace("\\", "/")

			# Temporary (?) fix for cross-platform paths
			if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
				if jobpath.startswith(osx_root):
					jobpath = os.path.normpath( jobpath.replace(osx_root, win_root) )
				elif jobpath.startswith(linux_root):
					jobpath = os.path.normpath( jobpath.replace(linux_root, win_root) )
			elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				if jobpath.startswith(win_root):
					jobpath = os.path.normpath( jobpath.replace(win_root, osx_root) )
				elif jobpath.startswith(linux_root):
					jobpath = os.path.normpath( jobpath.replace(linux_root, osx_root) )
			else:
				if jobpath.startswith(win_root):
					jobpath = os.path.normpath( jobpath.replace(win_root, linux_root) )
				elif jobpath.startswith(osx_root):
					jobpath = os.path.normpath( jobpath.replace(osx_root, linux_root) )

			if os.path.exists(jobpath): # Only add jobs which exist on disk
				dic[job.find('name').text] = jobpath

except:
	sys.exit("ERROR: Jobs file not found, or contents are invalid.")

if not dic:
	sys.exit("ERROR: No active jobs found.")


class jobs():
	"""Deals with the current jobs database.
	   Add and remove jobs, make jobs active or inactive, modify job properties.
	"""
	def __init__(self, datafile):
		self.joblist = {}
		self.datafile = datafile

		try:
			self.tree = ET.parse(self.datafile)
			self.root = self.tree.getroot()
		except (IOError, ET.ParseError):
			print "Warning: XML data file is invalid or doesn't exist."
			self.root = ET.Element('root')
			self.tree = ET.ElementTree(self.root)


	def ls(self):
		"""Print job database in a human-readable pretty format. - NOT YET IMPLEMENTED
		"""


#	def getPath(self, jobName):
#		"""Get path
#		"""
#		path = self.root.find('job')
#		return path.find('path').text


	def readjobs(self):
		"""Read job database from XML file and store active jobs in dictionary.
		"""
		for job in root.findall('job'):
			self.joblist[job.find('name').text] = job.find('path').text, job.get('active')


	def writejobs(self):
		"""Write job database to XML file. - NOT YET IMPLEMENTED
		"""


	def refresh(self):
		"""Reload job database. - REDUNDANT?
		"""
		self.readjobs()


	def add(self, jobName, jobPath):
		"""Add a new job to the database.
		"""
		self.joblistactive[jobName] = jobPath


	def rm(self, jobName):
		"""Remove a job from the database.
		"""
		#del self.joblist[jobName]
		print 'deleting %s' %jobName


	def modify(self, jobName, jobPath, active):
		"""Modify job properties, currently name, path, and active status.
		"""

