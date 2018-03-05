#!/usr/bin/python

# [Icarus] jobs.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2015-2017 Gramercy Park Studios
#
# Manipulates the database of jobs running in the CG department.


import os
import xml.etree.ElementTree as ET

# Import custom modules
import job__env__
import osOps
import verbose
import xmlData


class jobs(xmlData.XMLData):
	""" Manipulates XML database for storing jobs.
		Add and remove jobs, make jobs active or inactive, modify job
		properties.
		Inherits XMLData class.
	"""
	def __init__(self):
		""" Automatically load datafile on initialisation.
		"""
		self.loadXML(os.path.join(os.environ['IC_CONFIGDIR'], 'jobs.xml'))
		self.getRootPaths()


	def setup(self, jobName, shotName, storeLastJob=True):
		""" Set job.
		"""
		jobPath = self.getPath(jobName, translate=True)
		shotPath = osOps.absolutePath("%s/$SHOTSROOTRELATIVEDIR/%s" %(jobPath, shotName))

		# Create environment variables
		if job__env__.setEnv(jobName, shotName, shotPath):

			# Create folder structure
			self.createDirs()

			# Remember for next time
			if storeLastJob:
				import userPrefs
				newEntry = '%s,%s' % (jobName, shotName)
				# userPrefs.edit('main', 'lastjob', newEntry)
				userPrefs.updateRecentShots(newEntry)

			return True

		else:
			return False


	def checkShotExists(self, jobName, shotName):
		""" Check if shot path exists.
		"""
		jobPath = self.getPath(jobName, translate=True)
		shotPath = osOps.absolutePath("%s/$SHOTSROOTRELATIVEDIR/%s" %(jobPath, shotName))
		if os.path.isdir(shotPath):
			return True
		else:
			return False


	def createDirs(self):
		""" Create directory structure inside shot folder.
			TODO: The folder structure should be defined in an XML data file
			and generated based on that.
		"""
		# Published asset directories
		for directory in (os.environ['JOBPUBLISHDIR'], os.environ['SHOTPUBLISHDIR']):
			if not os.path.isdir(directory):
				osOps.createDir(directory)

		# Plate directories
		res_full = "%sx%s" %(os.environ['RESOLUTIONX'], os.environ['RESOLUTIONY'])
		res_proxy = "%sx%s" %(os.environ['PROXY_RESOLUTIONX'], os.environ['PROXY_RESOLUTIONY'])
		plates = (res_full, res_proxy)
		platesDir = os.path.join(os.environ['SHOTPATH'], 'Plate')
		if not os.path.isdir(platesDir):
			osOps.createDir(platesDir)

		# Delete any pre-existing redundant plate directories that are empty
		try:
			for directory in os.listdir(platesDir):
				existingDir = os.path.join(platesDir, directory)
				if os.path.isdir(existingDir) and not os.listdir(existingDir):
					if directory not in plates:
						osOps.recurseRemove(existingDir)

			# Create plate directory named with resolution
			for directory in plates:
				plateDir = os.path.join(platesDir, directory)
				if not os.path.isdir(plateDir):
					osOps.createDir(plateDir)

		except:
			pass


	def getRootPaths(self):
		""" Get root paths and set environment variables.
		"""
		try:
			self.win_root = self.root.find('jobs-root/win').text
			self.osx_root = self.root.find('jobs-root/osx').text
			self.linux_root = self.root.find('jobs-root/linux').text
			self.jobs_path = self.root.find('jobs-root/path').text

		except AttributeError:
			self.win_root = None
			self.osx_root = None
			self.linux_root = None
			self.jobs_path = None

		# Set environment variables
		os.environ['FILESYSTEMROOTWIN'] = str(self.win_root)
		os.environ['FILESYSTEMROOTOSX'] = str(self.osx_root)
		os.environ['FILESYSTEMROOTLINUX'] = str(self.linux_root)

		if os.environ['IC_RUNNING_OS'] == 'Windows':
			os.environ['FILESYSTEMROOT'] = str(self.win_root)
		elif os.environ['IC_RUNNING_OS'] == 'Darwin':
			os.environ['FILESYSTEMROOT'] = str(self.osx_root)
		else:
			os.environ['FILESYSTEMROOT'] = str(self.linux_root)

		#os.environ['JOBSROOT'] = osOps.absolutePath('$FILESYSTEMROOT/$JOBSROOTRELATIVEDIR', stripTrailingSlash=True)
		os.environ['JOBSROOT'] = osOps.absolutePath('$FILESYSTEMROOT/%s' %self.jobs_path, stripTrailingSlash=True)


	def setRootPaths(self, winPath=None, osxPath=None, linuxPath=None, jobsRelPath=None):
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

		if jobsRelPath is not None:
			pathElement = jobsRootElement.find('path')
			if pathElement is None:
				pathElement = ET.SubElement(jobsRootElement, 'path')
			pathElement.text = str(jobsRelPath)


	def getActiveJobs(self):
		""" Return all active jobs as a list. Only jobs that exist on disk
			will be added.
		"""
		jobLs = []
		for jobElement in self.root.findall("./job[@active='True']"):
			jobName = jobElement.find('name').text
			jobPath = jobElement.find('path').text

			jobPath = osOps.translatePath(jobPath)

			if os.path.exists(jobPath): # Only add jobs which exist on disk
				jobLs.append(jobName)

		return jobLs


	def getJobs(self):
		""" Return all jobs as elements.
		"""
		return self.root.findall("./job")


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
			return False


	def deleteJob(self, jobName):
		""" Delete job by name.
		"""
		element = self.root.find("./job/[name='%s']" %jobName)
		if element is not None:
			verbose.message("Deleted job %s" %jobName)
			self.root.remove(element)
			return True
		else:
			verbose.error("Could not delete job %s" %jobName)
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
			if active:
				action = "Enabled"
			else:
				action = "Disabled"
			verbose.message("%s job %s" %(action, jobName))
			element.set('active', '%s' %active)
			return True
		else:
			verbose.error("Could not %s job %s" %(action, jobName))
			return False


	def getPath(self, jobName, translate=False):
		""" Get path of the specified job.
			If 'translate' is True, attempt to translate the path for the
			current OS.
		"""
		#element = self.root.find("./job[@id='%s']" %jobID)
		element = self.root.find("./job[name='%s']" %jobName)
		if element is not None:
			jobPath = element.find('path').text
			if translate:
				return osOps.translatePath(jobPath)
			else:
				return jobPath


	def setPath(self, jobName, path):
		""" Set path of the specified job.
		"""
		#element = self.root.find("./job[@id='%s']" %jobID)
		element = self.root.find("./job[name='%s']" %jobName)
		if element is not None:
			element.find('path').text = path


	def listShots(self, jobName):
		""" Return a list of all available shots belonging to the specified
			job.
		"""
		jobPath = self.getPath(jobName, translate=True)
		shotsPath = osOps.absolutePath("%s/$SHOTSROOTRELATIVEDIR" %jobPath)

		# Check shot path exists before proceeding...
		if os.path.exists(shotsPath):
			dirContents = os.listdir(shotsPath)
			shotLs = []

			for item in dirContents:
				# Check for shot naming convention to disregard everything
				# else in directory
				if item.startswith('SH') or item.startswith('PC'):
					# Check that the directory is a valid shot by checking for
					# the existence of the '.icarus' subdirectory
					if os.path.isdir(osOps.absolutePath("%s/%s/$DATAFILESRELATIVEDIR" %(shotsPath, item))):
						shotLs.append(item)

			if len(shotLs):
				shotLs.sort()
				return shotLs

			else:
				verbose.warning('No valid shots found in job path "%s".' %shotsPath)
				return False

		else:
			verbose.error('The job path "%s" does not exist. The job may have been archived, moved or deleted.' %shotsPath)
			return False

