#!/usr/bin/python

# [Icarus] Batch Render Queue Manager queue__main__.py
# v0.1
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# A UI for managing the render queue.


from PySide import QtCore, QtGui
from queue_ui import * # <- import your app's UI file (as generated by pyside-uic)
import os, sys

# Import custom modules
import renderQueue


class gpsRenderQueueApp(QtGui.QMainWindow):

	def __init__(self, parent = None):
		super(gpsRenderQueueApp, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		# Instantiate render queue class and load data
		self.rq = renderQueue.renderQueue()
		self.rq.loadXML(os.path.join(os.environ['PIPELINE'], 'core', 'config', 'renderQueue.xml'))

		# Connect signals & slots
		self.ui.jobSubmit_toolButton.clicked.connect(self.launchRenderSubmit)
		self.ui.jobPriorityInc_toolButton.clicked.connect(lambda *args: self.changePriority(1))
		self.ui.jobPriorityDec_toolButton.clicked.connect(lambda *args: self.changePriority(-1))
		self.ui.jobDelete_toolButton.clicked.connect(self.deleteRenderJob)
		self.ui.refresh_toolButton.clicked.connect(self.updateRenderQueueView)

		self.updateRenderQueueView()


	def updateRenderQueueView(self):
		""" Populates the render queue tree view widget with entries for render jobs and tasks.
		"""
		self.rq.loadXML(quiet=True) # reload XML data

		self.ui.renderQueue_treeWidget.clear()

		# Populate render jobs
		for jobElement in self.rq.getJobs():
			renderJobItem = QtGui.QTreeWidgetItem(self.ui.renderQueue_treeWidget)

			# renderJobItem.setText(0, jobElement.find('name').text)
			# renderJobItem.setText(1, jobElement.find('frames').text)
			# renderJobItem.setText(2, jobElement.find('status').text)
			# renderJobItem.setText(3, jobElement.find('priority').text)
			# renderJobItem.setText(4, jobElement.find('user').text)
			# renderJobItem.setText(5, jobElement.find('submitTime').text)
			# renderJobItem.setText(6, jobElement.find('elapsedTime').text)

			renderJobItem.setText(0, self.rq.getValue(jobElement, 'name'))
			renderJobItem.setText(1, jobElement.get('id'))
			renderJobItem.setText(2, self.rq.getValue(jobElement, 'frames'))
			renderJobItem.setText(3, self.rq.getValue(jobElement, 'status'))
			renderJobItem.setText(4, self.rq.getValue(jobElement, 'priority'))
			renderJobItem.setText(5, self.rq.getValue(jobElement, 'user'))
			renderJobItem.setText(6, self.rq.getValue(jobElement, 'submitTime'))
			renderJobItem.setText(7, self.rq.getValue(jobElement, 'elapsedTime'))

			#renderJobItem.setExpanded(True)

			# Populate render tasks
			for taskElement in jobElement.findall('task'):
				renderTaskItem = QtGui.QTreeWidgetItem(renderJobItem)

				# renderTaskItem.setText(0, "Task %s" %taskElement.get('id'))
				# renderTaskItem.setText(1, taskElement.find('frames').text)
				# renderTaskItem.setText(2, taskElement.find('status').text)
				# renderTaskItem.setText(6, taskElement.find('elapsedTime').text)
				# renderTaskItem.setText(7, taskElement.find('slave').text)
				# renderTaskItem.setText(8, taskElement.find('command').text)

				renderTaskItem.setText(0, "Task %s" %taskElement.get('id'))
				renderTaskItem.setText(2, self.rq.getValue(taskElement, 'frames'))
				renderTaskItem.setText(3, self.rq.getValue(taskElement, 'status'))
				renderTaskItem.setText(7, self.rq.getValue(taskElement, 'elapsedTime'))
				renderTaskItem.setText(8, self.rq.getValue(taskElement, 'slave'))
				renderTaskItem.setText(9, self.rq.getValue(taskElement, 'command'))

			# Resize columns
			for i in range(0, self.ui.renderQueue_treeWidget.columnCount()):
				self.ui.renderQueue_treeWidget.resizeColumnToContents(i)

			# Hide ID column
			self.ui.renderQueue_treeWidget.setColumnHidden(1, True)

			# Sort by submit time column
			self.ui.renderQueue_treeWidget.sortByColumn(6, QtCore.Qt.DescendingOrder)


	def deleteRenderJob(self):
		""" Removes selected render job from the database and updates the view.
		"""
		indices = []

		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				indices.append(int(item.text(1)))
				#indices.append(self.ui.renderQueue_treeWidget.indexOfTopLevelItem(item))

			#indices.sort(reverse=True) # iterate over the list in reverse order to prevent the indices changing mid-operation

			for index in indices:
				print "Deleting job with ID %d" %index
				self.rq.loadXML(quiet=True) # reload XML data
				self.rq.deleteJob(index)
				self.rq.saveXML() # move load and save ops into delete function?

			self.updateRenderQueueView()

		except ValueError:
			pass


	def changePriority(self, amount):
		""" Changes priority of the selected render job by specified amount.
		"""
		try:
			for item in self.ui.renderQueue_treeWidget.selectedItems():
				index = int(item.text(1))
				priority = int(item.text(4))+amount
				self.rq.loadXML(quiet=True) # reload XML data
				self.rq.setPriority(index, priority)
				self.rq.saveXML() # move load and save ops into delete function?

			self.updateRenderQueueView()

		except ValueError:
			pass


	def launchRenderSubmit(self):
		""" Launches GPS Submit Render dialog.
		"""
		import submit__main__
		reload(submit__main__)


	def exit(self):
		""" Exit the dialog.
		"""
		self.hide()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	# Initialise Icarus environment
	os.environ['ICWORKINGDIR'] = "N:\Dev\icarus\core\ui" # temp assignment
	sys.path.append(os.environ['ICWORKINGDIR'])
	import env__init__
	env__init__.setEnv()

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	# app.setStyle('fusion') # Set UI style - you can also use a flag e.g. '-style plastique'

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	renderQueueApp = gpsRenderQueueApp()
	renderQueueApp.show()
	sys.exit(app.exec_())

else:
	renderQueueApp = gpsRenderQueueApp()
	print renderQueueApp
	renderQueueApp.show()

