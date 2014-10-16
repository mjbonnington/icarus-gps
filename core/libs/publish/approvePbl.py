#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:renderPbl
#copyright	:Gramercy Park Studios


#approval publish module

import os, verbose

def publish(apvDir, pblDir, assetDir, version):
	verbose.approval(start=True)
	approvedPblDir = str(os.path.join(apvDir, assetDir))
	
	
	#Creating version directory
	os.system('mkdir -p %s/%s' % (approvedPblDir, version))

	#softlinking
	#os.system('ln -Fs %s %s' % (pblDir, approvedPblDir))
	

	#Due to OS incompatibilities softlinking had been replace with creation of direcotry and hardlinking the contents.
	#Any child directories other then textures will be copied. Textures are still hard linked
	
	#getting contents and hardlinking files. Folders will be copied
	dirContents = os.listdir(pblDir)
	for content in dirContents:
		try:
			contentPath = '%s/%s' % (pblDir, content)
			if os.path.isfile(contentPath):
				os.system('ln -f %s/%s %s/%s/%s' % (pblDir, content, approvedPblDir, version, content))
				continue
			if os.path.isdir(contentPath):
				os.system('cp -r %s %s/%s' % (contentPath, approvedPblDir, version))
				continue
		except OSError:
			verbose.approvalOSError()
	
	verbose.approval(end=True)
	
