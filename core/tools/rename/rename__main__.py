#!/usr/bin/python

# [Icarus] rename__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2018 Gramercy Park Studios
#
# Batch Rename Tool
# A UI for batch renaming and renumbering sequences of files.
# TODO: Use unified dialog & methods for Maya advanced rename tools.


import os
import re
import sys

# Initialise Icarus environment
# sys.path.append(os.environ['IC_WORKINGDIR'])
# import env__init__
# env__init__.setEnv()

# Use NSURL as a workaround to PySide/Qt4 behaviour for dragging and dropping
# on macOS (test with PySide/Qt4 as PyQt5 works fine)
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
# Begin main application class
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

		# Restore splitter size state
		try:
			self.ui.splitter.restoreState(self.settings.value("splitterSizes")) #.toByteArray())
		except:
			pass

		# Set up keyboard shortcuts
		self.shortcutExpertMode = QtWidgets.QShortcut(self)
		self.shortcutExpertMode.setKey('Ctrl+E')
		self.shortcutExpertMode.activated.connect(self.toggleHiddenColumns)

		# Connect signals & slots
		self.ui.taskList_treeWidget.itemSelectionChanged.connect(self.updateToolbarUI)
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
		self.ui.rename_pushButton.clicked.connect(self.performFileRename)
		self.ui.cancel_pushButton.clicked.connect(self.cancelRename)

		# Context menus
		self.addContextMenu(self.ui.add_toolButton, "Directory...", self.addDirectory) #, 'icon_folder')
		self.addContextMenu(self.ui.add_toolButton, "Sequence...", self.addSequence) #, 'icon_file_sequence')

		self.addContextMenu(self.ui.fill_toolButton, "Copy filename prefix to 'Find' field", self.loadFindStr)
		self.addContextMenu(self.ui.fill_toolButton, "Copy filename prefix to 'Replace' field", self.loadReplaceStr)

		# Define status icons
		self.okIcon = QtGui.QIcon()
		self.okIcon.addPixmap(QtGui.QPixmap(osOps.absolutePath("$IC_FORMSDIR/rsc/status_icon_ok.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.readyIcon = QtGui.QIcon()
		self.readyIcon.addPixmap(QtGui.QPixmap(osOps.absolutePath("$IC_FORMSDIR/rsc/status_icon_ready.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.nullIcon = QtGui.QIcon()
		self.nullIcon.addPixmap(QtGui.QPixmap(osOps.absolutePath("$IC_FORMSDIR/rsc/status_icon_null.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.errorIcon = QtGui.QIcon()
		self.errorIcon.addPixmap(QtGui.QPixmap(osOps.absolutePath("$IC_FORMSDIR/rsc/status_icon_error.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		# Set input validators
		alphanumeric_filename_validator = QtGui.QRegExpValidator(QtCore.QRegExp(r'[\w\.-]+'), self.ui.replace_comboBox)
		self.ui.replace_comboBox.setValidator(alphanumeric_filename_validator)

		self.lastDir = None
		self.expertMode = False

		# Get current dir in which to rename files, and update render layer
		# tree view widget (but only when running as standalone app)
		if __name__ == "__main__":
			self.updateTaskListDir(os.getcwd())

		self.updateToolbarUI()
		self.toggleHiddenColumns()
		# self.getFindReplaceHistory()
		self.ui.rename_pushButton.show()
		self.ui.cancel_pushButton.hide()
		self.ui.rename_progressBar.hide()


	def updateToolbarUI(self):
		""" Update the toolbar UI based on the current selection.
		"""
		# No items selected...
		if len(self.ui.taskList_treeWidget.selectedItems()) == 0:
			self.ui.remove_toolButton.setEnabled(False)
			self.ui.fill_toolButton.setEnabled(False)
		# One item selected...
		elif len(self.ui.taskList_treeWidget.selectedItems()) == 1:
			self.ui.remove_toolButton.setEnabled(True)
			self.ui.fill_toolButton.setEnabled(True)
		# More than one item selected...
		else:
			self.ui.remove_toolButton.setEnabled(True)
			self.ui.fill_toolButton.setEnabled(False)

		# List is empty...
		if self.getChildItems(self.ui.taskList_treeWidget):
			self.ui.clear_toolButton.setEnabled(True)
		else:
			self.ui.clear_toolButton.setEnabled(False)


	def toggleHiddenColumns(self):
		""" Toggle visiblity of columns in the task list view.
		"""
		self.expertMode = not self.expertMode
		self.ui.taskList_treeWidget.setColumnHidden(0, self.expertMode)
		self.ui.taskList_treeWidget.setColumnHidden(6, self.expertMode)
		self.ui.taskList_treeWidget.setColumnHidden(7, self.expertMode)
		self.ui.taskList_treeWidget.setColumnHidden(8, self.expertMode)


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


	def getChildItems(self, widget):
		""" Return all top-level child items of the specified widget.
		"""
		items = []
		root = widget.invisibleRootItem()

		for i in range(root.childCount()):
			items.append(root.child(i))

		if items:
			return items
		else:
			return None


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
			self.lastDir = dirname
			self.updateTaskListDir(dirname)


	def addSequence(self):
		""" Open a dialog to select files to add.
		"""
		filename = self.fileDialog(self.getBrowseDir())
		if filename:
			filename = osOps.absolutePath(filename)
			self.lastDir = os.path.dirname(filename)
			self.updateTaskListFile(filename)


	def updateTaskListDir(self, dirpath):
		""" Update task list with detected file sequences in given directory.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		bases = sequence.getBases(dirpath, delimiter="")

		for base in bases:
			path, prefix, fr_range, ext, num_frames = sequence.getSequence(dirpath, base, delimiter="", ignorePadding=False)
			self.createTaskItem(path, prefix, fr_range, ext, num_frames)

		self.updateTaskListView()
		self.updateToolbarUI()


	def updateTaskListFile(self, filepath):
		""" Update task list with detected file sequence given a file path.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		if os.path.isfile(filepath):
			path, prefix, fr_range, ext, num_frames = sequence.detectSeq(filepath, delimiter="", ignorePadding=False)
			self.createTaskItem(path, prefix, fr_range, ext, num_frames)
			self.updateTaskListView()
			self.updateToolbarUI()


	def removeSelection(self):
		""" Removes selected items from the task list.
		"""
		for item in self.ui.taskList_treeWidget.selectedItems():
			index = self.ui.taskList_treeWidget.indexOfTopLevelItem(item)
			self.ui.taskList_treeWidget.takeTopLevelItem(index)

		self.updateTaskListView()
		self.updateToolbarUI()


	def clearTaskList(self):
		""" Clears the task list.
		"""
		self.ui.taskList_treeWidget.clear()
		self.updateToolbarUI()


	def createTaskItem(self, path, prefix, fr_range, ext, num_frames):
		""" Create a new task item, but only if a matching item doesn't
			already exist.
		"""
		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		# Check if matching item already exists
		for i in range(child_count):
			item = root.child(i)
			if item.text(self.header("Path")) == path and \
			   item.text(self.header("Prefix")) == prefix and \
			   item.text(self.header("Frames")) == fr_range and \
			   item.text(self.header("Extension")) == ext and \
			   item.text(self.header("Count")) == str(num_frames):
				verbose.print_("Task item already exists.")
				return item

		new_item = QtWidgets.QTreeWidgetItem(self.ui.taskList_treeWidget)
		new_item.setText(self.header("Path"), path)
		new_item.setText(self.header("Prefix"), prefix)
		new_item.setText(self.header("Frames"), fr_range)
		new_item.setText(self.header("Extension"), ext)
		new_item.setText(self.header("Count"), str(num_frames))
		return new_item


	def updateTaskListView(self):
		""" Populates the rename list tree view widget with entries.
		"""
		rename_count = 0
		total_count = 0

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

		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		for i in range(child_count):
			item = root.child(i)

			prefix = item.text(self.header("Prefix"))
			fr_range = item.text(self.header("Frames"))
			ext = item.text(self.header("Extension"))
			num_frames = int(item.text(self.header("Count")))

			item.setText(self.header("Task"), str(i))

			# Add entries
			if fr_range:
				file = "%s[%s]%s" %(prefix, fr_range, ext)
			else:
				file = "%s%s" %(prefix, ext)
			item.setText(self.header("Before"), file)

			renamedPrefix = rename.replaceTextRE(prefix, findStr, replaceStr, ignoreCase, regex)
			if fr_range:  # If sequence
				numLs = sequence.numList(fr_range)
				renumberedLs, padding = rename.renumber(numLs, start, step, padding, preserve, autopad)
				renumberedRange = sequence.numRange(renumberedLs, padding)
				renamedFile = "%s[%s]%s" %(renamedPrefix, renumberedRange, ext)
			else:
				renamedFile = "%s%s" %(renamedPrefix, ext)
			item.setText(self.header("After"), renamedFile)

			if file == renamedFile:  # Set text colour to indicate status
				item.setText(self.header("Status"), "Nothing to change")
				#item.setForeground(self.header("After"), QtGui.QBrush(QtGui.QColor("#666")))
				#item.setForeground(self.header("After"), QtGui.QBrush(QtGui.QColor("#f92672")))
				item.setIcon(self.header("Status"), self.nullIcon)
			else:
				item.setText(self.header("Status"), "Ready")
				item.setIcon(self.header("Status"), self.readyIcon)
				rename_count += num_frames

			#self.addContextMenu(item, "Copy to 'Find' field", self.loadFindStr)
			#item.setExpanded(True)

			total_count += num_frames

		# Resize columns
		# if self.renameTaskLs:
		for col in range(self.ui.taskList_treeWidget.columnCount()):
			self.ui.taskList_treeWidget.resizeColumnToContents(col)

		conflicts = self.checkConflicts()

		# Update button text
		if rename_count:
			self.ui.rename_pushButton.setText("Rename %d Files" %rename_count)
			self.ui.rename_progressBar.setMaximum(rename_count)
		else:
			self.ui.rename_pushButton.setText("Rename")

		# Enable or disable button
		if rename_count and not conflicts:
			self.ui.rename_pushButton.setEnabled(True)
		else:
			self.ui.rename_pushButton.setEnabled(False)


	def expandTask(self, item, column):
		""" Open a new view showing the individual frames in a sequence when
			the item is double-clicked.
		"""
		src_fileLs = sequence.expandSeq(item.text(self.header("Path")), item.text(self.header("Before")))
		dst_fileLs = sequence.expandSeq(item.text(self.header("Path")), item.text(self.header("After")))

		import rename_frame_view
		try:
			self.taskFrameViewUI.display(src_fileLs, dst_fileLs)
		except AttributeError:
			self.taskFrameViewUI = rename_frame_view.dialog(self)
			self.taskFrameViewUI.display(src_fileLs, dst_fileLs)


	def checkConflicts(self):
		""" Checks for conflicts in renamed files. - REWRITE THIS
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
				item.setText(self.header("Status"), "Conflict error")
				item.setIcon(self.header("Status"), self.errorIcon)

		# Check for conflicts with existing files on disk
		for item in children:
			for file in sequence.expandSeq(item.text(self.header("Path")), item.text(self.header("After"))):
				if not item.text(self.header("Before")) == item.text(self.header("After")):
					if os.path.isfile(file):
						item.setText(self.header("Status"), "File exists error")
						item.setIcon(self.header("Status"), self.errorIcon)

		self.ui.taskList_treeWidget.resizeColumnToContents(self.header("Status"))

		if len(conflicts):
			verbose.warning("%d rename %s found." %(len(conflicts), verbose.pluralise("conflict", len(conflicts))))

		return len(conflicts)


	def loadFindStr(self, item=None, column=0):
		""" Copies the selected file name prefix to the 'Find' text field.
		"""
		if not item:
			item = self.ui.taskList_treeWidget.selectedItems()[0]

		text = item.text(self.header("Prefix"))

		if self.ui.find_comboBox.findText(text) == -1:
			self.ui.find_comboBox.addItem(text)
		self.ui.find_comboBox.setCurrentIndex(self.ui.find_comboBox.findText(text))


	def loadReplaceStr(self, item=None, column=0):
		""" Copies the selected file name prefix to the 'Replace' text field.
			Non-alphanumeric characters will be replaced with underscores.
		"""
		if not item:
			item = self.ui.taskList_treeWidget.selectedItems()[0]

		text = item.text(self.header("Prefix"))
		text = osOps.sanitize(text, pattern=r'[^\w\.-]', replace='_')

		if self.ui.replace_comboBox.findText(text) == -1:
			self.ui.replace_comboBox.addItem(text)
		self.ui.replace_comboBox.setCurrentIndex(self.ui.replace_comboBox.findText(text))


	def performFileRename(self):
		""" Perform the file rename operation(s).
		"""
		# newTaskLs = []

		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		self.ui.rename_pushButton.hide()
		self.ui.cancel_pushButton.show()
		self.ui.rename_progressBar.show()
		self.ui.rename_progressBar.setValue(0)

		taskItems = []
		for i in range(child_count):
			taskItems.append(root.child(i))

		# Initialise worker thread, connect signals & slots, start processing
		self.workerThread = BatchRenameThread(taskItems, 
			ignore_errors=self.getCheckBoxValue(self.ui.ignoreErrors_checkBox))
		self.workerThread.printError.connect(verbose.error)
		self.workerThread.printMessage.connect(verbose.message)
		self.workerThread.printProgress.connect(verbose.progress)
		self.workerThread.updateProgressBar.connect(self.updateProgressBar)
		self.workerThread.returnNewTask.connect(self.taskCompleted)
		self.workerThread.finished.connect(self.renameCompleted)
		self.workerThread.start()

		# for i in range(child_count):
		# 	newTask = self.renameTask(root.child(i))
		# 	if newTask:
		# 		newTaskLs.append(newTask)

		# verbose.message("Batch rename job completed.")

		# self.clearTaskList()

		# # Update the task list to reflect the renamed files
		# for newTask in newTaskLs:
		# 	self.updateTaskListFile(newTask)


	@QtCore.Slot(int)
	def updateProgressBar(self, value):
		self.ui.rename_progressBar.setValue(value)


	@QtCore.Slot(tuple)
	def taskCompleted(self, new_task):
		""" Update task in list view. TBC
		"""
		pass
		#print(new_task)
		#self.updateTaskListItem(new_task)


	def renameCompleted(self):
		""" Function to execute when the rename operation finishes.
		"""
		verbose.message("Batch rename job completed.")

		self.ui.rename_pushButton.show()
		self.ui.cancel_pushButton.hide()
		self.ui.rename_progressBar.hide()

		#self.clearTaskList()

		# # Update the task list to reflect the renamed files
		# for newTask in newTaskLs:
		# 	self.updateTaskListFile(newTask)


	def cancelRename(self):
		""" Stop the rename operation.
		"""
		verbose.message("Aborting rename job")
		self.workerThread.terminate()  # Enclose in try/except?

		# self.renderTaskInterrupted = True

		# if self.slaveStatus == "rendering":
		# 	#self.renderProcess.terminate()
		# 	self.renderProcess.kill()
		# else:
		# 	verbose.message("No render in progress.")


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
		""" Event handler for files dropped on to the widget.
		"""
		if e.mimeData().hasUrls:
			e.setDropAction(QtCore.Qt.CopyAction)
			e.accept()
			for url in e.mimeData().urls():
				# # Workaround for macOS dragging and dropping
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


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.save()  # Save settings
		self.storeWindow()  # Store window geometry
		# Store splitter size state
		self.settings.setValue("splitterSizes", self.ui.splitter.saveState())

# ----------------------------------------------------------------------------
# End main application class
# ============================================================================
# Begin worker thread class
# ----------------------------------------------------------------------------

class BatchRenameThread(QtCore.QThread):
	""" Worker thread class.
	"""
	printError = QtCore.Signal(str)
	printMessage = QtCore.Signal(str)
	printProgress = QtCore.Signal(str)
	updateProgressBar = QtCore.Signal(int)
	returnNewTask = QtCore.Signal(tuple)

	def __init__(self, tasks, ignore_errors=True):
		QtCore.QThread.__init__(self)
		self.tasks = tasks
		self.ignore_errors = ignore_errors
		self.files_processed = 0


	def __del__(self):
		self.wait()


	def _rename_task(self, item):
		""" Perform the file rename operation(s).
		"""
		errors = 0

		task_id = item.text(0)
		# task_status = item.text(1)
		# task_count = item.text(2)
		task_before = item.text(3)
		task_after = item.text(4)
		task_path = item.text(5)

		src_fileLs = sequence.expandSeq(task_path, task_before)
		dst_fileLs = sequence.expandSeq(task_path, task_after)

		if task_before == task_after:
			self.printMessage.emit("%s: Rename task skipped as it would not make any changes." %task_id)
			item.setText(1, "Nothing to change")
			return "OK", src_fileLs[0]

		else:  # Only rename if the operation will make changes
			self.printMessage.emit("%s: Rename '%s' to '%s'" %(task_id, task_before, task_after))
			self.printMessage.emit("Renaming 0%")
			item.setText(1, "Processing")

			for j in range(len(src_fileLs)):
				success, msg = osOps.rename(src_fileLs[j], dst_fileLs[j], quiet=True)
				if success:
					progress = (j/len(src_fileLs))*100
					self.printProgress.emit("Renaming %d%%" %progress)
					#item.setText(1, "Renaming %d%%" %progress)
				else:
					errors += 1
					if not self.ignore_errors:
						self.printError.emit(msg)
						item.setText(1, "Incomplete")
						return "Incomplete", src_fileLs[j]
				self.files_processed += 1
				self.updateProgressBar.emit(self.files_processed)

			if errors == 0:
				self.printProgress.emit("Renaming 100%")
				item.setText(1, "Complete")
				#item.setIcon(1, self.okIcon)
				item.setText(3, task_after)
				return "Complete", dst_fileLs[j]
			else:
				self.printMessage.emit("Task generated %s errors." %errors)
				item.setText(1, "%d errors" %errors)
				#item.setIcon(1, self.errorIcon)
				return "%d errors" %errors, src_fileLs[j]


	def run(self):
		for item in self.tasks:
			new_task = self._rename_task(item)
			self.returnNewTask.emit(new_task)

# ----------------------------------------------------------------------------
# End worker thread class
# ============================================================================
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
		qss = os.path.join(os.environ['IC_FORMSDIR'], STYLESHEET)
		with open(qss, "r") as fh:
			app.setStyleSheet(fh.read())

	myApp = BatchRenameApp()
	myApp.show()
	sys.exit(app.exec_())

# else:
# 	myApp = BatchRenameApp()
# 	print(myApp)
# 	myApp.show()

