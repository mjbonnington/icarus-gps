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

	def newJob(self, genericOpts, renderOpts, tasks, user, submitTime, comment):
		""" Create a new render job on submission.
		"""
		self.loadXML(quiet=True) # reload XML data
		jobID = self.getNextID()

		jobName, jobType, frames, taskSize, priority = genericOpts
		#print jobType
		if jobType == 'Maya':
			#print "a"
			mayaScene, mayaProject, mayaFlags, mayaRenderCmd = renderOpts
		elif jobType == 'Nuke':
			#print "b"
			nukeScript, nukeFlags, nukeRenderCmd = renderOpts

		jobElement = self.root.find("job[@id='%s']" %jobID)
		if jobElement is None:
			jobElement = ET.SubElement(self.root, 'job')
			jobElement.set('id', str(jobID))

			nameElement = ET.SubElement(jobElement, 'name')
			nameElement.text = str(jobName)

			typeElement = ET.SubElement(jobElement, 'type')
			typeElement.text = str(jobType)

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

			commentElement = ET.SubElement(jobElement, 'comment')
			commentElement.text = str(comment)

			# totalTimeElement = ET.SubElement(jobElement, 'totalTime')
			# totalTimeElement.text = "0"

			if jobType == 'Maya':
				mayaSceneElement = ET.SubElement(jobElement, 'mayaScene')
				mayaSceneElement.text = str(mayaScene)

				mayaProjectElement = ET.SubElement(jobElement, 'mayaProject')
				mayaProjectElement.text = str(mayaProject)

				mayaFlagsElement = ET.SubElement(jobElement, 'mayaFlags')
				mayaFlagsElement.text = str(mayaFlags)

				mayaRenderCmdElement = ET.SubElement(jobElement, 'mayaRenderCmd')
				mayaRenderCmdElement.text = str(mayaRenderCmd)

			elif jobType == 'Nuke':
				nukeScriptElement = ET.SubElement(jobElement, 'nukeScript')
				nukeScriptElement.text = str(nukeScript)

				nukeFlagsElement = ET.SubElement(jobElement, 'nukeFlags')
				nukeFlagsElement.text = str(nukeFlags)

				nukeRenderCmdElement = ET.SubElement(jobElement, 'nukeRenderCmd')
				nukeRenderCmdElement.text = str(nukeRenderCmd)

			for i in range(len(tasks)):
				taskElement = ET.SubElement(jobElement, 'task')
				taskElement.set('id', str(i))

				taskStatusElement = ET.SubElement(taskElement, 'status')
				taskStatusElement.text = "Queued"

				taskFramesElement = ET.SubElement(taskElement, 'frames')
				taskFramesElement.text = str(tasks[i])

				# taskStartTimeElement = ET.SubElement(taskElement, 'startTime')

				taskTotalTimeElement = ET.SubElement(taskElement, 'totalTime')
				#taskTotalTimeElement.text = "0"

				taskSlaveElement = ET.SubElement(taskElement, 'slave')

				# commandElement = ET.SubElement(taskElement, 'command')
				# commandElement.text = str(taskCmds[i].replace("\\", "/"))

		self.saveXML()


	def deleteJob(self, jobID):
		""" Delete a render job.
		"""
		self.loadXML(quiet=True) # reload XML data
		for element in self.root.findall('./job'):
			if int(element.get('id')) == jobID:
				if "In Progress" in element.find('status').text:
					return False # ignore in-progress jobs
				else:
					self.root.remove(element)
					self.saveXML()
					return True


	def getJobs(self):
		""" Return all render jobs as elements.
		"""
		return self.root.findall("./job")


	def getValue(self, element, tag):
		""" Return the value of 'tag' belonging to 'element'.
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


	def setStatus(self, jobID, status):
		""" Set the status of a render job.
		"""
		#self.loadXML(quiet=True) # reload XML data
		element = self.root.find("./job[@id='%s']/status" %jobID)
		#print "Set status", element
		if element.text == str(status): # do nothing if status hasn't changed
			return
		else:
			element.text = str(status)
			self.saveXML()


	def dequeueJob(self):
		""" Find a job with the highest priority that isn't paused or completed.
		"""
		self.loadXML(quiet=True) # reload XML data

		for priority in range(100, 0, -1): # iterate over range starting at 100 and ending at 1 (zero is omitted)
			elements = self.root.findall("./job/[priority='%s']" %priority) # get all <job> elements with the highest priority
			if elements is not None:
				for element in elements:
					#print "[Priority %d] Job ID %s: %s (%s)" %(priority, element.get('id'), element.find('name').text, element.find('status').text),
					if element.find('status').text != "Done":
						if element.find("task/[status='Queued']") is not None: # does this job have any queued tasks?
							#print "This will do, let's render it!"
							return element
					#print "Not yet, keep searching..."

		return None


	def dequeueTask(self, jobID, hostID):
		""" Dequeue the next queued task belonging to the specified job, mark it as 'In Progress', and return the task ID and the frame range.
		"""
		self.loadXML(quiet=True) # reload XML data
		element = self.root.find("./job[@id='%s']/task/[status='Queued']" %jobID) # get the first <task> element with 'Queued' status
		#element = self.root.find("./job[@id='%s']/task" %jobID) # get the first <task> element
		if element is not None:
			#if element.find('status').text is not "Done":
			element.find('status').text = "In Progress"
			element.find('slave').text = str(hostID)
			self.saveXML()
			return element.get('id'), element.find('frames').text

		else:
			return False, False


	def completeTask(self, jobID, taskID, hostID=None, taskTime=0):
		""" Mark the specified task as 'Done'.
		"""
		self.loadXML(quiet=True) # reload XML data
		element = self.root.find("./job[@id='%s']/task[@id='%s']" %(jobID, taskID)) # get the <task> element
		if element is not None:
			if element.find('status').text == "Done": # do nothing if status is 'Done'
				return
			# elif element.find('status').text == "In Progress": # do nothing if status is 'In Progress'
			# 	return
			else:
				element.find('status').text = "Done"
				element.find('slave').text = str(hostID)
				element.find('totalTime').text = str(taskTime)
				self.saveXML()


	def requeueTask(self, jobID, taskID):
		""" Requeue the specified task, mark it as 'Queued'.
		"""
		self.loadXML(quiet=True) # reload XML data
		element = self.root.find("./job[@id='%s']/task[@id='%s']" %(jobID, taskID)) # get the <task> element
		if element.find('status').text == "Queued": # do nothing if status is 'Queued'
			return
		# elif element.find('status').text == "In Progress": # do nothing if status is 'In Progress'
		# 	return
		else:
			element.find('status').text = "Queued"
			element.find('totalTime').text = ""
			element.find('slave').text = ""
			self.saveXML()

