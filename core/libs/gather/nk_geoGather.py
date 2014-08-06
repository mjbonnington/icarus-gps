#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:nk_geoGather
#copyright	:Gramercy Park Studios

import os, sys, traceback
import pblChk, verbose, pDialog, nukeOps
import nuke

def gather(gatherPath):

	#retrieves icData from gatherPath
	sys.path.append(gatherPath)
	import icData; reload(icData)
	if icData.assetType == 'ic_pointCloud':
		import trsData; reload(trsData)
	sys.path.remove(gatherPath)
	
	#check if objects with same name exist in script
	icSetName = 'ICSet_%s_%s' % (icData.assetPblName, icData.version)
	nukeOps.resolveNameConflict(icSetName)
		
	try:	
		#gets published asset from the gatherPath
		assetExt = icData.assetExt
		assetPath = os.path.join(gatherPath, '%s.%s' % (icData.assetPblName, assetExt))
		if not os.path.isfile(assetPath):
			verbose.noAsset()
			return
		
		#deselecting all nodes
		selNodes = nuke.selectedNodes()
		for selNode in selNodes:
			selNode['selected'].setValue(False)
	
		#creating readGeo
		icSet = nuke.createNode('ReadGeo2', 'file {%s}' % assetPath)
		
		#making all items in geo hierarchy visible in scene view
		sceneView = icSet['scene_view'] 
		allItems = sceneView.getAllItems() 
		sceneView.setImportedItems(allItems)
		sceneView.setSelectedItems(allItems)		
				
		#adding ICSet custom attributes
		tileRGB = 0.316
		fontRGB = 0.65
		tileHex = int('%02x%02x%02x%02x' % (tileRGB*255, tileRGB*255, tileRGB*255,1), 16)
		fontHex = int('%02x%02x%02x%02x' % (fontRGB*255, fontRGB*255, fontRGB*255,1), 16)
		icarusIcon =  '<center><img src=icarus.png>\n%s' % icData.assetType
		notesTab = nuke.Tab_Knob( 'icNotes', 'Icarus Notes' )
		notesKnob = nuke.Multiline_Eval_String_Knob('notes', 'Notes')
		icSet.addKnob(notesTab)
		icSet.addKnob(notesKnob)
		icSet['notes'].setValue(icData.notes)
		icSet['name'].setValue(icSetName)
		icSet['cacheLocal'].setValue(0)
		icSet['label'].setValue(icarusIcon)
		icSet['note_font_size'].setValue(15)
		icSet['tile_color'].setValue(tileHex)
		icSet['note_font_color'].setValue(fontHex)
		
		#locking attributes
		icSet['notes'].setEnabled(False)
		icSet['label'].setEnabled(False)
		icSet['file'].setEnabled(False)	
		
		#if geo is pointCloud applies transformation matrix
		if icData.assetType == 'ic_pointCloud':
			icSet['translate'].setValue(trsData.t[0],0)
			icSet['translate'].setValue(trsData.t[1],1)
			icSet['translate'].setValue(trsData.t[2],2)
			icSet['rotate'].setValue(trsData.r[0],0)
			icSet['rotate'].setValue(trsData.r[1],1)
			icSet['rotate'].setValue(trsData.r[2],2)
			icSet['scaling'].setValue(trsData.s[0],0)
			icSet['scaling'].setValue(trsData.s[1],1)
			icSet['scaling'].setValue(trsData.s[2],2)
			icSet['xform_order'].setValue(0)
			icSet['rot_order'].setValue(0)
			icSet['display'].setValue(1)	

		#update message
		#nuke.message('WARNING:\nPlease update ReadGeo node frame rate to shot settings')
		
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		dialogTitle = 'Gather Warning'
		dialogMsg = 'Errors occured during asset update.\nPlease check console for details'
		dialog = pDialog.dialog()
		dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
