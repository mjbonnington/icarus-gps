#!/usr/bin/python

# [Icarus] Render Browser rb__init__.py
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2016 Gramercy Park Studios
#
# A UI to browse render folders and provide at-a-glance review of layers, passes/AOVs, sequences, etc.


from PySide import QtCore, QtGui
from rb_ui import * # <- import your app's UI file (as generated by pyside-uic)
import os, re, sys

# Initialise Icarus environment
sys.path.append(os.environ['ICWORKINGDIR'])
import env__init__
env__init__.setEnv()
#env__init__.appendSysPaths()

import sequence as seq
import djvOps, osOps


class renderBrowserApp(QtGui.QMainWindow):

	def __init__(self, parent = None):
		super(renderBrowserApp, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.relativeRootDir = os.environ['SHOTPATH']
		self.relativeRootToken = '$SHOTPATH'

		# Connect signals & slots
		self.ui.renderPblAdd_pushButton.clicked.connect(self.renderTableAdd)
		self.ui.renderPblRemove_pushButton.clicked.connect(self.renderTableRemove)
		self.ui.renderPblClear_pushButton.clicked.connect(self.renderTableClear)
		self.ui.renderPbl_treeWidget.itemDoubleClicked.connect(self.renderPreview)

		# Get current dir for renders and update render layer tree view widget
		self.renderPath = os.getcwd()
		self.renderTableUpdate()


	def relativePath(self, absPath):
		if absPath.startswith(self.relativeRootDir):
			return absPath.replace(self.relativeRootDir, self.relativeRootToken)
		else:
			return absPath


	def absolutePath(self, relPath):
		return relPath.replace(self.relativeRootToken, self.relativeRootDir)


	def generateThumbnail(self, imagePath, imagePrefix, extension, posterFrame=os.environ['STARTFRAME']):
		""" Generates a low-res JPEG thumbnail from the image path provided.
		"""
		inPrefix = os.path.join(imagePath, imagePrefix)
		outPrefix = os.path.join(imagePath, '.icThumbs', imagePrefix)
		outFile = '%s.%s.jpg' % (outPrefix, posterFrame)
		if not os.path.isfile(outFile):
			print "Generating thumbnails..."
			osOps.createDir( os.path.join(imagePath, '.icThumbs') )
			djvOps.prcImg(inPrefix, outPrefix, posterFrame, posterFrame, extension.split('.', 1)[1], outExt='jpg', resize=(512,288))
		return outFile


	def renderPreview(self, item, column):
		""" Launches sequence viewer when entry is double-clicked.
		"""
		#print item.text(column), column
		path = seq.getFirst( self.absolutePath(item.text(3)) )
		#print path
		djvOps.viewer(path)


	def folderDialog(self, dialogHome):
		""" Opens a file dialog to choose which directory to browse.
		"""
		dialog = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Directory'), dialogHome, 
				 QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)
		return dialog


	def renderTableClear(self):
		""" Clears the render layer tree view widget.
		"""
		self.ui.renderPbl_treeWidget.clear()


	def renderTableUpdate(self):
		""" Populates the render layer tree view widget with entries.
		"""
		renderPath = self.renderPath
		if renderPath:
			renderLayerDirs = []

			# Get subdirectories
			subdirs = next(os.walk(renderPath))[1]
			if subdirs:
				for subdir in subdirs:
					if not subdir.startswith('.'): # ignore directories that start with a dot
						renderLayerDirs.append(subdir)
			if renderLayerDirs:
				renderLayerDirs.sort()
			else: # use parent dir
				renderLayerDirs = [os.path.basename(renderPath)]
				renderPath = os.path.dirname(renderPath)
			print renderPath, renderLayerDirs

			self.ui.renderPbl_treeWidget.setIconSize(QtCore.QSize(128, 72))

			# Add render layers
			for renderLayerDir in renderLayerDirs:
				renderPasses = seq.getBases(os.path.join(renderPath, renderLayerDir))

				# Only continue if render pass sequences exist in this directory, and ignore directories that start with a dot
				if renderPasses and not renderLayerDir.startswith('.'):
					renderLayerItem = QtGui.QTreeWidgetItem(self.ui.renderPbl_treeWidget)
					renderLayerItem.setText(0, '%s (%d)' % (renderLayerDir, len(renderPasses)))
					renderLayerItem.setText(2, 'layer')
					#renderLayerItem.setText(3, os.path.join(renderPath, renderLayerDir))
					renderLayerItem.setText(3, self.relativePath(os.path.join(renderPath, renderLayerDir)))
					self.ui.renderPbl_treeWidget.addTopLevelItem(renderLayerItem)
					renderLayerItem.setExpanded(True)

					# Add render passes
					for renderPass in renderPasses:
						renderPassItem = QtGui.QTreeWidgetItem(renderLayerItem)
						path, prefix, fr_range, ext, num_frames = seq.getSequence( os.path.join(renderPath, renderLayerDir), renderPass )
						renderPassItem.setText(0, prefix)
						iconPath = self.generateThumbnail(os.path.join(renderPath, renderLayerDir), prefix, ext)
						#print iconPath
						renderPassItem.setIcon(0, QtGui.QIcon(iconPath))
						renderPassItem.setText(1, fr_range)
						if not fr_range == os.environ['FRAMERANGE']: # set red text for sequence mismatch
							renderPassItem.setForeground(1, QtGui.QBrush(QtGui.QColor("#c33")))
						renderPassItem.setText(2, ext.split('.', 1)[1])
						#renderPassItem.setText(3, path)
						renderPassItem.setText(3, self.relativePath(os.path.join(renderPath, renderLayerDir, renderPass)))
						self.ui.renderPbl_treeWidget.addTopLevelItem(renderPassItem)

			# Resize columns
			self.ui.renderPbl_treeWidget.resizeColumnToContents(0)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(1)
			self.ui.renderPbl_treeWidget.resizeColumnToContents(2)


	def renderTableAdd(self):
		""" Adds entries to the render layer tree view widget.
		"""
		if os.environ.get('MAYARENDERSDIR') is None:
			renderBrowseDir = os.getcwd()
		else:
			renderBrowseDir = os.environ['MAYARENDERSDIR']

		self.renderPath = self.folderDialog(renderBrowseDir)
		self.renderTableUpdate()


	def renderTableRemove(self):
		""" Removes the selected entry from the render layer tree view widget.
			TODO: allow passes to be removed as well as layers.
		"""
		for item in self.ui.renderPbl_treeWidget.selectedItems():
			self.ui.renderPbl_treeWidget.takeTopLevelItem( self.ui.renderPbl_treeWidget.indexOfTopLevelItem(item) )


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)

	#app.setStyle('fusion') # Set UI style - you can also use a flag e.g. '-style plastique'

	import rsc_rc # TODO: Check why this isn't working from within the UI file

	# Apply UI style sheet
	qss=os.path.join(os.environ['ICWORKINGDIR'], "style.qss")
	with open(qss, "r") as fh:
		app.setStyleSheet(fh.read())

	rbApp = renderBrowserApp()
	rbApp.show()
	sys.exit(app.exec_())

