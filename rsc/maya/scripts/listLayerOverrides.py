#!/usr/bin/python

# [GPS] listLayerOverrides.py
# v0.2
#
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2018 Gramercy Park Studios
#
# Provides a UI to view and manage all attribute overrides for a particular
# render layer.


import maya.cmds as mc
#import mGui.gui as ui
from mGui.gui import *
from mGui.forms import *
from mGui.styles import CSS


class RenderLayerOverrides():

	def __init__(self):
		self.winTitle = "Manage Layer Overrides"
		self.winName = "gpsRenderLayerOverrides"

		self.renderLayers = mc.ls(type='renderLayer')
		self.currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)


	def UI(self):
		""" Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Show window if it already exists
		# try:
		# 	window.show()

		# Build UI
		# except:
		btns = CSS(None, margin=(4,4), spacing=(2,0))

		with Window(self.winName, title=self.winTitle) as window:
			with VerticalThreePane() as vertical_layout1:
				with HorizontalForm(css=btns) as layer_layout1:
					with HorizontalExpandForm() as layer_layout2:
						layer_label = Text(label="Layer: ")
						layer_comboBox = OptionMenu()
					reloadLayers_button = SymbolButton(image="refresh.png", width=26, height=26)
				text_scroll = TextScrollList()
				with HorizontalStretchForm(css=btns) as buttonBox:
					# yes_button = Button('Yes')
					# no_button = Button('No')
					close_button = Button('Close')
					close_button.command += self.close

		window.show()


	def close(self, *args, **kwargs):
		mc.deleteUI(self.winName)


	# def fileUI(self, name, parent, collapse=False):
	# 	""" Create panel UI controls.
	# 	"""
	# 	mc.frameLayout(width=400, collapsable=True, cl=collapse, label="Options")
	# 	mc.columnLayout(name)

	# 	mc.separator(height=4, style="none")
	# 	mc.optionMenuGrp("renderLayer", label="Layer: ")
	# 	for item in self.renderLayers:
	# 		mc.menuItem(label=item)
	# 	mc.symbolButton(image="reload.png", width=26, height=26, command=lambda *args: self.reloadLayers(self.currentLayer))
	# 	mc.setParent(name)

	# 	mc.separator(height=4, style="none")
	# 	mc.rowLayout(numberOfColumns=1, columnAttach1="left", columnAlign1="both", columnOffset1=4)
	# 	mc.text("labelOverrides", label="Overrides:", wordWrap=True, align="left", width=392, enable=False)
	# 	mc.setParent(name)

	# 	mc.separator(height=2, style="none")
	# 	mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
	# 	mc.iconTextScrollList("txList", width=360, height=108, allowMultiSelection=True, enable=False)
	# 	mc.symbolButton(image="reload.png", width=26, height=26, command=lambda *args: self.reloadLayers(self.currentLayer))
	# 	mc.separator(height=8, style="none")
	# 	mc.setParent(parent)


	def reloadLayers(layer):
		""" Return layer overrides for 'layer'.
		"""
		self.renderLayers = mc.ls(type='renderLayer')
		self.currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)


def list():
	""" Return layer overrides for 'layer'.
	"""
	layer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
	adjLs = mc.editRenderLayerAdjustment(layer, query=True, layer=True)

	print("\n*** List of overrides for layer '%s:' ***" %layer)

	if adjLs:
		for adj in adjLs:
			print("%s = %s" %(adj, mc.getAttr(adj)))

	else:
		print("None")

	print("\n")

