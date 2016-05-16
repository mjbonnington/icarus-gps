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


	# def getTasks(self, job):
	# 	""" Return list of render tasks associated with job.
	# 	"""
	# 	elements = self.root.findall("./job[@name='%s']/path" %app)
	# 	tasks = []
	# 	for element in elements:
	# 		tasks.append( element.get('id') )
	# 		rank = element.find('rank').text
	# 	return tasks


	def getNextID(self):
		""" Return the next unused job ID integer.
		"""
		elements = self.root.findall("./job")
		jobIDs = []
		for element in elements:
			jobIDs.append( int(element.get('id')) )
		return max(jobIDs)+1


	def newJob(self, jobName, priority, frames, taskFrames, taskCmds):
		""" Create a new render job on submission.
		"""
		jobID = self.getNextID()

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

			for i in range(len(taskCmds)):
				taskElement = ET.SubElement(jobElement, 'task')
				taskElement.set('id', str(i))

				taskStatusElement = ET.SubElement(taskElement, 'status')
				taskStatusElement.text = "Queued"

				taskFramesElement = ET.SubElement(taskElement, 'frames')
				taskFramesElement.text = str(taskFrames[i])

				taskFramesElement = ET.SubElement(taskElement, 'slave')

				commandElement = ET.SubElement(taskElement, 'command')
				commandElement.text = str(taskCmds[i].replace("\\", "/"))

