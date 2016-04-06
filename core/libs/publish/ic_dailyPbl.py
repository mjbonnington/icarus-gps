#!/usr/bin/python

# [Icarus] ic_dailyPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2016 Gramercy Park Studios
#
# Dailies publishing module.


import os, sys, time, traceback
import pblChk, pblOptsPrc, vCtrl, pDialog, osOps, icPblData, verbose, djvOps, inProgress, sequence


def publish(dailyPblOpts, pblTo, pblNotes):

	dailySeq, dailyRange, dailyType, dailyPath = dailyPblOpts
	nameBody, extension = os.path.splitext(dailySeq)
	extension = extension[1:] # remove leading dot from file extension

	job = os.environ['JOB']
	assetType = 'dailies'
	prefix = ''
	convention = ''
	suffix = ''
	subsetName = dailyType
	assetExt = ''
	assetPblName = '%s%s%s' % (prefix, convention, suffix)
	assetName = assetPblName 

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	renderRootPblDir = pblDir

	# Version control
	currentVersion = vCtrl.version(pblDir, current=True)
	version = vCtrl.version(pblDir)

	# Confirmation dialog
	dialogMsg = ''
	dialogTitle = 'Publishing'
	dialogMsg += 'Name:\t%s_%s\n\nVersion:\t%s\n\nNotes:\t%s' % (os.environ['SHOT'], subsetName, version, pblNotes)
	dialog = pDialog.dialog()
	if not dialog.dialogWindow(dialogMsg, dialogTitle):
		return

	try:	
		verbose.pblFeed(begin=True)
		pblResult = 'SUCCESS'

		# Create publish directories
		pblDir = osOps.createDir(os.path.join(pblDir, version))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# File operations
		dailyPath = os.path.expandvars(dailyPath)
		paddingLs = sequence.numList(dailyRange) # need to add ability to detect sequences with inconsistent padding
		startFrame = min(paddingLs)
		endFrame = max(paddingLs)
		try:
			posterFrame = int(os.environ['POSTERFRAME'])
		except ValueError:
			posterFrame = -1
		if not (startFrame <= posterFrame <= endFrame): # if poster frame is not within frame range, use mid frame
			posterFrame = int((startFrame+endFrame) / 2)

		# Pass arguments to djv to process the files in djvOps
		dailyFileBody = '%s_dailies_%s' % (os.environ['SHOT'], subsetName)
		dailyFile = '%s.%s.jpg' % (dailyFileBody, startFrame)
		inFile = os.path.join(dailyPath, nameBody)
		#print inFile
		outFile = os.path.join(pblDir, dailyFileBody)
		#djvOps.prcImg(inFile, outFile, startFrame, endFrame, extension, outExt='jpg', fps=os.environ['FPS'])
		djvOps.prcQt(inFile, pblDir, startFrame, endFrame, extension, name='%s_%s' % (dailyFileBody, version))

		# Hard linking daily to dated folder in wips dir
		dailyFileLs = os.listdir(pblDir)
		dailyDateDir = time.strftime('%Y_%m_%d')
		dailyDatePath = os.path.join(os.environ['WIPSDIR'], 'CGI', dailyDateDir, '%s_%s_%s' % (os.environ['SHOT'], subsetName, version))
		osOps.createDir(dailyDatePath)
		excludeLs = ['in_progress.tmp']
		for file_ in dailyFileLs:
			if file_ not in excludeLs:
				osOps.hardLink(os.path.join(pblDir, file_), os.path.join(dailyDatePath, file_))
				dailyFile = file_

		# Create daily snapshot
		previewoutFile = os.path.join(pblDir, 'preview')
		djvOps.prcImg(inFile, previewoutFile, posterFrame, posterFrame, extension, resize=(512,288), outExt='jpg')
		#djvOps.prcQt(inFile, pblDir, startFrame, endFrame, extension, resize=(512,288))

		# Store asset metadata in file
		assetPblName += '_%s' % version
		#src = renderDic['main']
		src = dailySeq
		icPblData.writeData(pblDir, assetPblName, assetName, assetType, assetExt, version, pblNotes, src)

		# Delete in-progress tmp file
		inProgress.end(pblDir)
		inProgress.end(dailyDatePath)

		# Published asset check
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

	# Show publish result dialog
	dialogTitle = "Publish Report"
	dialogMsg = "Render:\t%s\n\nVersion:\t%s\n\n\n%s" % (assetPblName, version, pblResult)
	dialog = pDialog.dialog()
	dialog.dialogWindow(dialogMsg, dialogTitle, conf=True)

