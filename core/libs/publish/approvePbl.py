#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:approvePbl
#copyright	:Gramercy Park Studios


#approval publish module

import os, verbose

def publish(apvDir, pblDir, assetDir, assetType, version):
	verbose.approval(start=True)
	approvedPblDir = str(os.path.join(apvDir, assetDir))
	ignoreLs = ('approved.ic', 'icData.py')
	
	if assetType == 'render':
		approvedPblDir = str(os.path.join(approvedPblDir, '3D', version))
	else:
		approvedPblDir = str(os.path.join(approvedPblDir, version))
	
	#Creating version directory
	os.system('mkdir -p %s' % approvedPblDir)
	
	#softlinking
	#os.system('ln -Fs %s %s' % (pblDir, approvedPblDir))
	#Due to OS incompatibilities softlinking had been replace with replication of direcotry structures and hardlinking the contents.
	for dirName, dirNames, fileNames in os.walk(pblDir):
		#creating all direcotries and subdirectories
		apvDir = dirName.replace(pblDir, approvedPblDir)
		if not os.path.isdir(apvDir):
			os.system('mkdir -p %s' % apvDir)
		#hardlinking all files.
		for fileName in fileNames:
			#ignoring system files
			if fileName in ignoreLs or fileName.startswith('.'):
				continue
			os.system('ln -f %s %s' % (os.path.join(dirName, fileName), os.path.join(apvDir, fileName)))
	
	verbose.approval(end=True)
	
