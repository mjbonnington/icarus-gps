#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:renderPbl
#copyright	:Gramercy Park Studios


#render publish module
import os, sys, traceback
import pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, approvePbl, djvOps, inProgress

def publish(renderDic, pblTo, mainLayer, streamPbl, pblNotes, mail, approved):
	
	job = os.environ['JOB']
	assetType = 'render'
	prefix = ''
	convention = ''
	suffix = ''
	subsetName = os.environ['SHOT']
	assetExt = ''
	assetPblName = '%s%s%s' % (prefix, convention, suffix)
	assetName = assetPblName 
	assetType = 'render'
	
	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	renderRootPblDir = pblDir
	
	#approved publish directory
	apvDir = os.environ['SHOTAPPROVEDPUBLISHDIR']
	
	#version control
	currentVersion = '%s' % vCtrl.version(pblDir, current=True)
	version = '%s' % vCtrl.version(pblDir)
	
	#checks if no main layer was set and cancels publish if publishin first version
	if version == 'v001':
		if not mainLayer:
			verbose.noMainLayer()
			return
		
	#confirmation dialog
	dialogMsg = ''
	dialogTitle = 'Publishing'
	if not streamPbl:
		dialogMsg += "Warning:\n\nPublish won't be streamed.\nLayers from previous renders will not be ported.\n\n\n"
	if not mainLayer:
		dialogMsg += 'Warning:\n\nNo main layer was set.\nThe render main layer will be ported from the previous publish.\n\nContinue?\n\n\n'
	dialogMsg += 'Render:\t%s\n\nVersion:\t%s\n\nNotes:\t%s' % (assetPblName, version, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	try:	
		verbose.pblFeed(begin=True)
		pblResult = 'SUCCESS'
		#creating publish directories
		pblDir = osOps.createDir(os.path.join(pblDir, version))

		#creating in progress tmp file
		inProgress.start(pblDir)
		
		#file operations
		if not mainLayer:
			streamPbl = True
		elif version == 'v001':
			streamPbl = True
		#streaming publish. Hard linking previous version and removing previous icarus data files
		if streamPbl:
			if version != 'v001':
				#getting all layers in current publish 
				currentPblLayerLs = os.listdir(os.path.join(renderRootPblDir, currentVersion))
				for currentPblLayer in currentPblLayerLs:
					#creating respective layer folder in new version
					if os.path.isdir(os.path.join(renderRootPblDir, currentVersion, currentPblLayer)):
						osOps.createDir(os.path.join(pblDir, currentPblLayer))
						#getting all files in current layer
						currentLayerFileLs = sorted(os.listdir(os.path.join(renderRootPblDir, currentVersion, currentPblLayer)))
						#hard linking files to new version
						for currentLayerFile in currentLayerFileLs:
							verbose.pblFeed(msg='Processing %s' % currentLayerFile)
							osOps.hardLink(os.path.join(renderRootPblDir, currentVersion, currentPblLayer, currentLayerFile), os.path.join(pblDir, currentPblLayer))
			
		#processing all new layers and passes
		for key in renderDic.keys():
			outputDir = os.path.expandvars(renderDic[key])
			dirContents = sorted(os.listdir(outputDir))
			for file_ in dirContents:
				verbose.pblFeed(msg='Processing %s' % file_)
				if key == mainLayer:
					osOps.createDir(os.path.join(pblDir, 'main'))
					if os.path.isfile(os.path.join(outputDir, file_)):
						prcFile = pblOptsPrc.renderName_prc(key, 'main', file_)
						if prcFile:
							osOps.hardLink(os.path.join(outputDir, file_), os.path.join(pblDir, 'main', prcFile))
				else:
					if not os.path.isdir(os.path.join(pblDir, key)):
						osOps.createDir(os.path.join(pblDir, key))
					osOps.hardLink(os.path.join(outputDir, file_), os.path.join(pblDir, key))
		
		#creating publish snapshot from main layer new version
		mainLayerDir = os.path.join(pblDir, 'main')
		mainLayerFileLs = sorted(os.listdir(mainLayerDir))
		mainLayerPaddingLs = []
		snapShot = False
		for mainLayerFile in mainLayerFileLs:
			if '_main.' in mainLayerFile:
				snapShot = True
				mainLayerBody, mainLayerPadding, mainLayerExtension = pblOptsPrc.render_split(mainLayerFile)
				mainLayerPaddingLs.append(mainLayerPadding)
				
		if snapShot:
			startFrame = min(mainLayerPaddingLs)
			endFrame = max(mainLayerPaddingLs)
			midFrame = int((int(startFrame) + int(endFrame))/2)
			input = os.path.join(mainLayerDir, mainLayerBody)
			output = os.path.join(pblDir, 'preview')
			djvOps.prcImg(input, output, midFrame,  midFrame, mainLayerExtension, outExt='jpg')
			djvOps.prcQt(input, pblDir, startFrame, endFrame, mainLayerExtension, resize=(256, 144))
				
		#ic publishData files
		assetPblName += '_%s' % version		
		icPblData.writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, pblNotes)
			
		
		#inserting approval file
		apvFile = open(os.path.join(pblDir, 'approved.ic'), 'w')
		apvFile.write(str(approved))
		apvFile.close
			
		#Approving publish
		if approved:
			approvePbl.publish(apvDir, pblDir, assetDir, assetType, version)

		#deleting in progress tmp file
		inProgress.end(pblDir)			
		
		verbose.pblFeed(end=True)
		
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		osOps.recurseRemove(pblDir)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()
	
	#publish result dialog
	dialogTitle = "Publish Report"
	dialogMsg = "Render:\t%s\n\nVersion:\t%s\n\n\n%s" % (assetPblName, version, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
		
