#!/usr/bin/python

# [Icarus] ic_dailyPbl.py
#
# Nuno Pereira <nuno.pereira@gps-ldn.com>
# Mike Bonnington <mike.bonnington@gps-ldn.com>
# (c) 2013-2019 Gramercy Park Studios
#
# Dailies publishing module.


import os
import sys
import time
import traceback

from . import pblChk
from . import pblOptsPrc
from . import inProgress
from shared import djvOps
from shared import icPblData
from shared import os_wrapper
from shared import prompt
from shared import vCtrl
from shared import verbose


def publish(dailyPblOpts, pblTo, pblNotes):

	dailySeq, dailyRange, dailyType, dailyPath = dailyPblOpts
	#nameBody, extension = os.path.splitext(dailySeq)
	#extension = extension[1:] # remove leading dot from file extension
	nameBody, padding_, extension = dailySeq.rsplit('.', 2)
	padding = len(padding_)

	job = os.environ['IC_JOB']
	assetType = 'dailies'
	prefix = ''
	convention = ''
	suffix = ''
	subsetName = dailyType
	assetExt = ''
	assetPblName = '%s%s%s' % (prefix, convention, suffix)
	assetName = assetPblName
	shotSaneName = os.environ['IC_SHOT'].replace('/', '_')

	# Process asset publish options
	assetPblName, assetDir, pblDir = pblOptsPrc.prc(pblTo, subsetName, assetType, prefix, convention, suffix)
	renderRootPblDir = pblDir

	# Version control
	currentVersion = vCtrl.version(pblDir, current=True)
	version = vCtrl.version(pblDir)

	# Confirmation dialog
	dialogMsg = ''
	dialogTitle = 'Publishing'
	dialogMsg += 'Name:\t%s_%s\n\nVersion:\t%s\n\nNotes:\t%s' % (shotSaneName, subsetName, version, pblNotes)
	dialog = prompt.Dialog()
	if not dialog.display(dialogMsg, dialogTitle):
		return

	try:	
		verbose.pblFeed(begin=True)
		pblResult = 'SUCCESS'

		# Create publish directories
		pblDir = os_wrapper.createDir(os.path.join(pblDir, version))

		# Create in-progress tmp file
		inProgress.start(pblDir)

		# File operations
		dailyPath = os.path.expandvars(dailyPath)

		try:
			startFrame, endFrame = dailyRange.split('-')
		except ValueError:
			startFrame = endFrame = dailyRange # if frame range is a single frame

		try:
			posterFrame_ = int(os.environ['IC_POSTER_FRAME'])
		except ValueError:
			posterFrame_ = -1
		if not (int(startFrame) <= posterFrame_ <= int(endFrame)): # if poster frame is not within frame range, use mid frame
			posterFrame_ = (int(startFrame)+int(endFrame)) / 2
		posterFrame = str(posterFrame_).zfill(padding)

		# Pass arguments to djv to process the files in djvOps
		dailyFileBody = '%s_dailies_%s' % (shotSaneName, subsetName)
		dailyFile = '%s.%s.jpg' % (dailyFileBody, startFrame)
		inFile = os.path.join(dailyPath, nameBody)
		#print(inFile)
		outFile = os.path.join(pblDir, dailyFileBody)
		#djvOps.prcImg(inFile, outFile, startFrame, endFrame, extension, outExt='jpg', fps=os.environ['IC_FPS'])
		djvOps.prcQt(inFile, pblDir, startFrame, endFrame, extension, name='%s_%s' % (dailyFileBody, version))

		# Hard linking daily to dated folder in wips dir
		dailyFileLs = os.listdir(pblDir)
		dailyDateDir = time.strftime('%Y_%m_%d')
		dailyDatePath = os.path.join(os.environ['IC_WIPS_DIR'], 'CGI', dailyDateDir, '%s_%s_%s' % (shotSaneName, subsetName, version))
		os_wrapper.createDir(dailyDatePath)
		excludeLs = ['in_progress.tmp']
		for file_ in dailyFileLs:
			if file_ not in excludeLs:
				os_wrapper.hardLink(os.path.join(pblDir, file_), os.path.join(dailyDatePath, file_))
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
		print(os.path.join(pblDir, dailyFile))
		print(os.path.join(dailyDatePath, dailyFile))
		pblResult = 'SUCCESS'
		if pblDirResult != pblResult or dailyDirResult != pblResult:
			pblResult = 'FAILED'
			raise Exception(verbose.dailyFail())

		verbose.pblFeed(end=True)

	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		pathToPblAsset = ''
		os_wrapper.remove(pblDir)
		os_wrapper.remove(dailyDatePath)
		pblResult = pblChk.success(pathToPblAsset)
		pblResult += " - " + verbose.pblRollback()

	# Show publish result dialog
	dialogTitle = "Publish Report"
	dialogMsg = "Render:\t%s\n\nVersion:\t%s\n\n%s" % (assetPblName, version, pblResult)
	dialog = prompt.Dialog()
	dialog.display(dialogMsg, dialogTitle, conf=True)

