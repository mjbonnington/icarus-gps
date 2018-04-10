import maya.cmds as mc

def list():
	layer = mc.editRenderLayerGlobals(query=True, currentRenderLayer=True)
	adjLs = mc.editRenderLayerAdjustment(layer, query=True, layer=True)

	print("\n*** List of overrides for layer '%s:' ***" %layer)

	if adjLs:
		for adj in adjLs:
			print("%s = %s" %(adj, mc.getAttr(adj)))

	else:
		print("None")

	print("\n")
