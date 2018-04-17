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


	def close(self, *args, **kwargs):
		mc.deleteUI(self.winName)


	def reloadLayers(self, *args, **kwargs):
		""" 
		"""
		self.renderLayers = mc.ls(type='renderLayer')
		self.currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)


	def listOverrides(self, layer):
		""" Return layer overrides for 'layer'.
		"""
		results = []
		adjLs = mc.editRenderLayerAdjustment(layer, query=True, layer=True)

		if adjLs:
			for adj in adjLs:
				results.append("%s = %s" %(adj, mc.getAttr(adj)))

		return results


	def listOverrides(self, layer):
		""" Return layer overrides for 'layer'.
		"""
		results = []
		adjLs = mc.editRenderLayerAdjustment(layer, query=True, layer=True)

		if adjLs:
			for adj in adjLs:
				results.append("%s = %s" %(adj, mc.getAttr(adj)))

		return results


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
		layer_style = CSS(None, margin=(6,6), spacing=(4,4))
		button_style = CSS(None, margin=(0,0), spacing=(2,0))

		with Window(self.winName, title=self.winTitle) as window:
			with VerticalThreePane(css=layer_style) as vertical_layout1:
				with HorizontalThreePane() as layer_layout1:
					layer_label = Text(label="Layer: ")
					layer_comboBox = OptionMenu()
					for item in self.renderLayers:
						menu_item = MenuItem(label=item)
						#menu_item.command += self.listOverrides(self.currentLayer)
					reloadLayers_button = SymbolButton(image="refresh.png", width=20, height=20)
					reloadLayers_button.command += self.reloadLayers
				text_scroll = TextScrollList()
				text_scroll.append = self.listOverrides(self.currentLayer)
				with HorizontalStretchForm(css=button_style) as buttonBox:
					editOverride_button = Button('Edit Layer Override')
					removeOverride_button = Button('Delete Layer Override')
					close_button = Button('Close')
					close_button.command += self.close

		window.show()


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

