#!/usr/bin/python

about = """Layer Overrides
v0.1.3

Mike Bonnington <mjbonnington@gmail.com>
(c) 2018-2019

Provides a UI to view and manage all attribute overrides for a particular
render layer.
"""

import maya.cmds as mc


class LayerOverrides():

	def __init__(self):
		self.winTitle = "Layer Overrides"
		self.winName = "mjbLayerOverrides"

		self.reloadLayers()


	def UI(self):
		""" Create UI.
		"""
		# Check if UI window already exists
		if mc.window(self.winName, exists=True):
			mc.deleteUI(self.winName)

		# Create window
		mc.window(self.winName, title=self.winTitle, sizeable=True, menuBar=True, menuBarVisible=True)

		# Create menu bar
		mc.menu(label="Edit", tearOff=False)
		mc.menuItem(label="Reset Settings", command="")
		mc.menu(label="Help", tearOff=False)
		mc.menuItem(label="About...", command=lambda *args: mc.confirmDialog(parent=self.winName, title="About %s" %self.winTitle, message=about, button="OK"))

		# Create controls
		#setUITemplate -pushTemplate mjbToolsTemplate;
		mc.columnLayout("windowRoot")
		self.commonOptUI("commonOptPanel", "windowRoot")
		mc.separator(height=8, style="none")
		mc.rowLayout(numberOfColumns=1)
		mc.button(width=398, height=28, label="Close", command=lambda *args: mc.deleteUI(self.winName))
		#setUITemplate -popTemplate;

		self.listOverrides()

		mc.showWindow(self.winName)


	def commonOptUI(self, name, parent, collapse=False):
		""" Create common options panel UI controls.
		"""
		mc.frameLayout("commonOptRollout", width=400, collapsable=True, cl=collapse, label="Render Layer Overrides")
		mc.columnLayout(name)
		mc.separator(height=4, style="none")

		mc.optionMenuGrp("renderLayer_comboBox", label="Layer: ", changeCommand=lambda *args: self.listOverrides())
		for rl in self.renderLayers:
			mc.menuItem(label=rl)
		mc.optionMenuGrp("renderLayer_comboBox", edit=True, value=self.currentLayer)

		mc.separator(height=2, style="none")
		mc.rowLayout(numberOfColumns=2, columnAttach2=["left", "left"], columnAlign2=["both", "both"], columnOffset2=[4, 0])
		mc.iconTextScrollList("listView_overrides", width=360, height=108, allowMultiSelection=True)
		# table = mc.scriptTable(rows=4, columns=2, label=[(1,"Column 1"), (2,"Column 2")], cellChangedCmd=self.editCell)

		mc.setParent(name)

		mc.separator(height=4, style="none")
		mc.setParent(parent)


	def reloadLayers(self):
		""" Refresh list of render layers and current layer.
		"""
		self.renderLayers = mc.ls(type='renderLayer')
		self.currentLayer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)


	# def editCell(self, row, column, value):
	# 	""" 
	# 	"""
	# 	print(row, column, value)
	# 	return 1


	def listOverrides(self): #, layer=None):
		""" Return layer overrides for 'layer'.
		"""
		layer = mc.optionMenuGrp("renderLayer_comboBox", query=True, value=True)
		results = []
		adjustments = mc.editRenderLayerAdjustment(layer, query=True, layer=True)

		if adjustments:
			for adj in adjustments:
				results.append("%s = %s" %(adj, mc.getAttr(adj)))

		print(results)
		mc.iconTextScrollList("listView_overrides", edit=True, removeAll=True, deselectAll=True)
		mc.iconTextScrollList("listView_overrides", edit=True, append=results)
		return results


def list():
	""" Output layer overrides for the current layer.
	"""
	layer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
	adjustments = mc.editRenderLayerAdjustment(layer, query=True, layer=True)

	print("\n*** List of overrides for layer '%s:' ***" %layer)

	if adjustments:
		for adj in adjustments:
			print("%s = %s" %(adj, mc.getAttr(adj)))

	else:
		print("None")

	print("\n")
