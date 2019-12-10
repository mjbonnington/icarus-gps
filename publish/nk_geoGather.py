#!/usr/bin/python

# [Icarus] nk_geoGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Gather an asset of type 'ic_geo' or 'ic_pointCloud'.


import os
import sys
import traceback

import nuke

from rsc.nuke.scripts import nukeOps
from shared import prompt
from shared import settings_data_xml
from shared import verbose


def gather(gatherPath):

	gatherPath = os.path.expandvars(gatherPath)

	# Instantiate XML data classes
	assetData = settings_data_xml.SettingsData()
	assetData.loadXML(os.path.join(gatherPath, 'assetData.xml'), quiet=True)

	assetPblName = assetData.getValue('asset', 'assetPblName')
	assetType = assetData.getValue('asset', 'assetType')
	assetExt = assetData.getValue('asset', 'assetExt')
	version = assetData.getValue('asset', 'version')
	notes = assetData.getValue('asset', 'notes')

	# Retrieve trsData from gatherPath. I've left this here for compatibility, ultimately need to look into rewriting this.
	sys.path.append(gatherPath)
	if assetType == 'ic_pointCloud':
		import trsData; reload(trsData)
	sys.path.remove(gatherPath)

	# Check if objects with same name exist in script
	icSetName = 'ICSet_%s_%s' % (assetPblName, version)
	nukeOps.resolveNameConflict(icSetName)

	try:
		# Get published asset from the gatherPath
		assetPath = os.path.join(gatherPath, '%s.%s' % (assetPblName, assetExt))
		if not os.path.isfile(assetPath):
			verbose.noAsset()
			return

		# Deselect all nodes
		selNodes = nuke.selectedNodes()
		for selNode in selNodes:
			selNode['selected'].setValue(False)

		# Create readGeo
		icSet = nuke.createNode('ReadGeo2', 'file {%s}' % assetPath)

		# Make all items in geo hierarchy visible in scene view if geo type is alembic
		if assetExt == 'abc':
			sceneView = icSet['scene_view']
			allItems = sceneView.getAllItems()
			sceneView.setImportedItems(allItems)
			sceneView.setSelectedItems(allItems)

		# Add ICSet custom attributes
		tileRGB = 0.316
		fontRGB = 0.65
		tileHex = int('%02x%02x%02x%02x' % (tileRGB*255, tileRGB*255, tileRGB*255, 1), 16)
		fontHex = int('%02x%02x%02x%02x' % (fontRGB*255, fontRGB*255, fontRGB*255, 1), 16)
		icarusIcon = '<center><img src=icarus.png>\n%s' % assetType
		notesTab = nuke.Tab_Knob( 'icNotes', 'Icarus Notes' )
		notesKnob = nuke.Multiline_Eval_String_Knob('notes', 'Notes')
		icSet.addKnob(notesTab)
		icSet.addKnob(notesKnob)
		icSet['notes'].setValue(notes)
		icSet['name'].setValue(icSetName)
		icSet['cacheLocal'].setValue(0)
		icSet['label'].setValue(icarusIcon)
		icSet['note_font_size'].setValue(15)
		icSet['tile_color'].setValue(tileHex)
		icSet['note_font_color'].setValue(fontHex)
		# Lock attributes
		icSet['notes'].setEnabled(False)
		icSet['label'].setEnabled(False)
		icSet['file'].setEnabled(False)

		# If geo is pointCloud, apply transformation matrix
		if assetType == 'ic_pointCloud':
			icSet['translate'].setValue(trsData.t[0], 0)
			icSet['translate'].setValue(trsData.t[1], 1)
			icSet['translate'].setValue(trsData.t[2], 2)
			icSet['rotate'].setValue(trsData.r[0], 0)
			icSet['rotate'].setValue(trsData.r[1], 1)
			icSet['rotate'].setValue(trsData.r[2], 2)
			icSet['scaling'].setValue(trsData.s[0], 0)
			icSet['scaling'].setValue(trsData.s[1], 1)
			icSet['scaling'].setValue(trsData.s[2], 2)
			icSet['xform_order'].setValue(0)
			icSet['rot_order'].setValue(0)
			icSet['display'].setValue(1)

		# Update message
		#nuke.message('WARNING: Please update ReadGeo node frame rate to shot settings')


	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for more information.\n\n%s' % traceback.format_exc()
		dialog = prompt.dialog()
		dialog.display(dialogMsg, dialogTitle, conf=True)

