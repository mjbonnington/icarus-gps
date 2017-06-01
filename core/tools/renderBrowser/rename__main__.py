#!/usr/bin/python

# [Icarus] rename__main__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016-2017 Gramercy Park Studios
#
# Batch Rename Tool
# A UI for batch renaming / renumbering of files and folders.


import os
import re
import sys

from Qt import QtCore, QtGui, QtWidgets, QtCompat
# import rsc_rc  # Import resource file as generated by pyside-rcc

# Import custom modules
import osOps
import rename
import sequence


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Batch Rename"
WINDOW_OBJECT = "batchRenameUI"

# Set the UI and the stylesheet
UI_FILE = "rename_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet


# ----------------------------------------------------------------------------
# Main application class
# ----------------------------------------------------------------------------

class batchRenameApp(QtWidgets.QMainWindow):
	""" Main application class.
	"""
	def __init__(self, parent=None):
		super(batchRenameApp, self).__init__(parent)

		# Set object name and window title
		self.setObjectName(WINDOW_OBJECT)
		self.setWindowTitle(WINDOW_TITLE)

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Tool)

		# Load UI
		self.ui = QtCompat.load_ui(fname=os.path.join(os.path.dirname(os.path.realpath(__file__)), UI_FILE))
		if STYLESHEET is not None:
			with open(STYLESHEET, "r") as fh:
				self.ui.setStyleSheet(fh.read())

		# Set the main widget
		self.setCentralWidget(self.ui)

		# Connect signals & slots
		self.ui.find_lineEdit.textEdited.connect(self.updateTaskListView)
		self.ui.replace_lineEdit.textEdited.connect(self.updateTaskListView)
		self.ui.ignoreCase_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.regex_checkBox.stateChanged.connect(self.updateTaskListView)

		self.ui.preserveNumbering_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.start_spinBox.valueChanged.connect(self.updateTaskListView)
		self.ui.step_spinBox.valueChanged.connect(self.updateTaskListView)
		self.ui.autoPadding_checkBox.stateChanged.connect(self.updateTaskListView)
		self.ui.padding_spinBox.valueChanged.connect(self.updateTaskListView)

		self.ui.addDir_pushButton.clicked.connect(self.addDirectory)
		self.ui.add_pushButton.clicked.connect(self.addSequence)
		self.ui.remove_pushButton.clicked.connect(self.removeSelection)
		self.ui.clear_pushButton.clicked.connect(self.clearTaskList)
		self.ui.rename_pushButton.clicked.connect(self.performFileRename)
		self.ui.delete_pushButton.clicked.connect(self.performFileDelete)

		self.ui.taskList_treeWidget.itemDoubleClicked.connect(self.loadFindStr)

		# Set input validators
		alphanumeric_filename_validator = QtGui.QRegExpValidator( QtCore.QRegExp(r'[\w\.-]+'), self.ui.replace_lineEdit)
		self.ui.replace_lineEdit.setValidator(alphanumeric_filename_validator)

		self.ui.delete_pushButton.hide()  # Hide the delete button - too dangerous!

		self.renameTaskLs = []
		self.lastDir = None

		# Get current dir in which to rename files, and update render layer
		# tree view widget
		self.updateTaskListDir( os.getcwd() )


	def getCheckBoxValue(self, checkBox):
		""" Get the value from a checkbox and return a Boolean value.
		"""
		if checkBox.checkState() == QtCore.Qt.Checked:
			return True
		else:
			return False


	def folderDialog(self, dialogHome):
		""" Opens a dialog from which to select a directory to browse.
		"""
		dialog = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, 
				 QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly)

		self.lastDir = os.path.dirname(dialog)
		if dialog:
			return osOps.absolutePath(dialog)
		else:
			return '.'


	def fileDialog(self, dialogHome):
		""" Opens a dialog from which to select a single file.
		"""
		dialog = QtWidgets.QFileDialog.getOpenFileName(self, self.tr('Files'), dialogHome, 'All files (*.*)')

		self.lastDir = os.path.dirname(dialog[0])
		return osOps.absolutePath(dialog[0])


	def getBrowseDir(self):
		""" Decide which directory to start browsing from.
		"""
		if self.lastDir:
			browseDir = self.lastDir
		elif os.environ.get('MAYARENDERSDIR') is not None:
			browseDir = os.environ['MAYARENDERSDIR']
		else:
			browseDir = os.getcwd()

		return browseDir


	def addDirectory(self):
		""" Scan a directory for sequences to be added to the task list.
		"""
		self.updateTaskListDir(self.folderDialog( self.getBrowseDir() ))


	def addSequence(self):
		""" Scan a directory for sequences to be added to the task list.
		"""
		self.updateTaskListFile(self.fileDialog( self.getBrowseDir() ))


	def removeSelection(self):
		""" Removes selected items from the task list.
		"""
		indices = []

		for item in self.ui.taskList_treeWidget.selectedItems():
			indices.append(self.ui.taskList_treeWidget.indexOfTopLevelItem(item))
		#	self.ui.taskList_treeWidget.takeTopLevelItem(index)

		indices.sort(reverse=True)  # Iterate over the list in reverse order to prevent the indices changing mid-operation

		for index in indices:
			#print "Deleting item at index %d" %index
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
		bases = sequence.getBases(dirpath)

		for base in bases:
			path, prefix, fr_range, ext, num_frames = sequence.getSequence(dirpath, base)
			data = (path, prefix+'.', fr_range, ext, num_frames)
			if data not in self.renameTaskLs:
				self.renameTaskLs.append(data)

		self.updateTaskListView()


	def updateTaskListFile(self, filepath):
		""" Update task list with detected file sequence given a file path.
			Pre-existing tasks will not be added, to avoid duplication.
		"""
		if os.path.isfile(filepath):
			path, prefix, fr_range, ext, num_frames = sequence.detectSeq(filepath) #, ignorePadding=True)
			data = (path, prefix+'.', fr_range, ext, num_frames)
			if data not in self.renameTaskLs:
				self.renameTaskLs.append(data)

			self.updateTaskListView()


	def updateTaskListView(self):
		""" Populates the rename list tree view widget with entries.
		"""
		renameCount = 0
		totalCount = 0

		# Get find & replace options
		findStr = self.ui.find_lineEdit.text()
		replaceStr = self.ui.replace_lineEdit.text()
		ignoreCase = self.getCheckBoxValue(self.ui.ignoreCase_checkBox)
		regex = self.getCheckBoxValue(self.ui.regex_checkBox)

		# Get renumbering options
		start = self.ui.start_spinBox.value()
		step = self.ui.step_spinBox.value()
		padding = self.ui.padding_spinBox.value()
		preserve = self.getCheckBoxValue(self.ui.preserveNumbering_checkBox)
		autopad = self.getCheckBoxValue(self.ui.autoPadding_checkBox)

		self.ui.taskList_treeWidget.clear()

		for task in self.renameTaskLs:
			path, prefix, fr_range, ext, num_frames = task

			# Add entries
			file = "%s[%s]%s" %(prefix, fr_range, ext)
			taskItem = QtWidgets.QTreeWidgetItem(self.ui.taskList_treeWidget)

			taskItem.setText(0, str(num_frames))
			taskItem.setText(1, file)

			renamedPrefix = rename.replaceTextRE(prefix, findStr, replaceStr, ignoreCase, regex)
			numLs = sequence.numList(fr_range)
			renumberedLs, padding = rename.renumber(numLs, start, step, padding, preserve, autopad)
			renumberedRange = sequence.numRange(renumberedLs, padding)
			renamedFile = "%s[%s]%s" %(renamedPrefix, renumberedRange, ext)
			taskItem.setText(2, renamedFile)

			if file == renamedFile: # set text colour to indicate status
				taskItem.setForeground(2, QtGui.QBrush(QtGui.QColor("#666")))
				#taskItem.setForeground(2, QtGui.QBrush(QtGui.QColor("#c33")))
			else:
				renameCount += num_frames

			taskItem.setText(3, path)

			self.ui.taskList_treeWidget.addTopLevelItem(taskItem)
			#taskItem.setExpanded(True)

			totalCount += num_frames

		# Resize columns
		self.ui.taskList_treeWidget.resizeColumnToContents(0)
		self.ui.taskList_treeWidget.resizeColumnToContents(1)
		self.ui.taskList_treeWidget.resizeColumnToContents(2)
		self.ui.taskList_treeWidget.resizeColumnToContents(3)
		#self.ui.taskList_treeWidget.setColumnHidden(3, True)

		self.checkConflicts()

		# Update button text
		if renameCount:
			self.ui.rename_pushButton.setText("Rename %d Files" %renameCount)
			self.ui.rename_pushButton.setEnabled(True)
		else:
			self.ui.rename_pushButton.setText("Rename")
			self.ui.rename_pushButton.setEnabled(False)

		if totalCount:
			self.ui.delete_pushButton.setText("Delete %d Files" %totalCount)
			self.ui.delete_pushButton.setEnabled(True)
		else:
			self.ui.delete_pushButton.setText("Delete")
			self.ui.delete_pushButton.setEnabled(False)


	def checkConflicts(self):
		""" Checks renamed files for conflicts with existing files.
		"""
		#results = []
		children = []
		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()
		for i in range(child_count):
			children.append(root.child(i))

		for i, item1 in enumerate(children, 1):
			for item2 in children[i:]:
				if (item1.text(2) == item2.text(2)) and (item1.text(3) == item2.text(3)):
					print "Warning: Rename conflict found. %s is not unique." %item1.text(2)
					item1.setBackground(2, QtGui.QBrush(QtGui.QColor("#c33")))
					item1.setForeground(2, QtGui.QBrush(QtGui.QColor("#fff")))
					item2.setBackground(2, QtGui.QBrush(QtGui.QColor("#c33")))
					item2.setForeground(2, QtGui.QBrush(QtGui.QColor("#fff")))


	def loadFindStr(self, item, column):
		""" Copies the selected file name prefix to the 'Find' text field when
			the item is double-clicked.
		"""
		index = self.ui.taskList_treeWidget.indexOfTopLevelItem(item)

		#text = item.text(1)
		text = self.renameTaskLs[index][1]

		self.ui.find_lineEdit.setText(text)
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
		padding = len( re.split(r'[-,\s]', fr_range)[-1] ) # detect padding
		numList = sequence.numList(fr_range)

		for i in numList:
			frame = str(i).zfill(padding)
			file = "%s%s%s" %(prefix, frame, ext)
			filePath = os.path.join(inputDir, file) #.replace("\\", "/")
			fileLs.append(filePath)

		return fileLs


	def performFileRename(self):
		""" Perform the file rename operation(s).
		"""
		newTaskLs = []

		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		for i in range(child_count):
			item = root.child(i)
			if not item.text(1) == item.text(2): # only rename if the operation will make any changes
				print "Renaming '%s' to '%s' ..." %(item.text(1), item.text(2)),
				src_fileLs = self.expandSeq(item.text(3), item.text(1))
				dst_fileLs = self.expandSeq(item.text(3), item.text(2))
				for j in range(len(src_fileLs)):
					osOps.rename( src_fileLs[j], dst_fileLs[j] )

				print "Done"
				newTaskLs.append(dst_fileLs[j])

		print "Batch rename job completed.\n"
		self.clearTaskList()

		# Update the task list to reflect the renamed files
		for newTask in newTaskLs:
			self.updateTaskListFile(newTask)


	def performFileDelete(self):
		""" Perform the file rename operation(s).
			TODO: confirmation dialog
		"""
		#QtWidgets.QMessageBox.about(self, 'Title','Message')
		root = self.ui.taskList_treeWidget.invisibleRootItem()
		child_count = root.childCount()

		for i in range(child_count):
			item = root.child(i)
			print "Deleting '%s' ..." %item.text(1),
			src_fileLs = self.expandSeq(item.text(3), item.text(1))
			for j in range(len(src_fileLs)):
				osOps.recurseRemove( src_fileLs[j] )

			print "Done"

		print "Batch deletion job completed.\n"
		self.clearTaskList()

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
	#env__init__.appendSysPaths()

	import rsc_rc

	# Set UI style - you can also use a flag e.g. '-style plastique'
	#app.setStyle('fusion')

	# Apply UI style sheet
	if STYLESHEET is not None:
		qss=os.path.join(os.environ['ICWORKINGDIR'], STYLESHEET)
		with open(qss, "r") as fh:
			app.setStyleSheet(fh.read())

	myApp = batchRenameApp()
	myApp.show()
	sys.exit(app.exec_())

# else:
# 	myApp = batchRenameApp()
# 	print myApp
# 	myApp.show()

