#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#support	:Michael Bonnington - mike.bonnington@gps-ldn.com
#title    	:jobLs
#copyright	:Gramercy Park Studios

#This file holds the jobs running in the CG Department

import os, sys
import xml.etree.ElementTree as ET


# Legacy code to work with current icarus implementation
dic = {}
try:
	tree = ET.parse(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'jobs.xml'))
	root = tree.getroot()
	for job in root.findall('job'):
		if job.get('active') == 'True': # Only add jobs tagged as 'active'
			if os.path.exists(job.find('path').text): # Only add jobs which exist on disk
				dic[job.find('name').text] = job.find('path').text
except:
	sys.exit("ERROR: Jobs file not found.")


class jobs():
	"""Deals with the current jobs database.
	Add and remove jobs, make jobs active or inactive, modify job properties."""

	def __init__(self, datafile, active=True):
		self.joblist = {}
		#self.datafile = os.path.join(os.environ['PIPELINE'], 'core', 'config', 'jobs.xml')
		self.datafile = datafile
		self.readjobs()

		tree = ET.parse(datafile)
		self.root = tree.getroot()

	def ls(self):
		"""Print job database in a human-readable pretty format - NOT YET IMPLEMENTED"""

	def readjobs(self):
		"""Read job database from XML file and store active jobs in dictionary"""

		tree = ET.parse(self.datafile)
		root = tree.getroot()
		for job in root.findall('job'):
			self.joblist[job.find('name').text] = job.find('path').text, job.get('active')

	def writejobs(self):
		"""Write job database to XML file - NOT YET IMPLEMENTED"""

	def refresh(self):
		"""Reload job database"""

		self.readjobs()

	def add(self, jobName, jobPath):
		"""Add a new job to the database"""

		self.joblistactive[jobName] = jobPath

	def rm(self, jobName):
		"""Remove a job from the database"""

		#del self.joblist[jobName]

	def modify(self, jobName, jobPath, active):
		"""Modify job properties, currently name, path, and active status"""

