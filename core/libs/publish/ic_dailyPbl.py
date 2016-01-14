#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:ic_dailyPbl
#copyright	:Gramercy Park Studios


#daily publish module
import os, sys, traceback, time
import pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, djvOps, inProgress

def publish(dailySeq, dailyPath, dailyType, pblTo, pblNotes, mail):
	
	job = os.environ['JOB']
	assetType = 'daily'
	prefix = ''
	convention = ''
	suffix = ''
	subsetName = dailyType
	assetExt = ''
	assetPblName = '%s%s%s' % (prefix, convention, suffix)
	assetName = assetPblName 
	assetType = 'daily'

	#processing asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	renderRootPblDir = pblDir
	
	#version control
	currentVersion = vCtrl.version(pblDir, current=True)
	version = vCtrl.version(pblDir)
	
	#confirmation dialog
	dialogMsg = ''
	dialogTitle = 'Publishing'
	dialogMsg += 'Daily:\t%s_%s\n\nVersion:\t%s\n\nNotes:\t%s' % (os.environ['SHOT'], subsetName, version, pblNotes)
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
		dailyPath = os.path.expandvars(dailyPath)
		dailyPathLs = os.listdir(dailyPath)
		dailyPathLs = sorted(dailyPathLs)
		paddingLs = []
		#getting all frames from sequence and appending to padding list
		for file_ in dailyPathLs:
			if '%s.' % dailySeq in file_:
				fileSplit = pblOptsPrc.render_split(file_)
				if fileSplit:
					nameBody, padding, extension = fileSplit
					paddingLs.append(padding)
		startFrame = min(paddingLs)
		endFrame = max(paddingLs)
		midFrame = int((int(startFrame) + int(endFrame))/2)
		#passing arguments to djv to process the files in djvOps
		dailyFileBody = '%s_daily_%s' % (os.environ['SHOT'], subsetName)
		dailyFile = '%s.%s.jpg' % (dailyFileBody, startFrame)
		input = os.path.join(dailyPath, nameBody)
		output = os.path.join(pblDir, dailyFileBody)
		#djvOps.prcImg(input, output, startFrame, endFrame, extension, outExt='jpg', fps=os.environ['FPS'])
		djvOps.prcQt(input, pblDir, startFrame, endFrame, extension, name='%s_%s' % (dailyFileBody, version))
		#hard linking daily to dated folder in editorial
		dailyFileLs = os.listdir(pblDir)
		dailyDateDir = time.strftime('%Y_%m_%d')
		dailyDatePath = os.path.join(os.environ['WIPSDIR'], 'CGI', dailyDateDir, '%s_%s_%s' % (os.environ['SHOT'], subsetName, version))
		osOps.createDir(dailyDatePath)
		excludeLs = ['in_progress.tmp']
		for file_ in dailyFileLs:
			if file_ not in excludeLs:
				osOps.hardLink(os.path.join(pblDir, file_), os.path.join(dailyDatePath, file_))
				dailyFile = file_

		#creating daily snapshot
		previewOutput = os.path.join(pblDir, 'preview')
		djvOps.prcImg(input, previewOutput, midFrame, midFrame, extension, resize=(512,288), outExt='jpg')
		#djvOps.prcQt(input, pblDir, startFrame, endFrame, extension, resize=(256, 144))
				
		#ic publishData files
		assetPblName += '_%s' % version		
		icPblData.writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, pblNotes)
		
		#deleting in progress tmp file from .publish and wips folder
		inProgress.end(pblDir)
		inProgress.end(dailyDatePath)

		#published asset check
		pblDirResult = pblChk.success(os.path.join(pblDir, dailyFile)) 
		dailyDirResult = pblChk.success(os.path.join(dailyDatePath, dailyFile))
		pblResult = 'SUCCESS'
		if pblDirResult != pblResult or dailyDirResult != pblResult:
			pblResult = 'FAIL'
			raise Exception(verbose.dailyFail())

		verbose.pblFeed(end=True)
		
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		osOps.recurseRemove(pblDir)
		osOps.recurseRemove(dailyDatePath)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += verbose.pblRollback()
	
	#publish result dialog
	dialogTitle = "Publish Report"
	dialogMsg = "Render:\t%s\n\nVersion:\t%s\n\n\n%s" % (assetPblName, version, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)
		
