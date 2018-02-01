#!/usr/bin/python

# [Icarus] rename__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# Batch Rename Tool
# A UI for batch renaming / renumbering of files and folders.
# TODO: Use unified dialog for Maya advanced rename tools.


import os
import re
import sys

# Initialise Icarus environment
# sys.path.append(os.environ['IC_WORKINGDIR'])
# import env__init__
# env__init__.setEnv()

# Use NSURL as a workaround to PySide/Qt4 behaviour for dragging and dropping
# on OSX (test with PySide/Qt4 as PyQt5 works fine)
# if os.environ['IC_RUNNING_OS'] == 'Darwin':
# 	from Foundation import NSURL

from Qt import QtCore, QtGui, QtWidgets
import ui_template as UI

# Import custom modules
import osOps
import rename
import sequence
import verbose


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Batch Rename"
WINDOW_OBJECT = "batchRenameUI"

# Set the UI and the stylesheet
UI_FILE = "rename_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Worker thread class
# ----------------------------------------------------------------------------

class RenameThread(QtCore.QThread):

	def __init__(self, tasks):
		QtCore.QThread.__init__(self)
		self.tasks = tasks


	def __del__(self):
		self.wait()


	def _rename_task(self, item):
		""" Perform the file rename operation(s).
		"""
		errors = 0

		task_id = item.text(0)
		src_fileLs = self.expandSeq(item.text(4), item.text(2))
		dst_fileLs = self.expandSeq(item.text(4), item.text(3))

		if item.text(2) == item.text(3):
			verbose.print_("%s: Rename task skipped as it would not make any changes." %task_id)
			return src_fileLs[0]

		else:  # Only rename if the operation will make changes
			verbose.message("%s: Rename '%s' to '%s'" %(task_id, item.text(2), item.text(3)))
			verbose.message("Renaming 0%")

			for j in range(len(src_fileLs)):
				if osOps.rename(src_fileLs[j], dst_fileLs[j], quiet=True):
				#if self.rename(src_fileLs[j], dst_fileLs[j]):
					progress = (j/len(src_fileLs))*100
					verbose.progress("Renaming %d%%" %progress)
					self.files_processed += 1
					# self.ui.rename_progressBar.setValue((self.files_processed/self.files_to_process)*100)
				else:
					errors += 1
					if not self.getCheckBoxValue(self.ui.continueOnError_checkBox):
						return None

			if errors == 0:
				verbose.progress("Renaming 100%")
				return dst_fileLs[j]
			else:
				return src_fileLs[j]


	def run(self):
		for item in self.tasks:
			new_task = self._rename_task(item)
			#self.emit(SIGNAL('add_post(QString)'), new_task)

# ----------------------------------------------------------------------------
# Main application class
# ----------------------------------------------------------------------------

