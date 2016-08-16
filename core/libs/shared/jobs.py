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
	def getRootPaths(self):
		""" Get root paths.
		"""
		try:
			self.win_root = self.root.find('jobs-root/win').text
			self.osx_root = self.root.find('jobs-root/osx').text
			self.linux_root = self.root.find('jobs-root/linux').text
		except AttributeError:
			self.win_root = None
			self.osx_root = None
			self.linux_root = None


	def setRootPaths(self, winPath=None, osxPath=None, linuxPath=None):
		""" Set root paths. Create elements if they don't exist.
		"""
		jobsRootElement = self.root.find("./jobs-root")
		if jobsRootElement is None:
			jobsRootElement = ET.SubElement(self.root, 'jobs-root')

		if winPath is not None:
			pathElement = jobsRootElement.find('win')
			if pathElement is None:
				pathElement = ET.SubElement(jobsRootElement, 'win')
			pathElement.text = str(winPath)

		if osxPath is not None:
			pathElement = jobsRootElement.find('osx')
			if pathElement is None:
				pathElement = ET.SubElement(jobsRootElement, 'osx')
			pathElement.text = str(osxPath)

		if linuxPath is not None:
			pathElement = jobsRootElement.find('linux')
			if pathElement is None:
				pathElement = ET.SubElement(jobsRootElement, 'linux')
			pathElement.text = str(linuxPath)



	def getJobs(self):
		""" Return all jobs as elements.
		"""
		return self.root.findall("./job")


	def getDict(self):
		""" Read job database from XML file and return dictionary of active jobs. Bit untidy atm
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

			# Root paths for cross-platform support
			if os.environ['ICARUS_RUNNING_OS'] == 'Windows':
				os.environ['FILESYSTEMROOT'] = self.win_root
			elif os.environ['ICARUS_RUNNING_OS'] == 'Darwin':
				os.environ['FILESYSTEMROOT'] = self.osx_root
			else:
				os.environ['FILESYSTEMROOT'] = self.linux_root

			os.environ['JOBSROOTWIN'] = self.win_root
			os.environ['JOBSROOTOSX'] = self.osx_root
		#	os.environ['JOBSROOTLINUX'] = self.linux_root # not currently required as Linux & OSX mount points should be the same

			return dic

		except:
			return False
			#sys.exit("ERROR: Jobs file not found, or contents are invalid.")


	def addJob(self, jobName="New_Job", jobPath="", active=True):
		""" Add a new job to the database.
		"""
		jobElement = self.root.find("./job[name='%s']" %jobName)
		if jobElement is None:
			jobElement = ET.SubElement(self.root, 'job')
			jobElement.set('active', str(active))

			nameElement = ET.SubElement(jobElement, 'name')
			nameElement.text = str(jobName)

			pathElement = ET.SubElement(jobElement, 'path')
			pathElement.text = str(jobPath)
			return True

		else:
			verbose.error("Could not create job as a job with the name '%s' already exists." %jobName)
			return False


	def renameJob(self, jobName, newJobName):
		""" Rename job.
		"""
		if newJobName == jobName: # do nothing
			return True

		jobElement = self.root.find("./job/[name='%s']" %newJobName)
		if jobElement is None:
			element = self.root.find("./job/[name='%s']" %jobName)
			if element is not None:
				element.find('name').text = newJobName
				return True

		else:
			verbose.error("Could not rename job as a job with the name '%s' already exists." %newJobName)
			return False


	def deleteJob(self, jobName):
		""" Delete job by name.
		"""
		element = self.root.find("./job/[name='%s']" %jobName)
		if element is not None:
			#print "Deleted job %s" %jobName
			self.root.remove(element)
			return True
		else:
			#print "Could not delete job %s" %jobName
			return False


	def getEnabled(self, jobName):
		""" Get enable/disable status of the specified job.
		"""
		#element = self.root.find("./job[@id='%s']" %jobID)
		element = self.root.find("./job[name='%s']" %jobName)
		if element is not None:
			if element.get('active') == 'True':
				return True
			else:
				return False


	def enableJob(self, jobName, active):
		""" Enable/disable job by name.
		"""
		element = self.root.find("./job/[name='%s']" %jobName)
		if element is not None:
			#print "Set job %s active status to %s" %(jobName, active)
			element.set('active', '%s' %active)
			return True
		else:
			#print "Could not set job %s active status to %s" %(jobName, active)
			return False


	def getPath(self, jobName):
		""" Get path of the specified job.
		"""
		#element = self.root.find("./job[@id='%s']" %jobID)
		element = self.root.find("./job[name='%s']" %jobName)
		if element is not None:
			return element.find('path').text


	def setPath(self, jobName, path):
		""" Set path of the specified job.
		"""
		#element = self.root.find("./job[@id='%s']" %jobID)
		element = self.root.find("./job[name='%s']" %jobName)
		if element is not None:
			element.find('path').text = path

