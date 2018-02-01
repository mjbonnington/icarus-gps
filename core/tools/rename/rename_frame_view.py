#!/usr/bin/python

# [Icarus] rename_frame_view.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2018 Gramercy Park Studios
#
# Batch Rename Tool
# A popup UI to display an expanded file sequence.


from Qt import QtCore, QtWidgets
import ui_template as UI

# Import custom modules


# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

# Set window title and object names
WINDOW_TITLE = "Frame View"
WINDOW_OBJECT = "frameViewUI"

# Set the UI and the stylesheet
UI_FILE = "rename_frame_view_ui.ui"
STYLESHEET = "style.qss"  # Set to None to use the parent app's stylesheet

# Other options
STORE_WINDOW_GEOMETRY = True


# ----------------------------------------------------------------------------
# Main dialog class
# ----------------------------------------------------------------------------

class dialog(QtWidgets.QDialog, UI.TemplateUI):
	""" Main dialog class.
	"""
	def __init__(self, parent=None):
		super(dialog, self).__init__(parent)
		self.parent = parent

		self.setupUI(window_object=WINDOW_OBJECT, 
					 window_title=WINDOW_TITLE, 
					 ui_file=UI_FILE, 
					 stylesheet=STYLESHEET, 
					 store_window_geometry=STORE_WINDOW_GEOMETRY)  # re-write as **kwargs ?

		# Set window flags
		self.setWindowFlags(QtCore.Qt.Dialog) #QtCore.Qt.Tool

		# Set other Qt attributes
		#self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)


	def display(self, src_fileLs, dst_fileLs):
		""" Display the dialog.
		"""
		self.ui.frameList_treeWidget.clear()

		for row in range(len(src_fileLs)):
			item = QtWidgets.QTreeWidgetItem(self.ui.frameList_treeWidget)
			item.setText(0, src_fileLs[row])
			item.setText(1, dst_fileLs[row])

		for col in range(self.ui.frameList_treeWidget.columnCount()):
			self.ui.frameList_treeWidget.resizeColumnToContents(col)

		return self.exec_()


	def hideEvent(self, event):
		""" Event handler for when window is hidden.
		"""
		self.storeWindow()  # Store window geometry

