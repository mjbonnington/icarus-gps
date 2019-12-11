#!/usr/bin/python

# [Icarus] nk_assetGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Gather a published asset.


import os
import sys
import traceback

import nuke

from rsc.nuke.scripts import nukeOps
from shared import prompt
from shared import json_metadata as metadata
from shared import verbose


def gather(gatherPath):

	gatherPath = os.path.expandvars(gatherPath)

	# Instantiate data classes
	assetData = metadata.Metadata(os.path.join(gatherPath, 'asset_data.json'))

	assetPblName = assetData.get_attr('asset', 'assetPblName')
	assetType = assetData.get_attr('asset', 'assetType')
	assetExt = assetData.get_attr('asset', 'assetExt')
	version = assetData.get_attr('asset', 'version')
	notes = assetData.get_attr('asset', 'notes')

	# Check if objects with same name exist in script
	icSetName = 'ICSet_%s_%s' % (assetPblName, version)
	nukeOps.resolveNameConflict(icSetName)

	# Check for preferred .nk extension
	for item_ in os.listdir(gatherPath):
		if item_.endswith('.nk'):
			assetExt = 'nk'

	try:
		# Get published asset from the gatherPath
		gatherPath += '/%s.%s' % (assetPblName, assetExt)
		if not os.path.isfile(gatherPath):
			verbose.noAsset()
			return

		# Gathering...
		nuke.nodePaste(gatherPath)

		# Add ICSet custom attributes
		tileRGB = 0.316
		fontRGB = 0.65
		tileHex = int('%02x%02x%02x%02x' % (tileRGB*255, tileRGB*255, tileRGB*255, 1), 16)
		fontHex = int('%02x%02x%02x%02x' % (fontRGB*255, fontRGB*255, fontRGB*255, 1), 16)
		icarusIcon = '<center><img src=icarus.png>'
		icSet = nuke.toNode(assetPblName)
		notesTab = nuke.Tab_Knob( 'icNotes', 'Icarus Notes' )
		notesKnob = nuke.Multiline_Eval_String_Knob('notes', 'Notes')
		icSet.addKnob(notesTab)
		icSet.addKnob(notesKnob)
		icSet['notes'].setValue(notes)
		icSet['name'].setValue(icSetName)
		icSet['label'].setValue('%s\n%s' % (icarusIcon, assetType))
		icSet['note_font_size'].setValue(15)
		icSet['tile_color'].setValue(tileHex)
		icSet['note_font_color'].setValue(fontHex)
		# Lock attributes
		icSet['notes'].setEnabled(False)
		icSet['label'].setEnabled(False)


	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for more information.\n\n%s' % traceback.format_exc()
		dialog = prompt.dialog()
		dialog.display(dialogMsg, dialogTitle, conf=True)

