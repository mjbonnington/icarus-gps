import maya.cmds as mc


# TODO: prevent multiple scriptJobs from being created
refreshPostSceneReadID = mc.scriptJob(compressUndo=True, protected=True, event=['PostSceneRead', 'refreshPanel()'])
refreshNewSceneOpenedID = mc.scriptJob(compressUndo=True, protected=True, event=['NewSceneOpened', 'refreshPanel()'])
#print refreshPostSceneReadID, refreshNewSceneOpenedID


def gpsDockableOutliner():
	""" Create dockable outliner.
	"""
	if not mc.window('gpsDockableOutlinerWindow', query=True, exists=True):
		#print "Creating window & frame"
		mc.window('gpsDockableOutlinerWindow', title='[GPS] Outliner', widthHeight=[256, 768])
		mc.frameLayout('gpsDockableOutlinerFrame', parent='gpsDockableOutlinerWindow', marginHeight=0, marginWidth=0, borderVisible=False, labelVisible=False)

	if not mc.dockControl('gpsOutlinerDockControl', query=True, exists=True):
		#print "Creating dock control"
		mc.dockControl('gpsOutlinerDockControl', label='[GPS] Outliner', width=256, area='left', allowedArea=['left', 'right'], content='gpsDockableOutlinerWindow')
	else:
		#print "Making dock control visible"
		mc.dockControl('gpsOutlinerDockControl', edit=True, visible=True)

	refreshPanel()


def refreshPanel():
	""" Create or recreate the outliner panel.
	"""
	if not mc.outlinerPanel('gpsDockableOutlinerPanel', query=True, exists=True):
		#print "Creating outliner panel"
		mc.outlinerPanel('gpsDockableOutlinerPanel', parent='gpsDockableOutlinerFrame')
	else:
		#print "Making outliner panel visible"
		mc.panel('gpsDockableOutlinerPanel', edit=True, parent='gpsDockableOutlinerFrame')

