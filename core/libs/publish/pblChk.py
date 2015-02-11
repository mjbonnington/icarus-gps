#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:pblChk
#copyright	:Gramercy Park Studios


import os
import verbose

#checks if a publish for the same asset is currently under progress
def concurrentPbl(pblDir):
	if os.path.isdir(os.path.join(pblDir, version)):
		import time
		dirSize1 = os.path.getsize(pblDir)
		time.sleep(5)
		dirSize2 = os.path.getsize(pblDir)
		if dirSize1 != dirSize2:
			return -1
		else:
			return 0
	else:
		return 0
	
#checks if directory exists
def chkDir(path, verbose=True):
	if not os.path.isdir(path):
		if verbose:
			verbose.noDir()
		return
	return 1
	
#checks for directory contents
def chkDirContents(path, hidden=False):
	dirContents = os.listdir(path)
	if not hidden:
		for content in dirContents:
			if content.startswith('.'):
				dirContents.remove(content)
	if len(dirContents) == 0 :
		verbose.noDirContents()
		return
	return 1
	
#checks if file exists
def chkFile(path, verbose=True):
	if not os.path.isfile(path):
		if verbose:
			verbose.noFile()
		return
	return 1

#check for entries in mandatory fields
def chkOpts(opts):
	if '' in opts or None in opts:
		verbose.redFields()
		return
	else:
		return 1

#checks selection. May accept only one item
def itemCount(itemLs, mult=False):
	if len(itemLs) == 0:
		verbose.itemSel()
		return
	if not mult:
		if len(itemLs) > 1:
			verbose.itemSel()
			return
	return 1

#checks for layer and pass structure in the file name
def layerPassChk(renderFile):
	if len(renderFile.split('_')) < 2:
		return
	else:
		return 1
	
#checks for padding in the file name
def paddingChk(renderFile):
	if len(renderFile.split('.')) != 3:
		return
	try:
		int(renderFile.split('.')[1])
	except ValueError:
		return

	return 1
	
#sucessful publish confirmation 
def success(pathToPblAsset):
	if os.path.isfile(pathToPblAsset) == True:
		return 'SUCCESS'
	return 'FAILED'
	
#checks if versioned items exist
def versionedItems(path, vb=True):
	import vCtrl
	if vCtrl.version(path) == 'v001':
		if vb:
			verbose.noVersion()
		return
	else:
		return 1
