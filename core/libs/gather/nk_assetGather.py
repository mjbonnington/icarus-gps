#!/usr/bin/python

# [Icarus] nk_assetGather.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Gather a published asset.


import os, sys, traceback
import jobSettings, nukeOps, pDialog, verbose
import nuke


def gather(gatherPath):

	gatherPath = os.path.expandvars(gatherPath)

	# Instantiate XML data classes
	assetData = jobSettings.jobSettings()
	assetData.loadXML(os.path.join(gatherPath, 'assetData.xml'), quiet=True)

	assetPblName = assetData.getValue('asset', 'assetPblName')
	assetType = assetData.getValue('asset', 'assetType')
	assetExt = assetData.getValue('asset', 'assetExt')
	version = assetData.getValue('asset', 'version')
	notes = assetData.getValue('asset', 'notes')

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
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

