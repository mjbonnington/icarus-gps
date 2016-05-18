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

	def getJobs(self):
		""" Return a render job elements.
		"""
		return self.root.findall("./job")


	def getValue(self, element, tag):
		""" Return the specified value of tag belonging to specified element.
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


	def getPriority(self, jobID):
		""" Get the priority of a render job.
		"""
		element = self.root.find("./job[@id='%s']/priority" %jobID)
		return int(element.text)


	def setPriority(self, jobID, priority):
		""" Set the priority of a render job.
		"""
		self.loadXML(quiet=True) # reload XML data
		element = self.root.find("./job[@id='%s']/priority" %jobID)
		if 0 <= priority <= 100:
			element.text = str(priority)
		self.saveXML()


	# def setStatus(self, element, status):
	# 	""" Set the status of a render job or task.
	# 	"""
	# 	self.loadXML(quiet=True) # reload XML data
	# 	elem = element.find('./priority')
	# 	elem.text = str(status)
	# 	self.saveXML()


	def newJob(self, genericOpts, mayaOpts, tasks, user, submitTime):
		""" Create a new render job on submission.
		"""
		self.loadXML(quiet=True) # reload XML data
		jobID = self.getNextID()

		jobName, priority, frames, taskSize = genericOpts
		mayaScene, mayaProject, mayaFlags, mayaRenderCmd = mayaOpts

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

			mayaRenderCmdElement = ET.SubElement(jobElement, 'mayaRenderCmd')
			mayaRenderCmdElement.text = str(mayaRenderCmd)

			mayaFlagsElement = ET.SubElement(jobElement, 'mayaFlags')
			mayaFlagsElement.text = str(mayaFlags)

			for i in range(len(tasks)):
				taskElement = ET.SubElement(jobElement, 'task')
				taskElement.set('id', str(i))

				taskStatusElement = ET.SubElement(taskElement, 'status')
				taskStatusElement.text = "Queued"

				taskFramesElement = ET.SubElement(taskElement, 'frames')
				taskFramesElement.text = str(tasks[i])

				taskSlaveElement = ET.SubElement(taskElement, 'slave')

				#commandElement = ET.SubElement(taskElement, 'command')
				#commandElement.text = str(taskCmds[i].replace("\\", "/"))

		self.saveXML()


	def deleteJob(self, jobID):
		""" Delete a new render job.
		"""
		self.loadXML(quiet=True) # reload XML data
		for element in self.root.findall('./job'):
			if int(element.get('id')) == jobID:
				self.root.remove(element)
		self.saveXML()


	def getHighestPriorityJob(self):
		""" Find the highest priority job and return the first queued task found.
		"""
		#self.loadXML(quiet=True) # reload XML data
		elements = self.root.findall('./job/priority')
		priorityLs = []
		for element in elements:
			priorityLs.append( int(element.text) )
		priorityLs.sort(reverse=True)

		return self.root.find("./job/[priority='%s']" %priorityLs[0])


	def dequeueTask(self, jobElement, hostID):
		""" Dequeue the first queued task found belonging to the given job element.
		"""
		self.loadXML(quiet=True) # reload XML data
		taskElement = jobElement.find("./task/[status='Queued']")

		print jobElement.find('status').text
		print taskElement.find('status').text
		print taskElement.find('slave').text
		jobElement.find('status').text = "In Progress"
		taskElement.find('status').text = "In Progress"
		taskElement.find('slave').text = str(hostID)
		print jobElement.find('status').text
		print taskElement.find('status').text
		print taskElement.find('slave').text
		# self.setStatus(jobElement, "In Progress")

		self.saveXML()
		return taskElement.find('frames').text

