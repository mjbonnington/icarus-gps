#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:nk_assetGather
#copyright	:Gramercy Park Studios

import os, sys, traceback
import pblChk, verbose, pDialog, nukeOps
import nuke

def gather(gatherPath):

	#retrieves icData from gatherPath
	sys.path.append(gatherPath)
	import icData; reload(icData)
	sys.path.remove(gatherPath)
	
	#check if objects with same name exist in script
	icSetName = 'ICSet_%s_%s' % (icData.assetPblName, icData.version)
	nukeOps.resolveNameConflict(icSetName)
	
	#checks for prefered .nk extension
	assetExt = icData.assetExt
	for item_ in os.listdir(gatherPath):
		if item_.endswith('.nk'):
			assetExt = 'nk'
		
	try:	
		#gets published asset from the gatherPath
		gatherPath += '/%s.%s' % (icData.assetPblName, assetExt)
		if not os.path.isfile(gatherPath):
			verbose.noAsset()
			return
	
		#gathering
		nuke.nodePaste(gatherPath)
		
		#adding ICSet custom attributes
		tileRGB = 0.316
		fontRGB = 0.65
		tileHex = int('%02x%02x%02x%02x' % (tileRGB*255, tileRGB*255, tileRGB*255,1), 16)
		fontHex = int('%02x%02x%02x%02x' % (fontRGB*255, fontRGB*255, fontRGB*255,1), 16)
		icarusIcon =  '<center><img src=icarus.png>'
		icSet = nuke.toNode(icData.assetPblName)
		notesTab = nuke.Tab_Knob( 'icNotes', 'Icarus Notes' )
		notesKnob = nuke.Multiline_Eval_String_Knob('notes', 'Notes') 
		icSet.addKnob(notesTab)
		icSet.addKnob(notesKnob)
		icSet['notes'].setValue(icData.notes)
		icSet['name'].setValue(icSetName)
		icSet['label'].setValue('%s\n%s' % (icarusIcon, icData.assetType))
		icSet['note_font_size'].setValue(15)
		icSet['tile_color'].setValue(tileHex)
		icSet['note_font_color'].setValue(fontHex)
		#locking attributes
		icSet['notes'].setEnabled(False)
		icSet['label'].setEnabled(False)
			
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for details'
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
