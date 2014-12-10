#!/usr/bin/python
#support	:Nuno Pereira - nuno.pereira@gps-ldn.com
#title     	:mkPblDirs
#copyright	:Gramercy Park Studios


#crates publish directories
import os

def mkDirs(pblDir, version, textures=False):
	pblDir = '%s/%s' % (pblDir, version)	
	os.system('mkdir -p %s' % pblDir)
	if textures:
		pblTxDir = '%s/tx' % pblDir
		os.system('mkdir -p %s' % pblTxDir)
	return pblDir
