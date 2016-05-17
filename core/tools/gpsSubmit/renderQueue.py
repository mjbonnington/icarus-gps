#!/usr/bin/python

# [Icarus] renderQueue.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# Manages the Render Queue XML database.


import xml.etree.ElementTree as ET
import xmlData


class renderQueue(xmlData.xmlData):
	""" Class to hold the render queue database.
		Inherits xmlData class
	"""

	def getJobs(self, activeOnly=False):
		""" Return a list of render jobs.
		"""
		# elements = self.root.findall("./job")
		# jobs = []
		# for element in elements:
		# 	print element.tag, element.attrib
		# 	print element.find('name').text
		# 	print element.find('priority').text
		# 	print element.find('status').text
		# 	print element.find('frames').text
		# 	print element.find('taskSize').text
		# 	jobs.append( element.get('id') )
		# return jobs
		return self.root.findall("./job")


	def getValue(self, element, tag):
		""" Return the specified value.
		"""
		elem = element.find(tag)
		if elem is not None:
			text = elem.text
			if text is not None:
				return text

		#return "" # return an empty string, not None, so value can be stored in an environment variable without raising an error


	def getNextID(self):
		""" Return the next unused job ID integer.
		"""
		try:
			elements = self.root.findall("./job")
			jobIDs = []
			for element in elements:
				jobIDs.append( int(element.get('id')) )
			return max(jobIDs)+1

		except ValueError:
			return 0


	def newJob(self, genericOpts, mayaOpts, tasks, user, submitTime):
		""" Create a new render job on submission.
		"""
		jobID = self.getNextID()

		jobName, priority, frames, taskSize = genericOpts
		mayaScene, mayaProject, mayaFlags = mayaOpts

		jobElement = self.root.find("job[@id='%s']" %jobID)
		if jobElement is None:
			jobElement = ET.SubElement(self.root, 'job')
			jobElement.set('id', str(jobID))

			nameElement = ET.SubElement(jobElement, 'name')
			nameElement.text = str(jobName)

			priorityElement = ET.SubElement(jobElement, 'priority')
			priorityElement.text = str(priority)

			statusElement = ET.SubElement(jobElement, 'status')
			statusElement.text = "Queued"

			framesElement = ET.SubElement(jobElement, 'frames')
			framesElement.text = str(frames)

			taskSizeElement = ET.SubElement(jobElement, 'taskSize')
			taskSizeElement.text = str(taskSize)

			userElement = ET.SubElement(jobElement, 'user')
			userElement.text = str(user)

			submitTimeElement = ET.SubElement(jobElement, 'submitTime')
			submitTimeElement.text = str(submitTime)

			mayaSceneElement = ET.SubElement(jobElement, 'mayaScene')
			mayaSceneElement.text = str(mayaScene)

			mayaProjectElement = ET.SubElement(jobElement, 'mayaProject')
			mayaProjectElement.text = str(mayaProject)

			mayaFlagsElement = ET.SubElement(jobElement, 'mayaFlags')
			mayaFlagsElement.text = str(mayaFlags)

			for i in range(len(tasks)):
				taskElement = ET.SubElement(jobElement, 'task')
				taskElement.set('id', str(i))

				taskStatusElement = ET.SubElement(taskElement, 'status')
				taskStatusElement.text = "Queued"

				taskFramesElement = ET.SubElement(taskElement, 'frames')
				taskFramesElement.text = str(tasks[i])

				taskFramesElement = ET.SubElement(taskElement, 'slave')

				commandElement = ET.SubElement(taskElement, 'command')
				#commandElement.text = str(taskCmds[i].replace("\\", "/"))


	def deleteJob(self, jobID):
		""" Delete a new render job.
		"""
		for element in self.root.findall('./job'):
			if int(element.get('id')) == jobID:
				self.root.remove(element)


	def setPriority(self, jobID, priority):
		""" Set the priority of a render job.
		"""
		element = self.root.find("./job[@id='%s']/priority" %jobID)
		if 0 <= priority <= 100:
			element.text = str(priority)

