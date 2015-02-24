#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:pblOptsPrc
#copyright	:Gramercy Park Studios


import os
import pblChk, verbose


#Processes publish options arriving from the different publish modules


#######################GENERIC PUBLISHING OPTIONS PROCESSING########################
####################################################################################
#processes publish options and naming convention variables
def prc(pblTo, subset, assetType, prefix, convention, suffix):
	assetPblName = prefix + convention + suffix
	#if subset:
	assetDir = os.path.join(assetType, subset, convention)
	#else:
	#	assetDir = os.path.join(assetType, assetPblName)
	pblDir = os.path.join(pblTo, assetDir)
	return assetPblName, assetDir, pblDir


###################RENDER PUBLISHING SPECIFIC OPTIONS PROCESSING####################
####################################################################################
#splits a sequence file and returns the different render components
def render_split(file_):
	if file_.startswith('.'):
		return
	if not pblChk.paddingChk(file_):
		return
	nameBody, padding, extension = file_.split('.')
	return nameBody, padding, extension


#processes a dictionary contaning the format layer_pass:full/sequence/path. Returns the path with the old file name and with the name convention applied
def renderName_prc(key, convention, file_):
		file_split = render_split(file_)
		if file_split:
			prcFile = file_.replace(key, convention)
			return prcFile
		else:
			return
		
#processes the provided render path and returns a dictionary of layer and respective full sequence path
def renderPath_prc(renderPath):
	expRenderPath = os.path.expandvars(renderPath)
	dirContents = sorted(os.listdir(expRenderPath))
	renderDic = {}
	seqChkLs = []
	for content in dirContents:
		try:
			expLayerPath = os.path.join(expRenderPath, content)
			if os.path.isdir(expLayerPath):
				if content not in renderDic.keys():
					fileContentLs = os.listdir(expLayerPath)
					for file_ in fileContentLs:
						if pblChk.paddingChk(file_):
							renderDic[content] = os.path.join(renderPath, content)
							if content in seqChkLs:
								seqChkLs.remove(content)
							break
						else:
							if content not in seqChkLs:
								seqChkLs.append(content)
		except TypeError:
			continue
			
	if len(seqChkLs) > 0:
		verbose.noSeq(seqChkLs)
				
	if not renderDic:
		return
	else:
		return renderDic
			
		
####################DAILY PUBLISHING SPECIFIC OPTIONS PROCESSING####################
####################################################################################
#processes the provided path and returns a dictionary of layer and respective full sequence path
def dailyPath_prc(path):
	expPath = os.path.expandvars(path)
	filePath, file_ = os.path.split(expPath)
	fileSplit = render_split(file_)
	renderDic = {}
	if fileSplit:
		nameBody, padding, extension = render_split(file_)
		renderDic[nameBody] = filePath
		return renderDic
	else:
		return
		