class BatchRenameApp(QtWidgets.QMainWindow, UI.TemplateUI):
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(BatchRenameApp, self).__init__(parent)
		self.parent = parent

		xml_data = os.path.join(os.environ['IC_USERPREFS'], 'batchRename.xml')

		self.setupUI(window_object=WINDOW_OBJECT, 
					 window_title=WINDOW_TITLE, 
					 ui_file=UI_FILE, 
					 stylesheet=STYLESHEET, 
					 xml_data=xml_data, 
					 store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Window) #QtCore.Qt.Tool

		# Set other Qt attributes
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

		# Create a QProcess object to handle the renaming process
		# asynchronously
		# self.renameProcess = QtCore.QProcess(self)
		# self.renameProcess.finished.connect(self.renameComplete)
		# self.renameProcess.readyReadStandardOutput.connect(self.updateSlaveView)

		# Connect signals & slots
		self.ui.taskList_treeWidget.itemSelectionChanged.connect(self.updateToolbarUI)
		#self.ui.taskList_treeWidget.itemDoubleClicked.connect(self.loadFindStr)
		self.ui.taskList_treeWidget.itemDoubleClicked.connect(self.expandTask)

		self.ui.find_comboBox.editTextChanged.connect(self.updateTaskListView)
		self.ui.replace_comboBox.editTextChanged.connect(self.updateTaskListView)
		self.ui.ignoreCase_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.regex_checkBox.stateChanged.connect(self.updateTaskListView)

		self.ui.preserveNumbering_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.start_spinBox.valueChanged.connect(self.updateTaskListView)
		self.ui.step_spinBox.valueChanged.connect(self.updateTaskListView)
		self.ui.autoPadding_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.padding_spinBox.valueChanged.connect(self.updateTaskListView)

		self.ui.remove_toolButton.clicked.connect(self.removeSelection)
		self.ui.clear_toolButton.clicked.connect(self.clearTaskList)
		self.ui.rename_toolButton.clicked.connect(self.performFileRename)
		# self.ui.cancel_toolButton.clicked.connect(self.cancelRename)
		# self.ui.delete_pushButton.clicked.connect(self.performFileDelete)

		# Context menus
		self.addContextMenu(self.ui.add_toolButton, "Directory...", self.addDirectory) #, 'icon_folder')
		self.addContextMenu(self.ui.add_toolButton, "Sequence...", self.addSequence) #, 'icon_file_sequence')

		# Set input validators
		alphanumeric_filename_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-]+'), self.ui.replace_comboBox)
		self.ui.replace_comboBox.setValidator(alphanumeric_filename_validator)

		# self.ui.delete_pushButton.hide()  # Hide the delete button - too dangerous!

		self.renameTaskLs = []
		self.lastDir = None

		# Get current dir in which to rename files, and update render layer
		# tree view widget (when in standalone mode)
		# if __name__ == "__main__":
		# 	self.updateTaskListDir(os.getcwd())

		self.updateToolbarUI()
		# self.getFindReplaceHistory()
		self.ui.sidebarStatusbar_frame.hide()
		self.ui.sidebarToolbar_frame.show()


	def updateToolbarUI(self):
		""" Update the toolbar UI based on the current selection.
		"""
		# No items selected...
		if len(self.ui.taskList_treeWidget.selectedItems()) == 0:
			self.ui.remove_toolButton.setEnabled(False)
		# One item selected...
		elif len(self.ui.taskList_treeWidget.selectedItems()) == 1:
			self.ui.remove_toolButton.setEnabled(True)
		# More than one item selected...
		else:
			self.ui.remove_toolButton.setEnabled(True)


	# def getFindReplaceHistory(self):
	# 	""" 
	# 	"""
	# 	elements = self.xd.root.findall("./data[@category='textsubstitution']/findhistory/item")
	# 	find_history = []
	# 	for element in elements:
	# 		find_history.append(element.text)

	# 	elements = self.xd.root.findall("./data[@category='textsubstitution']/replacehistory/item")
	# 	replace_history = []
	# 	for element in elements:
	# 		replace_history.append(element.text)

	# 	self.populateComboBox(self.ui.find_comboBox, find_history)
	# 	self.populateComboBox(self.ui.replace_comboBox, replace_history)


	# def addComboBoxHistory(self, comboBox, newText):
	# 	""" 
	# 	"""
	# 	history = []  # Clear list

	# 	elements = self.xd.root.findall("./data[@category='textsubstitution']/findhistory/item")
	# 	for element in elements:
	# 		history.append(element.text)

	# 	if newText in history:  # If entry already exists, delete it
	# 		history.remove(newText)

	# 	history.insert(0, newText)  # Prepend entry to the list

	# 	while len(history) > 10:
	# 		history.pop()

	# 	parentElement = self.root.find("./data[@category='textsubstitution']/findhistory")
	# 	for text in history:
	# 		settingElem = ET.SubElement(parentElement, "item")
	# 		settingElem.text = str(text)

	# 	self.populateComboBox(comboBox, history)
	# 	# if comboBox.findText(newText) == -1:
	# 	# 	comboBox.insertItem(newText, 0)
	# 	# comboBox.setCurrentIndex(comboBox.findText(newText))


	def header(self, text):
		""" Returns the column number for the specified header text.
		"""
		for col in range(self.ui.taskList_treeWidget.columnCount()):
			if text == self.ui.taskList_treeWidget.headerItem().text(col):
				return col
		return -1


	def getBrowseDir(self):
		""" Decide which directory to start browsing from.
		"""
		if self.lastDir:
			browseDir = self.lastDir
		elif os.environ.get('MAYARENDERSDIR') is not None:
			browseDir = os.environ['MAYARENDERSDIR']
		else:
			browseDir = os.environ['FILESYSTEMROOT']
			#browseDir = os.getcwd()

		return browseDir


	def addDirectory(self):
		""" Open a dialog to select a folder to add files from.
		"""
		dirname = self.folderDialog(self.getBrowseDir())
		if dirname:
			dirname = osOps.absolutePath(dirname)
			self.lastDir = os.path.dirname(dirname)
			self.updateTaskListDir(dirname)


	def addSequence(self):
		""" Open a dialog to select files to add.
		"""
		filename = self.fileDialog(self.getBrowseDir())
		self.lastDir = os.path.dirname(filename)

		self.updateTaskListFile(osOps.absolutePath(filename))


	def removeSelection(self):
		""" Removes selected items from the task list.
		"""
		indices = []

		for item in self.ui.taskList_treeWidget.selectedItems():
			indices.append(self.ui.taskList_treeWidget.indexOfTopLevelItem(item))
			# self.ui.taskList_treeWidget.takeTopLevelItem(index)

		indices.sort(reverse=True)  # Iterate over the list in reverse order to prevent the indices changing mid-operation

		for index in indices:
			verbose.print_("Deleting item at index %d" %index)
			del self.renameTaskLs[index]

		self.updateTaskListView()


	def clearTaskList(self):
		""" Clears the task list.
		"""
		self.renameTaskLs = []
		self.updateTaskListView()


	def updateTaskListDir(self, dirpath):
		""" Update task list with detected file sequences in given directory.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		bases = sequence.getBases(dirpath, delimiter="")

		for base in bases:
			path, prefix, fr_range, ext, num_frames = sequence.getSequence(dirpath, base, delimiter="", ignorePadding=False)
			#data = (path, prefix+'.', fr_range, ext, num_frames)
			data = (path, prefix, fr_range, ext, num_frames)
			if data not in self.renameTaskLs:
				self.renameTaskLs.append(data)

		self.updateTaskListView()


	def updateTaskListFile(self, filepath):
		""" Update task list with detected file sequence given a file path.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		if os.path.isfile(filepath):
			path, prefix, fr_range, ext, num_frames = sequence.detectSeq(filepath, delimiter="", ignorePadding=False)
			#data = (path, prefix+'.', fr_range, ext, num_frames)
			data = (path, prefix, fr_range, ext, num_frames)
			if data not in self.renameTaskLs:
				self.renameTaskLs.append(data)

			self.updateTaskListView()


	def updateTaskListView(self):
		""" Populates the rename list tree view widget with entries.
		"""
		renameCount = 0
		totalCount = 0

		# Get find & replace options
		findStr = self.ui.find_comboBox.currentText()
		replaceStr = self.ui.replace_comboBox.currentText()
		ignoreCase = self.getCheckBoxValue(self.ui.ignoreCase_checkBox)
		regex = self.getCheckBoxValue(self.ui.regex_checkBox)

		# Get renumbering options
		start = self.ui.start_spinBox.value()
		step = self.ui.step_spinBox.value()
		padding = self.ui.padding_spinBox.value()
		preserve = self.getCheckBoxValue(self.ui.preserveNumbering_checkBox)
		autopad = self.getCheckBoxValue(self.ui.autoPadding_checkBox)

		self.ui.taskList_treeWidget.clear()

		for i, task in enumerate(self.renameTaskLs):
			path, prefix, fr_range, ext, num_frames = task

			# Add entries
			file = "%s[%s]%s" %(prefix, fr_range, ext)
			taskItem = QtWidgets.QTreeWidgetItem(self.ui.taskList_treeWidget)

			taskItem.setText(self.header("Task"), str(i))
			taskItem.setText(self.header("Count"), str(num_frames))
			taskItem.setText(self.header("Before"), file)

			renamedPrefix = rename.replaceTextRE(prefix, findStr, replaceStr, ignoreCase, regex)
			numLs = sequence.numList(fr_range)
			renumberedLs, padding = rename.renumber(numLs, start, step, padding, preserve, autopad)
			renumberedRange = sequence.numRange(renumberedLs, padding)
			renamedFile = "%s[%s]%s" %(renamedPrefix, renumberedRange, ext)
			taskItem.setText(self.header("After"), renamedFile)

			if file == renamedFile: # set text colour to indicate status
				taskItem.setForeground(self.header("After"), QtGui.QBrush(QtGui.QColor("#666")))
				#taskItem.setForeground(self.header("After"), QtGui.QBrush(QtGui.QColor("#f92672")))
			else:
				renameCount += num_frames

			taskItem.setText(self.header("Path"), path)

			self.ui.taskList_treeWidget.addTopLevelItem(taskItem)

			#self.addContextMenu(taskItem, "Copy to 'Find' field", self.loadFindStr)
			#taskItem.setExpanded(True)

			totalCount += num_frames

		# Resize columns
		if self.renameTaskLs:
			for col in range(self.ui.taskList_treeWidget.columnCount()):
				self.ui.taskList_treeWidget.resizeColumnToContents(col)

		conflicts = self.checkConflicts()

		# Update button text
		if renameCount:
			self.ui.rename_toolButton.setText("Rename %d Files" %renameCount)
			# self.files_to_process = renameCount
			self.ui.rename_progressBar.setMaximum(renameCount)
		else:
			self.ui.rename_toolButton.setText("Rename")

		if renameCount and not conflicts:
			self.ui.rename_toolButton.setEnabled(True)
		else:
			self.ui.rename_toolButton.setEnabled(False)

		# if totalCount:
		# 	self.ui.delete_pushButton.setText("Delete %d Files" %totalCount)
		# 	self.ui.delete_pushButton.setEnabled(True)
		# else:
		# 	self.ui.delete_pushButton.setText("Delete")
		# 	self.ui.delete_pushButton.setEnabled(False)


	def expandTask(self, item, column):
		""" Open a new view showing the individual frames in a sequence when
			the item is double-clicked.
		"""
		#index = self.ui.taskList_treeWidget.indexOfTopLevelItem(item)

		src_fileLs = self.expandSeq(item.text(self.header("Path")), item.text(self.header("Before")))
		dst_fileLs = self.expandSeq(item.text(self.header("Path")), item.text(self.header("After")))

		import rename_frame_view
		try:
			self.taskFrameViewUI.display(src_fileLs, dst_fileLs)
		except AttributeError:
			self.taskFrameViewUI = rename_frame_view.dialog(self)
			self.taskFrameViewUI.display(src_fileLs, dst_fileLs)


	# def drawProgressIndicator(self, renderJobItem, completedTaskFrameCount,
	# 						 inProgressTaskFrameCount, totalFrameCount,
	# 						 colProgress):
	# 	""" Draw a pixmap to represent the progress of a task.
	# 	"""
	# 	border = 1
	# 	width = self.ui.renderQueue_treeWidget.columnWidth(4)
	# 	height = self.ui.renderQueue_treeWidget.rowHeight(self.ui.renderQueue_treeWidget.indexFromItem(renderJobItem))
	# 	barWidth = width - (border*2)
	# 	barHeight = height - (border*2)
	# 	completedRatio = float(completedTaskFrameCount) / float(totalFrameCount)
	# 	inProgressRatio = float(inProgressTaskFrameCount) / float(totalFrameCount)
	# 	completedLevel = math.ceil(completedRatio*barWidth)
	# 	inProgressLevel = math.ceil((completedRatio+inProgressRatio)*barWidth)

	# 	image = QtGui.QPixmap(width, height)

	# 	qp = QtGui.QPainter()
	# 	qp.begin(image)
	# 	pen = QtGui.QPen()
	# 	pen.setStyle(QtCore.Qt.NoPen)
	# 	qp.setPen(pen)
	# 	qp.setBrush(self.colBorder)
	# 	qp.drawRect(0, 0, width, height)
	# 	qp.setBrush(self.colBlack)
	# 	qp.drawRect(border, border, barWidth, barHeight)
	# 	qp.setBrush(self.colActive)
	# 	qp.drawRect(border, border, inProgressLevel, barHeight)
	# 	qp.setBrush(colProgress)
	# 	qp.drawRect(border, border, completedLevel, barHeight)
	# 	qp.end()

	# 	# renderJobItem.setBackground(4, image)  # PyQt5 doesn't like this
	# 	renderJobItem.setBackground(4, QtGui.QBrush(image))  # Test with Qt4/PySide
	# 	renderJobItem.setForeground(4, QtGui.QBrush(self.colWhite))


	def checkConflicts(self):
		""" Checks for conflicts in renamed files.
		"""
		children = []
		outputs = []
		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()
		for i in range(child_count):
			children.append(root.child(i))
			outpath = "%s/%s" %(root.child(i).text(self.header("Path")), root.child(i).text(self.header("After")))
			outputs.append(outpath.lower())

		# Find duplicate outputs
		conflicts = set([x for x in outputs if outputs.count(x) > 1])

		# Highlight duplicates in list view
		for item in children:
			outpath = "%s/%s" %(item.text(self.header("Path")), item.text(self.header("After")))
			if outpath.lower() in conflicts:
				item.setBackground(self.header("After"), QtGui.QBrush(QtGui.QColor("#f92672")))
				item.setForeground(self.header("After"), QtGui.QBrush(QtGui.QColor("#fff")))

		# Check for conflicts with existing files on disk
		for item in children:
			for file in self.expandSeq(item.text(self.header("Path")), item.text(self.header("After"))):
				if not item.text(self.header("Before")) == item.text(self.header("After")):  # Only rename if the operation will make any changes
					if os.path.isfile(file):
						item.setBackground(self.header("After"), QtGui.QBrush(QtGui.QColor("#fd971f")))
						item.setForeground(self.header("After"), QtGui.QBrush(QtGui.QColor("#fff")))


		if len(conflicts):
			verbose.warning("%d rename %s found." %(len(conflicts), verbose.pluralise("conflict", len(conflicts))))

		return len(conflicts)


	def loadFindStr(self, item, column):
		""" Copies the selected file name prefix to the 'Find' text field when
			the item is double-clicked.
		"""
		index = self.ui.taskList_treeWidget.indexOfTopLevelItem(item)

		#text = item.text(1)
		text = self.renameTaskLs[index][1]

		# self.ui.find_lineEdit.setText(text)
		if self.ui.find_comboBox.findText(text) == -1:
			self.ui.find_comboBox.addItem(text)
		self.ui.find_comboBox.setCurrentIndex(self.ui.find_comboBox.findText(text))
		self.updateTaskListView()


	def expandSeq(self, inputDir, inputFileSeq):
		""" Expand a filename sequence in the format 'name.[start-end].ext' to
			a list of individual frames.
			Return a list containing the full path to each file in the
			sequence.
		"""
		fileLs = []

		# Split filename and separate sequence numbering
		prefix, fr_range, ext = re.split(r'[\[\]]', inputFileSeq)
		padding = len(re.split(r'[-,\s]', fr_range)[-1])  # Detect padding
		numList = sequence.numList(fr_range)

		for i in numList:
			frame = str(i).zfill(padding)
			file = "%s%s%s" %(prefix, frame, ext)
			filePath = os.path.join(inputDir, file).replace("\\", "/")
			fileLs.append(filePath)

		return fileLs


	def performFileRename(self):
		""" Perform the file rename operation(s).
		"""
		newTaskLs = []
		self.files_processed = 0

		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		self.ui.sidebarToolbar_frame.hide()
		self.ui.sidebarStatusbar_frame.show()
		self.ui.rename_progressBar.setValue(0)

		taskItems = []
		for i in range(child_count):
			taskItems.append(root.child(i))
		self.renameThread = RenameThread(taskItems)
		# self.connect(self.renameThread, SIGNAL("add_post(QString)"), self.add_post)
		self.renameThread.finished.connect(self.done)
		self.renameThread.start()
		self.ui.cancel_toolButton.clicked.connect(self.renameThread.terminate)

		# for i in range(child_count):
		# 	newTask = self.renameTask(root.child(i))
		# 	if newTask:
		# 		newTaskLs.append(newTask)

		# verbose.message("Batch rename job completed.")

		# self.ui.sidebarStatusbar_frame.hide()
		# self.ui.sidebarToolbar_frame.show()

		# self.clearTaskList()

		# # Update the task list to reflect the renamed files
		# for newTask in newTaskLs:
		# 	self.updateTaskListFile(newTask)


	# def renameTask(self, item):
	# 	""" Perform the file rename operation(s).
	# 	"""
	# 	errors = 0

	# 	task_id = item.text(self.header("Task"))
	# 	src_fileLs = self.expandSeq(item.text(self.header("Path")), item.text(self.header("Before")))
	# 	dst_fileLs = self.expandSeq(item.text(self.header("Path")), item.text(self.header("After")))

	# 	if item.text(self.header("Before")) == item.text(self.header("After")):
	# 		verbose.print_("%s: Rename task skipped as it would not make any changes." %task_id)
	# 		return src_fileLs[0]

	# 	else:  # Only rename if the operation will make changes
	# 		verbose.message("%s: Rename '%s' to '%s'" %(task_id, item.text(self.header("Before")), item.text(self.header("After"))))
	# 		verbose.message("Renaming 0%")

	# 		for j in range(len(src_fileLs)):
	# 			if osOps.rename(src_fileLs[j], dst_fileLs[j], quiet=True):
	# 			#if self.rename(src_fileLs[j], dst_fileLs[j]):
	# 				progress = (j/len(src_fileLs))*100
	# 				verbose.progress("Renaming %d%%" %progress)
	# 				self.files_processed += 1
	# 				self.ui.rename_progressBar.setValue((self.files_processed/self.files_to_process)*100)
	# 			else:
	# 				errors += 1
	# 				if not self.getCheckBoxValue(self.ui.continueOnError_checkBox):
	# 					return None

	# 		if errors == 0:
	# 			verbose.progress("Renaming 100%")
	# 			return dst_fileLs[j]
	# 		else:
	# 			return src_fileLs[j]


	# def rename(self, source, destination):
	# 	""" Rename a file or folder using the low-level os method.
	# 	"""
	# 	src = os.path.normpath(source)
	# 	dst = os.path.normpath(destination)

	# 	if os.environ['IC_RUNNING_OS'] == 'Windows':
	# 		cmdStr = 'ren "%s" "%s"' %(src, dst)
	# 	else:
	# 		cmdStr = 'mv "%s" "%s"' %(src, dst)

	# 	try:
	# 		#verbose.print_(cmdStr, 4)
	# 		#os.system(cmdStr)
	# 		self.renameProcess.start(cmdStr)
	# 		return True
	# 	except:
	# 		return False


	# def performFileDelete(self):
	# 	""" Perform the file rename operation(s).
	# 		TODO: confirmation dialog
	# 	"""
	# 	#QtWidgets.QMessageBox.about(self, 'Title','Message')
	# 	root = self.ui.taskList_treeWidget.invisibleRootItem()
	# 	child_count = root.childCount()

	# 	for i in range(child_count):
	# 		item = root.child(i)
	# 		verbose.print_("Deleting '%s'" %item.text(1),)
	# 		src_fileLs = self.expandSeq(item.text(3), item.text(1))
	# 		for j in range(len(src_fileLs)):
	# 			osOps.recurseRemove( src_fileLs[j] )

	# 		verbose.print_("Done")

	# 	verbose.print_("Batch deletion job completed.\n")
	# 	self.clearTaskList()


	def add_post(self, post_text):
		"""
		"""
		print(post_text)
		#self.list_submissions.addItem(post_text)
		self.ui.rename_progressBar.setValue(self.ui.rename_progressBar.value()+1)


	def done(self):
		""" Function to ececute when the rename operation finishes.
		"""
		verbose.message("Batch rename job completed.")

		self.ui.sidebarStatusbar_frame.hide()
		self.ui.sidebarToolbar_frame.show()

		self.clearTaskList()

		# # Update the task list to reflect the renamed files
		# for newTask in newTaskLs:
		# 	self.updateTaskListFile(newTask)


	# def cancelRename(self):
	# 	""" Stop the rename operation.
	# 	"""
	# 	verbose.message("Aborting rename job")
	# 	self.renameThread.terminate()

	# 	# self.renderTaskInterrupted = True

	# 	# if self.slaveStatus == "rendering":
	# 	# 	#self.renderProcess.terminate()
	# 	# 	self.renderProcess.kill()
	# 	# else:
	# 	# 	verbose.message("No render in progress.")


	#-------------------------------------------------------------------------
	# The following three methods set up dragging and dropping for the app...
	def dragEnterEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()

	def dragMoveEvent(self, e):
		if e.mimeData().hasUrls:
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, e):
		""" Drop files directly onto the widget.

			File locations are stored in fname
			:param e:
			:return:
		"""
		if e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			# Workaround for OSX dragging and dropping
			for url in e.mimeData().urls():
				# if os.environ['IC_RUNNING_OS'] == 'Darwin':
				# 	fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
				# else:
				# 	fname = str(url.toLocalFile())
				fname = str(url.toLocalFile())

			#self.fname = fname
			verbose.print_("Dropped '%s' on to window." %fname)
			if os.path.isdir(fname):
				self.updateTaskListDir(fname)
			elif os.path.isfile(fname):
				self.updateTaskListFile(fname)
		else:
			e.ignore()
	#
	#-------------------------------------------------------------------------


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry

# ----------------------------------------------------------------------------
# End of main application class
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Run as standalone app
# ----------------------------------------------------------------------------

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)

	# Initialise Icarus environment
	sys.path.append(os.environ['IC_WORKINGDIR'])
	import env__init__
	env__init__.setEnv()

	import rsc_rc

	# Set UI style - you can also use a flag e.g. '-style plastique'
	#app.setStyle('fusion')

	# Apply UI style sheet
	if STYLESHEET is not None:
		qss = os.path.join(os.environ['ICWORKINGDIR'], STYLESHEET)
		with open(qss, "r") as fh:
			app.setStyleSheet(fh.read())

	myApp = BatchRenameApp()
	myApp.show()
	sys.exit(app.exec_())

# else:
# 	myApp = BatchRenameApp()
# 	print(myApp)
# 	myApp.show()

