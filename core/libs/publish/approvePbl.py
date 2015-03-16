#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:approvePbl
#copyright	:Gramercy Park Studios


#approval publish module

import os, verbose
import osOps

def publish(apvDir, pblDir, assetDir, assetType, version):
	verbose.approval(start=True)
	approvedPblDir = str(os.path.join(apvDir, assetDir))
	ignoreLs = ('approved.ic', 'icData.py', 'in_progress.tmp')
	
	if assetType == 'render':
		approvedPblDir = str(os.path.join(approvedPblDir, '3D', version))
	else:
		approvedPblDir = str(os.path.join(approvedPblDir, version))
	
	#Creating version directory
	osOps.createDir(approvedPblDir)
	
	#linking
	for dirName, dirNames, fileNames in os.walk(pblDir):
		#creating all direcotries and subdirectories
		apvDir = dirName.replace(pblDir, approvedPblDir)
		osOps.createDir(apvDir)
		#hardlinking all files.
		for fileName in fileNames:
			#ignoring system files
			if fileName in ignoreLs or fileName.startswith('.'):
				continue
			osOps.hardLink(os.path.join(dirName, fileName), os.path.join(apvDir, fileName))
	
	verbose.approval(end=True)
	
